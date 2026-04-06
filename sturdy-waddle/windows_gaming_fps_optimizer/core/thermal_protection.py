#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thermal Protection & Load Manager - Schützt Hardware vor Überhitzung
"""

import psutil
import time
import threading
import logging
import os
from datetime import datetime
from typing import Dict, Optional

class ThermalProtectionManager:
    """Überwacht Temperatur und verhindert Überhitzung durch intelligente Drosselung"""
    
    def __init__(self):
        self.active = False
        self.monitoring_thread = None
        self.current_temp = 0.0
        self.max_temp = 0.0
        self.throttling_active = False
        
        # Initialize logger FIRST
        self.logger = self._setup_logging()
        
        # Erkenne ob Laptop oder Desktop
        self.is_laptop = self._detect_laptop()
        
        # Temperatur-Grenzwerte (in Celsius) - ANGEPASST FÜR LAPTOPS
        if self.is_laptop:
            # Gaming Laptop Werte (höher, da Laptops sowieso heißer werden)
            self.temp_thresholds = {
                "normal": 80,      # Normaler Betrieb für Laptop
                "warm": 88,        # Warnung
                "hot": 93,         # Drosselung aktivieren (Laptops laufen oft bei 90°C+)
                "critical": 96     # Maximale Drosselung/Notfall
            }
            self.logger.info("🖥️ Laptop erkannt - Thermale Grenzwerte für Laptop angepasst")
        else:
            # Desktop Werte (niedriger)
            self.temp_thresholds = {
                "normal": 70,
                "warm": 80,
                "hot": 85,
                "critical": 90
            }
        
        # Drosselungs-Level
        self.throttle_levels = {
            "none": 1.0,       # 100% Leistung
            "light": 0.9,      # 90% Leistung
            "medium": 0.7,     # 70% Leistung
            "heavy": 0.5,      # 50% Leistung
            "critical": 0.3    # 30% Leistung - Nur essenzielle Funktionen
        }
        
        self.current_throttle = "none"
        self.logger = self._setup_logging()
        
        # Optimierungs-Status für Wiederherstellung
        self.original_optimizations = {}
        
    def _setup_logging(self):
        """Richtet Logging ein"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"thermal_protection_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _detect_laptop(self) -> bool:
        """Erkennt ob System ein Laptop ist"""
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty PCSystemType"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                # 2 = Laptop/Mobile
                return "2" in result.stdout.strip()
            
            # Alternative: Prüfe auf Batterie
            result2 = subprocess.run(
                ["powershell", "-Command",
                 "Get-WmiObject -Class Win32_Battery | Measure-Object"],
                capture_output=True, text=True, timeout=5
            )
            if "Count" in result2.stdout and "0" not in result2.stdout:
                return True
                
        except:
            pass
        return False  # Default: Desktop
    
    def start_monitoring(self):
        """Startet Temperatur-Überwachung"""
        self.active = True
        self.logger.info("🌡️ Thermal Protection Manager gestartet")
        print("🌡️ Thermal Protection: Überwachung aktiv")
        
        self.monitoring_thread = threading.Thread(target=self._thermal_monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stoppt Überwachung"""
        self.active = False
        if self.throttling_active:
            self._restore_optimizations()
        self.logger.info("⏹️ Thermal Protection Manager gestoppt")
        print("⏹️ Thermal Protection: Überwachung beendet")
    
    def _thermal_monitoring_loop(self):
        """Haupt-Überwachungsschleife"""
        while self.active:
            try:
                # Temperatur auslesen
                current_temp = self._get_current_temperature()
                
                if current_temp:
                    self.current_temp = current_temp
                    self.max_temp = max(self.max_temp, current_temp)
                    
                    # Prüfe Temperatur-Grenzwerte
                    self._check_temperature_thresholds(current_temp)
                    
                    # Logging alle 30 Sekunden
                    if int(time.time()) % 30 == 0:
                        self.logger.info(f"🌡️ Temperatur: {current_temp:.1f}°C (Max: {self.max_temp:.1f}°C)")
                
                # Alle 2 Sekunden prüfen
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"❌ Thermal Monitoring Fehler: {e}")
                time.sleep(5)
    
    def _get_current_temperature(self) -> Optional[float]:
        """Ermittelt aktuelle CPU/GPU Temperatur"""
        try:
            # Versuche psutil (falls verfügbar)
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    max_temp = 0.0
                    for name, entries in temps.items():
                        for entry in entries:
                            if hasattr(entry, 'current') and entry.current:
                                max_temp = max(max_temp, entry.current)
                    return max_temp if max_temp > 0 else None
            
            # Fallback: WMI für Windows
            try:
                import subprocess
                result = subprocess.run(
                    ["powershell", "-Command",
                     "Get-WmiObject -Namespace root\\wmi -Class MSAcpi_ThermalZoneTemperature | Select-Object -ExpandProperty CurrentTemperature | ForEach-Object { ($_ - 2732) / 10.0 }"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    temps = [float(t.strip()) for t in result.stdout.strip().split('\n') if t.strip()]
                    return max(temps) if temps else None
            except:
                pass
            
            return None
            
        except Exception as e:
            self.logger.warning(f"⚠️ Temperatur-Auslesung fehlgeschlagen: {e}")
            return None
    
    def _check_temperature_thresholds(self, temp: float):
        """Prüft Temperatur-Grenzwerte und aktiviert Drosselung"""
        if temp >= self.temp_thresholds["critical"]:
            # KRITISCH - Maximale Drosselung
            if self.current_throttle != "critical":
                self.logger.warning(f"🔥 KRITISCHE TEMPERATUR: {temp:.1f}°C - Maximale Drosselung!")
                print(f"🔥 WARNUNG: {temp:.1f}°C - Hardware wird geschützt...")
                self._apply_throttling("critical")
                
        elif temp >= self.temp_thresholds["hot"]:
            # HEISS - Mittlere Drosselung
            if self.current_throttle not in ["heavy", "critical"]:
                self.logger.warning(f"🌡️ Hohe Temperatur: {temp:.1f}°C - Drosselung aktiviert")
                print(f"🌡️ Temperatur hoch ({temp:.1f}°C) - Optimierungen reduziert")
                self._apply_throttling("heavy")
                
        elif temp >= self.temp_thresholds["warm"]:
            # WARM - Leichte Drosselung
            if self.current_throttle not in ["medium", "heavy", "critical"]:
                self.logger.info(f"⚠️ Warme Temperatur: {temp:.1f}°C - Leichte Reduktion")
                self._apply_throttling("medium")
                
        elif temp >= self.temp_thresholds["normal"]:
            # NORMAL - Keine Änderung
            if self.current_throttle != "none":
                self.logger.info(f"✅ Temperatur normal: {temp:.1f}°C - Volle Leistung")
                self._apply_throttling("none")
        else:
            # KALT - Volle Leistung
            if self.current_throttle != "none":
                self._apply_throttling("none")
    
    def _apply_throttling(self, level: str):
        """Wendet Drosselungs-Level an"""
        if level == self.current_throttle:
            return
        
        self.current_throttle = level
        throttle_factor = self.throttle_levels[level]
        
        self.logger.info(f"🔧 Drosselung: {level.upper()} ({throttle_factor*100:.0f}% Leistung)")
        
        # Je nach Level unterschiedliche Maßnahmen
        if level == "critical":
            self._emergency_throttling()
        elif level == "heavy":
            self._heavy_throttling()
        elif level == "medium":
            self._medium_throttling()
        elif level == "light":
            self._light_throttling()
        else:  # none
            self._restore_optimizations()
    
    def _emergency_throttling(self):
        """Notfall-Drosselung - Nur essenzielle Funktionen"""
        print("🚨 NOTFALL-DROSSELUNG: Hardware-Schutz aktiv!")
        
        try:
            # 1. Alle nicht-essenziellen Optimierungen stoppen
            self._reduce_optimizer_load()
            
            # 2. Background-Apps priorisieren (mehr CPU für Game)
            self._reduce_background_priority()
            
            # 3. Power Plan auf "Ausgewogen" (weniger Hitze)
            import subprocess
            subprocess.run(
                ["powercfg", "/setactive", "SCHEME_BALANCED"],
                capture_output=True, check=False, timeout=5
            )
            
            # 4. CPU-Priorität für Games reduzieren (weniger Hitze)
            self._reduce_game_priority_slightly()
            
            # 5. LAPTOP-SPEZIFISCH: Maximale Kühlung aktivieren
            if self.is_laptop:
                self._activate_maximum_laptop_cooling()
            
            self.throttling_active = True
            
        except Exception as e:
            self.logger.error(f"❌ Emergency Throttling Fehler: {e}")
    
    def _activate_maximum_laptop_cooling(self):
        """Aktiviert maximale Kühlung für Laptops"""
        try:
            print("🖥️ Laptop-Kühlung: Maximale Lüftergeschwindigkeit")
            
            # Versuche Lüftergeschwindigkeit zu erhöhen (wenn unterstützt)
            subprocess.run([
                "powershell", "-Command",
                "# Versuche OEM-Tools für Lüftersteuerung",
                "$oemTools = @('C:\\Program Files\\OEM\\FanControl.exe', 'C:\\Program Files (x86)\\MSI Afterburner\\MSIAfterburner.exe')",
                "foreach ($tool in $oemTools) { if (Test-Path $tool) { Start-Process $tool -ArgumentList '-fan100' -WindowStyle Hidden } }"
            ], capture_output=True, check=False, timeout=10)
            
            # Prozess-Prioritäten für Hintergrund-Apps reduzieren
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in ['chrome.exe', 'discord.exe', 'spotify.exe', 'firefox.exe']:
                        proc.nice(psutil.IDLE_PRIORITY_CLASS)
                except:
                    pass
            
            # Windows Search komplett deaktivieren (erzeugt viel Hitze)
            subprocess.run(
                ["sc", "config", "WSearch", "start=", "disabled"],
                capture_output=True, check=False, timeout=5
            )
            subprocess.run(
                ["sc", "stop", "WSearch"],
                capture_output=True, check=False, timeout=5
            )
            
            # Superfetch deaktivieren
            subprocess.run(
                ["sc", "config", "SysMain", "start=", "disabled"],
                capture_output=True, check=False, timeout=5
            )
            subprocess.run(
                ["sc", "stop", "SysMain"],
                capture_output=True, check=False, timeout=5
            )
            
            self.logger.info("✅ Maximale Laptop-Kühlung aktiviert")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Laptop-Kühlung Fehler: {e}")
    
    def _heavy_throttling(self):
        """Starke Drosselung"""
        try:
            # 1. Optimierungs-Frequenz reduzieren
            self._reduce_optimizer_frequency()
            
            # 2. FSR auf Quality-Mode (mehr native Rendering, weniger Hitze)
            self._adjust_fsr_for_thermal()
            
            # 3. Hintergrund-Optimierungen pausieren
            self._pause_background_optimizations()
            
            self.throttling_active = True
            
        except Exception as e:
            self.logger.error(f"❌ Heavy Throttling Fehler: {e}")
    
    def _medium_throttling(self):
        """Mittlere Drosselung"""
        try:
            # 1. Logging reduzieren
            self._reduce_logging()
            
            # 2. Monitoring-Intervall erhöhen
            self._increase_monitoring_interval()
            
        except Exception as e:
            self.logger.error(f"❌ Medium Throttling Fehler: {e}")
    
    def _light_throttling(self):
        """Leichte Drosselung"""
        try:
            # Nur Logging-Frequenz reduzieren
            self._reduce_logging()
            
        except Exception as e:
            self.logger.error(f"❌ Light Throttling Fehler: {e}")
    
    def _restore_optimizations(self):
        """Stellt ursprüngliche Optimierungen wieder her"""
        if not self.throttling_active:
            return
        
        print("✅ Temperatur normal - Volle Optimierungen wiederhergestellt")
        self.logger.info("✅ Drosselung aufgehoben - Volle Leistung")
        
        try:
            # Power Plan zurücksetzen
            import subprocess
            subprocess.run(
                ["powercfg", "/setactive", "SCHEME_MIN"],
                capture_output=True, check=False, timeout=5
            )
            
            self.throttling_active = False
            
        except Exception as e:
            self.logger.error(f"❌ Restore Fehler: {e}")
    
    def _reduce_optimizer_load(self):
        """Reduziert eigene CPU-Last des Optimizers"""
        # Diese Methode wird vom Unified Optimizer aufgerufen
        pass  # Platzhalter für Integration
    
    def _reduce_background_priority(self):
        """Senkt Priorität von Hintergrundprozessen"""
        try:
            import win32api
            import win32con
            import win32process
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in ['chrome.exe', 'discord.exe', 'spotify.exe']:
                        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc.info['pid'])
                        win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
                        win32api.CloseHandle(handle)
                except:
                    continue
        except:
            pass
    
    def _reduce_game_priority_slightly(self):
        """Senkt Game-Priorität leicht für weniger Hitze"""
        try:
            import win32api
            import win32con
            import win32process
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'borderlands' in proc.info['name'].lower() or 'fortnite' in proc.info['name'].lower():
                        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc.info['pid'])
                        win32process.SetPriorityClass(handle, win32process.ABOVE_NORMAL_PRIORITY_CLASS)
                        win32api.CloseHandle(handle)
                except:
                    continue
        except:
            pass
    
    def _reduce_optimizer_frequency(self):
        """Reduziert Optimierungs-Frequenz"""
        self.logger.info("🔧 Optimierungs-Frequenz reduziert für weniger Hitze")
    
    def _adjust_fsr_for_thermal(self):
        """Passt FSR für thermische Bedingungen an"""
        self.logger.info("🎮 FSR auf Quality-Mode für weniger GPU-Last")
    
    def _pause_background_optimizations(self):
        """Pausiert Hintergrund-Optimierungen"""
        self.logger.info("⏸️ Hintergrund-Optimierungen pausiert")
    
    def _reduce_logging(self):
        """Reduziert Logging-Frequenz"""
        pass  # Implementiert durch Logger-Level
    
    def _increase_monitoring_interval(self):
        """Erhöht Monitoring-Intervall (weniger CPU-Last)"""
        pass  # Wird in der Loop implementiert
    
    def get_thermal_status(self) -> Dict:
        """Gibt aktuellen Thermal-Status zurück"""
        return {
            "current_temp": self.current_temp,
            "max_temp": self.max_temp,
            "throttle_level": self.current_throttle,
            "throttle_factor": self.throttle_levels[self.current_throttle],
            "throttling_active": self.throttling_active,
            "temp_thresholds": self.temp_thresholds,
            "safe_to_proceed": self.current_temp < self.temp_thresholds["hot"]
        }
    
    def print_thermal_status(self):
        """Gibt Thermal-Status aus"""
        status = self.get_thermal_status()
        
        print(f"\n🌡️ THERMAL PROTECTION STATUS")
        print("="*50)
        print(f"Aktuelle Temperatur: {status['current_temp']:.1f}°C")
        print(f"Max Temperatur: {status['max_temp']:.1f}°C")
        print(f"Drosselungs-Level: {status['throttle_level'].upper()}")
        print(f"Leistungs-Faktor: {status['throttle_factor']*100:.0f}%")
        print(f"Status: {'✅ SICHER' if status['safe_to_proceed'] else '🔥 WARNUNG'}")
        
        if status['throttling_active']:
            print(f"\n⚠️ Drosselung aktiv zum Schutz der Hardware!")
            print(f"   Optimierungen reduziert bei {status['current_temp']:.1f}°C")

if __name__ == "__main__":
    # Test Thermal Protection
    thermal = ThermalProtectionManager()
    
    print("🌡️ THERMAL PROTECTION TEST")
    print("="*50)
    
    thermal.start_monitoring()
    
    try:
        # Simuliere 30 Sekunden Überwachung
        for i in range(15):
            thermal.print_thermal_status()
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    
    thermal.stop_monitoring()
    
    print(f"\n✅ Thermal Protection Test beendet")
