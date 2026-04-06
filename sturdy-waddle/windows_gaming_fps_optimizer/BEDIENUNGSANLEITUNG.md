# 🎮 Unified Gaming Optimizer - Vollständige Bedienungsanleitung

## 📋 INHALTSVERZEICHNIS
1. [Erste Schritte auf deinem System](#1-erste-schritte-auf-deinem-system)
2. [Tägliche Nutzung](#2-tägliche-nutzung)
3. [Installation auf anderen PCs](#3-installation-auf-anderen-pcs)
4. [Best Practices](#4-best-practices)
5. [Fehlerbehebung](#5-fehlerbehebung)

---

## 1. ERSTE SCHRITTE AUF DEINEM SYSTEM

### 🚀 Schnellstart (Empfohlen)

#### Option A: Automatische Installation
```cmd
# 1. Öffne PowerShell oder CMD als Administrator
# 2. Navigiere zum Ordner:
cd C:\Users\franz\Documents\Windows_FPS_Optimierer\windows_gaming_fps_optimizer

# 3. Führe die Installation aus:
install.bat
```

#### Option B: Manuelle Installation
```cmd
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. Installation testen
python test_production.py

# 3. Optimizer starten
python START_HERE.bat
```

### 🎯 Erste Konfiguration

#### Schritt 1: System-Check
```cmd
python borderlands4_debugger.py
```
**Das macht es:**
- Analysiert dein System
- Findet Performance-Probleme
- Zeigt Empfehlungen

#### Schritt 2: Automatische Fehlerbehebung
```cmd
python borderlands4_autofix.py
```
**Das macht es:**
- Behebt automatisch alle gefundenen Probleme
- Optimiert Windows-Einstellungen
- Erstellt Game-Configs

#### Schritt 3: PC neu starten
```
🔄 WICHTIG: PC unbedingt neu starten!
Alle Änderungen werden erst nach Neustart wirksam.
```

---

## 2. TÄGLICHE NUTZUNG

### 🎮 Für Gaming (Automatisch)

```cmd
# Starte den Optimizer VOR dem Spielen:
python quick_start.py

# Oder:
python run_optimizer.py
```

**Was passiert automatisch:**
1. ✅ Game wird erkannt (Fortnite, Borderlands 4, etc.)
2. 🚀 FSR Optimierung startet
3. 🎮 DirectX 12 wird optimiert
4. 🔧 Hintergrundprozesse werden reduziert
5. ⚡ CPU/GPU Priorität wird erhöht
6. 📊 Performance wird überwacht

### 📊 Manuelle Steuerung

```
🎮 UNIFIED GAMING OPTIMIZER - HAUPTMENÜ

[1] Profil wechseln          → Silent/Balanced/Gaming/Performance
[2] Performance-Benchmark    → System testen
[3] System-Report           → Detaillierte Infos
[4] Einstellungen           → Konfiguration
[5] Performance-Graph       → Visualisierung
[6] Monitoring              → Echtzeit-Überwachung
[7] FSR Optimierung         → Custom FSR Einstellungen
[8] DirectX 12            → DX12 Optimierung
[9] Hintergrundprozesse     → Windows optimieren
[0] Beenden
```

### 🎯 Empfohlene Workflows

#### Workflow A: Schnelles Gaming
```cmd
1. START_HERE.bat starten
2. Option [9] wählen → Gaming-Modus aktivieren
3. Spiel starten
4. Nach dem Spielen: Option [0] → Alle Optimierungen zurücksetzen
```

#### Workflow B: Borderlands 4 (Probleme)
```cmd
1. borderlands4_autofix.py ausführen (einmalig)
2. PC neu starten
3. run_optimizer.py starten
4. Borderlands 4 starten
5. Alles läuft automatisch!
```

#### Workflow C: FPS-Probleme analysieren
```cmd
1. borderlands4_debugger.py ausführen
2. Probleme identifizieren
3. borderlands4_autofix.py ausführen
4. Testen
```

---

## 3. INSTALLATION AUF ANDEREN PCS

### 📦 Methode 1: Kompletter Ordner kopieren (Empfohlen)

#### Schritt 1: Vorbereitung
```
Auf deinem PC (Quelle):
1. Ordner packen: C:\Users\franz\Documents\Windows_FPS_Optimierer
2. In ZIP packen oder auf USB-Stick kopieren
```

#### Schritt 2: Auf neuem PC installieren
```cmd
# Auf dem neuen PC:
1. Ordner kopieren nach: C:\Users\[Username]\Documents\
2. Ordner umbenennen in: Windows_FPS_Optimierer

# Installation:
cd C:\Users\%USERNAME%\Documents\Windows_FPS_Optimierer\windows_gaming_fps_optimizer
install.bat
```

#### Schritt 3: Anpassen für neuen PC
```cmd
# Wichtig: Neue Konfiguration erstellen
python borderlands4_debugger.py
python borderlands4_autofix.py
```

### 📦 Methode 2: GitHub/Cloud Installation

#### Schritt 1: ZIP erstellen
```cmd
# Auf deinem PC:
cd C:\Users\franz\Documents

# ZIP erstellen:
powershell Compress-Archive -Path Windows_FPS_Optimierer -DestinationPath GamingOptimizer.zip
```

#### Schritt 2: Auf anderen PCs verteilen
```
Optionen:
• USB-Stick
• Cloud-Speicher (OneDrive, Dropbox, Google Drive)
• Netzwerk-Freigabe
• GitHub Repository
```

#### Schritt 3: Installation auf neuem PC
```cmd
# 1. ZIP entpacken
cd C:\Users\%USERNAME%\Documents
powershell Expand-Archive -Path GamingOptimizer.zip -DestinationPath .

# 2. Installation
cd Windows_FPS_Optimierer\windows_gaming_fps_optimizer
install.bat
```

### 📦 Methode 3: Portable Version (Für USB-Stick)

#### Portable Version erstellen:
```cmd
# Struktur für USB-Stick:
GamingOptimizer\
├── install.bat
├── START_HERE.bat
├── requirements.txt
├── unified_optimizer.py
├── core\
│   ├── real_time_optimizer.py
│   ├── system_monitor.py
│   ├── hardware_benchmark.py
│   ├── fsr_optimizer.py
│   ├── directx12_optimizer_safe.py
│   ├── background_process_optimizer.py
│   └── ue5_stability_optimizer.py
└── logs\
```

#### Nutzung vom USB-Stick:
```cmd
# 1. USB-Stick einstecken
# 2. Auf fremden PC:
E:\GamingOptimizer\windows_gaming_fps_optimizer\START_HERE.bat

# Hinweis: Python muss auf dem PC installiert sein!
```

---

## 4. BEST PRACTICES

### ✅ DO's (Empfohlen)

```
✅ IMMER tun:
• Vor dem Spielen: Optimizer starten
• Nach dem Spielen: Optimizer beenden (Option [0])
• Regelmäßig: borderlands4_debugger.py ausführen
• Bei Problemen: borderlands4_autofix.py ausführen
• Updates: requirements.txt aktuell halten
• Backup: Wichtige Configs sichern
```

### ❌ DON'Ts (Vermeiden)

```
❌ NIE tun:
• Mehrere Optimizer gleichzeitig laufen lassen
• Registry manuell bearbeiten
• Systemdateien löschen
• Antivirus während Gaming deaktivieren (nur Ausnahmen!)
• Ohne Backup experimentieren
```

### 🎮 Optimale Einstellungen

#### Für Fortnite:
```cmd
# FSR Modus: Performance (67% Render)
# Target FPS: 144
# Algorithmen: Edge-Aware + Temporal
```

#### Für Borderlands 4:
```cmd
# FSR Modus: Quality (89% Render)
# Target FPS: 60
# UE5: Lumen deaktiviert, Nanite aktiviert
```

#### Für Valorant:
```cmd
# FSR Modus: Ultra Performance (50% Render)
# Target FPS: 240
# Algorithmen: Minimal (nur Anti-Aliasing)
```

---

## 5. FEHLERBEHEBUNG

### 🔧 Häufige Probleme

#### Problem 1: "Module not found"
```cmd
Lösung:
pip install -r requirements.txt
```

#### Problem 2: "Zugriff verweigert"
```cmd
Lösung:
# Als Administrator ausführen!
Rechtsklick auf START_HERE.bat → "Als Administrator ausführen"
```

#### Problem 3: FPS nicht besser
```cmd
Lösung:
1. borderlands4_debugger.py ausführen
2. borderlands4_autofix.py ausführen
3. PC neu starten
4. Im Spiel: Settings auf Medium statt Low!
```

#### Problem 4: Game erkannt nicht
```cmd
Lösung:
# Manuelles Profil wählen:
Option [1] → gaming
```

#### Problem 5: Optimizer stürzt ab
```cmd
Lösung:
# Logs prüfen:
cd logs
type optimizer_YYYYMMDD.log
```

### 🆘 Support

#### Wichtige Dateien für Support:
```
Bei Problemen diese Dateien bereithalten:
• logs/optimizer_YYYYMMDD.log
• borderlands4_debug_*.json
• borderlands4_fixes_*.json
• system_specs.json
```

#### Debug-Modus:
```cmd
# Ausführliche Logs:
python run_optimizer.py --debug
```

---

## 📊 Übersicht: Alle verfügbaren Scripts

| Script | Zweck | Nutzung |
|--------|-------|---------|
| `START_HERE.bat` | Haupt-Einstieg | Täglich |
| `quick_start.py` | Schneller Start | Täglich |
| `run_optimizer.py` | Vollständiger Start | Täglich |
| `install.bat` | Erstinstallation | Einmalig |
| `test_production.py` | Installation testen | Nach Installation |
| `borderlands4_debugger.py` | Probleme finden | Bei Problemen |
| `borderlands4_autofix.py` | Probleme beheben | Bei Problemen |
| `test_benchmark.py` | Performance testen | Nach Änderungen |
| `bug_analysis.py` | Fehleranalyse | Entwicklung |

---

## 🎉 ZUSAMMENFASSUNG

### Für deinen täglichen Gebrauch:
```cmd
# Morgen:
1. START_HERE.bat
2. Option [9] → Gaming-Modus
3. Spielen

# Abend:
1. Option [0] → Beenden
```

### Für andere PCs:
```cmd
# 1. Ordner kopieren
# 2. install.bat ausführen
# 3. borderlands4_autofix.py ausführen
# 4. PC neu starten
# 5. Fertig!
```

---

**Viel Spaß mit stabilen FPS! 🎮🚀**

*Letzte Aktualisierung: 2026-04-06*
