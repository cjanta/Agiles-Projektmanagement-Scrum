import pandas as pd
import numpy as np
from database import get_session, PriceData
from sqlalchemy import select
import ta


# Vor dem ausführen des Codes: pip install ta


class DataProcessor:
    def __init__(self):
        self.session = get_session()

    def get_price_data(self, limit=None):
        """Lade Preisdaten aus der Datenbank"""
        query = select(PriceData).order_by(PriceData.timestamp)
        if limit:
            query = query.limit(limit)
            
        result = self.session.execute(query)
        records = result.scalars().all()
        
        # Konvertiere zu DataFrame
        df = pd.DataFrame([{
            'timestamp': r.timestamp,
            'open': r.open,
            'high': r.high,
            'low': r.low,
            'close': r.close,
            'volume': r.volume
        } for r in records])
        
        return df

    def calculate_indicators(self, df):
        """Berechne technische Indikatoren"""
        # Stelle sicher, dass genügend Daten vorhanden sind
        if len(df) < 50:
            raise ValueError("Nicht genügend Daten für die Berechnung der Indikatoren")

        # RSI (Relative Strength Index)
        df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()

        # MACD (Moving Average Convergence Divergence)
        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(df['close'])
        df['bb_high'] = bollinger.bollinger_hband()
        df['bb_mid'] = bollinger.bollinger_mavg()
        df['bb_low'] = bollinger.bollinger_lband()

        # Moving Averages
        df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(df['close'], window=50).sma_indicator()
        df['sma_200'] = ta.trend.SMAIndicator(df['close'], window=200).sma_indicator()

        # ATR (Average True Range)
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
    
        return df

    def analyze_market_conditions(self, df):
        """Analysiere Marktbedingungen basierend auf technischen Indikatoren"""
        latest = df.iloc[-1]
        
        conditions = {
            'trend': {
                'short_term': 'bullish' if latest['close'] > latest['sma_20'] else 'bearish',
                'medium_term': 'bullish' if latest['close'] > latest['sma_50'] else 'bearish',
                'long_term': 'bullish' if latest['close'] > latest['sma_200'] else 'bearish'
            },
            'momentum': {
                'rsi': latest['rsi'],
                'rsi_condition': 'overbought' if latest['rsi'] > 70 else 'oversold' if latest['rsi'] < 30 else 'neutral',
                'macd': 'bullish' if latest['macd'] > latest['macd_signal'] else 'bearish'
            },
            'volatility': {
                'bb_position': (latest['close'] - latest['bb_low']) / (latest['bb_high'] - latest['bb_low']),
                'atr': latest['atr']
            }
        }
        
        return conditions

    def generate_signals(self, df):
        """Generiere Trading-Signale basierend auf der technischen Analyse"""
        conditions = self.analyze_market_conditions(df)
        
        # Trading-Signal-Logik
        signal = 'hold'  # Standard: halten
        
        # RSI-basierte Signale
        if conditions['momentum']['rsi'] < 30:  # Überverkauft
            signal = 'buy'
        elif conditions['momentum']['rsi'] > 70:  # Überkauft
            signal = 'sell'
            
        # MACD-Bestätigung
        if signal == 'buy' and conditions['momentum']['macd'] == 'bearish':
            signal = 'hold'  # Kein Kauf ohne MACD-Bestätigung
        elif signal == 'sell' and conditions['momentum']['macd'] == 'bullish':
            signal = 'hold'  # Kein Verkauf ohne MACD-Bestätigung
            
        # Trend-Bestätigung
        if signal == 'buy' and conditions['trend']['medium_term'] == 'bearish':
            signal = 'hold'  # Kein Kauf gegen den mittelfristigen Trend
        elif signal == 'sell' and conditions['trend']['medium_term'] == 'bullish':
            signal = 'hold'  # Kein Verkauf gegen den mittelfristigen Trend
        
        return {
            'signal': signal,
            'conditions': conditions,
            'timestamp': df.iloc[-1]['timestamp']
        }

if __name__ == "__main__":
    # Test der Implementierung
    processor = DataProcessor()
    
    # Lade die letzten 1000 Datenpunkte
    print("Lade Daten aus der Datenbank...")
    df = processor.get_price_data(limit=11000)
    
    if not df.empty:
        print(f"Daten geladen. Anzahl der Datenpunkte: {len(df)}")
        
        # Berechne Indikatoren
        print("Berechne technische Indikatoren...")
        df_with_indicators = processor.calculate_indicators(df)
        
        # Generiere Trading-Signal
        print("\nGeneriere Trading-Signal...")
        signal_data = processor.generate_signals(df_with_indicators)
        
        print("\nAktuelles Trading-Signal:")
        print(f"Zeitpunkt: {signal_data['timestamp']}")
        print(f"Signal: {signal_data['signal'].upper()}")
        print("\nMarktbedingungen:")
        for category, data in signal_data['conditions'].items():
            print(f"\n{category.capitalize()}:")
            for key, value in data.items():
                print(f"  {key}: {value}")
    else:
        print("Keine Daten in der Datenbank gefunden.")
