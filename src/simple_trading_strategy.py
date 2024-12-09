from database import get_session, PriceData
from sqlalchemy import select
import pandas as pd
from datetime import datetime

class SimpleTrader:
    def __init__(self):
        self.session = get_session()
        self.bought_price = None
        self.wins = 0
        self.losses = 0

    def get_price_data(self, start_date, end_date):
        """Lade Preisdaten aus der Datenbank für einen bestimmten Zeitraum"""
        query = select(PriceData).where(
            PriceData.timestamp.between(start_date, end_date)
        ).order_by(PriceData.timestamp)
        
        result = self.session.execute(query)
        records = result.scalars().all()
        
        return pd.DataFrame([{
            'timestamp': r.timestamp,
            'open': r.open,
            'high': r.high,
            'low': r.low,
            'close': r.close,
            'volume': r.volume
        } for r in records])

    def run_strategy(self, start_date, end_date):
        """Führe die Trading-Strategie für den angegebenen Zeitraum aus"""
        # Hole Daten
        df = self.get_price_data(start_date, end_date)
        if df.empty:
            print("Keine Daten für den angegebenen Zeitraum gefunden.")
            return

        # Trading-Logik
        for i in range(1, len(df)):
            current = df.iloc[i]
            previous = df.iloc[i-1]

            if self.bought_price is None:
                # Kaufbedingung: Preis fällt um 10%
                if (min(current['open'], current['high'], 
                       current['low'], current['close']) <= 0.9 * previous['close']):
                    self.bought_price = min(current['open'], current['high'],
                                          current['low'], current['close'])
                    print(f"Kauf BTC bei {self.bought_price} um {current['timestamp']}")
            else:
                # Verkaufsbedingungen
                if current['high'] >= 1.1 * self.bought_price:  # 10% Gewinn
                    self.wins += 1
                    print(f"Verkauf BTC bei {current['high']} (Gewinn) um {current['timestamp']}")
                    self.bought_price = None
                elif current['low'] <= 0.9 * self.bought_price:  # 10% Verlust
                    self.losses += 1
                    print(f"Verkauf BTC bei {current['low']} (Verlust) um {current['timestamp']}")
                    self.bought_price = None

        # Zeige Endergebnisse
        print("\nTrading-Ergebnisse:")
        print(f"Gewinne: {self.wins}")
        print(f"Verluste: {self.losses}")
        if self.wins + self.losses > 0:
            win_rate = self.wins/(self.wins + self.losses)*100
            print(f"Gewinn/Verlust-Verhältnis: {win_rate:.2f}%")
        else:
            print("Keine Trades ausgeführt.")

if __name__ == "__main__":
    # Beispiel für die Verwendung
    trader = SimpleTrader()
    
    # Definiere Zeitraum (2012-2013 für Testdaten)
    start_date = datetime(2012, 1, 1)
    end_date = datetime(2013, 12, 31)
    
    print(f"Starte Trading-Simulation von {start_date} bis {end_date}")
    trader.run_strategy(start_date, end_date)
