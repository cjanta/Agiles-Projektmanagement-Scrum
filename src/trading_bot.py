import pandas as pd
import numpy as np
from datetime import datetime
from data_processor import DataProcessor

class TradingBot:
    def __init__(self):
        self.processor = DataProcessor()
        self.processor.calculate_indicators()
        self.position = None
        self.balance = 10000  # Startkapital
        self.btc_amount = 0
        self.trades = []

    def analyze_market(self, row):
        """Marktanalyse basierend auf technischen Indikatoren"""
        signals = {
            'buy': 0,
            'sell': 0
        }

        # RSI Signale
        if row['RSI'] < 30:  # Überverkauft
            signals['buy'] += 1
        elif row['RSI'] > 70:  # Überkauft
            signals['sell'] += 1

        # MACD Signale
        if row['MACD'] > row['Signal_Line']:
            signals['buy'] += 1
        elif row['MACD'] < row['Signal_Line']:
            signals['sell'] += 1

        # SMA Signale
        if row['Close'] > row['SMA_20']:
            signals['buy'] += 1
        elif row['Close'] < row['SMA_20']:
            signals['sell'] += 1

        return signals

    def execute_trade(self, action, price, timestamp):
        """Handel ausführen"""
        if action == 'buy' and self.position != 'long':
            # Kaufe BTC
            btc_to_buy = self.balance / price
            self.btc_amount = btc_to_buy
            self.balance = 0
            self.position = 'long'
            self.trades.append({
                'timestamp': timestamp,
                'action': 'buy',
                'price': price,
                'amount': btc_to_buy,
                'balance': self.balance + (self.btc_amount * price)
            })

        elif action == 'sell' and self.position == 'long':
            # Verkaufe BTC
            self.balance = self.btc_amount * price
            self.btc_amount = 0
            self.position = None
            self.trades.append({
                'timestamp': timestamp,
                'action': 'sell',
                'price': price,
                'amount': 0,
                'balance': self.balance
            })

    def backtest(self):
        """Backtest-Strategie"""
        print("Starte Backtest...")
        
        for index, row in self.processor.df.iterrows():
            if pd.isna(row['RSI']) or pd.isna(row['MACD']) or pd.isna(row['Signal_Line']) or pd.isna(row['SMA_20']):
                continue

            signals = self.analyze_market(row)
            
            if signals['buy'] >= 2 and self.position != 'long':
                self.execute_trade('buy', row['Close'], row['Timestamp'])
            elif signals['sell'] >= 2 and self.position == 'long':
                self.execute_trade('sell', row['Close'], row['Timestamp'])

        # Performance-Analyse
        if self.trades:
            initial_balance = 10000
            final_balance = self.balance + (self.btc_amount * self.processor.df['Close'].iloc[-1])
            total_return = ((final_balance - initial_balance) / initial_balance) * 100
            
            print(f"\nBacktest-Ergebnisse:")
            print(f"Anzahl Trades: {len(self.trades)}")
            print(f"Initiales Kapital: ${initial_balance:,.2f}")
            print(f"Finales Kapital: ${final_balance:,.2f}")
            print(f"Gesamtrendite: {total_return:.2f}%")
            
            # Zeige die ersten 5 Trades
            print("\nErste 5 Trades:")
            for trade in self.trades[:5]:
                print(f"Zeitpunkt: {trade['timestamp']}, Aktion: {trade['action']}, "
                      f"Preis: ${trade['price']:.2f}, Balance: ${trade['balance']:.2f}")

if __name__ == "__main__":
    bot = TradingBot()
    bot.backtest()
