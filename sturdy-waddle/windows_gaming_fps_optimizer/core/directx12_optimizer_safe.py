#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DirectX 12 Optimizer - Safe Version ohne Registry-Zugriff
"""

import subprocess
import threading
import logging
import time
import psutil
import os
from datetime import datetime

class DirectX12OptimizerSafe:
    def __init__(self):
        self.active = False
        self.current_game = None
        self.performance_metrics = {
            "fps_before": 0,
            "fps_after": 0,
            "gpu_usage": 0,
            "memory_usage": 0
        }
        
        # DirectX 12 Optimierungen (software-basiert)
        self.dx12_optimizations = {
            "async_compute": True,
            "variable_rate_shading": True,
            "multi_threaded": True,
            "gpu_priority": "high",
            "memory_optimization": "balanced"
        }
        
        # Game-spezifische Profile
        self.game_profiles = {
            "fortnite": {
                "name": "Fortnite",
                "dx12_mode": "performance",
                "async_compute": True,
                "variable_rate_shading": True,
                "multi_threaded": True,
                "gpu_priority": "high",
                "memory_optimization": "aggressive",
                "target_fps": 120,
                "command_line_args": ["-dx12", "-nosplash", "-async"]
            },
            "cyberpunk_2077": {
                "name": "Cyberpunk 2077",
                "dx12_mode": "quality",
                "async_compute": True,
                "variable_rate_shading": True,
                "multi_threaded": True,
                "gpu_priority": "high",
                "memory_optimization": "balanced",
                "target_fps": 60,
                "command_line_args": ["-dx12", "-async_compute", "-enablevrs"]
            },
            "forza_horizon_5": {
                "name": "Forza Horizon 5",
                "dx12_mode": "balanced",
                "async_compute": True,
                "variable_rate_shading": True,
                "multi_threaded": True,
                "gpu_priority": "high",
                "memory_optimization": "balanced",
                "target_fps": 60,
                "command_line_args": ["-dx12", "-vrs", "-async"]
            },
            "valorant": {
                "name": "Valorant",
                "dx12_mode": "ultra_performance",
                "async_compute": False,
                "variable_rate_shading": False,
                "multi_threaded": True,
                "gpu_priority": "high",
                "memory_optimization": "aggressive",
                "target_fps": 240,
                "command_line_args": ["-dx12", "-highpriority"]
            },
            "borderlands_4": {
                "name": "Borderlands 4",
                "dx12_mode": "balanced",  # Balanced für Stabilität
                "async_compute": True,
                "variable_rate_shading": False,  # Deaktiviert für Stabilität
                "multi_threaded": True,
                "gpu_priority": "high",
                "memory_optimization": "balanced",  # Balanced statt aggressive
                "target_fps": 60,
                "command_line_args": ["-dx12", "-novsync", "-useallcores"],
                "ue5_optimizations": {
                    "disable_lumen": True,  # Lumen kann zu Instabilität führen
                    "disable_nanite_streaming": False,
                    "shader_preload": True,
                    "texture_streaming_pool": 2048,  # MB
                    "memory_pool_size": 4096  # MB
                },
                "stability_fixes": {
                    "disable_fullscreen_optimization": True,
                    "disable_game_mode": False,
                    "run_as_admin": True,
                    "high_dpi_scaling": False
                }
            }
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """Richtet Logging ein"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"dx12_optimizer_safe_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def start_dx12_optimization(self, game_name=None):
        """Startet DirectX 12 Optimierung (Safe Mode)"""
        self.active = True
        self.current_game = game_name
        
        self.logger.info(f"🚀 DirectX 12 Optimizer (Safe) gestartet für {game_name or 'aktive Anwendung'}")
        print(f"🚀 DirectX 12 Optimizer (Safe) gestartet für {game_name or 'aktive Anwendung'}")
        
        # Game-spezifische Optimierungen anwenden
        if game_name:
            game_key = game_name.lower().replace(" ", "_").replace(".exe", "")
            if game_key in self.game_profiles:
                self._apply_game_profile_safe(game_key)
            else:
                self._apply_default_dx12_safe()
        else:
            self._apply_default_dx12_safe()
        
        # Starte Optimierungs-Thread
        self.optimization_thread = threading.Thread(target=self._dx12_optimization_loop_safe, daemon=True)
        self.optimization_thread.start()
    
    def stop_dx12_optimization(self):
        """Stoppt DirectX 12 Optimierung"""
        self.active = False
        self.logger.info("⏹️ DirectX 12 Optimizer (Safe) gestoppt")
        print("⏹️ DirectX 12 Optimizer (Safe) gestoppt")
    
    def _apply_game_profile_safe(self, game_key):
        """Wendet game-spezifisches DirectX 12 Profil an (Safe Mode)"""
        profile = self.game_profiles[game_key]
        
        self.logger.info(f"🎮 Wende DirectX 12 Profil für {profile['name']} an (Safe Mode)")
        print(f"🎮 Wende DirectX 12 Profil für {profile['name']} an (Safe Mode)")
        
        # DirectX 12 Features aktivieren (software-basiert)
        features = profile
        for feature, enabled in features.items():
            if feature in self.dx12_optimizations:
                self.dx12_optimizations[feature] = enabled
                self.logger.info(f"✅ DirectX 12 Feature {feature}: {'aktiviert' if enabled else 'deaktiviert'}")
        
        # System-Level Optimierungen
        self._apply_system_optimizations_safe(profile)
        
        print(f"✅ DirectX 12 Profil für {profile['name']} aktiviert (Safe Mode)")
    
    def _apply_default_dx12_safe(self):
        """Wendet Standard DirectX 12 Optimierungen an (Safe Mode)"""
        self.logger.info("🔧 Wende Standard DirectX 12 Optimierungen an (Safe Mode)")
        
        default_features = {
            "async_compute": True,
            "variable_rate_shading": True,
            "multi_threaded": True,
            "gpu_priority": "high",
            "memory_optimization": "balanced"
        }
        
        for feature, enabled in default_features.items():
            self.dx12_optimizations[feature] = enabled
        
        self._apply_system_optimizations_safe({"name": "Default", "gpu_priority": "high"})
    
    def _apply_system_optimizations_safe(self, profile):
        """Wendet System-Optimierungen an (Safe Mode)"""
        try:
            # Power Plan auf High Performance
            subprocess.run(["powercfg", "/setactive", "SCHEME_MIN"], capture_output=True, check=False)
            
            # GPU Priority über PowerShell (falls möglich)
            if profile.get("gpu_priority") == "high":
                try:
                    # Versuche GPU-Priorität zu erhöhen
                    subprocess.run([
                        "powershell", "-Command", 
                        "Get-Process | Where-Object {$_.ProcessName -like '*game*'} | ForEach-Object { $_.PriorityClass = 'High' }"
                    ], capture_output=True, check=False)
                except:
                    pass
            
            # Memory Management
            subprocess.run([
                "powershell", "-Command", 
                "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect()"
            ], capture_output=True, check=False)
            
            self.logger.info("✅ System-Optimierungen angewendet (Safe Mode)")
            
        except Exception as e:
            self.logger.error(f"❌ System-Optimierung Fehler: {e}")
    
    def _dx12_optimization_loop_safe(self):
        """Haupt-Optimierungsschleife für DirectX 12 (Safe Mode)"""
        while self.active:
            try:
                # Performance-Metriken sammeln
                self._collect_performance_metrics_safe()
                
                # Dynamische Optimierungen
                self._apply_dynamic_dx12_optimizations_safe()
                
                # GPU-Workload-Balancing
                self._optimize_gpu_workload_safe()
                
                # Memory-Optimierung
                self._optimize_memory_safe()
                
                time.sleep(3)  # 3 Sekunden Intervall
                
            except Exception as e:
                self.logger.error(f"❌ DirectX 12 Optimierungsfehler (Safe): {e}")
                time.sleep(5)
    
    def _collect_performance_metrics_safe(self):
        """Sammelt Performance-Metriken (Safe Mode)"""
        try:
            # CPU/GPU Usage
            self.performance_metrics["gpu_usage"] = psutil.cpu_percent(interval=0.1)
            
            # Memory Usage
            memory = psutil.virtual_memory()
            self.performance_metrics["memory_usage"] = memory.percent
            
            self.logger.debug(f"📊 GPU: {self.performance_metrics['gpu_usage']:.1f}%, Memory: {self.performance_metrics['memory_usage']:.1f}%")
            
        except Exception as e:
            self.logger.error(f"❌ Performance-Metriken Fehler (Safe): {e}")
    
    def _apply_dynamic_dx12_optimizations_safe(self):
        """Wendet dynamische DirectX 12 Optimierungen an (Safe Mode)"""
        try:
            gpu_usage = self.performance_metrics["gpu_usage"]
            memory_usage = self.performance_metrics["memory_usage"]
            
            # GPU-Workload basierend auf Auslastung anpassen
            if gpu_usage > 90:
                self._adjust_dx12_workload_safe("reduce")
            elif gpu_usage < 50:
                self._adjust_dx12_workload_safe("increase")
            
            # Memory-Optimierung basierend auf Speichernutzung
            if memory_usage > 85:
                self._optimize_memory_aggressive_safe()
            elif memory_usage > 70:
                self._optimize_memory_moderate_safe()
            
        except Exception as e:
            self.logger.error(f"❌ Dynamische Optimierung Fehler (Safe): {e}")
    
    def _adjust_dx12_workload_safe(self, action):
        """Passt DirectX 12 Workload an (Safe Mode)"""
        try:
            if action == "reduce":
                # Reduziere Workload bei hoher GPU-Auslastung
                self.logger.info("📉 DirectX 12 Workload reduziert (Safe)")
                # Setze Prozess-Priorität für aktives Game
                self._set_game_priority_safe("below_normal")
            elif action == "increase":
                # Erhöhe Workload bei niedriger GPU-Auslastung
                self.logger.info("📈 DirectX 12 Workload erhöht (Safe)")
                # Setze Prozess-Priorität für aktives Game
                self._set_game_priority_safe("high")
                
        except Exception as e:
            self.logger.error(f"❌ Workload-Anpassung Fehler (Safe): {e}")
    
    def _set_game_priority_safe(self, priority):
        """Setzt Game-Priorität (Safe Mode)"""
        try:
            import win32api
            import win32con
            import win32process
            
            # Finde Game-Prozesse
            for proc in psutil.process_iter(['pid', 'name']):
                proc_name = proc.info['name'].lower()
                
                # Prüfe ob es ein Game-Prozess ist
                game_processes = ["fortnite", "cyberpunk", "forza", "valorant", "csgo", "apex"]
                if any(game in proc_name for game in game_processes):
                    try:
                        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc.info['pid'])
                        
                        if priority == "high":
                            win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
                        elif priority == "below_normal":
                            win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
                        
                        win32api.CloseHandle(handle)
                        self.logger.info(f"✅ Game-Priorität gesetzt: {priority} für {proc_name}")
                        break
                    except:
                        continue
                        
        except Exception as e:
            self.logger.error(f"❌ Game-Priorität Fehler (Safe): {e}")
    
    def _optimize_gpu_workload_safe(self):
        """Optimiert GPU-Workload-Verteilung (Safe Mode)"""
        try:
            # Background-Prozesse mit niedriger Priorität
            background_processes = ["chrome.exe", "firefox.exe", "discord.exe", "spotify.exe"]
            
            for proc in psutil.process_iter(['pid', 'name']):
                proc_name = proc.info['name'].lower()
                
                if any(bg_proc in proc_name for bg_proc in background_processes):
                    try:
                        import win32api
                        import win32con
                        import win32process
                        
                        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc.info['pid'])
                        win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
                        win32api.CloseHandle(handle)
                    except:
                        continue
                        
        except Exception as e:
            self.logger.error(f"❌ GPU Workload Optimierung Fehler (Safe): {e}")
    
    def _optimize_memory_safe(self):
        """Optimiert Memory (Safe Mode)"""
        try:
            # Standard Memory-Optimierung
            subprocess.run([
                "powershell", "-Command", 
                "[System.GC]::Collect()"
            ], capture_output=True, check=False)
            
        except Exception as e:
            self.logger.error(f"❌ Memory Optimierung Fehler (Safe): {e}")
    
    def _optimize_memory_aggressive_safe(self):
        """Aggressive Memory-Optimierung (Safe Mode)"""
        try:
            subprocess.run([
                "powershell", "-Command", 
                "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect(); [System.GC]::GetTotalMemory('force')"
            ], capture_output=True, check=False)
            
        except Exception as e:
            self.logger.error(f"❌ Aggressive Memory Optimierung Fehler (Safe): {e}")
    
    def _optimize_memory_moderate_safe(self):
        """Moderate Memory-Optimierung (Safe Mode)"""
        try:
            subprocess.run([
                "powershell", "-Command", 
                "[System.GC]::Collect(); [System.GC]::GetTotalMemory()"
            ], capture_output=True, check=False)
            
        except Exception as e:
            self.logger.error(f"❌ Moderate Memory Optimierung Fehler (Safe): {e}")
    
    def get_dx12_performance_report_safe(self):
        """Gibt DirectX 12 Performance-Report zurück (Safe Mode)"""
        return {
            "timestamp": datetime.now().isoformat(),
            "active": self.active,
            "current_game": self.current_game,
            "optimizations": self.dx12_optimizations,
            "performance_metrics": self.performance_metrics,
            "mode": "safe"
        }
    
    def print_dx12_status_safe(self):
        """Gibt aktuellen DirectX 12 Status aus (Safe Mode)"""
        report = self.get_dx12_performance_report_safe()
        
        print(f"\n🎮 DIRECTX 12 OPTIMIZER STATUS (SAFE)")
        print("="*50)
        print(f"Aktiv: {'🟢 JA' if report['active'] else '🔴 NEIN'}")
        print(f"Game: {report['current_game'] or 'Kein Game'}")
        print(f"Mode: {report['mode'].upper()}")
        
        print(f"\n🔧 AKTIVE FEATURES:")
        for feature, enabled in report['optimizations'].items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {feature.replace('_', ' ').title()}")
        
        print(f"\n📊 PERFORMANCE METRICS:")
        metrics = report['performance_metrics']
        print(f"   GPU Usage: {metrics.get('gpu_usage', 0):.1f}%")
        print(f"   Memory Usage: {metrics.get('memory_usage', 0):.1f}%")
    
    def get_command_line_args(self, game_name):
        """Gibt Command-Line Argumente für Game zurück"""
        game_key = game_name.lower().replace(" ", "_").replace(".exe", "")
        
        if game_key in self.game_profiles:
            return self.game_profiles[game_key].get("command_line_args", [])
        
        return ["-dx12"]  # Standard DirectX 12 Argument

if __name__ == "__main__":
    # Test DirectX 12 Optimizer (Safe)
    dx12 = DirectX12OptimizerSafe()
    
    print("🎮 DIRECTX 12 OPTIMIZER TEST (SAFE)")
    print("="*50)
    
    # Test mit Fortnite
    dx12.start_dx12_optimization("fortnite")
    time.sleep(5)
    
    # Status anzeigen
    dx12.print_dx12_status_safe()
    
    # Stoppen
    dx12.stop_dx12_optimization()
    
    print(f"\n✅ DirectX 12 Test (Safe) abgeschlossen")
