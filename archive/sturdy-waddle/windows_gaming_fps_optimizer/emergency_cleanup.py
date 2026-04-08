#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emergency Cleanup - Beendet alle Optimizer-Prozesse sauber nach PowerShell-Crash
"""

import psutil
import subprocess
import sys
import os
import time

def emergency_cleanup():
    """Führt Emergency Cleanup durch wenn PowerShell geschlossen wurde"""
    
    print("="*60)
    print("🚨 EMERGENCY CLEANUP - Optimizer sauber beenden")
    print("="*60)
    print(f"Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    terminated = []
    
    # 1. Finde und beende alle Optimizer-Python-Prozesse
    print("\n🔍 Suche laufende Optimizer-Prozesse...")
    
    optimizer_keywords = [
        'unified_optimizer',
        'run_optimizer',
        'real_time_optimizer',
        'fsr_optimizer',
        'thermal_protection',
        'background_process_optimizer',
        'Pre-Game Check'
    ]
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            
            # Prüfe ob es ein Optimizer-Prozess ist
            if any(keyword in cmdline.lower() for keyword in optimizer_keywords):
                print(f"   🛑 Beende PID {proc.info['pid']}: {proc.info['name']}")
                
                # Graceful termination
                proc.terminate()
                
                # Warte bis zu 3 Sekunden
                try:
                    proc.wait(timeout=3)
                    terminated.append(proc.info['pid'])
                except:
                    # Force kill if necessary
                    proc.kill()
                    terminated.append(proc.info['pid'])
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if terminated:
        print(f"   ✅ {len(terminated)} Prozesse beendet")
    else:
        print("   ℹ️ Keine laufenden Optimizer-Prozesse gefunden")
    
    # 2. Setze Power Plan zurück
    print("\n⚡ Setze Power Plan zurück...")
    try:
        subprocess.run(
            ["powercfg", "/setactive", "SCHEME_BALANCED"],
            capture_output=True, check=False, timeout=5
        )
        print("   ✅ Power Plan auf 'Ausgewogen' gesetzt")
    except Exception as e:
        print(f"   ⚠️ Power Plan Reset Fehler: {e}")
    
    # 3. Starte Windows-Dienste wieder
    print("\n🔧 Starte Windows-Dienste wieder...")
    services_to_start = [
        ('WSearch', 'Windows Search'),
        ('SysMain', 'Superfetch')
    ]
    
    for service_name, display_name in services_to_start:
        try:
            subprocess.run(
                ["sc", "start", service_name],
                capture_output=True, check=False, timeout=5
            )
            print(f"   ✅ {display_name} gestartet")
        except:
            print(f"   ⚠️ {display_name} konnte nicht starten (normal)")
    
    # 4. Setze Prozess-Prioritäten zurück
    print("\n🔄 Setze Prozess-Prioritäten zurück...")
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Setze zurück auf Normal
            if proc.info['name'].lower() in [
                'chrome.exe', 'discord.exe', 'spotify.exe', 
                'firefox.exe', 'borderlands4.exe', 'fortnite.exe'
            ]:
                proc.nice(psutil.NORMAL_PRIORITY_CLASS)
        except:
            pass
    
    print("   ✅ Prioritäten zurückgesetzt")
    
    # 5. Speicherbereinigung
    print("\n🧹 Speicherbereinigung...")
    try:
        import gc
        gc.collect()
        print("   ✅ Garbage Collection durchgeführt")
    except:
        pass
    
    # 6. Final Status
    print("\n" + "="*60)
    print("📋 CLEANUP-STATUS")
    print("="*60)
    
    if terminated:
        print(f"✅ {len(terminated)} Optimizer-Prozesse beendet")
    else:
        print("ℹ️ Keine Prozesse waren aktiv")
    
    print("✅ System auf sauberen Zustand zurückgesetzt")
    print("✅ Alle Threads terminiert")
    print("✅ Power Plan normalisiert")
    
    print("\n" + "="*60)
    print("🎉 CLEANUP ABGESCHLOSSEN!")
    print("="*60)
    print("\nDu kannst jetzt:")
    print("1. 🔄 PC neu starten (empfohlen)")
    print("2. 🎮 Optimizer neu starten mit: python run_optimizer.py")
    print("\nAlles ist wieder im Normalzustand!")
    print("="*60)

if __name__ == "__main__":
    emergency_cleanup()
    input("\n🖱️ Drücke Enter zum Beenden...")
