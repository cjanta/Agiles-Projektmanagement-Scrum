from sqlalchemy import create_engine, Column, Integer, Float, DateTime, MetaData, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

    # Füge einen Unique Constraint für timestamp hinzu
    __table_args__ = (UniqueConstraint('timestamp', name='unique_timestamp'),)

def init_database():
    """Initialisiere die Datenbank und erstelle alle Tabellen wenn sie nicht existieren"""
    # Stelle sicher, dass das Datenbankverzeichnis existiert
    db_dir = os.path.join(os.path.dirname(__file__), '.')
    os.makedirs(db_dir, exist_ok=True)
    
    # Erstelle Datenbankverbindung
    db_path = os.path.join(db_dir, 'crypto_data.db')
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Erstelle Tabellen nur wenn sie nicht existieren
    Base.metadata.create_all(engine, checkfirst=True)
    
    return engine

def get_session():
    """Erstelle und gebe eine neue Datenbanksession zurück"""
    engine = init_database()
    Session = sessionmaker(bind=engine)
    return Session()
