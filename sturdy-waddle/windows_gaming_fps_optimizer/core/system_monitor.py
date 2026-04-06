#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced System Monitor - Detaillierte Systemüberwachung
"""

import psutil
import time
import threading
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class SystemMonitor:
    def __init__(self, history_size=300):  # 5 Minuten bei 2s Intervall
        self.history_size = history_size
        self.monitoring = False
        self.monitor_thread = None
        
        # Historische Daten
        self.history = {
            "cpu_usage": deque(maxlen=history_size),
            "memory_usage": deque(maxlen=history_size),
            "gpu_usage": deque(maxlen=history_size),
            "temperature": deque(maxlen=history_size),
            "fps": deque(maxlen=history_size),
            "timestamps": deque(maxlen=history_size)
        }
        
        # System-Informationen
        self.system_info = self._get_system_info()
        
        # Alert thresholds
        self.thresholds = {
            "cpu_warning": 80,
            "cpu_critical": 95,
            "memory_warning": 85,
            "memory_critical": 95,
            "gpu_warning": 85,
            "gpu_critical": 95,
            "temp_warning": 75,
            "temp_critical": 85
        }
        
        # Performance alerts
        self.alerts = []
        
    def _get_system_info(self):
        """Sammelt detaillierte System-Informationen"""
        info = {
            "cpu": {
                "name": psutil.cpu_count(logical=False),
                "cores": psutil.cpu_count(logical=True),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "usage_per_core": psutil.cpu_percent(percpu=True)
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "swap": psutil.swap_memory()._asdict()
            },
            "disk": [],
            "network": psutil.net_io_counters()._asdict(),
            "boot_time": psutil.boot_time()
        }
        
        # Disk-Informationen
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info["disk"].append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free
                })
            except:
                pass
        
        # GPU-Informationen
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            info["gpu"] = []
            for gpu in gpus:
                info["gpu"].append({
                    "id": gpu.id,
                    "name": gpu.name,
                    "memory_total": gpu.memoryTotal,
                    "memory_used": gpu.memoryUsed,
                    "memory_free": gpu.memoryFree,
                    "driver": gpu.driver,
                    "temperature": gpu.temperature,
                    "load": gpu.load * 100
                })
        except:
            info["gpu"] = []
        
        return info
    
    def start_monitoring(self):
        """Startet System-Monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("📊 System Monitor gestartet")
    
    def stop_monitoring(self):
        """Stoppt System-Monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("⏹️ System Monitor gestoppt")
    
    def _monitor_loop(self):
        """Haupt-Monitoring-Schleife"""
        while self.monitoring:
            try:
                timestamp = datetime.now()
                
                # Metriken sammeln
                cpu_usage = psutil.cpu_percent()
                memory_usage = psutil.virtual_memory().percent
                gpu_usage, temp = self._get_gpu_metrics()
                
                # Historie aktualisieren
                self.history["cpu_usage"].append(cpu_usage)
                self.history["memory_usage"].append(memory_usage)
                self.history["gpu_usage"].append(gpu_usage)
                self.history["temperature"].append(temp)
                self.history["timestamps"].append(timestamp)
                
                # Alerts prüfen
                self._check_alerts(cpu_usage, memory_usage, gpu_usage, temp)
                
                # System-Info aktualisieren
                if len(self.history["timestamps"]) % 30 == 0:  # Alle 60 Sekunden
                    self.system_info = self._get_system_info()
                
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Monitor Fehler: {e}")
                time.sleep(5)
    
    def _get_gpu_metrics(self):
        """Holt GPU-Metriken"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return gpu.load * 100, gpu.temperature
        except:
            pass
        return 0, 0
    
    def _check_alerts(self, cpu, memory, gpu, temp):
        """Prüft auf Performance-Alerts"""
        current_time = datetime.now()
        
        # CPU Alerts
        if cpu >= self.thresholds["cpu_critical"]:
            self._add_alert("critical", "CPU", f"CPU-Auslastung kritisch: {cpu:.1f}%")
        elif cpu >= self.thresholds["cpu_warning"]:
            self._add_alert("warning", "CPU", f"CPU-Auslastung hoch: {cpu:.1f}%")
        
        # Memory Alerts
        if memory >= self.thresholds["memory_critical"]:
            self._add_alert("critical", "Memory", f"Speichernutzung kritisch: {memory:.1f}%")
        elif memory >= self.thresholds["memory_warning"]:
            self._add_alert("warning", "Memory", f"Speichernutzung hoch: {memory:.1f}%")
        
        # GPU Alerts
        if gpu >= self.thresholds["gpu_critical"]:
            self._add_alert("critical", "GPU", f"GPU-Auslastung kritisch: {gpu:.1f}%")
        elif gpu >= self.thresholds["gpu_warning"]:
            self._add_alert("warning", "GPU", f"GPU-Auslastung hoch: {gpu:.1f}%")
        
        # Temperature Alerts
        if temp >= self.thresholds["temp_critical"]:
            self._add_alert("critical", "Temperature", f"Temperatur kritisch: {temp:.1f}°C")
        elif temp >= self.thresholds["temp_warning"]:
            self._add_alert("warning", "Temperature", f"Temperatur hoch: {temp:.1f}°C")
        
        # Alte Alerts aufräumen
        self.alerts = [alert for alert in self.alerts 
                      if (current_time - alert["timestamp"]).seconds < 300]
    
    def _add_alert(self, level, component, message):
        """Fügt Alert hinzu"""
        # Verhindere Duplikate
        for alert in self.alerts:
            if alert["component"] == component and alert["level"] == level:
                return
        
        self.alerts.append({
            "level": level,
            "component": component,
            "message": message,
            "timestamp": datetime.now()
        })
        
        print(f"🚨 {level.upper()} - {component}: {message}")
    
    def get_current_metrics(self):
        """Gibt aktuelle Metriken zurück - holt LIVE Daten wenn History leer"""
        # Wenn History vorhanden, nutze diese
        if self.history["cpu_usage"]:
            return {
                "cpu_usage": self.history["cpu_usage"][-1],
                "memory_usage": self.history["memory_usage"][-1],
                "gpu_usage": self.history["gpu_usage"][-1],
                "temperature": self.history["temperature"][-1],
                "timestamp": self.history["timestamps"][-1]
            }
        
        # Sonst: LIVE Daten holen
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory_usage = psutil.virtual_memory().percent
            gpu_usage, temperature = self._get_gpu_metrics()
            
            return {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "gpu_usage": gpu_usage,
                "temperature": temperature,
                "timestamp": datetime.now()
            }
        except Exception as e:
            print(f"⚠️ Fehler beim Holen von Live-Metriken: {e}")
            return {
                "cpu_usage": 0,
                "memory_usage": 0,
                "gpu_usage": 0,
                "temperature": 0,
                "timestamp": datetime.now()
            }
    
    def get_performance_summary(self):
        """Gibt Performance-Zusammenfassung zurück - mit Live-Daten wenn History leer"""
        # Wenn History leer, hole Live-Daten
        if not self.history["cpu_usage"]:
            live_metrics = self.get_current_metrics()
            cpu_avg = live_metrics["cpu_usage"]
            memory_avg = live_metrics["memory_usage"]
            gpu_avg = live_metrics["gpu_usage"]
            temp_avg = live_metrics["temperature"]
        else:
            cpu_avg = np.mean(self.history["cpu_usage"])
            memory_avg = np.mean(self.history["memory_usage"])
            gpu_avg = np.mean(self.history["gpu_usage"])
            temp_avg = np.mean(self.history["temperature"])
        
        cpu_max = np.max(self.history["cpu_usage"]) if self.history["cpu_usage"] else cpu_avg
        memory_max = np.max(self.history["memory_usage"]) if self.history["memory_usage"] else memory_avg
        gpu_max = np.max(self.history["gpu_usage"]) if self.history["gpu_usage"] else gpu_avg
        temp_max = np.max(self.history["temperature"]) if self.history["temperature"] else temp_avg
        
        # Performance-Score berechnen
        performance_score = self._calculate_performance_score(
            cpu_avg, memory_avg, gpu_avg, temp_avg
        )
        
        return {
            "performance_score": performance_score,
            "cpu": {"average": cpu_avg, "peak": cpu_max},
            "memory": {"average": memory_avg, "peak": memory_max},
            "gpu": {"average": gpu_avg, "peak": gpu_max},
            "temperature": {"average": temp_avg, "peak": temp_max},
            "alerts_count": len(self.alerts),
            "status": self._get_status_level(performance_score)
        }
    
    def _calculate_performance_score(self, cpu_avg, memory_avg, gpu_avg, temp_avg):
        """Berechnet Performance-Score (0-100)"""
        # Je niedriger die Auslastung, desto besser der Score
        cpu_score = max(0, 100 - cpu_avg)
        memory_score = max(0, 100 - memory_avg)
        gpu_score = max(0, 100 - gpu_avg)
        
        # Temperatur-Score (niedriger ist besser)
        temp_score = max(0, 100 - (temp_avg - 30) * 2)  # 30°C = 100 Punkte
        
        # Gewichteter Durchschnitt
        weights = {"cpu": 0.3, "memory": 0.2, "gpu": 0.3, "temperature": 0.2}
        
        total_score = (
            cpu_score * weights["cpu"] +
            memory_score * weights["memory"] +
            gpu_score * weights["gpu"] +
            temp_score * weights["temperature"]
        )
        
        return round(total_score, 1)
    
    def _get_status_level(self, score):
        """Gibt Status-Level basierend auf Score zurück"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "moderate"
        elif score >= 20:
            return "poor"
        else:
            return "critical"
    
    def generate_performance_report(self):
        """Generiert detaillierten Performance-Report"""
        summary = self.get_performance_summary()
        current = self.get_current_metrics()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self.system_info,
            "current_metrics": current,
            "performance_summary": summary,
            "active_alerts": self.alerts,
            "recommendations": self._generate_recommendations(summary)
        }
        
        return report
    
    def _generate_recommendations(self, summary):
        """Generiert Optimierungsempfehlungen"""
        recommendations = []
        
        if summary["cpu"]["average"] > 80:
            recommendations.append({
                "type": "cpu",
                "priority": "high",
                "message": "CPU-Auslastung sehr hoch - Hintergrundprozesse beenden"
            })
        
        if summary["memory"]["average"] > 85:
            recommendations.append({
                "type": "memory",
                "priority": "high",
                "message": "Speichernutzung hoch - Speicherbereinigung durchführen"
            })
        
        if summary["temperature"]["peak"] > 80:
            recommendations.append({
                "type": "thermal",
                "priority": "critical",
                "message": "Temperatur zu hoch - Kühlung überprüfen"
            })
        
        if summary["performance_score"] < 50:
            recommendations.append({
                "type": "general",
                "priority": "medium",
                "message": "System-Performance niedrig - Optimierung empfohlen"
            })
        
        return recommendations
    
    def save_history_to_file(self, filename):
        """Speichert Historie in Datei"""
        data = {
            "history": {key: list(value) for key, value in self.history.items()},
            "system_info": self.system_info,
            "alerts": self.alerts
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"📁 Performance-Daten gespeichert: {filename}")
    
    def create_performance_graph(self, save_path=None):
        """Erstellt Performance-Graphen"""
        if not self.history["cpu_usage"]:
            print("❌ Keine Daten für Graphen verfügbar")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        timestamps = list(self.history["timestamps"])
        
        # CPU Usage
        ax1.plot(timestamps, list(self.history["cpu_usage"]), 'b-', label='CPU Usage')
        ax1.set_title('CPU Usage (%)')
        ax1.set_ylabel('Usage %')
        ax1.grid(True)
        ax1.legend()
        
        # Memory Usage
        ax2.plot(timestamps, list(self.history["memory_usage"]), 'g-', label='Memory Usage')
        ax2.set_title('Memory Usage (%)')
        ax2.set_ylabel('Usage %')
        ax2.grid(True)
        ax2.legend()
        
        # GPU Usage
        ax3.plot(timestamps, list(self.history["gpu_usage"]), 'r-', label='GPU Usage')
        ax3.set_title('GPU Usage (%)')
        ax3.set_ylabel('Usage %')
        ax3.grid(True)
        ax3.legend()
        
        # Temperature
        ax4.plot(timestamps, list(self.history["temperature"]), 'orange', label='Temperature')
        ax4.set_title('Temperature (°C)')
        ax4.set_ylabel('Temperature °C')
        ax4.grid(True)
        ax4.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Graph gespeichert: {save_path}")
        else:
            plt.show()
        
        plt.close()
