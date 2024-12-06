import pandas as pd

# CSV-Datei lesen
df = pd.read_csv('btcusd_1-min_data.csv')

# Erste 5 Zeilen anzeigen
print("\nErste 5 Zeilen der Daten:")
print(df.head())

# Informationen über den Datensatz
print("\nDatensatz-Info:")
print(df.info())
