#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Gaming Optimizer - Kombiniert FPS Optimizer + Driver Suite
Konkurrenz zu G-Helper/Armoury Crate durch Code-Optimierung statt Overclocking
"""

import sys
import os
import time
import threading
import json
from datetime import datetime

sys.path.insert(0, 'core')
sys.path.insert(0, '../windows_gaming_driver_suite')

from real_time_optimizer import RealTimeOptimizer
from system_monitor import SystemMonitor
from hardware_benchmark import HardwareBenchmark
from fsr_optimizer import CustomFSROptimizer
from directx12_optimizer_safe import DirectX12OptimizerSafe
from background_process_optimizer import BackgroundProcessOptimizer
from ue5_stability_optimizer import UE5StabilityOptimizer
from thermal_protection import ThermalProtectionManager

class UnifiedGamingOptimizer:
    def __init__(self):
        self.config_file = "unified_config.json"
        self.config = self.load_config()
        
        # Komponenten initialisieren
        self.real_time_optimizer = RealTimeOptimizer()
        self.system_monitor = SystemMonitor()
        self.hardware_benchmark = HardwareBenchmark()
        self.fsr_optimizer = CustomFSROptimizer()
        self.dx12_optimizer = DirectX12OptimizerSafe()
        self.bg_optimizer = BackgroundProcessOptimizer()
        self.ue5_optimizer = UE5StabilityOptimizer()
        self.thermal_manager = ThermalProtectionManager()
        
        # Status
        self.active = False
        self.current_mode = "balanced"
        self.active_game = None
        
        # Performance-Profile
        self.profiles = {
            "silent": {
                "name": "Silent Mode",
                "description": "Leiser Betrieb mit reduzierter Performance",
                "icon": "🔇",
                "optimizations": ["cpu_priority_normal", "background_aggressive", "power_saver"]
            },
            "balanced": {
                "name": "Balanced Mode", 
                "description": "Ausgewogene Performance für tägliche Nutzung",
                "icon": "⚖️",
                "optimizations": ["cpu_priority_above_normal", "background_moderate", "power_balanced"]
            },
            "gaming": {
                "name": "Gaming Mode",
                "description": "Maximale Performance für Gaming",
                "icon": "🎮",
                "optimizations": ["cpu_priority_high", "background_minimal", "power_high_performance"]
            },
            "performance": {
                "name": "Performance Mode",
                "description": "Maximale System-Performance",
                "icon": "🚀",
                "optimizations": ["cpu_priority_realtime", "background_minimal", "power_ultimate"]
            }
        }
        
        # Game-spezifische Profile
        self.game_profiles = {
            "csgo.exe": {
                "profile": "performance",
                "target_fps": 240,
                "optimizations": ["high_fps_priority", "input_lag_reduction"]
            },
            "valorant.exe": {
                "profile": "performance", 
                "target_fps": 240,
                "optimizations": ["high_fps_priority", "input_lag_reduction"]
            },
            "cyberpunk2077.exe": {
                "profile": "gaming",
                "target_fps": 60,
                "optimizations": ["ray_tracing_optimization", "memory_management"]
            },
            "fortnite.exe": {
                "profile": "gaming",
                "target_fps": 144,
                "optimizations": ["competitive_optimization"]
            },
            "borderlands4.exe": {
                "profile": "gaming",
                "target_fps": 60,
                "optimizations": ["unreal_engine_5", "stability_optimization", "memory_management"]
            }
        }
    
    def load_config(self):
        """Lädt Konfiguration"""
        default_config = {
            "auto_mode_switching": True,
            "game_detection": True,
            "thermal_management": True,
            "background_optimization": True,
            "power_management": True,
            "performance_logging": True,
            "default_profile": "balanced",
            "notifications": True,
            "auto_start_monitoring": False
        }
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
        except:
            return default_config
    
    def save_config(self):
        """Speichert Konfiguration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def start(self):
        """Startet den Unified Optimizer"""
        print("🚀 Unified Gaming Optimizer wird gestartet...")
        
        # Komponenten starten
        if self.config["auto_start_monitoring"]:
            self.system_monitor.start_monitoring()
        
        self.real_time_optimizer.start_monitoring()
        
        # Thermal Protection starten
        self.thermal_manager.start_monitoring()
        
        self.active = True
        self.main_loop()
        
        print("✅ Unified Gaming Optimizer aktiv")
        print("🌡️ Thermal Protection: Aktiv")
    
    def stop(self):
        """Stoppt den Unified Optimizer"""
        print("⏹️ Unified Gaming Optimizer wird beendet...")
        
        self.active = False
        
        # Thermal Protection stoppen
        self.thermal_manager.stop_monitoring()
        self.real_time_optimizer.stop_monitoring()
        self.system_monitor.stop_monitoring()
        
        print("✅ Unified Gaming Optimizer beendet")
    
    def main_loop(self):
        """Haupt-Schleife für Mode-Switching und Optimierung"""
        while self.active:
            try:
                # Game-Erkennung
                if self.config["game_detection"]:
                    detected_game = self._detect_game()
                    if detected_game != self.active_game:
                        self.active_game = detected_game
                        self._handle_game_change(detected_game)
                
                # Dynamische Mode-Anpassung
                if self.config["auto_mode_switching"]:
                    self._auto_adjust_mode()
                
                # Performance-Logging
                if self.config["performance_logging"]:
                    self._log_performance()
                
                time.sleep(5)  # 5 Sekunden Intervall
                
            except Exception as e:
                print(f"❌ Main Loop Fehler: {e}")
                time.sleep(10)
    
    def _detect_game(self):
        """Erkennt aktives Game"""
        current_metrics = self.system_monitor.get_current_metrics()
        processes = self.system_monitor.system_info.get("processes", [])
        
        # Hohe CPU/GPU Auslastung als Game-Indikator
        if (current_metrics["cpu_usage"] > 60 or 
            current_metrics["gpu_usage"] > 70):
            
            # Game-Prozesse durchsuchen
            for proc in processes:
                proc_name = proc.get("name", "").lower()
                for game_exe in self.game_profiles.keys():
                    if game_exe in proc_name:
                        return game_exe
        
        return None
    
    def _handle_game_change(self, game_exe):
        """Behandelt Game-Wechsel"""
        if game_exe:
            print(f"🎮 Game erkannt: {game_exe}")
            
            # Game-spezifisches Profil anwenden
            if game_exe in self.game_profiles:
                profile = self.game_profiles[game_exe]
                self.apply_profile(profile["profile"])
                print(f"⚡ {profile['profile']} Profil aktiviert")
                print(f"🎯 Target FPS: {profile['target_fps']}")
            
            # Custom FSR Optimierung starten
            game_name = game_exe.replace(".exe", "").title()
            self.fsr_optimizer.apply_game_profile(game_name)
            self.fsr_optimizer.start_fsr_optimization(game_name)
            print(f"🚀 Custom FSR für {game_name} gestartet")
            
            # DirectX 12 Optimierung starten
            self.dx12_optimizer.start_dx12_optimization(game_name)
            print(f"🎮 DirectX 12 für {game_name} optimiert")
            
            # Background Process Optimierung starten
            self.bg_optimizer.start_optimization()
            print(f"🔧 Hintergrundprozesse optimiert")
            
            # UE5 Stabilitäts-Optimierung für Borderlands 4
            if "borderlands" in game_name.lower():
                print(f"🎮 Borderlands 4 erkannt - Starte UE5 Stabilitäts-Optimierung...")
                self.ue5_optimizer.apply_ue5_stability_profile()
            
        else:
            print("💻 Kein Game aktiv - Normalmodus")
            self.apply_profile(self.config["default_profile"])
            self.fsr_optimizer.stop_fsr_optimization()
            self.dx12_optimizer.stop_dx12_optimization()
            self.bg_optimizer.stop_optimization()
    
    def _auto_adjust_mode(self):
        """Passt Modus automatisch an"""
        current_metrics = self.system_monitor.get_current_metrics()
        summary = self.system_monitor.get_performance_summary()
        
        # Basierend auf Auslastung und Performance-Score entscheiden
        if summary["performance_score"] < 30:
            recommended_mode = "silent"
        elif summary["performance_score"] < 60:
            recommended_mode = "balanced"
        elif current_metrics["cpu_usage"] > 80 or current_metrics["gpu_usage"] > 80:
            recommended_mode = "performance"
        else:
            recommended_mode = "gaming"
        
        if recommended_mode != self.current_mode:
            self.apply_profile(recommended_mode)
            print(f"🔄 Auto-Adjust: {self.current_mode} → {recommended_mode}")
    
    def apply_profile(self, profile_name):
        """Wendet Performance-Profil an"""
        if profile_name not in self.profiles:
            return
        
        profile = self.profiles[profile_name]
        self.current_mode = profile_name
        
        print(f"🎯 {profile['icon']} {profile['name']} aktiviert")
        print(f"📝 {profile['description']}")
        
        # Optimierungen anwenden
        for optimization in profile["optimizations"]:
            self._apply_optimization(optimization)
    
    def _apply_optimization(self, optimization):
        """Wendet spezifische Optimierung an"""
        if optimization == "cpu_priority_normal":
            self.real_time_optimizer.set_optimization_level("silent")
        elif optimization == "cpu_priority_above_normal":
            self.real_time_optimizer.set_optimization_level("balanced")
        elif optimization == "cpu_priority_high":
            self.real_time_optimizer.set_optimization_level("performance")
        elif optimization == "cpu_priority_realtime":
            self.real_time_optimizer.set_optimization_level("performance")
        elif optimization == "power_saver":
            self._set_power_plan("power_saver")
        elif optimization == "power_balanced":
            self._set_power_plan("balanced")
        elif optimization == "power_high_performance":
            self._set_power_plan("high_performance")
        elif optimization == "power_ultimate":
            self._set_power_plan("high_performance")
    
    def _set_power_plan(self, plan):
        """Setzt Windows Power Plan"""
        try:
            import subprocess
            if plan == "power_saver":
                subprocess.run(["powercfg", "/setactive", "SCHEME_MAX"], 
                             check=True, capture_output=True)
            elif plan == "balanced":
                subprocess.run(["powercfg", "/setactive", "SCHEME_BALANCED"], 
                             check=True, capture_output=True)
            elif plan == "high_performance":
                subprocess.run(["powercfg", "/setactive", "SCHEME_MIN"], 
                             check=True, capture_output=True)
        except:
            pass
    
    def _log_performance(self):
        """Loggt Performance-Daten"""
        if not hasattr(self, '_last_log_time'):
            self._last_log_time = time.time()
        
        current_time = time.time()
        if current_time - self._last_log_time >= 60:  # Alle 60 Sekunden
            report = self.system_monitor.generate_performance_report()
            
            # In Datei loggen
            log_file = f"performance_log_{datetime.now().strftime('%Y%m%d')}.json"
            with open(log_file, 'a') as f:
                json.dump({
                    "timestamp": report["timestamp"],
                    "mode": self.current_mode,
                    "game": self.active_game,
                    "performance_score": report["performance_summary"]["performance_score"],
                    "alerts": len(report["active_alerts"])
                }, f)
                f.write("\n")
            
            self._last_log_time = current_time
    
    def show_dashboard(self):
        """Zeigt Unified Dashboard"""
        print("\n" + "="*80)
        print("🎮 UNIFIED GAMING OPTIMIZER DASHBOARD")
        print("="*80)
        
        # Aktuelle Status
        current_metrics = self.system_monitor.get_current_metrics()
        summary = self.system_monitor.get_performance_summary()
        
        print(f"\n📊 AKTUELLER STATUS:")
        print(f"   Mode: {self.profiles[self.current_mode]['icon']} {self.profiles[self.current_mode]['name']}")
        print(f"   Game: {self.active_game or 'Kein Game aktiv'}")
        print(f"   Performance Score: {summary.get('performance_score', 0):.1f}/100")
        print(f"   Status: {summary.get('status', 'unknown').upper()}")
        
        print(f"\n📈 SYSTEM-METRIKEN:")
        print(f"   CPU: {current_metrics['cpu_usage']:.1f}%")
        print(f"   Memory: {current_metrics['memory_usage']:.1f}%")
        print(f"   GPU: {current_metrics['gpu_usage']:.1f}%")
        print(f"   Temperatur: {current_metrics['temperature']:.1f}°C")
        
        # Thermal Protection Status
        thermal_status = self.thermal_manager.get_thermal_status()
        if thermal_status['current_temp'] > 0:
            temp_icon = "🌡️" if thermal_status['safe_to_proceed'] else "🔥"
            print(f"\n{temp_icon} THERMAL PROTECTION:")
            print(f"   Temperatur: {thermal_status['current_temp']:.1f}°C")
            print(f"   Drosselung: {thermal_status['throttle_level'].upper()}")
            print(f"   Status: {'✅ SICHER' if thermal_status['safe_to_proceed'] else '⚠️ REDUZIERT'}")
        
        # FSR Performance
        if self.fsr_optimizer.active:
            fsr_report = self.fsr_optimizer.get_performance_report()
            print(f"\n🚀 FSR OPTIMIZATION:")
            print(f"   Mode: {fsr_report['fsr_mode']}")
            print(f"   Game: {fsr_report['current_game']}")
            print(f"   FPS Gain: +{fsr_report['performance_metrics']['performance_gain']:.1f}%")
        
        # DirectX 12 Performance
        if self.dx12_optimizer.active:
            dx12_report = self.dx12_optimizer.get_dx12_performance_report()
            print(f"\n🎮 DIRECTX 12 OPTIMIZATION:")
            print(f"   Game: {dx12_report['current_game']}")
            print(f"   GPU Usage: {dx12_report['performance_metrics']['gpu_usage_after']:.1f}%")
            print(f"   Memory Usage: {dx12_report['performance_metrics']['memory_usage_after']:.1f}%")
            
            # Aktive DirectX 12 Features
            active_features = dx12_report['dx12_features']
            enabled_features = [name for name, enabled in active_features.items() if enabled]
            print(f"   Active Features: {len(enabled_features)}/4")
        
        # Alerts
        alerts = self.system_monitor.alerts
        if alerts:
            print(f"\n🚨 AKTIVE ALERTS ({len(alerts)}):")
            for alert in alerts[-5:]:  # Letzte 5 Alerts
                level_icon = "🔴" if alert["level"] == "critical" else "🟡"
                print(f"   {level_icon} {alert['component']}: {alert['message']}")
        else:
            print(f"\n✅ Keine aktiven Alerts")
        
        # Empfehlungen
        report = self.system_monitor.generate_performance_report()
        recommendations = report.get("recommendations", [])
        if recommendations:
            print(f"\n💡 EMPFEHLUNGEN:")
            for rec in recommendations[:3]:
                priority_icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
                print(f"   {priority_icon} {rec['message']}")
        
        print(f"\n⚙️ VERFÜGBARE PROFILE:")
        for key, profile in self.profiles.items():
            current = "← AKTIV" if key == self.current_mode else ""
            print(f"   [{key}] {profile['icon']} {profile['name']} {current}")
    
    def show_menu(self):
        """Zeigt interaktives Menü"""
        while True:
            self.show_dashboard()
            
            print(f"\n🔧 OPTIONEN:")
            print("   [1] Profil wechseln")
            print("   [2] Performance-Benchmark")
            print("   [3] System-Report")
            print("   [4] Einstellungen")
            print("   [5] Performance-Graph erstellen")
            print("   [6] Monitoring starten/stoppen")
            print("   [7] FSR Optimierung")
            print("   [8] DirectX 12 Optimierung")
            print("   [9] Hintergrundprozesse optimieren")
            print("   [0] Beenden")
            
            choice = input(f"\nWähle Option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self._profile_selection_menu()
            elif choice == "2":
                self._run_benchmark()
            elif choice == "3":
                self._show_system_report()
            elif choice == "4":
                self._settings_menu()
            elif choice == "5":
                self._create_performance_graph()
            elif choice == "6":
                self._toggle_monitoring()
            elif choice == "7":
                self._fsr_menu()
            elif choice == "8":
                self._dx12_menu()
            elif choice == "9":
                self._bg_optimizer_menu()
            
            input("\nDrücke Enter für Hauptmenü...")
    
    def _profile_selection_menu(self):
        """Profil-Auswahl Menü"""
        print(f"\n🎯 PROFIL-AUSWAHL:")
        
        for key, profile in self.profiles.items():
            current = "← AKTIV" if key == self.current_mode else ""
            print(f"   [{key}] {profile['icon']} {profile['name']}")
            print(f"        {profile['description']} {current}")
        
        choice = input(f"\nWähle Profil: ").strip()
        if choice in self.profiles:
            self.apply_profile(choice)
    
    def _run_benchmark(self):
        """Führt Benchmark durch"""
        print(f"\n📊 PERFORMANCE-BENCHMARK")
        print("="*50)
        
        # Hardware-Benchmark
        benchmark_results = self.hardware_benchmark.run_full_benchmark()
        
        print(f"🔥 CPU Score: {benchmark_results['cpu']['score']:.1f}")
        print(f"🧠 Memory Score: {benchmark_results['memory']['score']:.1f}")
        print(f"🎮 GPU Score: {benchmark_results['gpu']['score']:.1f}")
        print(f"📈 Overall Score: {benchmark_results['overall']['score']:.1f}")
        
        # Performance-Kategorie
        score = benchmark_results['overall']['score']
        if score >= 80:
            category = "🔥 Extreme Gaming"
        elif score >= 60:
            category = "🎮 High-End Gaming"
        elif score >= 40:
            category = "👍 Mid-Range Gaming"
        elif score >= 25:
            category = "⚡ Entry-Level Gaming"
        else:
            category = "💻 Office/Browsing"
        
        print(f"🎯 Kategorie: {category}")
    
    def _show_system_report(self):
        """Zeigt detaillierten System-Report"""
        report = self.system_monitor.generate_performance_report()
        
        print(f"\n📋 DETAILLIERTER SYSTEM-REPORT")
        print("="*60)
        print(f"Zeitpunkt: {report['timestamp']}")
        print(f"Performance Score: {report['performance_summary']['performance_score']:.1f}/100")
        print(f"Status: {report['performance_summary']['status'].upper()}")
        
        print(f"\n📊 PERFORMANCE-DETAILS:")
        cpu = report['performance_summary']['cpu']
        print(f"   CPU: Ø {cpu['average']:.1f}% | Peak {cpu['peak']:.1f}%")
        
        memory = report['performance_summary']['memory']
        print(f"   Memory: Ø {memory['average']:.1f}% | Peak {memory['peak']:.1f}%")
        
        gpu = report['performance_summary']['gpu']
        print(f"   GPU: Ø {gpu['average']:.1f}% | Peak {gpu['peak']:.1f}%")
        
        temp = report['performance_summary']['temperature']
        print(f"   Temperatur: Ø {temp['average']:.1f}°C | Peak {temp['peak']:.1f}°C")
        
        # System-Info
        sys_info = report['system_info']
        print(f"\n💻 SYSTEM-INFORMATIONEN:")
        print(f"   CPU Cores: {sys_info['cpu']['cores']}")
        print(f"   Memory Total: {sys_info['memory']['total'] / (1024**3):.1f} GB")
        
        if sys_info.get('gpu'):
            print(f"   GPU: {sys_info['gpu'][0]['name']}")
    
    def _settings_menu(self):
        """Einstellungen-Menü"""
        print(f"\n⚙️ EINSTELLUNGEN")
        print("="*40)
        
        settings = [
            ("auto_mode_switching", "Automatischer Modus-Wechsel"),
            ("game_detection", "Game-Erkennung"),
            ("thermal_management", "Thermal-Management"),
            ("background_optimization", "Hintergrund-Optimierung"),
            ("power_management", "Power-Management"),
            ("performance_logging", "Performance-Logging"),
            ("notifications", "Benachrichtigungen")
        ]
        
        for key, description in settings:
            status = "✅" if self.config[key] else "❌"
            print(f"   [{key}] {description}: {status}")
        
        print(f"\n[default] Standard-Profil: {self.config['default_profile']}")
        
        choice = input(f"\nEinstellung ändern (oder 'back'): ").strip()
        
        if choice in self.config:
            self.config[choice] = not self.config[choice]
            self.save_config()
            print(f"✅ {choice} = {self.config[choice]}")
        elif choice == "default":
            profiles = list(self.profiles.keys())
            print(f"Verfügbare Profile: {', '.join(profiles)}")
            new_default = input(f"Neues Standard-Profil: ").strip()
            if new_default in profiles:
                self.config["default_profile"] = new_default
                self.save_config()
                print(f"✅ Standard-Profil: {new_default}")
    
    def _create_performance_graph(self):
        """Erstellt Performance-Graph"""
        filename = f"performance_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.system_monitor.create_performance_graph(filename)
        print(f"📊 Graph gespeichert: {filename}")
    
    def _toggle_monitoring(self):
        """Schaltet Monitoring ein/aus"""
        if self.system_monitor.monitoring:
            self.system_monitor.stop_monitoring()
            print("⏹️ Monitoring gestoppt")
        else:
            self.system_monitor.start_monitoring()
            print("▶️ Monitoring gestartet")
    
    def _fsr_menu(self):
        """FSR Optimierung Menü"""
        print(f"\n🚀 FSR OPTIMIERUNG")
        print("="*50)
        
        print(f"Status: {'🟢 AKTIV' if self.fsr_optimizer.active else '🔴 INAKTIV'}")
        if self.fsr_optimizer.active:
            report = self.fsr_optimizer.get_performance_report()
            print(f"Aktuelles Game: {report['current_game'] or 'Kein Game'}")
            print(f"FSR Modus: {report['fsr_mode']}")
            print(f"FPS Gain: +{report['performance_metrics']['performance_gain']:.1f}%")
        
        print(f"\n🔧 FSR OPTIONEN:")
        print("   [1] FSR Modus ändern")
        print("   [2] Game-spezifisches Profil anwenden")
        print("   [3] Custom Sharpening anpassen")
        print("   [4] FSR starten/stoppen")
        print("   [5] FSR Performance-Report")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self._fsr_mode_menu()
        elif choice == "2":
            self._fsr_game_profile_menu()
        elif choice == "3":
            self._fsr_sharpening_menu()
        elif choice == "4":
            self._toggle_fsr()
        elif choice == "5":
            self._fsr_performance_report()
        elif choice == "0":
            return
    
    def _fsr_mode_menu(self):
        """FSR Modus Auswahl"""
        print(f"\n🎯 FSR MODUS AUSWAHL:")
        
        modes = {
            "ultra_performance": "Ultra Performance (50% Render)",
            "performance": "Performance (67% Render)",
            "balanced": "Balanced (77% Render)",
            "quality": "Quality (89% Render)",
            "ultra_quality": "Ultra Quality (100% Render)"
        }
        
        for key, description in modes.items():
            current = "← AKTIV" if self.fsr_optimizer.fsr_mode == key else ""
            print(f"   [{key}] {description} {current}")
        
        choice = input(f"\nWähle Modus: ").strip()
        if choice in modes:
            self.fsr_optimizer.set_fsr_mode(choice)
    
    def _fsr_game_profile_menu(self):
        """Game-spezifisches FSR Profil"""
        print(f"\n🎮 GAME FSR PROFILE:")
        
        games = ["Fortnite", "Valorant", "Cyberpunk 2077", "Apex Legends"]
        
        for i, game in enumerate(games, 1):
            print(f"   [{i}] {game}")
        
        choice = input(f"\nWähle Game: ").strip()
        try:
            game_idx = int(choice) - 1
            if 0 <= game_idx < len(games):
                game = games[game_idx]
                self.fsr_optimizer.apply_game_profile(game)
                print(f"✅ FSR Profil für {game} angewendet")
        except:
            pass
    
    def _fsr_sharpening_menu(self):
        """Custom Sharpening anpassen"""
        print(f"\n🔍 CUSTOM SHARPENING")
        print(f"Aktuell: {self.fsr_optimizer.custom_sharpening:.2f}")
        
        try:
            new_value = input(f"Neuer Wert (0.0-1.0): ").strip()
            strength = float(new_value)
            self.fsr_optimizer.set_custom_sharpening(strength)
        except:
            print("❌ Ungültiger Wert")
    
    def _toggle_fsr(self):
        """FSR starten/stoppen"""
        if self.fsr_optimizer.active:
            self.fsr_optimizer.stop_fsr_optimization()
            print("⏹️ FSR Optimierung gestoppt")
        else:
            game = input(f"Game-Name (oder Enter für aktives): ").strip()
            if not game:
                game = self.active_game or "Unknown"
            self.fsr_optimizer.start_fsr_optimization(game)
            print("▶️ FSR Optimierung gestartet")
    
    def _fsr_performance_report(self):
        """FSR Performance Report"""
        report = self.fsr_optimizer.get_performance_report()
        
        print(f"\n📊 FSR PERFORMANCE REPORT")
        print("="*50)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Active: {report['active']}")
        print(f"Game: {report['current_game']}")
        print(f"Mode: {report['fsr_mode']}")
        print(f"Target Resolution: {report['target_resolution']}")
        print(f"Render Resolution: {report['render_resolution']}")
        
        metrics = report['performance_metrics']
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   FPS Before: {metrics['fps_before']:.1f}")
        print(f"   FPS After: {metrics['fps_after']:.1f}")
        print(f"   Performance Gain: +{metrics['performance_gain']:.1f}%")
        print(f"   Processing Time: {metrics['processing_time']:.3f}s")
        
        print(f"\n🔧 ACTIVE ALGORITHMS:")
        for algo, active in report['algorithms'].items():
            status = "✅" if active else "❌"
            print(f"   {status} {algo.replace('_', ' ').title()}")
    
    def _dx12_menu(self):
        """DirectX 12 Optimierung Menü"""
        print(f"\n🎮 DIRECTX 12 OPTIMIERUNG")
        print("="*50)
        
        print(f"Status: {'🟢 AKTIV' if self.dx12_optimizer.active else '🔴 INAKTIV'}")
        if self.dx12_optimizer.active:
            report = self.dx12_optimizer.get_dx12_performance_report()
            print(f"Aktuelles Game: {report['current_game'] or 'Kein Game'}")
            print(f"GPU Usage: {report['performance_metrics']['gpu_usage_after']:.1f}%")
            print(f"Memory Usage: {report['performance_metrics']['memory_usage_after']:.1f}%")
        
        print(f"\n🔧 DIRECTX 12 OPTIONEN:")
        print("   [1] DirectX 12 starten/stoppen")
        print("   [2] Game-spezifisches Profil anwenden")
        print("   [3] DirectX 12 Features anzeigen")
        print("   [4] DirectX 12 Performance-Report")
        print("   [5] Registry-Einstellungen zurücksetzen")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self._toggle_dx12()
        elif choice == "2":
            self._dx12_game_profile_menu()
        elif choice == "3":
            self._dx12_features_menu()
        elif choice == "4":
            self._dx12_performance_report()
        elif choice == "5":
            self._reset_dx12_registry()
        elif choice == "0":
            return
    
    def _toggle_dx12(self):
        """DirectX 12 starten/stoppen"""
        if self.dx12_optimizer.active:
            self.dx12_optimizer.stop_dx12_optimization()
            print("⏹️ DirectX 12 Optimierung gestoppt")
        else:
            game = input(f"Game-Name (oder Enter für aktives): ").strip()
            if not game:
                game = self.active_game or "Unknown"
            self.dx12_optimizer.start_dx12_optimization(game)
            print("▶️ DirectX 12 Optimierung gestartet")
    
    def _dx12_game_profile_menu(self):
        """Game-spezifisches DirectX 12 Profil"""
        print(f"\n🎮 DIRECTX 12 GAME PROFILE:")
        
        games = ["Fortnite", "Cyberpunk 2077", "Forza Horizon 5"]
        
        for i, game in enumerate(games, 1):
            print(f"   [{i}] {game}")
        
        choice = input(f"\nWähle Game: ").strip()
        try:
            game_idx = int(choice) - 1
            if 0 <= game_idx < len(games):
                game = games[game_idx]
                self.dx12_optimizer.start_dx12_optimization(game.lower().replace(" ", "_"))
                print(f"✅ DirectX 12 Profil für {game} angewendet")
        except:
            pass
    
    def _dx12_features_menu(self):
        """DirectX 12 Features anzeigen"""
        print(f"\n🔧 DIRECTX 12 FEATURES:")
        
        features = self.dx12_optimizer._get_active_dx12_features()
        
        for feature, enabled in features.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {feature.replace('_', ' ').title()}")
        
        print(f"\n📊 Aktive Features: {sum(1 for e in features.values() if e)}/{len(features)}")
    
    def _dx12_performance_report(self):
        """DirectX 12 Performance Report"""
        report = self.dx12_optimizer.get_dx12_performance_report()
        
        print(f"\n📊 DIRECTX 12 PERFORMANCE REPORT")
        print("="*50)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Active: {report['active']}")
        print(f"Game: {report['current_game']}")
        
        metrics = report['performance_metrics']
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   GPU Usage: {metrics.get('gpu_usage_after', 0):.1f}%")
        print(f"   Memory Usage: {metrics.get('memory_usage_after', 0):.1f}%")
        
        print(f"\n🔧 ACTIVE OPTIMIZATIONS:")
        for opt, enabled in report['optimizations'].items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {opt.replace('_', ' ').title()}")
    
    def _bg_optimizer_menu(self):
        """Background Process Optimizer Menü"""
        print(f"\n🔧 HINTERGRUNDPROZESSE OPTIMIERUNG")
        print("="*50)
        
        print(f"Status: {'🟢 AKTIV' if self.bg_optimizer.active else '🔴 INAKTIV'}")
        if self.bg_optimizer.active:
            report = self.bg_optimizer.get_optimization_report()
            print(f"Deaktivierte Services: {report['disabled_services']}")
            print(f"Beendete Prozesse: {report['killed_processes']}")
            print(f"System-Auslastung: CPU {report['system_metrics']['cpu_after']:.1f}%, Memory {report['system_metrics']['memory_after']:.1f}%")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] Optimierung starten/stoppen")
        print("   [2] Services verwalten")
        print("   [3] Temp-Dateien löschen")
        print("   [4] Windows-Einstellungen optimieren")
        print("   [5] Status anzeigen")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self._toggle_bg_optimizer()
        elif choice == "2":
            self._manage_services_menu()
        elif choice == "3":
            self._clear_temp_files_manual()
        elif choice == "4":
            self._optimize_windows_settings_menu()
        elif choice == "5":
            self.bg_optimizer.print_status()
        elif choice == "0":
            return
    
    def _toggle_bg_optimizer(self):
        """Background Process Optimizer starten/stoppen"""
        if self.bg_optimizer.active:
            self.bg_optimizer.stop_optimization()
            print("⏹️ Hintergrundprozess-Optimierung gestoppt")
        else:
            self.bg_optimizer.start_optimization()
            print("▶️ Hintergrundprozess-Optimierung gestartet")
    
    def _manage_services_menu(self):
        """Services-Verwaltung Menü"""
        print(f"\n⚙️ SERVICES VERWALTEN")
        print("="*50)
        
        print(f"Unnötige Services die deaktiviert werden:")
        for i, service in enumerate(self.bg_optimizer.unnecessary_services[:10], 1):
            print(f"   {i}. {service}")
        
        if len(self.bg_optimizer.unnecessary_services) > 10:
            print(f"   ... und {len(self.bg_optimizer.unnecessary_services) - 10} weitere")
        
        print(f"\n� OPTIONEN:")
        print("   [1] Alle Services deaktivieren")
        print("   [2] Services wiederherstellen")
        print("   [3] Gaming-Modus aktivieren")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self.bg_optimizer._optimize_services()
            print("✅ Services deaktiviert")
        elif choice == "2":
            self.bg_optimizer._restore_services()
            print("✅ Services wiederhergestellt")
        elif choice == "3":
            self.bg_optimizer.optimization_settings["disable_windows_update"] = True
            self.bg_optimizer.optimization_settings["disable_superfetch"] = True
            self.bg_optimizer.optimization_settings["disable_windows_search"] = True
            self.bg_optimizer._optimize_services()
            self.bg_optimizer._optimize_windows_settings()
            print("✅ Gaming-Modus aktiviert - Alle unnötigen Services deaktiviert")
        elif choice == "0":
            return
    
    def _clear_temp_files_manual(self):
        """Temp-Dateien manuell löschen"""
        print(f"\n🧹 TEMP-DATEIEN LÖSCHEN")
        print("="*50)
        
        print("Lösche temporäre Dateien...")
        self.bg_optimizer._clear_temp_files()
    
    def _optimize_windows_settings_menu(self):
        """Windows-Einstellungen optimieren"""
        print(f"\n⚙️ WINDOWS-EINSTELLUNGEN OPTIMIEREN")
        print("="*50)
        
        print(f"Aktuelle Einstellungen:")
        for setting, enabled in self.bg_optimizer.optimization_settings.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {setting.replace('_', ' ').title()}")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] Alle Einstellungen optimieren")
        print("   [2] Visual Effects optimieren")
        print("   [3] Hintergrund-Apps deaktivieren")
        print("   [4] Power Plan optimieren")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self.bg_optimizer._optimize_windows_settings()
            print("✅ Alle Windows-Einstellungen optimiert")
        elif choice == "2":
            self.bg_optimizer._optimize_visual_effects()
            print("✅ Visual Effects optimiert")
        elif choice == "3":
            self.bg_optimizer._disable_background_apps()
            print("✅ Hintergrund-Apps deaktiviert")
        elif choice == "4":
            self.bg_optimizer._optimize_power_plan()
            print("✅ Power Plan optimiert")
        elif choice == "0":
            return

def main():
    """Hauptfunktion"""
    optimizer = UnifiedGamingOptimizer()
    
    try:
        # Starte im Hintergrund
        optimizer.start()
        
        # Zeige Dashboard
        optimizer.show_menu()
        
    except KeyboardInterrupt:
        print("\n👋 Programm beendet")
    finally:
        optimizer.stop()

if __name__ == "__main__":
    main()
