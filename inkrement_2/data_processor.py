import pandas as pd
import numpy as np
from datetime import datetime
from database import Database

class DataProcessor:
    def __init__(self, csv_file='btcusd_1-min_data.csv'):
        self.df = pd.read_csv(csv_file)
        self.prepare_data()
        self.db = Database()

    def prepare_data(self):
        """Daten vorbereiten und bereinigen"""
        # Timestamp in datetime umwandeln
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], unit='s')
        
        # Daten nach Timestamp sortieren
        self.df = self.df.sort_values('Timestamp')
        
        # Duplikate entfernen
        self.df = self.df.drop_duplicates()

    def calculate_indicators(self):
        """Technische Indikatoren berechnen"""
        # Simple Moving Average (SMA)
        self.df['SMA_20'] = self.df['Close'].rolling(window=20).mean()
        
        # Relative Strength Index (RSI)
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = self.df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.df['Close'].ewm(span=26, adjust=False).mean()
        self.df['MACD'] = exp1 - exp2
        self.df['Signal_Line'] = self.df['MACD'].ewm(span=9, adjust=False).mean()

    def save_to_database(self):
        """Daten in der Datenbank speichern"""
        self.db.store_data(self.df)

    def analyze_patterns(self):
        """Einfache Musteranalyse"""
        patterns = []
        
        # Bullish Pattern (3 steigende Kerzen)
        for i in range(len(self.df) - 3):
            if (self.df['Close'].iloc[i] > self.df['Open'].iloc[i] and
                self.df['Close'].iloc[i+1] > self.df['Open'].iloc[i+1] and
                self.df['Close'].iloc[i+2] > self.df['Open'].iloc[i+2]):
                patterns.append({
                    'timestamp': self.df['Timestamp'].iloc[i+2],
                    'pattern': 'Bullish',
                    'confidence': 0.8
                })
        
        return patterns

if __name__ == "__main__":
    processor = DataProcessor()
    processor.calculate_indicators()
    print("\nDaten mit Indikatoren:")
    print(processor.df.tail())
    
    print("\nMusteranalyse:")
    patterns = processor.analyze_patterns()
    for pattern in patterns[:5]:  # Erste 5 Muster anzeigen
        print(f"Zeitpunkt: {pattern['timestamp']}, Muster: {pattern['pattern']}, Konfidenz: {pattern['confidence']}")
