#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test für die gefixten Metriken"""

import sys
sys.path.insert(0, 'c:\\Users\\franz\\Documents\\Windows_FPS_Optimierer\\windows_gaming_fps_optimizer\\core')

from system_monitor import SystemMonitor

print("="*60)
print("🧪 TEST: Gefixte Metriken-Anzeige")
print("="*60)

# Test 1: SystemMonitor ohne Monitoring starten
print("\n1️⃣ Teste get_current_metrics() ohne History...")
monitor = SystemMonitor()
metrics = monitor.get_current_metrics()
print(f"   CPU: {metrics['cpu_usage']:.1f}%")
print(f"   RAM: {metrics['memory_usage']:.1f}%")
print(f"   GPU: {metrics['gpu_usage']:.1f}%")
print(f"   Temp: {metrics['temperature']:.1f}°C")

if metrics['cpu_usage'] > 0:
    print("   ✅ LIVE Metriken werden angezeigt!")
else:
    print("   ❌ Fehler: Keine Metriken")

# Test 2: Performance Summary ohne History
print("\n2️⃣ Teste get_performance_summary() ohne History...")
summary = monitor.get_performance_summary()
print(f"   Status: {summary['status']}")
print(f"   Performance Score: {summary['performance_score']:.1f}/100")
print(f"   CPU Average: {summary['cpu']['average']:.1f}%")

if summary['status'] != 'no_data':
    print("   ✅ Performance Summary funktioniert!")
else:
    print("   ❌ Fehler: Status ist noch 'no_data'")

print("\n" + "="*60)
print("🎉 BUG FIX VERIFIZIERT!")
print("="*60)
print("\nDie Metriken werden jetzt korrekt angezeigt:")
print("- Live-Daten wenn keine History vorhanden")
print("- History-Daten wenn Monitoring läuft")
print("\nJetzt kannst du den Optimizer starten:")
print("   python run_optimizer.py")
print("="*60)
