import pandas as pd 
from database import get_session, PriceData
import os
from datetime import datetime

def load_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.lower()
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.dropna()        
        return df
    except Exception as e:
        print(f"Fehler beim Laden der CSV-Datei: {e}")
        return None

def delete_database_if_exists():
    db_file = "./crypto_data.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Vorhandene Datenbank {db_file} wurde gelöscht.")

def price_data_from_row(row):
    return PriceData(
                    timestamp=row['timestamp'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume']
                )

def find_start_index(start_date, df):
    for i in range(0, len(df)):
        current = df.iloc[i]
        if current['timestamp'] > start_date:
            return i
    return 0

def insert_data(df):
    start_date = datetime(2024, 1, 1)
    start_index = find_start_index(start_date, df)
    delete_database_if_exists()
    session = get_session()
    
    try:
        batch_size = 10000
        for i in range(start_index, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            price_data_objects = []
            
            for _, row in batch.iterrows():      
                price_data = price_data_from_row(row)               
                price_data_objects.append(price_data)
            
            session.bulk_save_objects(price_data_objects)
            session.commit()
            
            print(f"Batch {i//batch_size + 1} verarbeitet: {i+len(batch)}/{len(df)} Einträge")
            
    except Exception as e:
        print(f"Fehler beim Einfügen der Daten: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    data_dir = os.path.join(os.path.dirname(__file__), '.', 'data')
    file_path = os.path.join(data_dir, 'btcusd_1-min_data.csv')
    
    os.makedirs(data_dir, exist_ok=True)
    
    if not os.path.exists(file_path):
        print(f"Datei nicht gefunden: {file_path}")
        return
    
    print("Lade CSV-Daten...")
    df = load_csv_data(file_path)
    
    if df is not None:
        print(f"CSV-Daten erfolgreich geladen. {len(df)} Einträge gefunden.")
        print("Beginne mit dem Einfügen in die Datenbank...")
        insert_data(df)
        print("Datenbankimport abgeschlossen!")
    else:
        print("Fehler beim Laden der CSV-Daten.")

if __name__ == "__main__":
    main()
