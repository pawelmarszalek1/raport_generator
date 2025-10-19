import streamlit as st
from dotenv import load_dotenv
import os
import datetime

from modules.data_processor import load_data, get_data_summary
from modules.gemini_client import get_gemini_insights
from modules.report_generator import create_pptx_report

load_dotenv()

# === Konfiguracja Strony (Dashboardu) ===
st.set_page_config(
    page_title="Generator Raportów Gemini",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Generator Raportów Sprzedażowych z Gemini")
st.markdown("Prześlij swoje dane sprzedażowe (CSV lub Excel), aby wygenerować automatyczną analizę i raport PPTX.")

# === Panel Boczny (Sidebar) ===
with st.sidebar:
    st.header("1. Konfiguracja")

    st.subheader("Ustawienia Raportu")
    report_title_input = st.text_input(
        "Tytuł raportu:",
        "Raport Sprzedaży i Marketingu"
    )
    report_subtitle_input = st.text_input(
        "Podtytuł raportu (np. data lub dział):",
        f"Automatyczna analiza z dnia {datetime.date.today().strftime('%Y-%m-%d')}"
    )
    st.divider()

    st.subheader("Źródło Danych")
    # Przesyłanie pliku
    uploaded_file = st.file_uploader(
        "Wybierz plik z danymi",
        type=["csv", "xlsx", "xls"]
    )
    
    # Wybór typu raportu
    report_type = st.selectbox(
        "Wybierz format raportu",
        ["PowerPoint (.pptx)"] # TODO: W przyszłości można dodać PDF
    )
    
    # Przycisk generowania
    generate_button = st.button("🚀 Generuj Raport", type="primary")

# === Główna logika aplikacji ===
if generate_button and uploaded_file:
    
    # Krok 1: Przetwarzanie danych
    with st.spinner("Krok 1/4: Przetwarzam Twoje dane..."):
        try:
            df = load_data(uploaded_file)
            data_summary = get_data_summary(df)
            
            st.subheader("Podgląd wczytanych danych:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Błąd podczas ładowania danych: {e}")
            st.stop() # Zatrzymaj wykonywanie

    # Krok 2: Generowanie analizy przez Gemini
    with st.spinner("Krok 2/4: Gemini analizuje dane i generuje wnioski..."):
        try:
            gemini_response = get_gemini_insights(data_summary)
            
            st.subheader("Analiza wygenerowana przez Gemini:")
            st.text_area("Surowa odpowiedź modelu:", gemini_response, height=300)
        except Exception as e:
            st.error(f"Błąd podczas komunikacji z API Gemini: {e}")
            st.stop()

    # Krok 3: Tworzenie pliku raportu
    with st.spinner("Krok 3/4: Składam raport PowerPoint..."):
        try:
            template_path = "templates/szablon_firmowy.pptx"
            if not os.path.exists(template_path):
                st.error(f"Błąd: Nie znaleziono szablonu w '{template_path}'.")
                st.stop()
                
            # --- ZAKTUALIZOWANE WYWOŁANIE FUNKCJI ---
            report_file_stream = create_pptx_report(
                gemini_response, 
                template_path,
                report_title_input,      # Przekazujemy tytuł
                report_subtitle_input    # Przekazujemy podtytuł
            )
            # --- KONIEC AKTUALIZACJI ---

        except Exception as e:
            st.error(f"Błąd podczas generowania pliku PPTX: {e}")
            st.stop()
            
    # Krok 4: Udostępnienie pliku do pobrania
    st.success("🎉 Raport został wygenerowany!")
    
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # Używamy oczyszczonego tytułu jako nazwy pliku
    safe_title = "".join(c for c in report_title_input if c.isalnum() or c in " _-").rstrip()
    file_name = f"{safe_title}_{today_date}.pptx"
    
    st.download_button(
        label="Pobierz gotowy raport (.pptx)",
        data=report_file_stream,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

elif generate_button and not uploaded_file:
    st.warning("Proszę, prześlij najpierw plik z danymi.")