@echo off
chcp 65001 >nul
title 🎮 Unified Gaming Optimizer - Installation

echo.
echo 🚀 UNIFIED GAMING OPTIMIZER - INSTALLATION
echo ========================================
echo.

:: Überprüfe Python Installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nicht gefunden!
    echo.
    echo Bitte installiere Python 3.8+ von:
    echo https://www.python.org/downloads/
    echo.
    echo Danach dieses Skript erneut ausführen.
    pause
    exit /b 1
)

echo ✅ Python gefunden
python --version

:: Überprüfe ob im richtigen Verzeichnis
if not exist "unified_optimizer.py" (
    echo ❌ unified_optimizer.py nicht gefunden!
    echo.
    echo Stelle sicher, dass du im richtigen Verzeichnis bist:
    echo windows_gaming_fps_optimizer\
    echo.
    pause
    exit /b 1
)

echo ✅ Dateien gefunden

:: Dependencies installieren
echo.
echo 🔧 Dependencies installieren...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Installation fehlgeschlagen!
    echo.
    echo Versuche manuelle Installation:
    echo pip install psutil numpy opencv-python pywin32 matplotlib
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies installiert

:: Erstelle Verzeichnisse
if not exist "logs" mkdir logs
if not exist "bug_reports" mkdir bug_reports

echo ✅ Verzeichnisse erstellt

:: Starte Quick Start
echo.
echo 🎮 Installation abgeschlossen!
echo.
echo 🚀 Gaming Optimizer wird gestartet...
echo.
pause
python quick_start.py

exit /b 0
