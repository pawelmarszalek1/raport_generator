import pandas as pd
import io

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith(('.xls','.xlsx')):
        df = pd.read_excel(file)
    else:
        raise ValueError("Nieobsługiwany format pliku. Użyj CSV lub Excel")
    
    #konwersja kolumny data na typ data 
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])

    return df

def get_data_summary(df):
    if len(df) > 50:
        summary = df.head(50).to_string()
    else:
        summary = df.to_string()

    summary =f"""Oto próbka danych sprzedażowo-marketingowych:
    {summary}

    Statystyki:
    {df.describe().to_string}"""

    return summary