# Windows Gaming FPS Optimizer

## 🎮 Projekt: Eigenständiges Windows Gaming FPS-Optimierungs-Tool

Dieses Projekt wurde aus dem Mainboard-Simulation-Projekt extrahiert und als eigenständiges Tool entwickelt.

## 🚀 Features

### ✅ Implementiert
- **Hardware-Benchmark** - CPU, GPU, RAM Performance-Analyse
- **FPS-Projektionen** - Realistische FPS-Vorhersagen für Games
- **System-Optimierung** - Windows Gaming-Einstellungen
- **Game-Tuning** - Spezifische Optimierungen für beliebte Games
- **Hardware-Datenbank** - 8 CPUs, 13 GPUs, 10 Games
- **Interaktives Menü** - Einfache Bedienung

### 🚧 In Entwicklung
- **Automatische Treiber-Updates**
- **Live Performance-Monitoring**
- **Overclocking-Helper**
- **GPU-Passthrough**

## 📋 Installation

```cmd
# 1. Projekt herunterladen/kopieren
# 2. Dependencies installieren
pip install -r requirements.txt

# 3. Starten
python fps_optimizer.py
```

## 🎯 Verwendung

### 1. Hardware konfigurieren
- CPU auswählen (Intel/AMD)
- GPU auswählen (NVIDIA/AMD)
- RAM Größe und Geschwindigkeit

### 2. Benchmark durchführen
- CPU-Test mit Matrix-Berechnungen
- Memory-Test mit Allokation/Sortierung
- GPU-Test basierend auf Hardware

### 3. FPS-Projektionen anzeigen
- 10 beliebte Games analysiert
- Realistische FPS-Vorhersagen
- Performance-Empfehlungen

### 4. System optimieren
- Game Mode aktivieren
- Power Plan optimieren
- Background Processes minimieren

## 📊 Performance-Kategorien

| Score | Kategorie | Beschreibung |
|-------|-----------|-------------|
| 80+   | 🔥 Extreme Gaming | 4K Gaming, Ray Tracing |
| 60-79 | 🎮 High-End Gaming | 1440p High Settings |
| 40-59 | 👍 Mid-Range Gaming | 1080p Medium-High |
| 25-39 | ⚡ Entry-Level Gaming | 1080p Low-Medium |
| <25   | 💻 Office/Browsing | Nicht für Gaming |

## 🎮 Unterstützte Games

- **FPS:** CS:GO, Valorant, Apex Legends
- **Battle Royale:** Fortnite, PUBG, Warzone
- **RPG:** Cyberpunk 2077, Witcher 3, Elden Ring
- **Racing:** Forza Horizon 5

## ⚡ Sofort-Optimierungen

1. **Game Mode aktivieren** (+5-15% FPS)
2. **Power Plan Maximum** (+3-8% FPS)
3. **XMP/EXPO Profile** (+5-12% FPS)
4. **Background Processes** (+2-6% FPS)

## 📈 Beispiel-Ergebnisse

```
📊 BENCHMARK ERGEBNISSE
🔥 CPU Score: 45.2 (AMD Ryzen 5 2600)
🧠 Memory Score: 38.5 (16GB @ 3200MHz)
🎮 GPU Score: 52.1 (NVIDIA GTX 1060)
📈 Overall Score: 48.9
🎮 Kategorie: 👍 Mid-Range Gaming

Game-Projektionen (1080p, Medium):
CS:GO: 125 FPS 🟢 Excellent
Valorant: 118 FPS 🟢 Excellent
Fortnite: 89 FPS 🟡 Good
Cyberpunk 2077: 45 FPS 🟠 Playable
```

## 🔧 Konfiguration

Settings.json wird automatisch erstellt:
```json
{
  "optimization_level": "balanced",
  "target_fps": 60,
  "max_temperature": 80,
  "enable_overclock": false,
  "auto_update_drivers": true,
  "selected_cpu": "AMD Ryzen 5 2600",
  "selected_gpu": "NVIDIA GTX 1060",
  "ram_gb": 16,
  "ram_speed": 3200
}
```

## � Projektstruktur

```
windows_gaming_fps_optimizer/
├── fps_optimizer.py              # Hauptanwendung
├── requirements.txt              # Dependencies
├── README.md                     # Diese Datei
├── settings.json                # Konfiguration (auto)
└── core/
    └── hardware_benchmark.py    # Benchmark-Modul
```

## 🛠️ Dependencies

- `psutil` - System-Informationen
- `GPUtil` - GPU-Informationen (optional)
- `matplotlib` - Graphen (zukünftig)
- `tkinter` - GUI (Python Standard)

## 🚀 Start

```cmd
# Interaktiver Modus
python fps_optimizer.py

# Nur Benchmark
python core/hardware_benchmark.py
```

## 📝 Lizenz

MIT License - Frei verwendbar

---

**Status:** ✅ Funktionstüchtig  
**Version:** 1.0.0  
**Kompatibilität:** Windows 10/11
