@echo off
chcp 65001 >nul
title 🎮 Unified Gaming Optimizer

echo.
echo 🎮 UNIFIED GAMING OPTIMIZER
echo ========================
echo.

:: Wechsle zum Skript-Verzeichnis
cd /d "%~dp0"

:: Überprüfe ob Optimizer existiert
if not exist "run_optimizer.py" (
    echo ❌ Gaming Optimizer nicht gefunden!
    echo.
    echo Stelle sicher, dass du im richtigen Verzeichnis bist.
    echo.
    pause
    exit /b 1
)

:: Starte Optimizer
echo 🚀 Gaming Optimizer wird gestartet...
echo.
python run_optimizer.py

:: Bei Fehler
if errorlevel 1 (
    echo.
    echo ❌ Fehler beim Start!
    echo.
    echo Überprüfe die Installation mit:
    echo install.bat
    echo.
    pause
    exit /b 1
)

echo.
echo 👋 Gaming Optimizer beendet
pause
