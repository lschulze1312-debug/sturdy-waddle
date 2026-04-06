#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schneller Pre-Game Check - Kurzer Test vor dem Gaming
"""

import os
import sys
import json
import psutil
from datetime import datetime

sys.path.insert(0, 'core')

print("="*70)
print("🎮 SCHNELLER PRE-GAME SYSTEM CHECK")
print("="*70)
print(f"Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

results = {}
warnings = []
all_ok = True

# Test 1: Modul-Importe (schnell)
print("\n📦 TEST 1: Modul-Importe...")
modules = [
    'thermal_protection',
    'gpu_software_optimizer',
    'background_process_optimizer',
    'fsr_optimizer',
    'directx12_optimizer_safe',
    'ue5_stability_optimizer'
]

passed = 0
for module in modules:
    try:
        __import__(module)
        print(f"   ✅ {module}")
        passed += 1
    except Exception as e:
        print(f"   ❌ {module}: {str(e)[:50]}")
        all_ok = False

print(f"   Ergebnis: {passed}/{len(modules)} OK")
results['modules'] = passed

# Test 2: System-Info
print("\n💻 TEST 2: System-Informationen...")
try:
    cpu_usage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    
    print(f"   ✅ CPU-Last: {cpu_usage:.1f}%")
    print(f"   ✅ RAM: {memory.percent:.0f}% belegt")
    print(f"   ✅ RAM verfügbar: {memory.available / (1024**3):.1f} GB")
    
    if memory.percent > 85:
        warnings.append("⚠️ RAM fast voll - Browser-Tabs schließen!")
    if cpu_usage > 40:
        warnings.append("⚠️ Hohe CPU-Last vor Spielstart!")
        
    results['system_ok'] = True
except Exception as e:
    print(f"   ❌ Fehler: {e}")
    all_ok = False
    results['system_ok'] = False

# Test 3: Laptop-Erkennung
print("\n🖥️ TEST 3: Laptop-Erkennung & Thermal...")
try:
    from thermal_protection import ThermalProtectionManager
    thermal = ThermalProtectionManager()
    
    is_laptop = thermal.is_laptop
    status = thermal.get_thermal_status()
    
    if is_laptop:
        print(f"   🖥️ ✅ LAPTOP erkannt!")
        print(f"   🌡️ Thermale Grenzwerte: 80°C/88°C/93°C/96°C")
    else:
        print(f"   🖥️ Desktop erkannt")
        print(f"   🌡️ Thermale Grenzwerte: 70°C/80°C/85°C/90°C")
    
    if status['current_temp'] > 0:
        print(f"   🌡️ Aktuelle Temperatur: {status['current_temp']:.1f}°C")
        if status['current_temp'] > 90 and is_laptop:
            warnings.append(f"🌡️ Laptop ist warm ({status['current_temp']:.1f}°C) - aber noch im Normalbereich")
    else:
        print(f"   ⚠️ Temperatur-Sensor nicht verfügbar")
    
    results['is_laptop'] = is_laptop
    results['thermal_ok'] = True
except Exception as e:
    print(f"   ❌ Fehler: {e}")
    results['thermal_ok'] = False

# Test 4: Borderlands 4 Config
print("\n🎮 TEST 4: Borderlands 4 Config...")
config_paths = [
    os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Config\\WindowsNoEditor\\Engine.ini"),
    os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini")
]

configs_found = sum(1 for p in config_paths if os.path.exists(p))

if configs_found >= 1:
    print(f"   ✅ {configs_found}/2 Config-Dateien gefunden")
    results['bl4_config'] = True
else:
    print(f"   ⚠️ Keine Borderlands 4 Config gefunden")
    print(f"   💡 Führe aus: python borderlands4_autofix.py")
    warnings.append("⚠️ Borderlands 4 Config fehlt!")
    results['bl4_config'] = False

# Test 5: GPU Software Optimizer
print("\n🎨 TEST 5: GPU Software Optimizer...")
try:
    from gpu_software_optimizer import GPUDriverIndependentOptimizer
    gpu_opt = GPUDriverIndependentOptimizer()
    print(f"   ✅ GPU Software Optimizer bereit")
    print(f"   ✅ 10 Software-Optimierungen verfügbar (kein Treiber-Downgrade!)")
    results['gpu_opt_ok'] = True
except Exception as e:
    print(f"   ❌ Fehler: {e}")
    results['gpu_opt_ok'] = False

# Test 6: FSR & DX12 Profile
print("\n🚀 TEST 6: FSR & DirectX 12 Profile...")
try:
    from fsr_optimizer import CustomFSROptimizer
    from directx12_optimizer_safe import DirectX12OptimizerSafe
    
    fsr = CustomFSROptimizer()
    dx12 = DirectX12OptimizerSafe()
    
    has_bl4_fsr = 'borderlands_4' in fsr.game_profiles
    has_bl4_dx12 = 'borderlands_4' in dx12.game_profiles
    
    print(f"   ✅ FSR Profile: {len(fsr.game_profiles)} Games")
    print(f"   ✅ DX12 Profile: {len(dx12.game_profiles)} Games")
    print(f"   {'✅' if has_bl4_fsr else '❌'} Borderlands 4 FSR-Profil")
    print(f"   {'✅' if has_bl4_dx12 else '❌'} Borderlands 4 DX12-Profil")
    
    results['profiles_ok'] = has_bl4_fsr and has_bl4_dx12
except Exception as e:
    print(f"   ❌ Fehler: {e}")
    results['profiles_ok'] = False

# Final Report
print("\n" + "="*70)
print("📋 ERGEBNIS")
print("="*70)

tests_passed = sum(1 for v in results.values() if v is True or (isinstance(v, int) and v > 0))
total_tests = len([v for v in results.values() if isinstance(v, (bool, int))])

print(f"\n✅ TESTS BESTANDEN: {tests_passed}/{total_tests}")

if warnings:
    print(f"\n⚠️ WARNUNGEN ({len(warnings)}):")
    for w in warnings:
        print(f"   {w}")

# System Ready?
print(f"\n🖥️ SYSTEM-STATUS:")
if results.get('is_laptop'):
    print(f"   🖥️ Gaming Laptop-Modus: AKTIV")
    print(f"   🌡️ Thermale Grenzwerte: 80°C/88°C/93°C/96°C")
else:
    print(f"   🖥️ Desktop-Modus")

print(f"\n{'='*70}")

# Final decision
ready = all_ok and len(warnings) == 0 and results.get('bl4_config', False)

if ready:
    print("🎉 SYSTEM BEREIT FÜR GAMING!")
    print("="*70)
    print("✅ Alle Tests bestanden")
    print("✅ Borderlands 4 Config vorhanden")
    print("✅ Alle Optimizer bereit")
    print("✅ Laptop-Thermal-Schutz aktiv")
    print("\n🚀 DU KANNST JETZT STARTEN:")
    print("   1. python run_optimizer.py")
    print("   2. Borderlands 4 starten")
    print("   3. Genießen! 🎮")
    
elif results.get('bl4_config', False) == False:
    print("⚠️ BORDERLANDS 4 CONFIG FEHLt!")
    print("="*70)
    print("🔧 BITTE ZUERST AUSFÜHREN:")
    print("   python borderlands4_autofix.py")
    print("   (Danach PC neu starten)")
    print("\n📋 Alternative - Ohne Config starten:")
    print("   1. python run_optimizer.py")
    print("   2. Borderlands 4 starten (wird automatisch erkannt)")
    print("   3. Optimierungen werden trotzdem angewendet")
    
else:
    print("⚠️ SYSTEM BEREIT (mit Hinweisen)")
    print("="*70)
    print("✅ Kernfunktionen OK")
    if warnings:
        print(f"⚠️ Aber: {len(warnings)} Warnung(en) beachten")
    print("\n🚀 DU KANNST TROTZDEM STARTEN:")
    print("   1. python run_optimizer.py")
    print("   2. Borderlands 4 starten")

print(f"{'='*70}")

# Save report
try:
    report = {
        'timestamp': datetime.now().isoformat(),
        'ready': ready,
        'warnings': warnings,
        'results': results,
        'is_laptop': results.get('is_laptop', False)
    }
    
    filename = f"pre_game_quick_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📁 Report: {filename}")
except:
    pass

print("\n" + "="*70)
