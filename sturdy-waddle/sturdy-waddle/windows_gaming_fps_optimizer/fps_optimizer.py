#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Gaming FPS Optimizer - Hauptanwendung
"""

import sys
import os
import time
import json
from datetime import datetime

sys.path.insert(0, 'core')
sys.path.insert(0, 'ui')
sys.path.insert(0, 'tools')

class FPSOptimizer:
    def __init__(self):
        self.config_file = "settings.json"
        self.config = self.load_config()
        
        # Hardware-Datenbank
        self.hardware_db = {
            "cpus": {
                "Intel Core i3-8100": {"score": 35, "cores": 4, "base_clock": 3.6},
                "Intel Core i5-8400": {"score": 45, "cores": 6, "base_clock": 2.8},
                "Intel Core i7-8700": {"score": 60, "cores": 6, "base_clock": 3.2},
                "Intel Core i9-9900": {"score": 75, "cores": 8, "base_clock": 3.1},
                "AMD Ryzen 3 1200": {"score": 30, "cores": 4, "base_clock": 3.1},
                "AMD Ryzen 5 2600": {"score": 50, "cores": 6, "base_clock": 3.4},
                "AMD Ryzen 7 2700": {"score": 65, "cores": 8, "base_clock": 3.2},
                "AMD Ryzen 9 3900": {"score": 80, "cores": 12, "base_clock": 3.1},
            },
            "gpus": {
                "NVIDIA GTX 1050": {"score": 25, "vram": 2048, "memory_clock": 7000},
                "NVIDIA GTX 1060": {"score": 40, "vram": 6072, "memory_clock": 8000},
                "NVIDIA GTX 1070": {"score": 55, "vram": 8192, "memory_clock": 8000},
                "NVIDIA GTX 1080": {"score": 70, "vram": 8192, "memory_clock": 10000},
                "NVIDIA RTX 2060": {"score": 60, "vram": 6144, "memory_clock": 14000},
                "NVIDIA RTX 2070": {"score": 75, "vram": 8192, "memory_clock": 14000},
                "NVIDIA RTX 2080": {"score": 85, "vram": 8192, "memory_clock": 14000},
                "AMD RX 570": {"score": 35, "vram": 4096, "memory_clock": 7000},
                "AMD RX 580": {"score": 45, "vram": 8192, "memory_clock": 8000},
                "AMD RX 590": {"score": 50, "vram": 8192, "memory_clock": 8000},
                "AMD RX 5600": {"score": 65, "vram": 6144, "memory_clock": 14000},
                "AMD RX 5700": {"score": 75, "vram": 8192, "memory_clock": 14000},
            },
            "games": {
                "CS:GO": {"cpu_req": 30, "gpu_req": 25, "ram_req": 4, "fps_target": 144},
                "Valorant": {"cpu_req": 35, "gpu_req": 30, "ram_req": 4, "fps_target": 144},
                "Apex Legends": {"cpu_req": 45, "gpu_req": 40, "ram_req": 8, "fps_target": 144},
                "Fortnite": {"cpu_req": 40, "gpu_req": 35, "ram_req": 8, "fps_target": 144},
                "PUBG": {"cpu_req": 50, "gpu_req": 45, "ram_req": 8, "fps_target": 60},
                "Warzone": {"cpu_req": 60, "gpu_req": 55, "ram_req": 12, "fps_target": 60},
                "Cyberpunk 2077": {"cpu_req": 70, "gpu_req": 80, "ram_req": 12, "fps_target": 60},
                "Witcher 3": {"cpu_req": 45, "gpu_req": 50, "ram_req": 8, "fps_target": 60},
                "Elden Ring": {"cpu_req": 55, "gpu_req": 60, "ram_req": 12, "fps_target": 60},
                "Forza Horizon 5": {"cpu_req": 60, "gpu_req": 65, "ram_req": 12, "fps_target": 60},
            }
        }
        
        self.current_hardware = {}
        self.benchmark_results = {}
    
    def load_config(self):
        """Lädt Konfiguration"""
        default_config = {
            "optimization_level": "balanced",
            "target_fps": 60,
            "max_temperature": 80,
            "enable_overclock": False,
            "auto_update_drivers": True,
            "selected_cpu": None,
            "selected_gpu": None,
            "ram_gb": 16,
            "ram_speed": 3200
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
    
    def show_main_menu(self):
        """Zeigt Hauptmenü"""
        print("\n" + "="*70)
        print("🎮 WINDOWS GAMING FPS OPTIMIZER")
        print("="*70)
        
        print(f"\n📊 AKTUELLE KONFIGURATION:")
        print(f"   CPU: {self.config['selected_cpu'] or 'Nicht ausgewählt'}")
        print(f"   GPU: {self.config['selected_gpu'] or 'Nicht ausgewählt'}")
        print(f"   RAM: {self.config['ram_gb']}GB @ {self.config['ram_speed']}MHz")
        print(f"   Target FPS: {self.config['target_fps']}")
        print(f"   Optimierung: {self.config['optimization_level']}")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] Hardware konfigurieren")
        print("   [2] Hardware-Benchmark durchführen")
        print("   [3] System optimieren")
        print("   [4] Game-Optimierung")
        print("   [5] FPS-Projektionen anzeigen")
        print("   [6] Performance-Monitoring")
        print("   [7] Treiber-Updates")
        print("   [8] Benchmark-Report")
        print("   [9] Einstellungen")
        print("   [0] Beenden")
    
    def show_hardware_menu(self):
        """Zeigt Hardware-Konfiguration"""
        print("\n🔧 HARDWARE KONFIGURATION")
        print("="*50)
        
        print("\n📋 VERFÜGBARE CPUs:")
        cpu_list = list(self.hardware_db["cpus"].keys())
        for i, cpu in enumerate(cpu_list, 1):
            specs = self.hardware_db["cpus"][cpu]
            print(f"   [{i:2d}] {cpu}")
            print(f"        Score: {specs['score']}, Cores: {specs['cores']}, Clock: {specs['base_clock']}GHz")
        
        print(f"\n📋 VERFÜGBARE GPUs:")
        gpu_list = list(self.hardware_db["gpus"].keys())
        for i, gpu in enumerate(gpu_list, 1):
            specs = self.hardware_db["gpus"][gpu]
            print(f"   [{i:2d}] {gpu}")
            print(f"        Score: {specs['score']}, VRAM: {specs['vram']}MB")
        
        print("\n[CPU] Wähle CPU (1-8): ", end="")
        try:
            cpu_choice = input()
            cpu_idx = int(cpu_choice) - 1
            if 0 <= cpu_idx < len(cpu_list):
                self.config['selected_cpu'] = cpu_list[cpu_idx]
                print(f"✅ CPU ausgewählt: {self.config['selected_cpu']}")
        except:
            pass
        
        print("[GPU] Wähle GPU (1-13): ", end="")
        try:
            gpu_choice = input()
            gpu_idx = int(gpu_choice) - 1
            if 0 <= gpu_idx < len(gpu_list):
                self.config['selected_gpu'] = gpu_list[gpu_idx]
                print(f"✅ GPU ausgewählt: {self.config['selected_gpu']}")
        except:
            pass
        
        print("[RAM] RAM Größe (4, 8, 16, 32): ", end="")
        try:
            ram_choice = input()
            ram_gb = int(ram_choice)
            if ram_gb in [4, 8, 16, 32]:
                self.config['ram_gb'] = ram_gb
                print(f"✅ RAM: {ram_gb}GB")
        except:
            pass
        
        print("[RAM] RAM Geschwindigkeit (2133, 2666, 3200, 3600): ", end="")
        try:
            speed_choice = input()
            ram_speed = int(speed_choice)
            if ram_speed in [2133, 2666, 3200, 3600]:
                self.config['ram_speed'] = ram_speed
                print(f"✅ RAM: {ram_speed}MHz")
        except:
            pass
        
        self.save_config()
    
    def run_hardware_benchmark(self):
        """Führt Hardware-Benchmark durch"""
        print("\n📊 HARDWARE BENCHMARK")
        print("="*50)
        
        if not self.config['selected_cpu'] or not self.config['selected_gpu']:
            print("❌ Bitte zuerst Hardware konfigurieren!")
            return
        
        cpu_score = self.hardware_db["cpus"][self.config['selected_cpu']]["score"]
        gpu_score = self.hardware_db["gpus"][self.config['selected_gpu']]["score"]
        
        # RAM-Score basierend auf Größe und Geschwindigkeit
        ram_score = (self.config['ram_gb'] / 16) * (self.config['ram_speed'] / 3200) * 50
        
        # Gesamtscore
        overall_score = (cpu_score * 0.3 + gpu_score * 0.5 + ram_score * 0.2)
        
        print(f"\n📈 BENCHMARK ERGEBNISSE:")
        print(f"   CPU Score: {cpu_score:.1f}")
        print(f"   GPU Score: {gpu_score:.1f}")
        print(f"   RAM Score: {ram_score:.1f}")
        print(f"   Overall Score: {overall_score:.1f}")
        
        # Performance-Kategorie
        if overall_score >= 80:
            category = "🔥 Extreme Gaming"
        elif overall_score >= 60:
            category = "🎮 High-End Gaming"
        elif overall_score >= 40:
            category = "👍 Mid-Range Gaming"
        elif overall_score >= 25:
            category = "⚡ Entry-Level Gaming"
        else:
            category = "💻 Office/Browsing"
        
        print(f"   Kategorie: {category}")
        
        # Speichern
        self.benchmark_results = {
            "cpu_score": cpu_score,
            "gpu_score": gpu_score,
            "ram_score": ram_score,
            "overall_score": overall_score,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
    
    def show_fps_projections(self):
        """Zeigt FPS-Projektionen für Games"""
        print("\n🎮 FPS PROJEKTIONEN")
        print("="*50)
        
        if not self.benchmark_results:
            print("❌ Bitte zuerst Benchmark durchführen!")
            return
        
        print(f"\n📊 Basierend auf Score: {self.benchmark_results['overall_score']:.1f}")
        print("\nGame-Projektionen (1080p, Medium Settings):")
        
        for game, requirements in self.hardware_db["games"].items():
            cpu_req = requirements["cpu_req"]
            gpu_req = requirements["gpu_req"]
            target_fps = requirements["fps_target"]
            
            # FPS-Kalkulation
            cpu_factor = min(1.0, self.benchmark_results["cpu_score"] / cpu_req)
            gpu_factor = min(1.0, self.benchmark_results["gpu_score"] / gpu_req)
            
            estimated_fps = target_fps * min(cpu_factor, gpu_factor)
            
            if estimated_fps >= target_fps * 0.9:
                status = "🟢 Excellent"
            elif estimated_fps >= target_fps * 0.7:
                status = "🟡 Good"
            elif estimated_fps >= target_fps * 0.5:
                status = "🟠 Playable"
            else:
                status = "🔴 Low"
            
            print(f"   {game:20s}: {estimated_fps:5.0f} FPS {status}")
    
    def show_system_optimization(self):
        """Zeigt System-Optimierungsoptionen"""
        print("\n⚡ SYSTEM OPTIMIERUNG")
        print("="*50)
        
        optimizations = [
            ("Game Mode aktivieren", "+5-15% FPS", "Einfach"),
            ("Power Plan Maximum", "+3-8% FPS", "Einfach"),
            ("XMP/EXPO RAM Profile", "+5-12% FPS", "Mittel"),
            ("Background Processes", "+2-6% FPS", "Mittel"),
            ("Windows Update deaktivieren", "+1-3% FPS", "Einfach"),
            ("Antivirus pausieren", "+2-4% FPS", "Einfach"),
            ("GPU Overclocking", "+15-30% FPS", "Schwer"),
            ("CPU Overclocking", "+10-20% FPS", "Schwer"),
        ]
        
        print("\nVerfügbare Optimierungen:")
        for opt, gain, difficulty in optimizations:
            print(f"   ✅ {opt:25s}: {gain:12s} ({difficulty})")
        
        print("\n📝 Empfehlung:")
        print("   1. Starte mit den 'Einfachen' Optimierungen")
        print("   2. Danach 'Mittel' für weitere Gewinne")
        print("   3. 'Schwer' nur mit Erfahrung und Kühlung")
    
    def show_game_optimization(self):
        """Zeigt Game-spezifische Optimierung"""
        print("\n🎮 GAME OPTIMIERUNG")
        print("="*50)
        
        games = list(self.hardware_db["games"].keys())
        print("\nVerfügbare Games:")
        for i, game in enumerate(games, 1):
            print(f"   [{i:2d}] {game}")
        
        print("[0] Zurück")
        
        try:
            choice = input("\nWähle Game: ")
            
            if choice == "0":
                return
            
            game_idx = int(choice) - 1
            if 0 <= game_idx < len(games):
                selected_game = games[game_idx]
                self.show_game_specific_tips(selected_game)
        except:
            print("❌ Ungültige Auswahl")
    
    def show_game_specific_tips(self, game):
        """Zeigt Game-spezifische Tipps"""
        print(f"\n🎮 {game} OPTIMIERUNG")
        print("="*50)
        
        tips = {
            "CS:GO": [
                "Launch Options: -novid -nojoy -high +fps_max 0",
                "Settings: Low/Medium für maximale FPS",
                "Resolution: 1280x960 oder 1440x1080 (4:3)",
                "Mouse: Raw Input aktivieren"
            ],
            "Valorant": [
                "Launch Options: -d3d9ex -novid",
                "Settings: Low/Multi-Threaded Rendering",
                "Resolution: 1920x1080 für Balance",
                "V-Sync: Deaktivieren"
            ],
            "Cyberpunk 2077": [
                "Settings: Medium/High statt Ultra",
                "DLSS: Quality oder Balanced",
                "Ray Tracing: Medium oder Aus",
                "Texture Streaming: Aktivieren"
            ]
        }
        
        if game in tips:
            print(f"\n💡 Optimierungs-Tipps für {game}:")
            for tip in tips[game]:
                print(f"   • {tip}")
        else:
            print(f"\n💡 Allgemeine Tipps für {game}:")
            print("   • Shadows auf Medium/Low")
            print("   • Anti-Aliasing: FXAA statt MSAA")
            print("   • Resolution: 1080p für maximale FPS")
            print("   • V-Sync: Deaktivieren für competitive Gaming")
    
    def show_settings(self):
        """Zeigt Einstellungen"""
        print("\n⚙️ EINSTELLUNGEN")
        print("="*50)
        
        print(f"\nAktuelle Einstellungen:")
        print(f"   Optimierungs-Level: {self.config['optimization_level']}")
        print(f"   Target FPS: {self.config['target_fps']}")
        print(f"   Max Temperatur: {self.config['max_temperature']}°C")
        print(f"   Overclock: {'Aktiviert' if self.config['enable_overclock'] else 'Deaktiviert'}")
        print(f"   Auto Driver Updates: {'Aktiviert' if self.config['auto_update_drivers'] else 'Deaktiviert'}")
        
        print("\n[1] Optimierungs-Level ändern")
        print("[2] Target FPS ändern")
        print("[3] Overclock-Toggle")
        print("[0] Zurück")
        
        try:
            choice = input("\nWähle Option: ")
            
            if choice == "1":
                levels = ["power_saving", "balanced", "performance", "extreme"]
                print("Verfügbare Levels:")
                for i, level in enumerate(levels, 1):
                    print(f"   [{i}] {level}")
                
                level_choice = input("Wähle Level: ")
                try:
                    level_idx = int(level_choice) - 1
                    if 0 <= level_idx < len(levels):
                        self.config['optimization_level'] = levels[level_idx]
                        print(f"✅ Level: {levels[level_idx]}")
                except:
                    pass
            
            elif choice == "2":
                fps_choice = input("Target FPS (30, 60, 120, 144): ")
                try:
                    fps = int(fps_choice)
                    if fps in [30, 60, 120, 144]:
                        self.config['target_fps'] = fps
                        print(f"✅ Target FPS: {fps}")
                except:
                    pass
            
            elif choice == "3":
                self.config['enable_overclock'] = not self.config['enable_overclock']
                status = "Aktiviert" if self.config['enable_overclock'] else "Deaktiviert"
                print(f"✅ Overclock: {status}")
            
            self.save_config()
            
        except:
            pass
    
    def run(self):
        """Haupt-Schleife"""
        while True:
            self.show_main_menu()
            
            try:
                choice = input("\nWähle Option: ")
                
                if choice == "0":
                    print("\n👋 Auf Wiedersehen!")
                    break
                elif choice == "1":
                    self.show_hardware_menu()
                elif choice == "2":
                    self.run_hardware_benchmark()
                elif choice == "3":
                    self.show_system_optimization()
                elif choice == "4":
                    self.show_game_optimization()
                elif choice == "5":
                    self.show_fps_projections()
                elif choice == "6":
                    print("\n📊 Performance-Monitoring")
                    print("Feature in Entwicklung...")
                elif choice == "7":
                    print("\n🔧 Treiber-Updates")
                    print("Feature in Entwicklung...")
                elif choice == "8":
                    print("\n📈 Benchmark-Report")
                    if self.benchmark_results:
                        print(f"Score: {self.benchmark_results['overall_score']:.1f}")
                        print(f"Kategorie: {self.benchmark_results['category']}")
                        print(f"Zeitpunkt: {self.benchmark_results['timestamp']}")
                    else:
                        print("❌ Keine Benchmark-Ergebnisse verfügbar")
                elif choice == "9":
                    self.show_settings()
                else:
                    print("❌ Ungültige Auswahl")
            except KeyboardInterrupt:
                print("\n\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
            
            input("\nDrücke ENTER für weiter...")


if __name__ == "__main__":
    optimizer = FPSOptimizer()
    optimizer.run()
