import ctypes
import json
import os
import subprocess
import sys
import time
import winreg
from pathlib import Path


class Optimizer:
    def __init__(self):
        self.config_path = Path("config.json")
        self.config = self._load_config()
        self.processes_to_kill = [
            "OneDrive.exe", "Teams.exe", "Discord.exe", "Spotify.exe",
            "Chrome.exe", "Firefox.exe", "Edge.exe", "Steam.exe",
            "EpicGamesLauncher.exe", "Origin.exe", "Battle.net.exe",
            "RiotClientServices.exe", "Overwolf.exe", "NVIDIA GeForce Experience.exe",
            "MSI Afterburner.exe", "WallpaperEngine.exe", "Rainmeter.exe"
        ]
        self.services_to_stop = [
            "WSearch", "SysMain", "DiagTrack", "dmwappushservice",
            "WMPNetworkSvc", "Fax", "MapsBroker", "TrkWks"
        ]

    def _load_config(self):
        defaults = {
            "aggressive": False,
            "thermal_limit": 85,
            "fps_target": 60,
            "auto_restore": True
        }
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    return {**defaults, **json.load(f)}
            except:
                pass
        return defaults

    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def _run(self, cmd, check=True):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, shell=True, check=check)
        except subprocess.CalledProcessError:
            return None

    def set_high_priority(self, pid=None):
        if pid is None:
            pid = os.getpid()
        try:
            handle = ctypes.windll.kernel32.OpenProcess(0x0200 | 0x0100, False, pid)
            ctypes.windll.kernel32.SetPriorityClass(handle, 0x00000080)
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        except:
            return False

    def kill_background_apps(self):
        killed = []
        for proc in self.processes_to_kill:
            result = self._run(f'taskkill /F /IM "{proc}" 2>nul', check=False)
            if result and result.returncode == 0:
                killed.append(proc)
        return killed

    def stop_services(self):
        stopped = []
        for svc in self.services_to_stop:
            result = self._run(f'net stop "{svc}" 2>nul', check=False)
            if result and result.returncode == 0:
                stopped.append(svc)
        return stopped

    def optimize_power_plan(self):
        try:
            self._run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', check=False)
            self._run('powercfg /change monitor-timeout-ac 0')
            self._run('powercfg /change monitor-timeout-dc 0')
            self._run('powercfg /change disk-timeout-ac 0')
            self._run('powercfg /change disk-timeout-dc 0')
            self._run('powercfg /change standby-timeout-ac 0')
            self._run('powercfg /change standby-timeout-dc 0')
            return True
        except:
            return False

    def disable_visual_effects(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            return True
        except:
            return False

    def clear_standby_list(self):
        try:
            result = self._run('powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName(\"System.Runtime.InteropServices\") | Out-Null; $mem = Add-Type -MemberDefinition \"[DllImport(\"kernel32.dll\")] public static extern bool SetProcessWorkingSetSize(IntPtr h, int min, int max);\" -Name ""Memory"" -PassThru; $mem::SetProcessWorkingSetSize([System.Diagnostics.Process]::GetCurrentProcess().Handle, -1, -1)"', check=False)
            return result is not None
        except:
            return False

    def optimize_gpu(self):
        tweaks = []
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            tweaks.append("hardware_scheduling")
        except:
            pass

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\DirectX\UserGpuPreferences",
                0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "GpuPreference", 0, winreg.REG_SZ, "2;0")
            winreg.CloseKey(key)
            tweaks.append("gpu_preference")
        except:
            pass

        return tweaks

    def optimize_full(self):
        results = {
            "priority_set": self.set_high_priority(),
            "apps_killed": self.kill_background_apps(),
            "services_stopped": self.stop_services(),
            "power_optimized": self.optimize_power_plan(),
            "visual_effects_disabled": self.disable_visual_effects(),
            "memory_cleared": self.clear_standby_list(),
            "gpu_tweaks": self.optimize_gpu()
        }
        return results

    def restore(self):
        for proc in self.processes_to_kill:
            self._run(f'start "" "{proc}" 2>nul', check=False)
        for svc in self.services_to_stop:
            self._run(f'net start "{svc}" 2>nul', check=False)
        self._run('powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e', check=False)
