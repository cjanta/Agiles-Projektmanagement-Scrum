# Trading Bot Simulator - Installation und Anleitung

## Requirements
* Empfohlen mit: VS-Code zu betreiben  
* os: python 3.10.6 oder höher  

## Virtuelle Umgebung

pandas==2.2.3  
python-dotenv==1.0.0  
sqlalchemy==2.0.21  
ccxt==4.1.13  
numpy==2.2.0  
pytest==7.4.2  
ta==0.11.0  
kaggle==1.6.17  
requests==2.31.0  

## Erstellen der venv
im terminal:  
python -m venv .\.venv


## Einspielen der requirements.txt

venv aktivieren:  
.venv/scripts/activate   


terminal zeile sollte nun ähnlich wie folgt beginnen: (.venv) usw.


pip install -r requirements.txt  

## Download via "./import_data.py"

ausführen mit python: import_data.py


im Ordner: .\data sollte nun die Datei sein: btcusd_1-min_data.csv 


Eine bereits vorhandene Datei wird ersetzt.

## Datenbank erstellen via  "./create_database.py"

ausführen mit python: create_database.py


Eine bereits vorhandene Datei wird ersetzt.

## Simple Trader aktivieren via  "./simple_trader.py"
ausführen mit python: simple_trader.py

Logging erfolgt im python terminal.
