# Abi-Orga – Dienste und Strafen

Ein leichtgewichtiges Tool zur Verwaltung von Schülerdiensten, Strafbeträgen und Fortschrittsanzeige im Rahmen der Abikassenorganisation.

## Inhalt

Dieses Repository enthält:

- `index.html`: Die Weboberfläche zur Abfrage von Punkten und Strafen.
- `data.json`: Die strukturierte Datendatei mit gehashten Benutzer-Keys, Dienstpunkten und Strafen.
- `convertjason.py`: Wandelt Rohdaten aus `databack.json` in ein gehashtes `data.json`-Format um.
- `main.py`: Interaktives CLI-Tool zum Batch-Editieren von Punkten und Strafen.
- `makelinks.py`, `keyhasher.py`: Unterstützende Scripte zur Verarbeitung oder Generierung.
- `links.txt`: Optional verwendete Hilfsdatei (z. B. zur Speicherung von Key-Links).

## Verwendung

### Webinterface

1. Öffne `index.html` lokal oder über einen Server.
2. Gib deinen persönlichen Key ein (z. B. `b36e3e62ac`).
3. Es wird angezeigt:
   - Anzahl und Art der geleisteten Dienste (grün, rot oder halb).
   - Aufgelistete Strafen inklusive Begründung und Betrag.
   - Fortschrittsbalken zur Finanzierung.

### Admin-Zugang

- Eingabe des Schlüssels `ADMIN` zeigt eine vollständige Übersicht aller Einträge (Name, Punkte, Strafen, Gesamtsumme).

### Daten vorbereiten

1. Rohdaten mit `"KEY"`-blöcken in `databack.json` bereitstellen.
2. `convertjason.py` ausführen:
   ```bash
   python convertjason.py
   ```
   → Erstellt `data.json` mit gehashten Keys.

### Batchbearbeitung (Punkte & Strafen)

Starte das CLI-Tool:

```bash
python main.py
```

Eingabeformat:

- `P3: Name1, Name2` → Fügt `3` bei Punkten hinzu.
- `H2: Name3` → Fügt `2` bei Halbpunkten hinzu.
- `S0: Name4` → Fügt Strafe vom Typ `0` hinzu.
- `-S1: Name5` → Hebt Strafe vom Typ `1` wieder auf.

Schlüssel:
- `P` = Punkte
- `H` = Halbe Punkte
- `S` = Strafen (`-S` = durchgestrichen)

Eingabe `end` zum Ausführen oder `exit` zum Beenden.

## Datenschutz

Alle Nutzerschlüssel sind mit SHA-256 gehasht, und auf der öffentlichen Seite werden lediglich Kürzel angezeigt – vollständige Namen sind dort nicht sichtbar. Die Datenstruktur unterstützt somit eine gewisse Anonymisierung.

Es ist jedoch zu beachten: Da das Repository öffentlich zugänglich ist, handelt es sich **nicht** um eine datenschutzkonforme Lösung. Ziel dieses Projekts ist es vielmehr, die klassischen öffentlichen „Stift-und-Papier“-Listen abzulösen und eine digitale Alternative zu bieten – insbesondere, um zu vermeiden, dass Straflisten oder Dienstzuweisungen offen in Stufengruppen gepostet werden.

**Hinweis:**  
Mit der Nutzung dieser Seite erklärt sich die Jahrgangsstufe damit einverstanden, dass die Dienst- und Strafübersicht digital verwaltet wird. Die Daten werden intern verarbeitet und dienen ausschließlich der Organisation des Abikomitees.

## Zuletzt aktualisiert

Diese Seite ist derzeit aktiv im Einsatz und wird von der Jahrgangsstufe zur Dienst- und Strafübersicht genutzt.  
17. Mai 2025
