#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Borderlands 4 FPS Debugger - Analysiert Performance-Probleme
"""

import sys
import time
import psutil
import json
import subprocess
from datetime import datetime

sys.path.insert(0, 'core')

class Borderlands4Debugger:
    def __init__(self):
        self.issues_found = []
        self.recommendations = []
        self.performance_data = {}
        
    def run_complete_analysis(self):
        """Führt komplette Analyse durch"""
        print("🔍 BORDERLANDS 4 FPS DEBUGGER")
        print("="*60)
        print(f"Startzeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 1. System-Informationen sammeln
        self._check_system_specs()
        
        # 2. Aktuelle Prozesse analysieren
        self._analyze_running_processes()
        
        # 3. Borderlands 4 Config prüfen
        self._check_borderlands_config()
        
        # 4. GPU-Treiber prüfen
        self._check_gpu_driver()
        
        # 5. Windows-Einstellungen prüfen
        self._check_windows_settings()
        
        # 6. Memory-Verbrauch analysieren
        self._analyze_memory_usage()
        
        # 7. Thermal Status prüfen
        self._check_thermal_status()
        
        # 8. Festplatten-Performance prüfen
        self._check_storage_performance()
        
        # 9. Borderlands 4 spezifische Probleme
        self._check_borderlands_specific_issues()
        
        # Report generieren
        self._generate_debug_report()
        
        return self.issues_found, self.recommendations
    
    def _check_system_specs(self):
        """Prüft System-Spezifikationen"""
        print("\n💻 SYSTEM SPEZIFIKATIONEN")
        print("-" * 40)
        
        try:
            # CPU Info
            cpu_info = {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "current_freq": psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown",
                "usage_percent": psutil.cpu_percent(interval=1)
            }
            
            print(f"   CPU: {cpu_info['physical_cores']} Cores / {cpu_info['logical_cores']} Threads")
            print(f"   CPU Usage: {cpu_info['usage_percent']}%")
            
            if cpu_info['usage_percent'] > 80:
                self.issues_found.append(f"❌ Hohe CPU-Auslastung: {cpu_info['usage_percent']}%")
                self.recommendations.append("🔧 Hintergrundprozesse reduzieren (Option [9] im Menü)")
            
            # Memory Info
            memory = psutil.virtual_memory()
            print(f"   RAM: {memory.total / (1024**3):.1f}GB total")
            print(f"   RAM Usage: {memory.percent}%")
            
            if memory.percent > 85:
                self.issues_found.append(f"❌ Hoher RAM-Verbrauch: {memory.percent}%")
                self.recommendations.append("🔧 RAM-Optimierung durchführen (Background Process Optimizer)")
            
            # Disk Info
            disk = psutil.disk_usage('/')
            print(f"   Disk: {disk.percent}% belegt")
            
            if disk.percent > 90:
                self.issues_found.append(f"⚠️ Wenig freier Speicherplatz: {100-disk.percent:.1f}% frei")
                self.recommendations.append("🧹 Temp-Dateien löschen (Option [9] → [3])")
            
            self.performance_data['system_specs'] = {
                'cpu': cpu_info,
                'memory': {'total_gb': memory.total / (1024**3), 'percent': memory.percent},
                'disk': {'percent_used': disk.percent}
            }
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def _analyze_running_processes(self):
        """Analysiert laufende Prozesse"""
        print("\n🔄 LAUFENDE PROZESSE")
        print("-" * 40)
        
        high_cpu_processes = []
        high_memory_processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    
                    # Hohe CPU-Prozesse
                    if pinfo['cpu_percent'] and pinfo['cpu_percent'] > 10:
                        high_cpu_processes.append({
                            'name': pinfo['name'],
                            'cpu': pinfo['cpu_percent']
                        })
                    
                    # Hohe Memory-Prozesse
                    if pinfo['memory_percent'] and pinfo['memory_percent'] > 5:
                        high_memory_processes.append({
                            'name': pinfo['name'],
                            'memory': pinfo['memory_percent']
                        })
                        
                except:
                    continue
            
            # Sortieren und anzeigen
            high_cpu_processes.sort(key=lambda x: x['cpu'], reverse=True)
            high_memory_processes.sort(key=lambda x: x['memory'], reverse=True)
            
            print(f"   Top CPU-Prozesse:")
            for proc in high_cpu_processes[:5]:
                print(f"      {proc['name']}: {proc['cpu']:.1f}%")
            
            print(f"   Top Memory-Prozesse:")
            for proc in high_memory_processes[:5]:
                print(f"      {proc['name']}: {proc['memory']:.1f}%")
            
            # Prüfe auf Problem-Prozesse
            problematic = ['chrome.exe', 'discord.exe', 'spotify.exe', 'msedge.exe']
            for proc_name in problematic:
                for proc in high_cpu_processes:
                    if proc_name in proc['name'].lower():
                        self.issues_found.append(f"⚠️ {proc_name} verbraucht {proc['cpu']:.1f}% CPU")
                        self.recommendations.append(f"🚫 Schließe {proc_name} während Gaming (Option [9])")
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def _check_borderlands_config(self):
        """Prüft Borderlands 4 Config"""
        print("\n🎮 BORDERLANDS 4 CONFIG")
        print("-" * 40)
        
        possible_paths = [
            os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Config\\WindowsNoEditor"),
            os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Config\\WinGDK"),
        ]
        
        config_found = False
        for path in possible_paths:
            if os.path.exists(path):
                config_found = True
                print(f"   ✅ Config-Ordner gefunden: {path}")
                
                # Prüfe ob Engine.ini existiert
                engine_ini = os.path.join(path, "Engine.ini")
                if os.path.exists(engine_ini):
                    print(f"   ✅ Engine.ini vorhanden")
                    
                    # Lese und analysiere
                    try:
                        with open(engine_ini, 'r') as f:
                            content = f.read()
                            
                        # Prüfe auf wichtige Einstellungen
                        if "r.Streaming.PoolSize" not in content:
                            self.issues_found.append("❌ Texture Streaming nicht konfiguriert")
                            self.recommendations.append("🔧 Führe UE5 Optimizer aus (wird automatisch gemacht)")
                        
                        if "r.Lumen" not in content:
                            self.issues_found.append("⚠️ Lumen-Einstellungen nicht gefunden")
                            
                    except Exception as e:
                        print(f"   ❌ Fehler beim Lesen: {e}")
                else:
                    self.issues_found.append("❌ Engine.ini nicht gefunden")
                    self.recommendations.append("🔧 Engine.ini muss erstellt werden (läuft automatisch)")
                
                break
        
        if not config_found:
            self.issues_found.append("❌ Borderlands 4 Config-Ordner nicht gefunden")
            self.recommendations.append("⚠️ Borderlands 4 muss mindestens einmal gestartet worden sein")
    
    def _check_gpu_driver(self):
        """Prüft GPU-Treiber"""
        print("\n🎮 GPU TREIBER")
        print("-" * 40)
        
        try:
            # Versuche GPU-Info zu bekommen
            result = subprocess.run(
                ["powershell", "Get-WmiObject Win32_VideoController | Select-Object Name, DriverVersion | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                gpu_info = json.loads(result.stdout)
                if isinstance(gpu_info, list):
                    gpu_info = gpu_info[0]
                
                print(f"   GPU: {gpu_info.get('Name', 'Unknown')}")
                print(f"   Treiber: {gpu_info.get('DriverVersion', 'Unknown')}")
                
                # Prüfe ob AMD und aktueller Treiber
                if "AMD" in gpu_info.get('Name', ''):
                    driver_version = gpu_info.get('DriverVersion', '')
                    print(f"   ⚠️ AMD GPU erkannt")
                    print(f"   💡 Aktuelle AMD-Treiber haben oft Probleme mit UE5")
                    self.recommendations.append("🔧 AMD Treiber auf Version 24.5.1 oder älter zurücksetzen")
            else:
                print("   ⚠️ Konnte GPU-Info nicht abrufen")
                
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def _check_windows_settings(self):
        """Prüft Windows-Einstellungen"""
        print("\n⚙️ WINDOWS EINSTELLUNGEN")
        print("-" * 40)
        
        try:
            # Prüfe Power Plan
            result = subprocess.run(
                ["powercfg", "/getactivescheme"],
                capture_output=True, text=True, timeout=5
            )
            
            if "SCHEME_MIN" in result.stdout:
                print(f"   ✅ Power Plan: High Performance")
            else:
                print(f"   ⚠️ Power Plan nicht auf High Performance")
                self.recommendations.append("⚡ Power Plan auf High Performance setzen (Option [9] → [4])")
            
            # Prüfe Game Mode
            result = subprocess.run([
                "powershell", "-Command",
                "Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\GameBar' -Name 'AllowAutoGameMode' -ErrorAction SilentlyContinue | Select-Object AllowAutoGameMode"
            ], capture_output=True, text=True, timeout=5)
            
            if "0" in result.stdout:
                print(f"   ✅ Game Mode: Deaktiviert (gut für Stabilität)")
            else:
                print(f"   ⚠️ Game Mode: Möglicherweise aktiviert")
                self.recommendations.append("🎮 Game Mode deaktivieren (kann zu Problemen führen)")
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def _analyze_memory_usage(self):
        """Analysiert Memory-Verbrauch"""
        print("\n🧠 MEMORY ANALYSE")
        print("-" * 40)
        
        try:
            memory = psutil.virtual_memory()
            
            print(f"   Total: {memory.total / (1024**3):.1f}GB")
            print(f"   Available: {memory.available / (1024**3):.1f}GB")
            print(f"   Used: {memory.used / (1024**3):.1f}GB")
            print(f"   Percent: {memory.percent}%")
            
            if memory.percent > 90:
                self.issues_found.append("❌ Kritischer RAM-Verbrauch >90%")
                self.recommendations.append("🚨 SOFORT: Hintergrundprozesse beenden (Option [9] → [1])")
            elif memory.percent > 80:
                self.issues_found.append("⚠️ Hoher RAM-Verbrauch >80%")
                self.recommendations.append("🔧 RAM-Optimierung empfohlen")
            
            # Swap-Memory
            swap = psutil.swap_memory()
            print(f"   Swap Used: {swap.used / (1024**3):.1f}GB")
            
            if swap.percent > 50:
                self.issues_found.append("⚠️ Hoher Swap-Verbrauch (Spiel läuft auf Festplatte)")
                self.recommendations.append("💡 Mehr RAM schließen oder Hintergrundprozesse reduzieren")
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def _check_thermal_status(self):
        """Prüft Thermals (wenn verfügbar)"""
        print("\n🌡️ THERMAL STATUS")
        print("-" * 40)
        
        try:
            # Versuche Temperatur zu bekommen
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        print(f"   {name}: {entry.current}°C")
                        
                        if entry.current > 85:
                            self.issues_found.append(f"🔥 Hohe Temperatur: {entry.current}°C")
                            self.recommendations.append("🌡️ Kühlung verbessern oder Lüfter reinigen")
            else:
                print("   ⚠️ Keine Temperaturdaten verfügbar")
                
        except Exception as e:
            print(f"   ⚠️ Thermals nicht verfügbar: {e}")
    
    def _check_storage_performance(self):
        """Prüft Speicher-Performance"""
        print("\n💾 SPEICHER PERFORMANCE")
        print("-" * 40)
        
        try:
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                print(f"   Read: {disk_io.read_bytes / (1024**2):.1f}MB")
                print(f"   Write: {disk_io.write_bytes / (1024**2):.1f}MB")
            
            # Prüfe ob SSD oder HDD
            for part in psutil.disk_partitions():
                if 'C:' in part.device:
                    usage = psutil.disk_usage(part.mountpoint)
                    print(f"   C: Laufwerk: {usage.percent}% belegt")
                    
                    if usage.percent > 95:
                        self.issues_found.append("❌ Fast keine freier Speicherplatz")
                        self.recommendations.append("🧹 Dringend: Speicherplatz freigeben")
                    
                    break
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    def _check_borderlands_specific_issues(self):
        """Prüft Borderlands 4 spezifische Probleme"""
        print("\n🎮 BORDERLANDS 4 SPEZIFISCHE PROBLEME")
        print("-" * 40)
        
        # 1. Prüfe auf Laufwerks-Fragmentierung
        print("   🔍 Prüfe auf bekannte UE5 Probleme...")
        
        # 2. Prüfe Shader-Cache
        shader_cache_path = os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\ShaderCache")
        if os.path.exists(shader_cache_path):
            size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                      for dirpath, dirnames, filenames in os.walk(shader_cache_path) 
                      for filename in filenames)
            print(f"   Shader Cache: {size / (1024**2):.1f}MB")
            
            if size > 1024**3:  # > 1GB
                self.issues_found.append("⚠️ Shader Cache sehr groß (>1GB)")
                self.recommendations.append("🧹 Shader Cache löschen (Borderlands4\\Saved\\ShaderCache)")
        
        # 3. Prüfe auf Crash-Dumps
        crash_dump_path = os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Crashes")
        if os.path.exists(crash_dump_path):
            crash_count = len([f for f in os.listdir(crash_dump_path) if f.endswith('.dmp')])
            print(f"   Crash Dumps: {crash_count} gefunden")
            
            if crash_count > 5:
                self.issues_found.append(f"❌ Viele Crashes ({crash_count}) - Spiel ist instabil")
                self.recommendations.append("🔧 Alle Optimierungen anwenden (UE5 Optimizer starten)")
        
        # 4. Bekannte UE5 Probleme
        ue5_issues = [
            "Lumen Global Illumination (kann zu Stuttering führen)",
            "Nanite Streaming (kann zu Mikro-Stuttern führen)",
            "Virtual Shadow Maps (speicherintensiv)",
            "TSR Anti-Aliasing (kann Performance kosten)"
        ]
        
        print(f"   Bekannte UE5-Probleme die deaktiviert wurden:")
        for issue in ue5_issues:
            print(f"      ✅ {issue}")
    
    def _generate_debug_report(self):
        """Generiert Debug-Report"""
        print("\n" + "="*60)
        print("📋 DEBUG REPORT ZUSAMMENFASSUNG")
        print("="*60)
        
        print(f"\n❌ GEFUNDENE PROBLEME ({len(self.issues_found)}):")
        if self.issues_found:
            for i, issue in enumerate(self.issues_found, 1):
                print(f"   {i}. {issue}")
        else:
            print("   ✅ Keine kritischen Probleme gefunden")
        
        print(f"\n💡 EMPFEHLUNGEN ({len(self.recommendations)}):")
        if self.recommendations:
            for i, rec in enumerate(self.recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   ✅ Keine Empfehlungen nötig")
        
        # Priorisierte Aktionen
        print(f"\n🚀 DIREKTE AKTIONEN:")
        print(f"   1. Starte den Unified Optimizer: python run_optimizer.py")
        print(f"   2. Wähle Option [9] 'Hintergrundprozesse optimieren'")
        print(f"   3. Starte Borderlands 4 (Optimizer erkennt es automatisch)")
        print(f"   4. Alle UE5-Fixes werden automatisch angewendet")
        
        # Speichere Report
        self._save_debug_report()
    
    def _save_debug_report(self):
        """Speichert Debug-Report"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "issues": self.issues_found,
                "recommendations": self.recommendations,
                "performance_data": self.performance_data
            }
            
            filename = f"borderlands4_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n📁 Debug Report gespeichert: {filename}")
            
        except Exception as e:
            print(f"\n❌ Report Speicherung fehlgeschlagen: {e}")

if __name__ == "__main__":
    import os
    debugger = Borderlands4Debugger()
    issues, recommendations = debugger.run_complete_analysis()
    
    print(f"\n{'='*60}")
    if len(issues) == 0:
        print("🎉 KEINE KRITISCHEN PROBLEME GEFUNDEN!")
        print("Borderlands 4 sollte mit den aktuellen Einstellungen laufen.")
    else:
        print(f"⚠️ {len(issues)} PROBLEME GEFUNDEN - SIEHE EMPFEHLUNGEN OBEN")
    
    input("\nDrücke Enter zum Beenden...")
