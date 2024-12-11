# Letzter Sprint
## Product Vision
Entwicklung eines automatisierten Handelssystems für Kryptowährungen mit Datenbankanbindung und API-Integration.

## Installation

Vorausetzungen os: Python ab 3.10.6, git
Empfohlen mit: VS-Code zu betreiben

1. Projekt von Git clonen
2. .venv erstellen: python -m venv .\.venv   
3. venv aktivieren: .venv/scripts/activate   
4. terminal zeile sollte nun ähnlich wie folgt beginnen: (.venv) usw.

5. pip install pandas==2.2.3
6. pip install requests==2.31.0
7. pip install python-dotenv==1.0.0
8. pip install sqlalchemy==2.0.21
9. pip install ccxt==4.1.13
10. pip install numpy==2.2.0
11. pip install pytest==7.4.2
12. pip install ta

oder

pip install -r rquirements.txt


optional: pip install kaggle
danach im Terminal zum Download: kaggle datasets download -d mczielinski/bitcoin-historical-data


### Ziel: Trading Bot Grundfunktionen

#### Sprint Backlog
1. Bot-Kernfunktionen
   + Order-Logik Simulation implementieren
   - ~Exchanger-API anbinden~
   - ~Sicherheitsmechanismen~

2. Testing und Optimierung
   + Umfangreiche Tests
   + Performance-Optimierung
   + Dokumentation

## Dailies
- Täglich 15 Minuten
- Zeitpunkt: 09:30 Uhr
- Format: Stand-up Meeting
- Fragen:
  * Was wurde gestern erreicht?
  * Was ist für heute geplant?
  * Gibt es Hindernisse?

## Retrospektive (Ende jedes Sprints)
- Dauer: 1 Stunde
- Fokus auf:
  * Was lief gut?
  * Was kann verbessert werden?
  * Welche Maßnahmen leiten wir ab?

# Epic 3: Trading Bot und Handelssystem
4. Als Benutzer möchte ich automatisierte Trades basierend auf erkannten Mustern ausführen
   - Priorität: Mittel
   - Akzeptanzkriterien:
     * [erledigt] Automatische Order-Ausführung (Bots/Agenten)
     * [erledigt] Logging aller Transaktionen