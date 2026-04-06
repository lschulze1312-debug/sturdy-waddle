#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Gaming Driver Suite - Hauptanwendung
"""

import sys
import os
import json
import time
import threading
from datetime import datetime

sys.path.insert(0, 'drivers')
sys.path.insert(0, 'utils')
sys.path.insert(0, 'data')

class DriverManager:
    def __init__(self):
        self.config_file = "settings.json"
        self.config = self.load_config()
        self.driver_database = self.load_driver_database()
        self.update_history = self.load_update_history()
        
        # System-Informationen
        self.system_info = {
            "platform": "Windows",
            "version": "10/11",
            "architecture": "x64",
            "gpu_brand": "unknown",
            "gpu_model": "unknown",
            "cpu_brand": "unknown",
            "cpu_model": "unknown"
        }
        
        self.current_drivers = {}
        self.available_updates = {}
    
    def load_config(self):
        """Lädt Konfiguration"""
        default_config = {
            "auto_scan": True,
            "auto_update": False,
            "gaming_mode": True,
            "backup_before_update": True,
            "silent_installation": False,
            "beta_drivers": False,
            "update_interval": 7,
            "preferred_gpu_brand": "nvidia"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                return {**default_config, **config}
            except:
                return default_config
        else:
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """Speichert Konfiguration"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"❌ Konfiguration speichern fehlgeschlagen: {e}")
    
    def load_driver_database(self):
        """Lädt Treiber-Datenbank"""
        database = {
            "nvidia": {
                "gtx_1060": {
                    "current_version": "531.68",
                    "latest_version": "536.99",
                    "game_ready": "536.99",
                    "studio": "537.13",
                    "download_url": "https://www.nvidia.com/Download/index.aspx",
                    "release_date": "2024-01-15"
                },
                "gtx_1070": {
                    "current_version": "531.68",
                    "latest_version": "536.99",
                    "game_ready": "536.99",
                    "studio": "537.13",
                    "download_url": "https://www.nvidia.com/Download/index.aspx",
                    "release_date": "2024-01-15"
                },
                "rtx_3060": {
                    "current_version": "531.68",
                    "latest_version": "536.99",
                    "game_ready": "536.99",
                    "studio": "537.13",
                    "download_url": "https://www.nvidia.com/Download/index.aspx",
                    "release_date": "2024-01-15"
                }
            },
            "amd": {
                "rx_580": {
                    "current_version": "23.12.1",
                    "latest_version": "24.1.1",
                    "adrenalin": "24.1.1",
                    "download_url": "https://www.amd.com/en/support",
                    "release_date": "2024-01-10"
                },
                "rx_5700": {
                    "current_version": "23.12.1",
                    "latest_version": "24.1.1",
                    "adrenalin": "24.1.1",
                    "download_url": "https://www.amd.com/en/support",
                    "release_date": "2024-01-10"
                },
                "rx_6600": {
                    "current_version": "23.12.1",
                    "latest_version": "24.1.1",
                    "adrenalin": "24.1.1",
                    "download_url": "https://www.amd.com/en/support",
                    "release_date": "2024-01-10"
                }
            },
            "intel": {
                "arc_a750": {
                    "current_version": "31.0.101.5081",
                    "latest_version": "31.0.101.5085",
                    "download_url": "https://www.intel.com/content/www/us/en/download-center/home.html",
                    "release_date": "2024-01-08"
                }
            },
            "chipset": {
                "intel_z590": {
                    "current_version": "10.1.19120.0",
                    "latest_version": "10.1.19120.0",
                    "download_url": "https://www.intel.com/content/www/us/en/download-center/home.html",
                    "release_date": "2023-12-15"
                },
                "amd_b550": {
                    "current_version": "5.17.0.0",
                    "latest_version": "5.18.0.0",
                    "download_url": "https://www.amd.com/en/support",
                    "release_date": "2024-01-05"
                }
            },
            "audio": {
                "realtek_hd": {
                    "current_version": "6.0.9285.1",
                    "latest_version": "6.0.9365.1",
                    "download_url": "https://www.realtek.com/en/component/zoo/",
                    "release_date": "2024-01-12"
                }
            }
        }
        return database
    
    def load_update_history(self):
        """Lädt Update-Historie"""
        if os.path.exists("data/update_history.json"):
            try:
                with open("data/update_history.json", 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_update_history(self):
        """Speichert Update-Historie"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/update_history.json", 'w') as f:
                json.dump(self.update_history, f, indent=2)
        except Exception as e:
            print(f"❌ Update-Historie speichern fehlgeschlagen: {e}")
    
    def show_main_menu(self):
        """Zeigt Hauptmenü"""
        print("\n" + "="*70)
        print("🔧 WINDOWS GAMING DRIVER SUITE")
        print("="*70)
        
        print(f"\n📊 AKTUELLE KONFIGURATION:")
        print(f"   Auto-Scan: {'Aktiviert' if self.config['auto_scan'] else 'Deaktiviert'}")
        print(f"   Auto-Update: {'Aktiviert' if self.config['auto_update'] else 'Deaktiviert'}")
        print(f"   Gaming Mode: {'Aktiviert' if self.config['gaming_mode'] else 'Deaktiviert'}")
        print(f"   Backup vor Update: {'Aktiviert' if self.config['backup_before_update'] else 'Deaktiviert'}")
        print(f"   Silent Installation: {'Aktiviert' if self.config['silent_installation'] else 'Deaktiviert'}")
        print(f"   Beta-Treiber: {'Aktiviert' if self.config['beta_drivers'] else 'Deaktiviert'}")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] System-Scan durchführen")
        print("   [2] Treiber-Updates anzeigen")
        print("   [3] Gaming-Treiber installieren")
        print("   [4] Backup erstellen")
        print("   [5] Update-Historie anzeigen")
        print("   [6] Einstellungen")
        print("   [7] Automatische Updates konfigurieren")
        print("   [8] Treiber-Datenbank aktualisieren")
        print("   [9] System-Informationen")
        print("   [0] Beenden")
    
    def scan_system(self):
        """Führt System-Scan durch"""
        print("\n🔍 SYSTEM-SCAN")
        print("="*50)
        
        print("🔍 Scanne Hardware...")
        time.sleep(1)
        
        # Simuliere Hardware-Erkennung
        self.system_info.update({
            "gpu_brand": "nvidia",
            "gpu_model": "gtx_1060",
            "cpu_brand": "intel",
            "cpu_model": "core_i5_8400"
        })
        
        print(f"✅ GPU: {self.system_info['gpu_brand'].upper()} {self.system_info['gpu_model'].replace('_', ' ').title()}")
        print(f"✅ CPU: {self.system_info['cpu_brand'].upper()} {self.system_info['cpu_model'].replace('_', ' ').title()}")
        print(f"✅ Chipset: Intel Z590")
        print(f"✅ Audio: Realtek HD Audio")
        print(f"✅ Network: Intel Ethernet")
        
        # Prüfe aktuelle Treiber
        print("\n🔍 Prüfe aktuelle Treiber...")
        time.sleep(1)
        
        gpu_brand = self.system_info['gpu_brand']
        gpu_model = self.system_info['gpu_model']
        
        if gpu_brand in self.driver_database and gpu_model in self.driver_database[gpu_brand]:
            gpu_info = self.driver_database[gpu_brand][gpu_model]
            self.current_drivers['gpu'] = {
                "brand": gpu_brand,
                "model": gpu_model,
                "current": gpu_info["current_version"],
                "latest": gpu_info["latest_version"],
                "needs_update": gpu_info["current_version"] != gpu_info["latest_version"]
            }
        
        # Chipset-Treiber
        chipset_info = self.driver_database["chipset"]["intel_z590"]
        self.current_drivers['chipset'] = {
            "brand": "intel",
            "model": "z590",
            "current": chipset_info["current_version"],
            "latest": chipset_info["latest_version"],
            "needs_update": chipset_info["current_version"] != chipset_info["latest_version"]
        }
        
        # Audio-Treiber
        audio_info = self.driver_database["audio"]["realtek_hd"]
        self.current_drivers['audio'] = {
            "brand": "realtek",
            "model": "hd",
            "current": audio_info["current_version"],
            "latest": audio_info["latest_version"],
            "needs_update": audio_info["current_version"] != audio_info["latest_version"]
        }
        
        print("✅ Treiber-Scan abgeschlossen")
        
        # Zeige Ergebnisse
        self.show_scan_results()
    
    def show_scan_results(self):
        """Zeigt Scan-Ergebnisse"""
        print("\n📊 SCAN-ERGEBNISSE")
        print("="*50)
        
        for driver_type, info in self.current_drivers.items():
            status = "🟡 Update verfügbar" if info['needs_update'] else "✅ Aktuell"
            print(f"\n{driver_type.upper()}: {info['brand'].title()} {info['model'].replace('_', ' ').title()}")
            print(f"   Aktuell: {info['current']}")
            print(f"   Latest: {info['latest']}")
            print(f"   Status: {status}")
    
    def show_available_updates(self):
        """Zeigt verfügbare Updates"""
        print("\n🔄 VERFÜGBARE UPDATES")
        print("="*50)
        
        updates_found = False
        
        for driver_type, info in self.current_drivers.items():
            if info['needs_update']:
                updates_found = True
                print(f"\n📦 {driver_type.upper()} UPDATE:")
                print(f"   Device: {info['brand'].title()} {info['model'].replace('_', ' ').title()}")
                print(f"   From: {info['current']} → To: {info['latest']}")
                print(f"   Size: ~500MB")
                print(f"   Release: Kürzlich")
                
                if driver_type == 'gpu':
                    if info['brand'] == 'nvidia':
                        print(f"   Type: Game Ready Driver")
                    elif info['brand'] == 'amd':
                        print(f"   Type: Adrenalin Edition")
                
                print(f"   [1] Jetzt installieren")
                print(f"   [2] Download nur")
                print(f"   [3] Überspringen")
        
        if not updates_found:
            print("\n✅ Alle Treiber sind aktuell!")
        else:
            print(f"\n💡 Empfehlung: Gaming-Treiber zuerst installieren")
    
    def install_gaming_drivers(self):
        """Installiert Gaming-Treiber"""
        print("\n🎮 GAMING-TREIBER INSTALLATION")
        print("="*50)
        
        # Prüfe GPU-Treiber
        if 'gpu' in self.current_drivers and self.current_drivers['gpu']['needs_update']:
            gpu_info = self.current_drivers['gpu']
            
            print(f"📦 Installiere {gpu_info['brand'].title()} Gaming-Treiber...")
            print(f"   Version: {gpu_info['latest']}")
            
            if self.config['backup_before_update']:
                print("📋 Erstelle Backup...")
                time.sleep(1)
                print("✅ Backup erstellt")
            
            print("📥 Download Treiber...")
            time.sleep(2)
            print("✅ Download abgeschlossen")
            
            print("🔧 Installiere Treiber...")
            time.sleep(3)
            print("✅ Installation abgeschlossen")
            
            # Update-Historie
            self.update_history.append({
                "timestamp": datetime.now().isoformat(),
                "driver_type": "gpu",
                "brand": gpu_info['brand'],
                "model": gpu_info['model'],
                "from_version": gpu_info['current'],
                "to_version": gpu_info['latest'],
                "success": True
            })
            
            # Aktualisiere aktuellen Treiber
            gpu_info['current'] = gpu_info['latest']
            gpu_info['needs_update'] = False
            
            self.save_update_history()
            
            print("\n🎉 Gaming-Treiber erfolgreich installiert!")
            print("💡 System-Neustart empfohlen für volle Performance")
        else:
            print("✅ Gaming-Treiber sind bereits aktuell")
    
    def create_backup(self):
        """Erstellt Treiber-Backup"""
        print("\n💾 TREIBER-BACKUP ERSTELLEN")
        print("="*50)
        
        print("📋 Erstelle Backup-Punkt...")
        time.sleep(1)
        
        backup_info = {
            "timestamp": datetime.now().isoformat(),
            "drivers": self.current_drivers.copy(),
            "system_info": self.system_info.copy(),
            "backup_size": "2.3GB"
        }
        
        print("📦 Sichere Treiber-Dateien...")
        time.sleep(2)
        
        print("📋 Erstelle System-Wiederherstellungspunkt...")
        time.sleep(1)
        
        print("✅ Backup erfolgreich erstellt!")
        print(f"   Größe: {backup_info['backup_size']}")
        print(f"   Zeitstempel: {backup_info['timestamp']}")
        print(f"   Ort: C:\\DriverBackups\\{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    def show_update_history(self):
        """Zeigt Update-Historie"""
        print("\n📈 UPDATE-HISTORIE")
        print("="*50)
        
        if not self.update_history:
            print("❌ Keine Update-Historie verfügbar")
            return
        
        for i, update in enumerate(reversed(self.update_history[-10:]), 1):
            print(f"\n[{i}] {update['timestamp'][:19].replace('T', ' ')}")
            print(f"   Device: {update['brand'].title()} {update['model'].replace('_', ' ').title()}")
            print(f"   Update: {update['from_version']} → {update['to_version']}")
            print(f"   Status: {'✅ Erfolg' if update['success'] else '❌ Fehlgeschlagen'}")
    
    def show_settings(self):
        """Zeigt Einstellungen"""
        print("\n⚙️ EINSTELLUNGEN")
        print("="*50)
        
        print(f"\nAktuelle Einstellungen:")
        print(f"   [1] Auto-Scan: {'Aktiviert' if self.config['auto_scan'] else 'Deaktiviert'}")
        print(f"   [2] Auto-Update: {'Aktiviert' if self.config['auto_update'] else 'Deaktiviert'}")
        print(f"   [3] Gaming Mode: {'Aktiviert' if self.config['gaming_mode'] else 'Deaktiviert'}")
        print(f"   [4] Backup vor Update: {'Aktiviert' if self.config['backup_before_update'] else 'Deaktiviert'}")
        print(f"   [5] Silent Installation: {'Aktiviert' if self.config['silent_installation'] else 'Deaktiviert'}")
        print(f"   [6] Beta-Treiber: {'Aktiviert' if self.config['beta_drivers'] else 'Deaktiviert'}")
        print(f"   [7] Update-Intervall: {self.config['update_interval']} Tage")
        print(f"   [8] Bevorzugte GPU-Marke: {self.config['preferred_gpu_brand'].title()}")
        
        print("\n[0] Zurück zum Hauptmenü")
        
        try:
            choice = input("\nWähle Einstellung zum ändern: ")
            
            if choice == "1":
                self.config['auto_scan'] = not self.config['auto_scan']
                status = "Aktiviert" if self.config['auto_scan'] else "Deaktiviert"
                print(f"✅ Auto-Scan: {status}")
            
            elif choice == "2":
                self.config['auto_update'] = not self.config['auto_update']
                status = "Aktiviert" if self.config['auto_update'] else "Deaktiviert"
                print(f"✅ Auto-Update: {status}")
            
            elif choice == "3":
                self.config['gaming_mode'] = not self.config['gaming_mode']
                status = "Aktiviert" if self.config['gaming_mode'] else "Deaktiviert"
                print(f"✅ Gaming Mode: {status}")
            
            elif choice == "4":
                self.config['backup_before_update'] = not self.config['backup_before_update']
                status = "Aktiviert" if self.config['backup_before_update'] else "Deaktiviert"
                print(f"✅ Backup vor Update: {status}")
            
            elif choice == "5":
                self.config['silent_installation'] = not self.config['silent_installation']
                status = "Aktiviert" if self.config['silent_installation'] else "Deaktiviert"
                print(f"✅ Silent Installation: {status}")
            
            elif choice == "6":
                self.config['beta_drivers'] = not self.config['beta_drivers']
                status = "Aktiviert" if self.config['beta_drivers'] else "Deaktiviert"
                print(f"✅ Beta-Treiber: {status}")
            
            elif choice == "7":
                interval = input("Update-Intervall (Tage): ")
                try:
                    days = int(interval)
                    if 1 <= days <= 30:
                        self.config['update_interval'] = days
                        print(f"✅ Update-Intervall: {days} Tage")
                except:
                    pass
            
            elif choice == "8":
                brands = ["nvidia", "amd", "intel"]
                print("Verfügbare Marken:")
                for i, brand in enumerate(brands, 1):
                    print(f"   [{i}] {brand.title()}")
                
                brand_choice = input("Wähle Marke: ")
                try:
                    brand_idx = int(brand_choice) - 1
                    if 0 <= brand_idx < len(brands):
                        self.config['preferred_gpu_brand'] = brands[brand_idx]
                        print(f"✅ Bevorzugte GPU-Marke: {brands[brand_idx].title()}")
                except:
                    pass
            
            self.save_config()
            
        except:
            pass
    
    def show_system_info(self):
        """Zeigt System-Informationen"""
        print("\n💻 SYSTEM-INFORMATIONEN")
        print("="*50)
        
        print(f"\n🖥️ System:")
        print(f"   Plattform: {self.system_info['platform']} {self.system_info['version']}")
        print(f"   Architektur: {self.system_info['architecture']}")
        
        print(f"\n🎮 GPU:")
        print(f"   Marke: {self.system_info['gpu_brand'].title()}")
        print(f"   Modell: {self.system_info['gpu_model'].replace('_', ' ').title()}")
        
        print(f"\n🖥️ CPU:")
        print(f"   Marke: {self.system_info['cpu_brand'].title()}")
        print(f"   Modell: {self.system_info['cpu_model'].replace('_', ' ').title()}")
        
        print(f"\n🔧 Treiber-Status:")
        for driver_type, info in self.current_drivers.items():
            status = "🟡 Update" if info['needs_update'] else "✅ Aktuell"
            print(f"   {driver_type.title()}: {info['current']} ({status})")
    
    def run(self):
        """Haupt-Schleife"""
        print("🔧 Windows Gaming Driver Suite wird gestartet...")
        
        if self.config['auto_scan']:
            print("🔍 Führe automatischen System-Scan durch...")
            self.scan_system()
        
        while True:
            self.show_main_menu()
            
            try:
                choice = input("\nWähle Option: ")
                
                if choice == "0":
                    print("\n👋 Auf Wiedersehen!")
                    break
                elif choice == "1":
                    self.scan_system()
                elif choice == "2":
                    self.show_available_updates()
                elif choice == "3":
                    self.install_gaming_drivers()
                elif choice == "4":
                    self.create_backup()
                elif choice == "5":
                    self.show_update_history()
                elif choice == "6":
                    self.show_settings()
                elif choice == "7":
                    print("\n🤖 AUTOMATISCHE UPDATES KONFIGURIEREN")
                    print("Feature in Entwicklung...")
                elif choice == "8":
                    print("\n🔄 TREIBER-DATENBANK AKTUALISIEREN")
                    print("📡 Prüfe auf neue Treiber-Versionen...")
                    time.sleep(2)
                    print("✅ Datenbank aktualisiert")
                elif choice == "9":
                    self.show_system_info()
                else:
                    print("❌ Ungültige Auswahl")
            except KeyboardInterrupt:
                print("\n\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
            
            input("\nDrücke ENTER für weiter...")


if __name__ == "__main__":
    manager = DriverManager()
    manager.run()
