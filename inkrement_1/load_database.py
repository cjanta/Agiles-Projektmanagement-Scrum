import pandas as pd 
from database import get_session, PriceData
import os
from datetime import datetime

def load_csv_data(file_path):
    """Lade und bereinige CSV-Daten"""
    try:
        # Lade CSV-Daten
        df = pd.read_csv(file_path)
        
        # Konvertiere Spaltennamen zu Kleinbuchstaben
        df.columns = df.columns.str.lower()
        
        # Konvertiere Timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Entferne NaN-Werte
        df = df.dropna()
        
        return df
    except Exception as e:
        print(f"Fehler beim Laden der CSV-Datei: {e}")
        return None

def insert_data(df):
    """Füge Daten in die Datenbank ein"""
    session = get_session()
    
    try:
        # Batch-Insert für bessere Performance
        batch_size = 1000
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            # Erstelle PriceData Objekte für den Batch
            price_data_objects = []
            
            for _, row in batch.iterrows():
                price_data = PriceData(
                    timestamp=row['timestamp'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume']
                )
                price_data_objects.append(price_data)
            
            # Füge Batch in die Datenbank ein
            session.bulk_save_objects(price_data_objects)
            session.commit()
            
            print(f"Batch {i//batch_size + 1} verarbeitet: {i+len(batch)}/{len(df)} Einträge")
            
    except Exception as e:
        print(f"Fehler beim Einfügen der Daten: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    # Definiere Dateipfad
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    file_path = os.path.join(data_dir, 'btcusd_1-min_data.csv')
    
    # Stelle sicher, dass das Datenverzeichnis existiert
    os.makedirs(data_dir, exist_ok=True)
    
    # Prüfe ob die Datei existiert
    if not os.path.exists(file_path):
        print(f"Datei nicht gefunden: {file_path}")
        return
    
    # Lade und verarbeite Daten
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
