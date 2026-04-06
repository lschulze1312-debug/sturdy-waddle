#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Profiler - Detaillierte System-Informationen
"""

import psutil
import platform
import subprocess
import json
from datetime import datetime

class SystemProfiler:
    def __init__(self):
        self.system_specs = self.get_complete_system_info()
    
    def get_complete_system_info(self):
        """Sammelt komplette System-Informationen"""
        specs = {
            "timestamp": datetime.now().isoformat(),
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "gpu": self.get_gpu_info(),
            "storage": self.get_storage_info(),
            "network": self.get_network_info(),
            "bios": self.get_bios_info()
        }
        
        return specs
    
    def get_system_info(self):
        """Grundlegende System-Informationen"""
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "platform_release": platform.release(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python_version": platform.python_version()
        }
    
    def get_cpu_info(self):
        """Detaillierte CPU-Informationen"""
        cpu_info = {
            "name": "Unknown",
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "frequency_current": 0,
            "frequency_min": 0,
            "frequency_max": 0,
            "usage_percent": psutil.cpu_percent(interval=1),
            "usage_per_core": psutil.cpu_percent(percpu=True),
            "architecture": platform.architecture()[0]
        }
        
        # CPU-Frequenz
        freq = psutil.cpu_freq()
        if freq:
            cpu_info.update({
                "frequency_current": freq.current,
                "frequency_min": freq.min,
                "frequency_max": freq.max
            })
        
        # CPU-Name via PowerShell (Windows-spezifisch)
        try:
            result = subprocess.run(
                ["powershell", "Get-WmiObject -Class Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                cpu_data = json.loads(result.stdout.strip())
                if isinstance(cpu_data, list) and cpu_data:
                    cpu_info.update({
                        "name": cpu_data[0].get("Name", "Unknown"),
                        "cores_physical": cpu_data[0].get("NumberOfCores", cpu_info["cores_physical"]),
                        "cores_logical": cpu_data[0].get("NumberOfLogicalProcessors", cpu_info["cores_logical"]),
                        "frequency_max": cpu_data[0].get("MaxClockSpeed", cpu_info["frequency_max"])
                    })
        except:
            pass
        
        return cpu_info
    
    def get_memory_info(self):
        """Detaillierte Memory-Informationen"""
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        
        memory_info = {
            "total_gb": round(virtual_memory.total / (1024**3), 2),
            "available_gb": round(virtual_memory.available / (1024**3), 2),
            "used_gb": round(virtual_memory.used / (1024**3), 2),
            "free_gb": round(virtual_memory.free / (1024**3), 2),
            "usage_percent": virtual_memory.percent,
            "swap_total_gb": round(swap_memory.total / (1024**3), 2),
            "swap_used_gb": round(swap_memory.used / (1024**3), 2),
            "swap_free_gb": round(swap_memory.free / (1024**3), 2),
            "swap_usage_percent": swap_memory.percent
        }
        
        # System-spezifische Memory-Info
        try:
            result = subprocess.run(
                ["powershell", "Get-WmiObject -Class Win32_ComputerSystem | Select-Object TotalPhysicalMemory | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                sys_data = json.loads(result.stdout.strip())
                if isinstance(sys_data, list) and sys_data:
                    total_bytes = sys_data[0].get("TotalPhysicalMemory", 0)
                    memory_info["system_total_gb"] = round(total_bytes / (1024**3), 2)
        except:
            pass
        
        return memory_info
    
    def get_gpu_info(self):
        """Detaillierte GPU-Informationen"""
        gpu_info = []
        
        # GPUtil für dedizierte GPUs
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                gpu_info.append({
                    "name": gpu.name,
                    "memory_total_mb": gpu.memoryTotal,
                    "memory_used_mb": gpu.memoryUsed,
                    "memory_free_mb": gpu.memoryFree,
                    "memory_usage_percent": (gpu.memoryUsed / gpu.memoryTotal) * 100,
                    "load_percent": gpu.load * 100,
                    "temperature": gpu.temperature,
                    "driver_version": gpu.driver,
                    "uuid": gpu.uuid,
                    "type": "dedicated"
                })
        except:
            pass
        
        # Windows-spezifische GPU-Info via PowerShell
        try:
            result = subprocess.run(
                ["powershell", "Get-WmiObject -Class Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                gpu_data = json.loads(result.stdout.strip())
                if isinstance(gpu_data, list):
                    for gpu in gpu_data:
                        gpu_entry = {
                            "name": gpu.get("Name", "Unknown"),
                            "memory_total_mb": round(gpu.get("AdapterRAM", 0) / (1024**2), 0),
                            "driver_version": gpu.get("DriverVersion", "Unknown"),
                            "type": "integrated" if "Intel" in gpu.get("Name", "") or "Radeon Graphics" in gpu.get("Name", "") else "dedicated"
                        }
                        
                        # Prüfen ob GPU bereits in der Liste ist
                        if not any(g["name"] == gpu_entry["name"] for g in gpu_info):
                            gpu_info.append(gpu_entry)
        except:
            pass
        
        return gpu_info
    
    def get_storage_info(self):
        """Storage-Informationen"""
        storage_info = []
        
        # Disk-Partitions
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                storage_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "usage_percent": round((usage.used / usage.total) * 100, 2)
                })
            except:
                continue
        
        return storage_info
    
    def get_network_info(self):
        """Network-Informationen"""
        net_io = psutil.net_io_counters()
        net_addrs = psutil.net_if_addrs()
        net_stats = psutil.net_if_stats()
        
        network_info = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "interfaces": []
        }
        
        # Interface-Details
        for interface_name, addresses in net_addrs.items():
            interface_info = {
                "name": interface_name,
                "addresses": []
            }
            
            for addr in addresses:
                interface_info["addresses"].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            
            # Stats hinzufügen
            if interface_name in net_stats:
                stats = net_stats[interface_name]
                interface_info.update({
                    "is_up": stats.isup,
                    "speed": stats.speed,
                    "mtu": stats.mtu
                })
            
            network_info["interfaces"].append(interface_info)
        
        return network_info
    
    def get_bios_info(self):
        """BIOS/Motherboard-Informationen"""
        bios_info = {
            "manufacturer": "Unknown",
            "model": "Unknown",
            "bios_version": "Unknown",
            "bios_date": "Unknown"
        }
        
        try:
            # Computer System Info
            result = subprocess.run(
                ["powershell", "Get-WmiObject -Class Win32_ComputerSystem | Select-Object Manufacturer, Model | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                sys_data = json.loads(result.stdout.strip())
                if isinstance(sys_data, list) and sys_data:
                    bios_info.update({
                        "manufacturer": sys_data[0].get("Manufacturer", "Unknown"),
                        "model": sys_data[0].get("Model", "Unknown")
                    })
            
            # BIOS Info
            result = subprocess.run(
                ["powershell", "Get-WmiObject -Class Win32_BIOS | Select-Object SMBIOSBIOSVersion, ReleaseDate | ConvertTo-Json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                bios_data = json.loads(result.stdout.strip())
                if isinstance(bios_data, list) and bios_data:
                    bios_info.update({
                        "bios_version": bios_data[0].get("SMBIOSBIOSVersion", "Unknown"),
                        "bios_date": str(bios_data[0].get("ReleaseDate", "Unknown"))
                    })
        except:
            pass
        
        return bios_info
    
    def get_gaming_performance_score(self):
        """Berechnet Gaming-Performance-Score basierend auf Hardware"""
        cpu = self.system_specs["cpu"]
        memory = self.system_specs["memory"]
        gpu = self.system_specs["gpu"]
        
        # CPU-Score basierend auf Cores und Frequenz
        cpu_score = 0
        if "Ryzen 7" in cpu["name"] or "Core i7" in cpu["name"]:
            cpu_score = 75
        elif "Ryzen 5" in cpu["name"] or "Core i5" in cpu["name"]:
            cpu_score = 60
        elif "Ryzen 9" in cpu["name"] or "Core i9" in cpu["name"]:
            cpu_score = 90
        else:
            cpu_score = 45
        
        # Memory-Score
        memory_score = 0
        if memory["total_gb"] >= 32:
            memory_score = 90
        elif memory["total_gb"] >= 16:
            memory_score = 75
        elif memory["total_gb"] >= 8:
            memory_score = 50
        else:
            memory_score = 25
        
        # GPU-Score basierend auf GPU-Modell
        gpu_score = 0
        for gpu_entry in gpu:
            gpu_name = gpu_entry["name"].upper()
            if "RX 7600S" in gpu_name or "RTX 4060" in gpu_name:
                gpu_score = max(gpu_score, 70)
            elif "RX 7700S" in gpu_name or "RTX 4070" in gpu_name:
                gpu_score = max(gpu_score, 80)
            elif "RX 7800S" in gpu_name or "RTX 4080" in gpu_name:
                gpu_score = max(gpu_score, 90)
            elif "RX 7900S" in gpu_name or "RTX 4090" in gpu_name:
                gpu_score = max(gpu_score, 95)
            elif "RX 6600" in gpu_name or "RTX 3060" in gpu_name:
                gpu_score = max(gpu_score, 60)
            elif "RX 6500" in gpu_name or "RTX 3050" in gpu_name:
                gpu_score = max(gpu_score, 50)
        
        # Overall Score
        weights = {"cpu": 0.3, "memory": 0.2, "gpu": 0.5}
        overall_score = (cpu_score * weights["cpu"] + 
                        memory_score * weights["memory"] + 
                        gpu_score * weights["gpu"])
        
        return {
            "cpu_score": cpu_score,
            "memory_score": memory_score,
            "gpu_score": gpu_score,
            "overall_score": round(overall_score, 1),
            "category": self.get_performance_category(overall_score)
        }
    
    def get_performance_category(self, score):
        """Gibt Performance-Kategorie zurück"""
        if score >= 80:
            return "🔥 Extreme Gaming"
        elif score >= 60:
            return "🎮 High-End Gaming"
        elif score >= 40:
            return "👍 Mid-Range Gaming"
        elif score >= 25:
            return "⚡ Entry-Level Gaming"
        else:
            return "💻 Office/Browsing"
    
    def print_system_specs(self):
        """Gibt System-Spezifikationen aus"""
        specs = self.system_specs
        
        print("🖥️ SYSTEM SPEZIFIKATIONEN")
        print("="*60)
        print(f"Zeitpunkt: {specs['timestamp']}")
        
        # System Info
        print(f"\n💻 SYSTEM:")
        print(f"   Platform: {specs['system']['platform']} {specs['system']['platform_version']}")
        print(f"   Architecture: {specs['system']['architecture']}")
        print(f"   Python: {specs['system']['python_version']}")
        
        # CPU Info
        cpu = specs['cpu']
        print(f"\n🔥 CPU:")
        print(f"   Name: {cpu['name']}")
        print(f"   Cores: {cpu['cores_physical']} Physical / {cpu['cores_logical']} Logical")
        print(f"   Frequency: {cpu['frequency_current']:.0f} MHz (Max: {cpu['frequency_max']:.0f} MHz)")
        print(f"   Usage: {cpu['usage_percent']:.1f}%")
        
        # Memory Info
        memory = specs['memory']
        print(f"\n🧠 MEMORY:")
        print(f"   Total: {memory['total_gb']} GB")
        print(f"   Available: {memory['available_gb']} GB")
        print(f"   Used: {memory['used_gb']} GB ({memory['usage_percent']:.1f}%)")
        print(f"   Swap: {memory['swap_total_gb']} GB")
        
        # GPU Info
        print(f"\n🎮 GPU:")
        for i, gpu in enumerate(specs['gpu'], 1):
            print(f"   GPU {i}: {gpu['name']}")
            print(f"       Memory: {gpu['memory_total_mb']} MB")
            print(f"       Type: {gpu['type']}")
            if 'load_percent' in gpu:
                print(f"       Load: {gpu['load_percent']:.1f}%")
            if 'temperature' in gpu:
                print(f"       Temperature: {gpu['temperature']}°C")
        
        # Storage Info
        print(f"\n💾 STORAGE:")
        for storage in specs['storage']:
            print(f"   {storage['device']} ({storage['fstype']})")
            print(f"       Total: {storage['total_gb']} GB")
            print(f"       Used: {storage['used_gb']} GB ({storage['usage_percent']:.1f}%)")
        
        # BIOS Info
        bios = specs['bios']
        print(f"\n🔧 BIOS/MOTHERBOARD:")
        print(f"   Manufacturer: {bios['manufacturer']}")
        print(f"   Model: {bios['model']}")
        print(f"   BIOS Version: {bios['bios_version']}")
        
        # Gaming Performance Score
        score = self.get_gaming_performance_score()
        print(f"\n📊 GAMING PERFORMANCE SCORE:")
        print(f"   CPU Score: {score['cpu_score']}/100")
        print(f"   Memory Score: {score['memory_score']}/100")
        print(f"   GPU Score: {score['gpu_score']}/100")
        print(f"   Overall Score: {score['overall_score']}/100")
        print(f"   Category: {score['category']}")
    
    def save_specs_to_file(self, filename=None):
        """Speichert System-Spezifikationen in Datei"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_specs_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.system_specs, f, indent=2, default=str)
        
        print(f"📁 System-Spezifikationen gespeichert: {filename}")
        return filename

if __name__ == "__main__":
    profiler = SystemProfiler()
    profiler.print_system_specs()
    
    # Speichern
    profiler.save_specs_to_file()
