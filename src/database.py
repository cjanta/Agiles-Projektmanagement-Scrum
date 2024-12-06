from sqlalchemy import create_engine, Column, Integer, Float, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

# Erstelle Base
Base = declarative_base()

class PriceData(Base):
    __tablename__ = 'price_data'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

def init_database():
    """Initialisiere die Datenbank und erstelle alle Tabellen"""
    # Stelle sicher, dass das Datenbankverzeichnis existiert
    db_dir = os.path.join(os.path.dirname(__file__), '..')
    os.makedirs(db_dir, exist_ok=True)
    
    # Erstelle Datenbankverbindung
    db_path = os.path.join(db_dir, 'crypto_data.db')
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Erstelle Tabellen
    Base.metadata.create_all(engine)
    
    return engine

def get_session():
    """Erstelle und gebe eine neue Datenbanksession zurück"""
    engine = init_database()
    Session = sessionmaker(bind=engine)
    return Session()

class Database:
    def __init__(self, db_url='sqlite:///crypto_data.db'):
        self.engine = init_database()
        self.Session = sessionmaker(bind=self.engine)

    def store_data(self, df):
        """
        Speichert DataFrame in der Datenbank
        """
        session = get_session()
        try:
            for _, row in df.iterrows():
                price_data = PriceData(
                    timestamp=row['timestamp'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume']
                )
                session.add(price_data)
            session.commit()
            print("Daten erfolgreich in der Datenbank gespeichert")
        except Exception as e:
            session.rollback()
            print(f"Fehler beim Speichern in der Datenbank: {e}")
        finally:
            session.close()

    def get_latest_data(self, limit=100):
        """
        Holt die neuesten Einträge aus der Datenbank
        """
        session = get_session()
        try:
            data = session.query(PriceData).order_by(PriceData.timestamp.desc()).limit(limit).all()
            return pd.DataFrame([{
                'timestamp': d.timestamp,
                'open': d.open,
                'high': d.high,
                'low': d.low,
                'close': d.close,
                'volume': d.volume
            } for d in data])
        finally:
            session.close()
