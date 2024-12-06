import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from database import Base, PriceData
import os

def load_csv_to_database(csv_path):
    try:
        # CSV-Datei laden
        print(f"Lade CSV-Datei von: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"Anzahl der geladenen Datensätze: {len(df)}")

        # Timestamp konvertieren und ungültige Timestamps entfernen
        print("Bereinige Timestamps...")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='coerce')
        df = df.dropna(subset=['Timestamp'])  # Entferne Zeilen mit ungültigen Timestamps

        # Datenbankverbindung herstellen
        db_path = os.path.join(os.path.dirname(__file__), '..', 'crypto_data.db')
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(engine)

        # Session erstellen
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Bestehende Daten löschen
            print("Lösche alte Daten...")
            session.query(PriceData).delete()
            session.commit()

            # Neue Daten einfügen
            print("Füge neue Daten ein...")
            batch_size = 1000  # Kleinere Batch-Größe für bessere Performance
            total_rows = len(df)
            count = 0

            for index, row in df.iterrows():
                price_data = PriceData(
                    timestamp=row['Timestamp'],
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume'])
                )
                session.add(price_data)
                count += 1

                # Batch-Commit für bessere Performance
                if count % batch_size == 0:
                    session.commit()
                    print(f"Fortschritt: {count}/{total_rows} Datensätze verarbeitet ({(count/total_rows*100):.2f}%)")

            # Restliche Daten committen
            session.commit()
            print(f"\nFertig! {count} Datensätze wurden in die Datenbank geschrieben.")

            # Überprüfung
            data_count = session.query(PriceData).count()
            print(f"\nAnzahl der Datensätze in der Datenbank: {data_count}")

            # Beispieldaten anzeigen
            print("\nErste 5 Einträge in der Datenbank:")
            first_entries = session.query(PriceData).limit(5).all()
            for entry in first_entries:
                print(f"Timestamp: {entry.timestamp}, Close: ${entry.close:.2f}")

        except Exception as e:
            print(f"Fehler beim Schreiben in die Datenbank: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    except Exception as e:
        print(f"Fehler beim Laden der Daten: {e}")
        raise

if __name__ == "__main__":
    # Pfad zur CSV-Datei
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'btcusd_1-min_data.csv')
    
    if not os.path.exists(csv_path):
        print(f"Fehler: CSV-Datei nicht gefunden unter {csv_path}")
        print("Bitte stellen Sie sicher, dass die Datei 'btcusd_1-min_data.csv' im richtigen Verzeichnis liegt.")
    else:
        load_csv_to_database(csv_path)
