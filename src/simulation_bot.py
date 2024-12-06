import pandas as pd
import numpy as np
from datetime import datetime

class TradingSimulation:
    def __init__(self, csv_file='btcusd_1-min_data.csv'):
        self.initial_balance = 10000  # Start mit 10.000 USD
        self.balance = self.initial_balance
        self.btc_amount = 0
        self.trades = []
        self.df = pd.read_csv(csv_file)
        self.prepare_data()

    def prepare_data(self):
        """Daten vorbereiten"""
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], unit='s')
        self.df = self.df.sort_values('Timestamp')
        
        # Technische Indikatoren berechnen
        self.df['SMA_20'] = self.df['Close'].rolling(window=20).mean()
        self.df['SMA_50'] = self.df['Close'].rolling(window=50).mean()

    def execute_trade(self, action, price, timestamp):
        """Handel ausführen"""
        if action == 'buy' and self.balance > 0:
            self.btc_amount = self.balance / price
            trade_value = self.balance
            self.balance = 0
            trade_type = 'Kauf'
        
        elif action == 'sell' and self.btc_amount > 0:
            trade_value = self.btc_amount * price
            self.balance = trade_value
            self.btc_amount = 0
            trade_type = 'Verkauf'
        else:
            return

        portfolio_value = self.balance + (self.btc_amount * price)
        profit = portfolio_value - self.initial_balance
        
        trade = {
            'Zeitpunkt': timestamp,
            'Aktion': trade_type,
            'Kurs': price,
            'Handelswert': trade_value,
            'Portfolio-Wert': portfolio_value,
            'Gewinn/Verlust': profit
        }
        self.trades.append(trade)
        
        print(f"\nNeuer Trade ausgeführt:")
        print(f"Zeitpunkt: {timestamp}")
        print(f"Aktion: {trade_type}")
        print(f"Bitcoin-Kurs: ${price:.2f}")
        print(f"Handelswert: ${trade_value:.2f}")
        print(f"Portfolio-Wert: ${portfolio_value:.2f}")
        print(f"Aktueller Gewinn/Verlust: ${profit:.2f}")
        print("-" * 50)

    def run_simulation(self, start_index=0, max_trades=10):
        """Trading-Simulation durchführen"""
        print("Starte Trading-Simulation...")
        print(f"Startkapital: ${self.initial_balance:.2f}")
        print("-" * 50)

        trade_count = 0
        in_position = False

        for i in range(start_index, len(self.df)-1):
            if trade_count >= max_trades:
                break

            current_price = self.df['Close'].iloc[i]
            next_price = self.df['Close'].iloc[i+1]
            timestamp = self.df['Timestamp'].iloc[i]

            # Einfache Trading-Strategie:
            # Kaufen wenn der Preis steigt
            # Verkaufen wenn der Preis fällt
            if not in_position and next_price > current_price:
                self.execute_trade('buy', current_price, timestamp)
                in_position = True
                trade_count += 1
            elif in_position and next_price < current_price:
                self.execute_trade('sell', current_price, timestamp)
                in_position = False
                trade_count += 1

        # Abschließende Performance-Analyse
        final_value = self.balance + (self.btc_amount * self.df['Close'].iloc[-1])
        total_return = ((final_value - self.initial_balance) / self.initial_balance) * 100
        
        print("\nSimulation abgeschlossen!")
        print(f"Anzahl durchgeführter Trades: {len(self.trades)}")
        print(f"Endkapital: ${final_value:.2f}")
        print(f"Gesamtrendite: {total_return:.2f}%")

if __name__ == "__main__":
    # Trading-Simulation starten
    simulator = TradingSimulation()
    # Führe maximal 10 Trades durch, beginnend vom Anfang der Daten
    simulator.run_simulation(start_index=100, max_trades=10)  # Start bei Index 100 um genug Daten für SMA zu haben
