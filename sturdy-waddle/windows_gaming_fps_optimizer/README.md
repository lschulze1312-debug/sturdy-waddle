# FPS Optimizer

Windows-Tool zur FPS-Optimierung für Gaming.

## Funktionen

- Beendet Hintergrund-Apps (Discord, Chrome, Spotify, etc.)
- Stoppt unnötige Windows-Services
- Aktiviert High-Performance Power-Plan
- Deaktiviert visuelle Effekte
- Setzt GPU auf High-Performance
- Zeigt CPU/GPU/RAM Info und Temperaturen

## Installation

```bash
pip install -r requirements.txt
```

## Nutzung

```bash
python main.py
```

Als Administrator ausführen für volle Funktionalität.

## Struktur

```
src/
  optimizer.py    # Haupt-Optimierungslogik
  system.py       # Hardware-Informationen
  gui.py          # Tkinter Interface
main.py           # Einstiegspunkt
```

## Hinweis

Nutzen auf eigene Verantwortung. Erstellt einen Wiederherstellungspunkt vor dem ersten Einsatz.
