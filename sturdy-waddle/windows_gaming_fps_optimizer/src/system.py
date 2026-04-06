import ctypes
import json
import subprocess
import winreg
from pathlib import Path
import wmi


class SystemInfo:
    def __init__(self):
        self.wmi = wmi.WMI()
        self._cache = {}

    def _run(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.stdout.strip()
        except:
            return ""

    def cpu(self):
        if "cpu" in self._cache:
            return self._cache["cpu"]
        try:
            proc = self.wmi.Win32_Processor()[0]
            info = {
                "name": proc.Name.strip(),
                "cores": proc.NumberOfCores,
                "threads": proc.NumberOfLogicalProcessors,
                "base_clock": proc.MaxClockSpeed / 1000
            }
            self._cache["cpu"] = info
            return info
        except:
            return {"name": "Unknown", "cores": 0, "threads": 0, "base_clock": 0}

    def gpu(self):
        if "gpu" in self._cache:
            return self._cache["gpu"]
        try:
            gpus = self.wmi.Win32_VideoController()
            dedicated = [g for g in gpus if "Intel" not in g.Name and g.AdapterRAM > 0]
            if dedicated:
                gpu = dedicated[0]
            else:
                gpu = gpus[0]
            vram_mb = gpu.AdapterRAM // (1024 * 1024) if gpu.AdapterRAM else 0
            info = {
                "name": gpu.Name.strip(),
                "vram_mb": vram_mb,
                "driver_version": gpu.DriverVersion
            }
            self._cache["gpu"] = info
            return info
        except:
            return {"name": "Unknown", "vram_mb": 0, "driver_version": ""}

    def ram(self):
        if "ram" in self._cache:
            return self._cache["ram"]
        try:
            mem = self.wmi.Win32_ComputerSystem()[0]
            total_gb = int(mem.TotalPhysicalMemory) // (1024**3)
            info = {"total_gb": total_gb}
            self._cache["ram"] = info
            return info
        except:
            return {"total_gb": 0}

    def temperatures(self):
        temps = {"cpu": None, "gpu": None}
        try:
            import psutil
            if hasattr(psutil, "sensors_temperatures"):
                sensors = psutil.sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        if "coretemp" in name.lower() or "cpu" in name.lower():
                            if entries:
                                temps["cpu"] = entries[0].current
                        elif "gpu" in name.lower():
                            if entries:
                                temps["gpu"] = entries[0].current
        except:
            pass
        return temps

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def all(self):
        return {
            "cpu": self.cpu(),
            "gpu": self.gpu(),
            "ram": self.ram(),
            "temps": self.temperatures(),
            "admin": self.is_admin()
        }
