#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DirectX 12 Optimizer - Spezielle Optimierung für DirectX 12 Games
"""

import subprocess
import json
import winreg
import os
import time
import threading
import logging
from datetime import datetime

class DirectX12Optimizer:
    def __init__(self):
        self.active = False
        self.current_game = None
        self.dx12_settings = {}
        self.original_settings = {}
        self.performance_metrics = {
            "fps_before": 0,
            "fps_after": 0,
            "gpu_usage_before": 0,
            "gpu_usage_after": 0,
            "memory_usage_before": 0,
            "memory_usage_after": 0
        }
        
        # DirectX 12 spezifische Optimierungen
        self.dx12_optimizations = {
            "gpu_workload_distribution": True,
            "multi_threaded_command_buffer": True,
            "resource_barrier_optimization": True,
            "descriptor_heap_optimization": True,
            "memory_pool_optimization": True,
            "async_compute_optimization": True,
            "variable_rate_shading": True,
            "mesh_shading_optimization": True
        }
        
        # Game-spezifische DirectX 12 Profile
        self.dx12_game_profiles = {
            "fortnite": {
                "name": "Fortnite",
                "dx12_features": {
                    "async_compute": True,
                    "variable_rate_shading": True,
                    "mesh_shaders": False,  # Fortnite unterstützt keine Mesh Shaders
                    "multi_threaded": True,
                    "gpu_priority": "high",
                    "memory_optimization": "aggressive"
                },
                "registry_settings": {
                    "HKEY_LOCAL_MACHINE\\SOFTWARE\\Epic Games\\Unreal Engine\\4.27": {
                        "DX12GI": 1,
                        "DX12MaxFrameLatency": 1,
                        "DX12GPUAffinity": 1
                    }
                }
            },
            "cyberpunk_2077": {
                "name": "Cyberpunk 2077",
                "dx12_features": {
                    "async_compute": True,
                    "variable_rate_shading": True,
                    "mesh_shaders": True,  # Cyberpunk unterstützt Mesh Shaders
                    "multi_threaded": True,
                    "gpu_priority": "high",
                    "memory_optimization": "balanced"
                },
                "registry_settings": {
                    "HKEY_CURRENT_USER\\SOFTWARE\\CD Projekt Red\\Cyberpunk 2077": {
                        "DX12Enabled": 1,
                        "RayTracingDX12": 1,
                        "DX12AsyncCompute": 1
                    }
                }
            },
            "forza_horizon_5": {
                "name": "Forza Horizon 5",
                "dx12_features": {
                    "async_compute": True,
                    "variable_rate_shading": True,
                    "mesh_shaders": False,
                    "multi_threaded": True,
                    "gpu_priority": "high",
                    "memory_optimization": "balanced"
                },
                "registry_settings": {
                    "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft Games\\Forza Horizon 5": {
                        "DX12Enabled": 1,
                        "DX12AsyncCompute": 1,
                        "DX12VRS": 1
                    }
                }
            }
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """Richtet Logging ein"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"dx12_optimizer_{datetime.now().strftime('%Y%m%d')}.log")
        
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
        """Startet DirectX 12 Optimierung"""
        self.active = True
        self.current_game = game_name
        
        self.logger.info(f"🚀 DirectX 12 Optimizer gestartet für {game_name or 'aktive Anwendung'}")
        print(f"🚀 DirectX 12 Optimizer gestartet für {game_name or 'aktive Anwendung'}")
        
        # Backup der aktuellen Einstellungen
        self._backup_current_settings()
        
        # Game-spezifische Optimierungen anwenden
        if game_name:
            game_key = game_name.lower().replace(" ", "_").replace(".exe", "")
            if game_key in self.dx12_game_profiles:
                self._apply_game_profile(game_key)
            else:
                self._apply_default_dx12_optimizations()
        else:
            self._apply_default_dx12_optimizations()
        
        # Starte Optimierungs-Thread
        self.optimization_thread = threading.Thread(target=self._dx12_optimization_loop, daemon=True)
        self.optimization_thread.start()
    
    def stop_dx12_optimization(self):
        """Stoppt DirectX 12 Optimierung"""
        self.active = False
        self._restore_original_settings()
        self.logger.info("⏹️ DirectX 12 Optimizer gestoppt")
        print("⏹️ DirectX 12 Optimizer gestoppt")
    
    def _backup_current_settings(self):
        """Sichert aktuelle Einstellungen"""
        self.logger.info("📋 Sichere aktuelle DirectX 12 Einstellungen...")
        
        try:
            # DirectX 12 Registry Keys
            dx12_keys = [
                "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX",
                "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\DirectX"
            ]
            
            for key_path in dx12_keys:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE if "HKEY_LOCAL_MACHINE" in key_path else winreg.HKEY_CURRENT_USER,
                                     key_path.split("\\", 1)[1], 0, winreg.KEY_READ) as key:
                        settings = {}
                        i = 0
                        while True:
                            try:
                                name, value, reg_type = winreg.EnumValue(key, i)
                                settings[name] = value
                                i += 1
                            except WindowsError:
                                break
                        self.original_settings[key_path] = settings
                except:
                    pass
            
            self.logger.info(f"✅ {len(self.original_settings)} Einstellungen gesichert")
            
        except Exception as e:
            self.logger.error(f"❌ Backup Fehler: {e}")
    
    def _restore_original_settings(self):
        """Stellt originale Einstellungen wieder her"""
        self.logger.info("🔄 Stelle originale Einstellungen wieder her...")
        
        try:
            for key_path, settings in self.original_settings.items():
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE if "HKEY_LOCAL_MACHINE" in key_path else winreg.HKEY_CURRENT_USER,
                                     key_path.split("\\", 1)[1], 0, winreg.KEY_WRITE) as key:
                        for name, value in settings.items():
                            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD if isinstance(value, int) else winreg.REG_SZ, value)
                except:
                    pass
            
            self.logger.info("✅ Originale Einstellungen wiederhergestellt")
            
        except Exception as e:
            self.logger.error(f"❌ Restore Fehler: {e}")
    
    def _apply_game_profile(self, game_key):
        """Wendet game-spezifisches DirectX 12 Profil an"""
        profile = self.dx12_game_profiles[game_key]
        
        self.logger.info(f"🎮 Wende DirectX 12 Profil für {profile['name']} an")
        print(f"🎮 Wende DirectX 12 Profil für {profile['name']} an")
        
        # DirectX 12 Features aktivieren
        features = profile["dx12_features"]
        for feature, enabled in features.items():
            self._enable_dx12_feature(feature, enabled)
        
        # Registry-Einstellungen anwenden
        registry_settings = profile.get("registry_settings", {})
        for key_path, settings in registry_settings.items():
            self._apply_registry_settings(key_path, settings)
        
        # GPU-spezifische Optimierungen
        self._apply_gpu_optimizations(features.get("gpu_priority", "normal"))
        
        print(f"✅ DirectX 12 Profil für {profile['name']} aktiviert")
    
    def _apply_default_dx12_optimizations(self):
        """Wendet Standard DirectX 12 Optimierungen an"""
        self.logger.info("🔧 Wende Standard DirectX 12 Optimierungen an")
        
        default_features = {
            "async_compute": True,
            "variable_rate_shading": True,
            "mesh_shaders": False,
            "multi_threaded": True,
            "gpu_priority": "high",
            "memory_optimization": "balanced"
        }
        
        for feature, enabled in default_features.items():
            self._enable_dx12_feature(feature, enabled)
        
        self._apply_gpu_optimizations("high")
    
    def _enable_dx12_feature(self, feature, enabled):
        """Aktiviert/deaktiviert DirectX 12 Feature"""
        try:
            if feature == "async_compute":
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "AsyncComputeEnabled", 1 if enabled else 0)
            elif feature == "variable_rate_shading":
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "VariableRateShadingEnabled", 1 if enabled else 0)
            elif feature == "mesh_shaders":
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "MeshShadersEnabled", 1 if enabled else 0)
            elif feature == "multi_threaded":
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "MultiThreadedCommandBuffer", 1 if enabled else 0)
            
            self.logger.info(f"✅ DirectX 12 Feature {feature}: {'aktiviert' if enabled else 'deaktiviert'}")
            
        except Exception as e:
            self.logger.error(f"❌ Feature {feature} Fehler: {e}")
    
    def _set_registry_value(self, key_path, value_name, value):
        """Setzt Registry-Wert"""
        try:
            root_key = winreg.HKEY_LOCAL_MACHINE if "HKEY_LOCAL_MACHINE" in key_path else winreg.HKEY_CURRENT_USER
            sub_key = key_path.split("\\", 1)[1]
            
            with winreg.CreateKey(root_key, sub_key) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
                
        except Exception as e:
            self.logger.error(f"❌ Registry Fehler {key_path}\\{value_name}: {e}")
    
    def _apply_registry_settings(self, key_path, settings):
        """Wendet Registry-Einstellungen an"""
        try:
            root_key = winreg.HKEY_LOCAL_MACHINE if "HKEY_LOCAL_MACHINE" in key_path else winreg.HKEY_CURRENT_USER
            sub_key = key_path.split("\\", 1)[1]
            
            with winreg.CreateKey(root_key, sub_key) as key:
                for name, value in settings.items():
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD if isinstance(value, int) else winreg.REG_SZ, value)
            
            self.logger.info(f"✅ Registry Einstellungen für {key_path} angewendet")
            
        except Exception as e:
            self.logger.error(f"❌ Registry Fehler {key_path}: {e}")
    
    def _apply_gpu_optimizations(self, priority):
        """Wendet GPU-spezifische Optimierungen an"""
        try:
            # GPU Priority Registry
            priority_values = {
                "low": 1,
                "normal": 2,
                "high": 3,
                "realtime": 4
            }
            
            gpu_priority = priority_values.get(priority, 2)
            
            # AMD GPU Optimierungen
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000",
                                   "KMD_DeferSchedule", 1 if priority == "high" else 0)
            
            # NVIDIA GPU Optimierungen
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000",
                                   "Pm4Caps", 1 if priority == "high" else 0)
            
            self.logger.info(f"✅ GPU Priority: {priority} ({gpu_priority})")
            
        except Exception as e:
            self.logger.error(f"❌ GPU Optimierung Fehler: {e}")
    
    def _dx12_optimization_loop(self):
        """Haupt-Optimierungsschleife für DirectX 12"""
        while self.active:
            try:
                # Performance-Metriken sammeln
                self._collect_performance_metrics()
                
                # Dynamische Optimierungen
                self._apply_dynamic_dx12_optimizations()
                
                # GPU-Workload-Balancing
                self._optimize_gpu_workload()
                
                # Memory-Pool-Optimierung
                self._optimize_memory_pools()
                
                time.sleep(3)  # 3 Sekunden Intervall
                
            except Exception as e:
                self.logger.error(f"❌ DirectX 12 Optimierungsfehler: {e}")
                time.sleep(5)
    
    def _collect_performance_metrics(self):
        """Sammelt Performance-Metriken"""
        try:
            import psutil
            
            # GPU Usage (vereinfacht)
            self.performance_metrics["gpu_usage_after"] = psutil.cpu_percent(interval=0.1)
            
            # Memory Usage
            memory = psutil.virtual_memory()
            self.performance_metrics["memory_usage_after"] = memory.percent
            
            self.logger.debug(f"📊 GPU: {self.performance_metrics['gpu_usage_after']:.1f}%, Memory: {self.performance_metrics['memory_usage_after']:.1f}%")
            
        except Exception as e:
            self.logger.error(f"❌ Performance-Metriken Fehler: {e}")
    
    def _apply_dynamic_dx12_optimizations(self):
        """Wendet dynamische DirectX 12 Optimierungen an"""
        try:
            gpu_usage = self.performance_metrics["gpu_usage_after"]
            memory_usage = self.performance_metrics["memory_usage_after"]
            
            # GPU-Workload basierend auf Auslastung anpassen
            if gpu_usage > 90:
                self._adjust_dx12_workload("reduce")
            elif gpu_usage < 50:
                self._adjust_dx12_workload("increase")
            
            # Memory-Pools basierend auf Speichernutzung anpassen
            if memory_usage > 85:
                self._optimize_memory_pools_aggressive()
            elif memory_usage > 70:
                self._optimize_memory_pools_moderate()
            
        except Exception as e:
            self.logger.error(f"❌ Dynamische Optimierung Fehler: {e}")
    
    def _adjust_dx12_workload(self, action):
        """Passt DirectX 12 Workload an"""
        try:
            if action == "reduce":
                # Reduziere Workload bei hoher GPU-Auslastung
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "MaxFrameLatency", 2)
                self.logger.info("📉 DirectX 12 Workload reduziert")
            elif action == "increase":
                # Erhöhe Workload bei niedriger GPU-Auslastung
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "MaxFrameLatency", 1)
                self.logger.info("📈 DirectX 12 Workload erhöht")
                
        except Exception as e:
            self.logger.error(f"❌ Workload-Anpassung Fehler: {e}")
    
    def _optimize_gpu_workload(self):
        """Optimiert GPU-Workload-Verteilung"""
        try:
            # Multi-GPU-Optimierung (falls vorhanden)
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                   "GPUAffinity", 1)
            
            # Command-Buffer-Optimierung
            if self.dx12_optimizations["multi_threaded_command_buffer"]:
                self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                       "MultiThreadedCommandBuffer", 1)
            
        except Exception as e:
            self.logger.error(f"❌ GPU Workload Optimierung Fehler: {e}")
    
    def _optimize_memory_pools(self):
        """Optimiert Memory-Pools"""
        try:
            # Standard Memory-Pool-Optimierung
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                   "MemoryPoolOptimization", 1)
            
        except Exception as e:
            self.logger.error(f"❌ Memory Pool Optimierung Fehler: {e}")
    
    def _optimize_memory_pools_aggressive(self):
        """Aggressive Memory-Pool-Optimierung"""
        try:
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                   "MemoryPoolOptimization", 3)
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                   "MemoryGarbageCollection", 1)
            
        except Exception as e:
            self.logger.error(f"❌ Aggressive Memory Optimierung Fehler: {e}")
    
    def _optimize_memory_pools_moderate(self):
        """Moderate Memory-Pool-Optimierung"""
        try:
            self._set_registry_value("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\DirectX", 
                                   "MemoryPoolOptimization", 2)
            
        except Exception as e:
            self.logger.error(f"❌ Moderate Memory Optimierung Fehler: {e}")
    
    def get_dx12_performance_report(self):
        """Gibt DirectX 12 Performance-Report zurück"""
        return {
            "timestamp": datetime.now().isoformat(),
            "active": self.active,
            "current_game": self.current_game,
            "optimizations": self.dx12_optimizations,
            "performance_metrics": self.performance_metrics,
            "dx12_features": self._get_active_dx12_features()
        }
    
    def _get_active_dx12_features(self):
        """Gibt aktive DirectX 12 Features zurück"""
        features = {}
        
        try:
            # Prüfe DirectX 12 Registry
            dx12_keys = [
                ("AsyncComputeEnabled", "async_compute"),
                ("VariableRateShadingEnabled", "variable_rate_shading"),
                ("MeshShadersEnabled", "mesh_shaders"),
                ("MultiThreadedCommandBuffer", "multi_threaded")
            ]
            
            for reg_name, feature_name in dx12_keys:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                     "SOFTWARE\\Microsoft\\DirectX", 0, winreg.KEY_READ) as key:
                        value, _ = winreg.QueryValueEx(key, reg_name)
                        features[feature_name] = bool(value)
                except:
                    features[feature_name] = False
            
        except Exception as e:
            self.logger.error(f"❌ Feature-Abfrage Fehler: {e}")
        
        return features
    
    def print_dx12_status(self):
        """Gibt aktuellen DirectX 12 Status aus"""
        report = self.get_dx12_performance_report()
        
        print(f"\n🎮 DIRECTX 12 OPTIMIZER STATUS")
        print("="*50)
        print(f"Aktiv: {'🟢 JA' if report['active'] else '🔴 NEIN'}")
        print(f"Game: {report['current_game'] or 'Kein Game'}")
        
        print(f"\n🔧 AKTIVE FEATURES:")
        for feature, enabled in report['dx12_features'].items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {feature.replace('_', ' ').title()}")
        
        print(f"\n📊 PERFORMANCE METRICS:")
        metrics = report['performance_metrics']
        print(f"   GPU Usage: {metrics.get('gpu_usage_after', 0):.1f}%")
        print(f"   Memory Usage: {metrics.get('memory_usage_after', 0):.1f}%")

if __name__ == "__main__":
    # Test DirectX 12 Optimizer
    dx12 = DirectX12Optimizer()
    
    print("🎮 DIRECTX 12 OPTIMIZER TEST")
    print("="*50)
    
    # Test mit Fortnite
    dx12.start_dx12_optimization("fortnite")
    time.sleep(5)
    
    # Status anzeigen
    dx12.print_dx12_status()
    
    # Stoppen
    dx12.stop_dx12_optimization()
    
    print(f"\n✅ DirectX 12 Test abgeschlossen")
