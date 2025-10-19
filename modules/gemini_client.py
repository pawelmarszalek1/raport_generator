import google.generativeai as genai
import os

def configure_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_insights(data_summary_text):
    if not os.getenv("GEMINI_API_KEY"):
        raise EnvironmentError("Nie znaleziono GEMINI_API_KEY. Ustaw go w pliku .env")
    
    configure_gemini()

    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""Jesteś ekspertem analityki biznesowej specjalizującym się w danych sprzedażowych i marketingowych. 
    Twoim zadaniem jest przygotowanie treści na slajdy do raportu dla zarządu.

    Przeanalizuj poniższe podsumowanie danych:
    {data_summary_text}

    Na tej podstawie wygeneruj treść raportu w trzech sekcjach. 
    Użyj profesjonalnego, ale zwięzłego języka biznesowego.
    NIE UŻYWAJ FORMATOWANIA MARKDOWN (np. **gwiazdek**).

    Oto format, którego masz rygorystycznie przestrzegać:

    [SEKCJA:PODSUMOWANIE_ZARZADU]
    (Tutaj wpisz 3 kluczowe punkty (bullet points) podsumowujące najważniejsze trendy, sukcesy lub problemy widoczne w danych.)

    [SEKCJA:ANALIZA_SPRZEDAZY]
    (Tutaj wpisz szczegółową analizę sprzedaży. Odpowiedz na pytania: Co się najlepiej sprzedaje? Jakie są trendy? Użyj 2-3 akapitów.)

    [SEKCJA:ANALIZA_MARKETINGU]
    (Tutaj wpisz analizę efektywności marketingu. Które kanały przynoszą największy przychód? Jaki jest zwrot z inwestycji (ROAS), jeśli można go oszacować?)

    [SEKCJA:WNIOSKI_I_REKOMENDACJE]
    (Tutaj wpisz 3 konkretne, aktywne rekomendacje biznesowe na kolejny miesiąc, bazując na danych. Np. "Zwiększyć budżet na...", "Zoptymalizować kampanię...")
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Wystąpił błąd podczas komunikacji z Gemini: {e}"