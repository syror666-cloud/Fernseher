# Dosisrechner Tierarzneimittel

Lokales Programm: Wirkstoff suchen, Körpergewicht des Tieres eingeben – alle
Dosisangaben pro kg (z. B. `12 - 15 mg/kg`) werden auf das Gewicht umgerechnet.

Enthalten sind die Dosierungen von der Seite
[vetpharm.uzh.ch – Ibuprofen, Dosierungen](https://www.vetpharm.uzh.ch/Wirkstoffe/000000001568/7211_05.html)
(13 Dosierungen für Pferd, Hund, Rind, Kaninchen, Maus, Huhn sowie die allgemeinen Hinweise,
z. B. die Warnung zu Ibuprofen beim Hund).

## Im Browser ohne Installation

`web/dosisrechner.html` ist eine einzelne Datei, die komplett im Browser läuft (Doppelklick genügt,
funktioniert auch offline – nur die Schriftart wird aus dem Internet geladen, sonst gilt die Systemschrift).
Sie lässt sich per E-Mail/Messenger weitergeben oder auf jeden Webspace legen.

Nach dem Import weiterer Wirkstoffe die Datei neu erzeugen:

```bash
python3 dosisrechner.py export-web
```

## Starten (lokale Python-Version)

Benötigt nur **Python 3.8+**, keine weiteren Pakete.

```bash
cd dosisrechner
python3 dosisrechner.py
```

Der Browser öffnet sich automatisch mit `http://127.0.0.1:8765/`. Das Programm läuft
nur lokal auf deinem Rechner. Beenden mit `Strg+C` im Terminal.

## Bedienung

- **Wirkstoff**: tippen, Vorschlag mit Enter/Maus auswählen
- **Körpergewicht**: in kg oder g (für Kleinsäuger), Komma oder Punkt erlaubt
- **Tierart**: optional filtern
- Berechnete Werte erscheinen blau hinter jeder mg/kg-Angabe (Dosis **pro Gabe**).
  Sehr kleine/große Werte werden zusätzlich in µg bzw. g angezeigt.

## Weitere Wirkstoffe hinzufügen

Die Dosierungsseite eines anderen Wirkstoffs auf vetpharm.uzh.ch (Adresse endet auf `_05.html`) importieren:

```bash
python3 dosisrechner.py import "https://www.vetpharm.uzh.ch/Wirkstoffe/<nummer>/<nummer>_05.html"
python3 dosisrechner.py liste
```

Ein erneuter Import desselben Wirkstoffs ersetzt die vorhandenen Daten.

## Aufbau

| Datei | Inhalt |
|---|---|
| `dosisrechner.py` | SQLite-Datenbank, lokaler Webserver, Kommandozeile |
| `dosis.py` | Erkennung der mg/kg-Angaben und Berechnung |
| `vetpharm_import.py` | Liest eine vetpharm-Dosierungsseite ein |
| `static/index.html` | Oberfläche der Python-Version |
| `static/web_vorlage.html` | Vorlage der eigenständigen Web-Version |
| `web/dosisrechner.html` | Fertige Web-Version mit allen Daten (erzeugt mit `export-web`) |
| `data/startdaten.json` | Startdaten (Ibuprofen); daraus wird beim ersten Start `data/dosierungen.db` erzeugt |
| `tests/` | Tests: `python3 -m unittest discover -s tests` |

## Hinweis

Daten: CliniPharm/CliniTox, Institut für Veterinärpharmakologie und ‑toxikologie, Universität Zürich.
Die Berechnung ersetzt keine tierärztliche Beurteilung – Angaben vor der Anwendung immer prüfen.
