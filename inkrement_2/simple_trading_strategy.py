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
        self.total_profit = 0
        self.initial_investment = 1000  # Startkapital in USD
        self.current_balance = self.initial_investment
        self.position_size = 0.2  # Nur 20% des Kapitals pro Trade
        self.fee_rate = 0.001  # 0.1% Handelsgebühr pro Trade
        self.trades_history = []

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

    def calculate_position_size(self):
        """Berechne die Positionsgröße basierend auf verfügbarem Kapital"""
        return self.current_balance * self.position_size

    def execute_trade(self, price, is_buy, timestamp):
        """Führe einen Trade aus und berücksichtige Gebühren"""
        position_size = self.calculate_position_size()
        fees = position_size * self.fee_rate
        
        if is_buy:
            btc_amount = (position_size - fees) / price
            self.current_balance -= position_size
            return btc_amount
        else:
            btc_amount = position_size / self.bought_price
            trade_value = btc_amount * price
            fees = trade_value * self.fee_rate
            profit = trade_value - fees - position_size
            self.current_balance += trade_value - fees
            return profit

    def run_strategy(self, start_date, end_date):
        """Führe die Trading-Strategie für den angegebenen Zeitraum aus"""
        df = self.get_price_data(start_date, end_date)
        if df.empty:
            print("Keine Daten für den angegebenen Zeitraum gefunden.")
            return

        for i in range(1, len(df)):
            current = df.iloc[i]
            previous = df.iloc[i-1]

            if self.bought_price is None:
                # Kaufbedingung: Preis fällt um 10%
                if (min(current['open'], current['high'], 
                       current['low'], current['close']) <= 0.9 * previous['close']):
                    self.bought_price = min(current['open'], current['high'],
                                          current['low'], current['close'])
                    btc_amount = self.execute_trade(self.bought_price, True, current['timestamp'])
                    investment = self.calculate_position_size()
                    print(f"Kauf BTC bei ${self.bought_price:.2f} um {current['timestamp']}")
                    print(f"Investment: ${investment:.2f}, BTC Menge: {btc_amount:.8f}")
            else:
                # Verkaufsbedingungen
                if current['high'] >= 1.1 * self.bought_price:  # 10% Gewinn
                    sell_price = current['high']
                    profit = self.execute_trade(sell_price, False, current['timestamp'])
                    self.total_profit += profit
                    self.wins += 1
                    self.trades_history.append({
                        'type': 'win',
                        'buy_price': self.bought_price,
                        'sell_price': sell_price,
                        'profit': profit,
                        'timestamp': current['timestamp']
                    })
                    print(f"Verkauf BTC bei ${sell_price:.2f} (Gewinn: ${profit:.2f}) um {current['timestamp']}")
                    self.bought_price = None
                elif current['low'] <= 0.95 * self.bought_price:  # 5% Verlust (engerer Stop-Loss)
                    sell_price = current['low']
                    loss = self.execute_trade(sell_price, False, current['timestamp'])
                    self.total_profit += loss
                    self.losses += 1
                    self.trades_history.append({
                        'type': 'loss',
                        'buy_price': self.bought_price,
                        'sell_price': sell_price,
                        'profit': loss,
                        'timestamp': current['timestamp']
                    })
                    print(f"Verkauf BTC bei ${sell_price:.2f} (Verlust: ${loss:.2f}) um {current['timestamp']}")
                    self.bought_price = None

        # Zeige Endergebnisse
        print("\nTrading-Ergebnisse:")
        print(f"Startkapital: ${self.initial_investment:.2f}")
        print(f"Endkapital: ${self.current_balance:.2f}")
        print(f"Gesamtgewinn/-verlust: ${self.total_profit:.2f}")
        print(f"Rendite: {((self.current_balance/self.initial_investment)-1)*100:.2f}%")
        print(f"\nAnzahl Trades:")
        print(f"Gewinne: {self.wins}")
        print(f"Verluste: {self.losses}")
        
        if self.wins + self.losses > 0:
            win_rate = self.wins/(self.wins + self.losses)*100
            print(f"Erfolgsquote: {win_rate:.2f}%")
            
            # Zeige durchschnittlichen Gewinn und Verlust
            win_trades = [t for t in self.trades_history if t['type'] == 'win']
            loss_trades = [t for t in self.trades_history if t['type'] == 'loss']
            
            if win_trades:
                avg_win = sum(t['profit'] for t in win_trades) / len(win_trades)
                print(f"\nDurchschnittlicher Gewinn pro Trade: ${avg_win:.2f}")
            if loss_trades:
                avg_loss = sum(t['profit'] for t in loss_trades) / len(loss_trades)
                print(f"Durchschnittlicher Verlust pro Trade: ${avg_loss:.2f}")
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
