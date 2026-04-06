@echo off
chcp 65001 >nul
title 🎮 Unified Gaming Optimizer - START HERE

echo.
echo 🎮 UNIFIED GAMING OPTIMIZER - START HERE
echo ========================================
echo.
echo 🚀 Willkommen zum Gaming Optimizer!
echo.
echo DEIN SYSTEM:
echo   🖥️  CPU: AMD Ryzen 7 7735HS
echo   🎮  GPU: AMD Radeon RX 7600S  
echo   🧠  RAM: 15.24GB DDR5
echo   💾  SSD: 928GB NVMe
echo.
echo 🎯 PERFORMANCE: HIGH-END GAMING (74.8/100)
echo.
echo 📋 VERFÜGBARE OPTIONEN:
echo   [1] 🚀 Gaming Optimizer starten
echo   [2] 🧪 Production Test durchführen
echo   [3] 📊 Performance Benchmark
echo   [4] 🚀 FSR Optimierung testen
echo   [5] 📋 Installation prüfen
echo   [0] Beenden
echo.

choice /c 123450 /n /m "Wähle Option: "

if errorlevel 5 goto install_check
if errorlevel 4 goto fsr_test
if errorlevel 3 goto benchmark
if errorlevel 2 goto production_test
if errorlevel 1 goto start_optimizer
if errorlevel 0 goto exit

:start_optimizer
echo.
echo 🚀 Gaming Optimizer wird gestartet...
echo.
python run_optimizer.py
goto end

:production_test
echo.
echo 🧪 Production Test wird durchgeführt...
echo.
python test_production.py
goto end

:benchmark
echo.
echo 📊 Performance Benchmark wird gestartet...
echo.
python test_benchmark.py
goto end

:fsr_test
echo.
echo 🚀 FSR Optimierung wird getestet...
echo.
python core\fsr_optimizer.py
goto end

:install_check
echo.
echo 📋 Installation wird überprüft...
echo.
python -m pip install -r requirements.txt
echo.
python test_production.py
goto end

:exit
echo.
echo 👋 Auf Wiedersehen und viel Spaß beim Gaming!
echo.
timeout /t 3 >nul
exit /b 0

:end
echo.
echo ✅ Vorgang abgeschlossen
echo.
pause
goto start

:main_menu
cls
goto main
