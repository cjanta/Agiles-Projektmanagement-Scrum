from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class PriceData(Base):
    __tablename__ = 'price_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

class Database:
    def __init__(self, db_url='sqlite:///crypto_data.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store_data(self, df):
        """
        Speichert DataFrame in der Datenbank
        """
        session = self.Session()
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
        session = self.Session()
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
