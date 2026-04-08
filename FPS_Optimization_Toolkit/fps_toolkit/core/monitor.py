import logging
import psutil
import ctypes
from typing import Dict, Optional, List
from dataclasses import dataclass

# Lazy import für WMI - verhindert Crash beim Modul-Import
wmi = None
try:
    import wmi
except Exception:
    pass  # WMI nicht verfügbar, wird in SystemMonitor abgefangen

logger = logging.getLogger(__name__)


@dataclass
class CPUInfo:
    name: str
    cores: int
    threads: int
    base_clock: float
    usage: float


@dataclass
class GPUInfo:
    name: str
    vram_mb: int
    driver_version: str
    usage: Optional[float] = None


@dataclass
class RAMInfo:
    total_gb: int
    available_gb: float
    usage_percent: float


@dataclass
class Temps:
    cpu: Optional[float] = None
    gpu: Optional[float] = None


class SystemMonitor:
    """Hardware-Informationen und Monitoring"""
    
    def __init__(self):
        self._wmi = None
        if wmi is not None:
            try:
                self._wmi = wmi.WMI()
            except Exception:
                pass  # WMI nicht verfügbar, Monitoring läuft eingeschränkt
        self._cache = {}

    def get_cpu_info(self) -> CPUInfo:
        try:
            if self._wmi:
                processors = self._wmi.Win32_Processor()
                if not processors:
                    return CPUInfo(name="No CPU found", cores=0, threads=0, base_clock=0, usage=0)
                proc = processors[0]
                usage = psutil.cpu_percent(interval=0.1)
                return CPUInfo(
                    name=proc.Name.strip() if hasattr(proc, 'Name') else "Unknown CPU",
                    cores=proc.NumberOfCores if hasattr(proc, 'NumberOfCores') else 0,
                    threads=proc.NumberOfLogicalProcessors if hasattr(proc, 'NumberOfLogicalProcessors') else 0,
                    base_clock=proc.MaxClockSpeed / 1000 if hasattr(proc, 'MaxClockSpeed') else 0,
                    usage=usage
                )
        except Exception:
            pass
        
        return CPUInfo(name="Unknown", cores=0, threads=0, base_clock=0, usage=0)

    def get_gpu_info(self) -> GPUInfo:
        try:
            if self._wmi:
                gpus = self._wmi.Win32_VideoController()
                if not gpus:
                    return GPUInfo(name="No GPU found", vram_mb=0, driver_version="Unknown")
                dedicated = [g for g in gpus if g.AdapterRAM and g.AdapterRAM > 0]
                gpu = dedicated[0] if dedicated else gpus[0]
                
                vram_mb = gpu.AdapterRAM // (1024 * 1024) if gpu.AdapterRAM else 0
                
                return GPUInfo(
                    name=gpu.Name.strip() if hasattr(gpu, 'Name') else "Unknown GPU",
                    vram_mb=vram_mb,
                    driver_version=gpu.DriverVersion if hasattr(gpu, 'DriverVersion') else "Unknown"
                )
        except Exception:
            pass
        
        return GPUInfo(name="Unknown", vram_mb=0, driver_version="Unknown")

    def get_ram_info(self) -> RAMInfo:
        try:
            mem = psutil.virtual_memory()
            return RAMInfo(
                total_gb=int(mem.total / (1024**3)),
                available_gb=round(mem.available / (1024**3), 1),
                usage_percent=mem.percent
            )
        except Exception:
            return RAMInfo(total_gb=0, available_gb=0, usage_percent=0)

    def get_temps(self) -> Temps:
        temps = Temps()
        
        try:
            if hasattr(psutil, "sensors_temperatures"):
                sensors = psutil.sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        if any(x in name.lower() for x in ["coretemp", "cpu", "k10temp", "zenpower"]):
                            if entries and len(entries) > 0:
                                temps.cpu = entries[0].current
                        elif "gpu" in name.lower():
                            if entries and len(entries) > 0:
                                temps.gpu = entries[0].current
        except Exception:
            pass
        
        return temps

    def get_disk_usage(self) -> Dict[str, float]:
        disks = {}
        try:
            for part in psutil.disk_partitions():
                if hasattr(part, 'opts') and ('fixed' in part.opts or 'rw' in part.opts):
                    try:
                        usage = psutil.disk_usage(part.mountpoint)
                        disks[part.device] = round(usage.percent, 1)
                    except (PermissionError, OSError):
                        pass  # Skip inaccessible drives
        except Exception:
            pass
        return disks

    def get_network_stats(self) -> Dict:
        try:
            net = psutil.net_io_counters()
            if net:
                return {
                    "sent_mb": round(net.bytes_sent / (1024*1024), 1),
                    "recv_mb": round(net.bytes_recv / (1024*1024), 1)
                }
        except Exception:
            pass
        return {"sent_mb": 0, "recv_mb": 0}

    def get_all_info(self) -> Dict:
        return {
            "cpu": self.get_cpu_info(),
            "gpu": self.get_gpu_info(),
            "ram": self.get_ram_info(),
            "temps": self.get_temps(),
            "disks": self.get_disk_usage(),
            "network": self.get_network_stats()
        }

    def is_admin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
