#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-Time Performance Optimizer - Alternative zu Overclocking
"""

import psutil
import time
import threading
import json
from datetime import datetime
import subprocess
import win32api
import win32con
import win32process

class RealTimeOptimizer:
    def __init__(self):
        self.running = False
        self.monitoring_thread = None
        self.optimization_level = "balanced"
        self.target_fps = 60
        self.current_game = None
        
        # Performance thresholds
        self.thresholds = {
            "cpu_usage": 80,
            "memory_usage": 85,
            "gpu_usage": 90,
            "temperature": 75
        }
        
        # Optimization settings
        self.optimization_profiles = {
            "silent": {
                "cpu_priority": "normal",
                "gpu_power_limit": 60,
                "background_processes": "aggressive",
                "power_plan": "power_saver"
            },
            "balanced": {
                "cpu_priority": "above_normal",
                "gpu_power_limit": 80,
                "background_processes": "moderate",
                "power_plan": "balanced"
            },
            "performance": {
                "cpu_priority": "high",
                "gpu_power_limit": 100,
                "background_processes": "minimal",
                "power_plan": "high_performance"
            }
        }
        
        self.system_metrics = {
            "cpu_usage": 0,
            "memory_usage": 0,
            "gpu_usage": 0,
            "temperature": 0,
            "active_processes": []
        }
        
    def start_monitoring(self):
        """Startet Echtzeit-Überwachung"""
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitoring_thread.start()
            print("🚀 Real-Time Optimizer gestartet")
    
    def stop_monitoring(self):
        """Stoppt Echtzeit-Überwachung"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("⏹️ Real-Time Optimizer gestoppt")
    
    def _monitor_loop(self):
        """Haupt-Überwachungsschleife"""
        while self.running:
            try:
                # System-Metriken sammeln
                self._collect_metrics()
                
                # Optimierungsentscheidungen treffen
                self._make_optimization_decisions()
                
                # Kurze Pause
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Monitoring Fehler: {e}")
                time.sleep(5)
    
    def _collect_metrics(self):
        """Sammelt System-Metriken"""
        # CPU-Auslastung
        self.system_metrics["cpu_usage"] = psutil.cpu_percent(interval=1)
        
        # Memory-Auslastung
        memory = psutil.virtual_memory()
        self.system_metrics["memory_usage"] = memory.percent
        
        # GPU-Auslastung (wenn verfügbar)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                self.system_metrics["gpu_usage"] = gpu.load * 100
                self.system_metrics["temperature"] = gpu.temperature
        except:
            self.system_metrics["gpu_usage"] = 0
            self.system_metrics["temperature"] = 0
        
        # Aktive Prozesse
        self.system_metrics["active_processes"] = self._get_active_processes()
    
    def _get_active_processes(self):
        """Holt Liste aktiver Prozesse"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if proc.info['cpu_percent'] > 1 or proc.info['memory_percent'] > 1:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': proc.info['cpu_percent'],
                        'memory': proc.info['memory_percent']
                    })
            except:
                continue
        
        # Sortieren nach CPU-Auslastung
        processes.sort(key=lambda x: x['cpu'], reverse=True)
        return processes[:10]  # Top 10 Prozesse
    
    def _make_optimization_decisions(self):
        """Trifft Optimierungsentscheidungen basierend auf Metriken"""
        metrics = self.system_metrics
        
        # Gaming-Erkennung
        detected_game = self._detect_running_game()
        if detected_game != self.current_game:
            self.current_game = detected_game
            if detected_game:
                print(f"🎮 Game erkannt: {detected_game}")
                self._apply_gaming_optimizations(detected_game)
            else:
                print("💻 Kein Game aktiv - Normalmodus")
                self._apply_normal_optimizations()
        
        # Dynamische Anpassung basierend auf Auslastung
        self._adjust_performance_dynamically(metrics)
    
    def _detect_running_game(self):
        """Erkennt laufende Games"""
        known_games = [
            "csgo.exe", "valorant.exe", "fortnite.exe", "apex.exe",
            "cod.exe", "battlefield.exe", "cyberpunk2077.exe",
            "witcher3.exe", "eldenring.exe", "forzahorizon5.exe"
        ]
        
        for proc in self.system_metrics["active_processes"]:
            proc_name = proc["name"].lower()
            for game in known_games:
                if game in proc_name:
                    return proc["name"]
        
        return None
    
    def _apply_gaming_optimizations(self, game_name):
        """Wendet Gaming-Optimierungen an"""
        print(f"🎯 Gaming-Optimierungen für {game_name}")
        
        # Game-spezifische Priorität setzen
        for proc in self.system_metrics["active_processes"]:
            if proc["name"] == game_name:
                try:
                    # Prozess-Priorität erhöhen
                    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc["pid"])
                    win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
                    win32api.CloseHandle(handle)
                    print(f"⚡ {game_name} Priorität erhöht")
                except:
                    pass
                break
        
        # Hintergrundprozesse optimieren
        self._optimize_background_processes("minimal")
        
        # Windows Power Plan anpassen
        self._set_power_plan("high_performance")
    
    def _apply_normal_optimizations(self):
        """Wendet normale Optimierungen an"""
        # Prozess-Prioritäten normalisieren
        self._normalize_process_priorities()
        
        # Hintergrundprozesse moderat optimieren
        self._optimize_background_processes("moderate")
        
        # Power Plan zurücksetzen
        self._set_power_plan("balanced")
    
    def _adjust_performance_dynamically(self, metrics):
        """Passt Performance dynamisch an"""
        # CPU-Überhitzungsschutz
        if metrics["temperature"] > self.thresholds["temperature"]:
            print("🌡️ Hohe Temperatur erkannt - Performance reduzieren")
            self._apply_thermal_throttling()
        
        # Memory-Optimierung bei hoher Verbrauch
        if metrics["memory_usage"] > self.thresholds["memory_usage"]:
            print("🧠 Hoher Memory-Verbrauch - Optimiere Speicher")
            self._optimize_memory_usage()
    
    def _optimize_background_processes(self, level):
        """Optimiert Hintergrundprozesse"""
        background_processes = [
            "teams.exe", "discord.exe", "slack.exe", "chrome.exe",
            "firefox.exe", "edge.exe", "spotify.exe", "steam.exe"
        ]
        
        for proc in self.system_metrics["active_processes"]:
            proc_name = proc["name"].lower()
            
            # Hintergrundprozesse mit niedrigerer Priorität
            for bg_proc in background_processes:
                if bg_proc in proc_name and level == "minimal":
                    try:
                        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc["pid"])
                        win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
                        win32api.CloseHandle(handle)
                    except:
                        pass
    
    def _normalize_process_priorities(self):
        """Normalisiert Prozess-Prioritäten"""
        for proc in self.system_metrics["active_processes"]:
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc["pid"])
                win32process.SetPriorityClass(handle, win32process.NORMAL_PRIORITY_CLASS)
                win32api.CloseHandle(handle)
            except:
                pass
    
    def _set_power_plan(self, plan_name):
        """Setzt Windows Power Plan"""
        try:
            if plan_name == "high_performance":
                subprocess.run(["powercfg", "/setactive", "SCHEME_MIN"], check=True, capture_output=True)
            elif plan_name == "balanced":
                subprocess.run(["powercfg", "/setactive", "SCHEME_BALANCED"], check=True, capture_output=True)
            elif plan_name == "power_saver":
                subprocess.run(["powercfg", "/setactive", "SCHEME_MAX"], check=True, capture_output=True)
            
            print(f"⚡ Power Plan: {plan_name}")
        except:
            pass
    
    def _apply_thermal_throttling(self):
        """Wendet Thermal Throttling an"""
        # CPU-Last reduzieren durch Prioritätsanpassung
        for proc in self.system_metrics["active_processes"]:
            if proc["cpu"] > 50 and proc["name"] != self.current_game:
                try:
                    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, proc["pid"])
                    win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
                    win32api.CloseHandle(handle)
                except:
                    pass
    
    def _optimize_memory_usage(self):
        """Optimiert Speichernutzung"""
        try:
            # Windows Memory Cleanup
            subprocess.run(["powershell", "-command", "Clear-Content", "-Path", "env:TEMP"], 
                         check=True, capture_output=True)
            
            # Speicherbereinigung durch Systemaufruf
            import ctypes
            ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
            
        except:
            pass
    
    def get_performance_report(self):
        """Gibt Performance-Report zurück"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.system_metrics,
            "current_game": self.current_game,
            "optimization_level": self.optimization_level,
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self):
        """Generiert Optimierungsempfehlungen"""
        recommendations = []
        metrics = self.system_metrics
        
        if metrics["cpu_usage"] > 85:
            recommendations.append("CPU-Auslastung hoch - Hintergrundprozesse beenden")
        
        if metrics["memory_usage"] > 85:
            recommendations.append("Speicher voll - Speicherbereinigung empfohlen")
        
        if metrics["temperature"] > 75:
            recommendations.append("Temperatur hoch - Kühlung überprüfen")
        
        if not self.current_game and metrics["cpu_usage"] < 20:
            recommendations.append("System im Leerlauf - Power Saver Modus möglich")
        
        return recommendations
    
    def set_optimization_level(self, level):
        """Setzt Optimierungslevel"""
        if level in self.optimization_profiles:
            self.optimization_level = level
            print(f"⚙️ Optimierungslevel: {level}")
            
            # Profilspezifische Einstellungen anwenden
            profile = self.optimization_profiles[level]
            self._set_power_plan(profile["power_plan"])
