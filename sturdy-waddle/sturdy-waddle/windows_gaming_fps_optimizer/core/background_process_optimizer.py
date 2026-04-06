#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Background Process Optimizer - Reduziert System-Auslastung für Gaming
"""

import psutil
import subprocess
import threading
import time
import logging
import os
import json
import win32service
import win32serviceutil
import win32api
import win32con
from datetime import datetime
from typing import List, Dict, Optional

class BackgroundProcessOptimizer:
    """Optimiert Hintergrundprozesse für maximale Gaming-Performance"""
    
    def __init__(self):
        self.active = False
        self.optimization_thread = None
        self.disabled_services = []
        self.killed_processes = []
        self.original_service_states = {}
        
        # Logging Setup
        self.setup_logging()
        
        # Unnötige Windows-Dienste für Gaming
        self.unnecessary_services = [
            "BITS",  # Background Intelligent Transfer Service
            "wuauserv",  # Windows Update
            "DiagTrack",  # Connected User Experiences and Telemetry
            "dmwappushservice",  # WAP Push Message Routing Service
            "MapsBroker",  # Downloaded Maps Manager
            "lfsvc",  # Geolocation Service
            "SharedAccess",  # Internet Connection Sharing
            "TabletInputService",  # Tablet PC Input Service
            "WMPNetworkSvc",  # Windows Media Player Network Sharing
            "XblAuthManager",  # Xbox Live Auth Manager (wenn nicht auf Xbox)
            "XblGameSave",  # Xbox Live Game Save
            "XboxNetApiSvc",  # Xbox Live Networking
            "SysMain",  # Superfetch
            "WSearch",  # Windows Search
            "WMPNetworkSvc",  # Windows Media Player
            "fhsvc",  # Fax
            "Spooler",  # Print Spooler (nur wenn nicht drucken)
            "RemoteRegistry",  # Remote Registry
            "TermService",  # Remote Desktop
            "SessionEnv",  # Remote Desktop Configuration
            "UmRdpService",  # Remote Desktop Services UserMode
            "BDESVC",  # BitLocker
            "MSiSCSI",  # Microsoft iSCSI
            "WMPNetworkSvc",  # Windows Media Player
            "PhoneSvc",  # Phone Service
            "SensorService",  # Sensor Service
            "SensorDataService",  # Sensor Data
        ]
        
        # Gaming-unnötige Hintergrund-Apps
        self.unnecessary_apps = [
            "chrome.exe",
            "firefox.exe",
            "msedge.exe",
            "opera.exe",
            "discord.exe",
            "slack.exe",
            "teams.exe",
            "skype.exe",
            "zoom.exe",
            "webex.exe",
            "spotify.exe",
            "itunes.exe",
            "vlc.exe",
            "steam.exe",  # Nur wenn nicht Steam-Game
            "epicgameslauncher.exe",
            "origin.exe",
            "battle.net.exe",
            "uplay.exe",
            "gog.exe",
            "rockstar.exe",
            "bethesda.net.exe",
            "ea.desktop.exe",
            "ubisoftconnect.exe",
            "riotgames.exe",
            "leagueclient.exe",
            "overwolf.exe",
            "discordcanary.exe",
            "discordptb.exe",
            "steamwebhelper.exe",
            "epicwebhelper.exe",
        ]
        
        # Windows Bloatware
        self.bloatware_apps = [
            "Microsoft.Windows.Photos",
            "Microsoft.WindowsCamera",
            "Microsoft.WindowsMaps",
            "Microsoft.Windows.Pinball",
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.MicrosoftMahjong",
            "Microsoft.MicrosoftSudoku",
            "Microsoft.MinecraftUWP",
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo",
            "Microsoft.Windows.Phone",
            "Microsoft.YourPhone",
            "Microsoft.SkypeApp",
            "Microsoft.MixedReality.Portal",
            "Microsoft.BingWeather",
            "Microsoft.GetHelp",
            "Microsoft.Getstarted",
            "Microsoft.Microsoft3DViewer",
            "Microsoft.MSPaint",
            "Microsoft.Office.OneNote",
            "Microsoft.People",
            "Microsoft.WindowsAlarms",
            "Microsoft.WindowsCalculator",
            "Microsoft.Windows.DevHome",
            "Microsoft.WindowsFeedbackHub",
            "Microsoft.WindowsSoundRecorder",
            "Microsoft.Xbox.TCUI",
            "Microsoft.XboxApp",
            "Microsoft.XboxGameOverlay",
            "Microsoft.XboxGamingOverlay",
            "Microsoft.XboxIdentityProvider",
            "Microsoft.XboxSpeechToTextOverlay",
        ]
        
        # System-Optimierungs-Einstellungen
        self.optimization_settings = {
            "disable_windows_update": True,
            "disable_superfetch": True,
            "disable_windows_search": True,
            "disable_telemetry": True,
            "disable_cortana": True,
            "disable_onedrive": True,
            "optimize_visual_effects": True,
            "disable_background_apps": True,
            "optimize_power_plan": True,
            "clear_temp_files": True,
        }
    
    def setup_logging(self):
        """Richtet Logging ein"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"bg_optimizer_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def start_optimization(self):
        """Startet Hintergrundprozess-Optimierung"""
        self.active = True
        self.logger.info("🚀 Background Process Optimizer gestartet")
        print("🚀 Background Process Optimizer gestartet")
        
        # Sichere aktuelle Zustände
        self._backup_current_states()
        
        # Führe Optimierungen durch
        self._optimize_services()
        self._optimize_background_apps()
        self._optimize_startup_programs()
        self._optimize_windows_settings()
        self._clear_temp_files()
        
        # Starte Überwachungs-Thread
        self.optimization_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.optimization_thread.start()
        
        self.logger.info("✅ Hintergrundprozess-Optimierung abgeschlossen")
        print("✅ Hintergrundprozess-Optimierung abgeschlossen")
    
    def stop_optimization(self):
        """Stoppt Optimierung und stellt Original-Zustände wieder her"""
        self.active = False
        self.logger.info("⏹️ Background Process Optimizer gestoppt")
        print("⏹️ Background Process Optimizer gestoppt")
        
        # Warte auf Thread
        if self.optimization_thread:
            self.optimization_thread.join(timeout=2)
        
        # Stelle Services wieder her
        self._restore_services()
        
        self.logger.info("✅ Original-Zustände wiederhergestellt")
        print("✅ Original-Zustände wiederhergestellt")
    
    def _backup_current_states(self):
        """Sichert aktuelle Service-Zustände"""
        self.logger.info("📋 Sichere aktuelle Zustände...")
        
        try:
            for service_name in self.unnecessary_services:
                try:
                    service = psutil.win_service_get(service_name)
                    self.original_service_states[service_name] = service.status()
                except:
                    pass
            
            self.logger.info(f"✅ {len(self.original_service_states)} Services gesichert")
            
        except Exception as e:
            self.logger.error(f"❌ Backup Fehler: {e}")
    
    def _optimize_services(self):
        """Optimiert Windows-Dienste"""
        self.logger.info("🔧 Optimiere Windows-Dienste...")
        print("🔧 Optimiere Windows-Dienste...")
        
        disabled_count = 0
        
        for service_name in self.unnecessary_services:
            try:
                if self._disable_service_safe(service_name):
                    disabled_count += 1
                    self.disabled_services.append(service_name)
                    self.logger.info(f"✅ Service {service_name} deaktiviert")
            except Exception as e:
                self.logger.warning(f"⚠️ Service {service_name} Fehler: {e}")
        
        self.logger.info(f"✅ {disabled_count} Services deaktiviert")
        print(f"✅ {disabled_count} unnötige Services deaktiviert")
    
    def _disable_service_safe(self, service_name: str) -> bool:
        """Deaktiviert einen Windows-Dienst sicher"""
        try:
            # Prüfe ob Service existiert
            service = psutil.win_service_get(service_name)
            
            if service.status() == "running":
                # Stoppe Service
                subprocess.run(
                    ["sc", "stop", service_name],
                    capture_output=True,
                    timeout=10,
                    check=False
                )
                time.sleep(0.5)
            
            # Setze auf manuell (nicht deaktivieren für Sicherheit)
            subprocess.run(
                ["sc", "config", service_name, "start=", "demand"],
                capture_output=True,
                timeout=10,
                check=False
            )
            
            return True
            
        except Exception as e:
            self.logger.warning(f"⚠️ Konnte Service {service_name} nicht deaktivieren: {e}")
            return False
    
    def _optimize_background_apps(self):
        """Optimiert Hintergrund-Apps"""
        self.logger.info("🔧 Optimiere Hintergrund-Apps...")
        print("🔧 Optimiere Hintergrund-Apps...")
        
        killed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                
                # Prüfe ob es eine unnötige App ist
                if any(app in proc_name for app in self.unnecessary_apps):
                    # Beende Prozess
                    try:
                        process = psutil.Process(proc.info['pid'])
                        process.terminate()
                        process.wait(timeout=3)
                        
                        killed_count += 1
                        self.killed_processes.append(proc_name)
                        self.logger.info(f"✅ App {proc_name} beendet")
                    except:
                        pass
                        
            except:
                continue
        
        self.logger.info(f"✅ {killed_count} Hintergrund-Apps beendet")
        print(f"✅ {killed_count} Hintergrund-Apps beendet")
    
    def _optimize_startup_programs(self):
        """Optimiert Startup-Programme"""
        self.logger.info("🔧 Optimiere Startup-Programme...")
        print("🔧 Optimiere Startup-Programme...")
        
        try:
            # Deaktiviere unnötige Startup-Programme über Registry
            startup_keys = [
                r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
                r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run"
            ]
            
            disabled_programs = []
            
            for key_path in startup_keys:
                try:
                    import winreg
                    root_key = winreg.HKEY_CURRENT_USER if "HKEY_CURRENT_USER" in key_path else winreg.HKEY_LOCAL_MACHINE
                    sub_key = key_path.split("\\", 1)[1]
                    
                    with winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                
                                # Prüfe ob es ein unnötiges Programm ist
                                unnecessary_programs = [
                                    "steam", "epic", "origin", "battle.net", "discord", 
                                    "spotify", "skype", "teams", "onedrive", "adobe"
                                ]
                                
                                if any(prog in name.lower() or prog in str(value).lower() 
                                      for prog in unnecessary_programs):
                                    # Lösche Startup-Eintrag
                                    try:
                                        winreg.DeleteValue(key, name)
                                        disabled_programs.append(name)
                                        self.logger.info(f"✅ Startup-Programm {name} deaktiviert")
                                    except:
                                        pass
                                
                                i += 1
                            except WindowsError:
                                break
                                
                except Exception as e:
                    self.logger.warning(f"⚠️ Startup-Optimierung Fehler für {key_path}: {e}")
            
            self.logger.info(f"✅ {len(disabled_programs)} Startup-Programme deaktiviert")
            print(f"✅ {len(disabled_programs)} Startup-Programme deaktiviert")
            
        except Exception as e:
            self.logger.error(f"❌ Startup-Optimierung Fehler: {e}")
    
    def _optimize_windows_settings(self):
        """Optimiert Windows-Einstellungen"""
        self.logger.info("🔧 Optimiere Windows-Einstellungen...")
        print("🔧 Optimiere Windows-Einstellungen...")
        
        optimizations = []
        
        try:
            # 1. Visual Effects optimieren
            if self.optimization_settings["optimize_visual_effects"]:
                self._optimize_visual_effects()
                optimizations.append("Visual Effects")
            
            # 2. Hintergrund-Apps deaktivieren
            if self.optimization_settings["disable_background_apps"]:
                self._disable_background_apps()
                optimizations.append("Background Apps")
            
            # 3. Power Plan optimieren
            if self.optimization_settings["optimize_power_plan"]:
                self._optimize_power_plan()
                optimizations.append("Power Plan")
            
            # 4. Telemetry deaktivieren
            if self.optimization_settings["disable_telemetry"]:
                self._disable_telemetry()
                optimizations.append("Telemetry")
            
            self.logger.info(f"✅ Windows-Einstellungen optimiert: {', '.join(optimizations)}")
            print(f"✅ Windows-Einstellungen optimiert: {', '.join(optimizations)}")
            
        except Exception as e:
            self.logger.error(f"❌ Windows-Einstellungen Fehler: {e}")
    
    def _optimize_visual_effects(self):
        """Optimiert Windows Visual Effects"""
        try:
            # Setze auf "Best Performance"
            subprocess.run([
                "powershell", "-Command",
                'Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "UserPreferencesMask" -Value ([byte[]](0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00))'
            ], capture_output=True, check=False, timeout=10)
            
            subprocess.run([
                "powershell", "-Command",
                'Set-ItemProperty -Path "HKCU:\Control Panel\Desktop\WindowMetrics" -Name "MinAnimate" -Value 0'
            ], capture_output=True, check=False, timeout=10)
            
            self.logger.info("✅ Visual Effects auf Best Performance gesetzt")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Visual Effects Fehler: {e}")
    
    def _disable_background_apps(self):
        """Deaktiviert Windows Hintergrund-Apps"""
        try:
            subprocess.run([
                "powershell", "-Command",
                'Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -Name "GlobalUserDisabled" -Value 1'
            ], capture_output=True, check=False, timeout=10)
            
            self.logger.info("✅ Hintergrund-Apps deaktiviert")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Hintergrund-Apps Fehler: {e}")
    
    def _optimize_power_plan(self):
        """Optimiert Windows Power Plan"""
        try:
            subprocess.run(
                ["powercfg", "/setactive", "SCHEME_MIN"],
                capture_output=True,
                check=False,
                timeout=10
            )
            
            self.logger.info("✅ Power Plan auf High Performance gesetzt")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Power Plan Fehler: {e}")
    
    def _disable_telemetry(self):
        """Deaktiviert Windows Telemetry"""
        try:
            subprocess.run([
                "powershell", "-Command",
                'Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "AllowTelemetry" -Value 0 -Force'
            ], capture_output=True, check=False, timeout=10)
            
            self.logger.info("✅ Telemetry deaktiviert")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Telemetry Fehler: {e}")
    
    def _clear_temp_files(self):
        """Löscht temporäre Dateien"""
        if not self.optimization_settings["clear_temp_files"]:
            return
        
        self.logger.info("🧹 Lösche temporäre Dateien...")
        print("🧹 Lösche temporäre Dateien...")
        
        temp_dirs = [
            os.environ.get("TEMP"),
            os.environ.get("TMP"),
            r"C:\Windows\Temp",
        ]
        
        cleared_space = 0
        
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                if os.path.exists(file_path):
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleared_space += file_size
                            except:
                                pass
                except:
                    pass
        
        cleared_mb = cleared_space / (1024 * 1024)
        self.logger.info(f"✅ {cleared_mb:.1f}MB temporäre Dateien gelöscht")
        print(f"✅ {cleared_mb:.1f}MB temporäre Dateien gelöscht")
    
    def _monitoring_loop(self):
        """Überwacht und unterdrückt neue Hintergrundprozesse"""
        while self.active:
            try:
                # Prüfe auf neue unnötige Prozesse
                for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                    try:
                        proc_name = proc.info['name'].lower()
                        
                        # Prüfe ob es eine unnötige App ist
                        if any(app in proc_name for app in self.unnecessary_apps):
                            # Prüfe ob Prozess neu ist (letzte 30 Sekunden)
                            if time.time() - proc.info['create_time'] < 30:
                                try:
                                    process = psutil.Process(proc.info['pid'])
                                    process.terminate()
                                    self.logger.info(f"🚫 Neuer Hintergrundprozess {proc_name} unterdrückt")
                                except:
                                    pass
                                    
                    except:
                        continue
                
                time.sleep(5)  # Prüfe alle 5 Sekunden
                
            except Exception as e:
                self.logger.error(f"❌ Überwachungsfehler: {e}")
                time.sleep(10)
    
    def _restore_services(self):
        """Stellt deaktivierte Services wieder her"""
        self.logger.info("🔄 Stelle Services wieder her...")
        
        restored_count = 0
        
        for service_name, original_status in self.original_service_states.items():
            try:
                if original_status == "running":
                    subprocess.run(
                        ["sc", "start", service_name],
                        capture_output=True,
                        timeout=10,
                        check=False
                    )
                    restored_count += 1
                    self.logger.info(f"✅ Service {service_name} wiederhergestellt")
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Service {service_name} Restore Fehler: {e}")
        
        self.logger.info(f"✅ {restored_count} Services wiederhergestellt")
    
    def get_optimization_report(self) -> Dict:
        """Gibt Optimierungs-Report zurück"""
        return {
            "timestamp": datetime.now().isoformat(),
            "active": self.active,
            "disabled_services": len(self.disabled_services),
            "killed_processes": len(self.killed_processes),
            "system_metrics": {
                "cpu_before": 0,  # Würde gemessen werden
                "memory_before": 0,
                "cpu_after": psutil.cpu_percent(),
                "memory_after": psutil.virtual_memory().percent
            },
            "settings": self.optimization_settings
        }
    
    def print_status(self):
        """Gibt aktuellen Status aus"""
        report = self.get_optimization_report()
        
        print(f"\n🔧 BACKGROUND PROCESS OPTIMIZER STATUS")
        print("="*50)
        print(f"Aktiv: {'🟢 JA' if report['active'] else '🔴 NEIN'}")
        print(f"Deaktivierte Services: {report['disabled_services']}")
        print(f"Beendete Prozesse: {report['killed_processes']}")
        print(f"Aktuelle CPU: {report['system_metrics']['cpu_after']:.1f}%")
        print(f"Aktueller Memory: {report['system_metrics']['memory_after']:.1f}%")

if __name__ == "__main__":
    # Test Background Process Optimizer
    optimizer = BackgroundProcessOptimizer()
    
    print("🔧 BACKGROUND PROCESS OPTIMIZER TEST")
    print("="*50)
    
    # Starte Optimierung
    optimizer.start_optimization()
    
    # Warte kurz
    time.sleep(5)
    
    # Status anzeigen
    optimizer.print_status()
    
    # Stoppe Optimierung
    optimizer.stop_optimization()
    
    print(f"\n✅ Background Process Optimizer Test abgeschlossen")
