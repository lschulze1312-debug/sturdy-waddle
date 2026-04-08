#!/usr/bin/env python3
"""
FPS Optimization Toolkit - Core Optimizer Module
Professionelle Version mit allen Stabilitäts-Fixes
"""

import ctypes
import json
import logging
import os
import re
import subprocess
import sys
import time
import winreg
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import threading

# =============================================================================
# LOGGING
# =============================================================================

def setup_logging() -> logging.Logger:
    """Zentrale Logging-Konfiguration mit sofortigem Flush"""
    # Entferne existierende Handler
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=logging.DEBUG,  # DEBUG fuer mehr Details
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('fps_optimizer.log', encoding='utf-8', mode='w'),  # 'w' = overwrite
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Python 3.8+: Erzwinge Neukonfiguration
    )
    
    # Sofortiger Test-Eintrag
    log = logging.getLogger(__name__)
    log.info("=" * 60)
    log.info("LOGGING INITIALIZED - FPS Optimization Toolkit Starting")
    log.info("=" * 60)
    
    # Force flush
    for handler in log.handlers:
        if hasattr(handler, 'flush'):
            handler.flush()
    
    return log

logger = setup_logging()

# =============================================================================
# KONSTANTEN
# =============================================================================

class PowerPlanUUIDs:
    """Power Plan UUIDs"""
    HIGH_PERFORMANCE = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"
    POWER_SAVER = "a1841308-3541-4fab-bc81-f71556f20b4a"


class ValidationPatterns:
    """Regex-Patterns fuer Input-Validierung"""
    # Prozessnamen: Erlaubt Leerzeichen fuer Namen wie "NVIDIA GeForce Experience.exe"
    PROCESS_NAME = re.compile(r'^[a-zA-Z0-9._\- ]+\.exe$', re.IGNORECASE)
    SERVICE_NAME = re.compile(r'^[a-zA-Z0-9_]+$')
    REGISTRY_PATH = re.compile(r'^[A-Za-z0-9_\\.\- ]+$')


class ProcessLists:
    """Hardcodierte Listen"""
    TO_KILL = [
        "OneDrive.exe", "Teams.exe", "Discord.exe", "Spotify.exe",
        "Chrome.exe", "Firefox.exe", "Edge.exe", "Steam.exe",
        "EpicGamesLauncher.exe", "Origin.exe", "Battle.net.exe",
        "RiotClientServices.exe", "Overwolf.exe",
        "NVIDIA GeForce Experience.exe", "MSI Afterburner.exe",
        "Wallpaper32.exe", "Rainmeter.exe", "MSIAfterburner.exe"
    ]
    
    TO_STOP = [
        "WSearch", "SysMain", "DiagTrack", "dmwappushservice",
        "WMPNetworkSvc", "Fax", "MapsBroker", "TrkWks",
        "WbioSrvc", "icssvc", "PhoneSvc"
    ]


class RegistryKeys:
    """Registry-Pfade"""
    GRAPHICS_DRIVERS = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
    GPU_PREFERENCES = r"Software\Microsoft\DirectX\UserGpuPreferences"
    PRIORITY_CONTROL = r"SYSTEM\CurrentControlSet\Control\PriorityControl"
    VISUAL_EFFECTS = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
    DESKTOP = r"Control Panel\Desktop"
    GAME_DVR = r"Software\Microsoft\Windows\CurrentVersion\GameDVR"
    GAME_DVR_POLICY = r"SOFTWARE\Policies\Microsoft\Windows\GameDVR"
    GAME_CONFIG_STORE = r"System\GameConfigStore"
    TCPIP_PARAMETERS = r"SYSTEM\CurrentControlSet\Services\TcpIp\Parameters"
    DEFENDER_RT_PROTECTION = r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection"


# =============================================================================
# DATENKLASSEN
# =============================================================================

@dataclass
class CommandResult:
    """Ergebnis eines Befehls"""
    success: bool
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0
    error_message: str = ""


@dataclass
class RegistryEntry:
    """Registry-Eintrag"""
    root: int
    path: str
    name: str
    value: Any
    value_type: int
    
    def validate(self) -> bool:
        """Validiert den Eintrag"""
        if not ValidationPatterns.REGISTRY_PATH.match(self.path):
            return False
        if not ValidationPatterns.REGISTRY_PATH.match(self.name):
            return False
        return True


@dataclass
class OptimizationResult:
    """Aggregiert alle Optimierungsergebnisse"""
    apps_killed: List[str] = field(default_factory=list)
    services_stopped: List[str] = field(default_factory=list)
    gpu_tweaks: List[str] = field(default_factory=list)
    power_optimized: bool = False
    priority_set: bool = False
    visual_effects_disabled: bool = False
    network_optimized: bool = False
    defender_disabled: bool = False
    superfetch_disabled: bool = False
    game_dvr_disabled: bool = False
    fullscreen_optimized: bool = False
    qos_optimized: bool = False
    timer_optimized: bool = False
    memory_cleared: bool = False
    errors: List[str] = field(default_factory=list)


@dataclass
class BackupState:
    """Backup-Zustand"""
    killed_processes: List[str] = field(default_factory=list)
    stopped_services: List[str] = field(default_factory=list)
    registry_backup: List[Dict] = field(default_factory=list)


# =============================================================================
# ABSTRAKTIONEN
# =============================================================================

class RegistryManager:
    """Zentrale Registry-Abstraktion mit Thread-Safety"""
    
    def __init__(self):
        self.backup_log: List[Dict] = []
        self._lock = threading.Lock()
    
    def set_value(self, entry: RegistryEntry, backup_first: bool = True) -> bool:
        """Setzt einen Registry-Wert mit automatischem Backup - THREAD-SAFE"""
        if not entry.validate():
            logger.error(f"Invalid registry entry: {entry}")
            return False
        
        # FIX: Lock für gesamte Operation (Backup + Write)
        with self._lock:
            if backup_first:
                self._backup_value(entry.root, entry.path, entry.name)
            
            try:
                with winreg.CreateKey(entry.root, entry.path) as key:
                    winreg.SetValueEx(key, entry.name, 0, entry.value_type, entry.value)
                logger.debug(f"Registry set: {entry.path}\\{entry.name}")
                return True
            except PermissionError:
                logger.error(f"Permission denied writing {entry.name}")
                return False
            except OSError as e:
                logger.error(f"OS error writing {entry.name}: {e}")
                return False
    
    def get_value(self, root: int, path: str, name: str) -> Optional[Tuple[Any, int]]:
        """Liest einen Registry-Wert sicher"""
        try:
            with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
                value, value_type = winreg.QueryValueEx(key, name)
                return value, value_type
        except (FileNotFoundError, PermissionError, OSError):
            return None
    
    def _backup_value(self, root: int, path: str, name: str) -> None:
        """Sichert einen Wert vor Aenderung - wird nur innerhalb Lock aufgerufen"""
        existing = self.get_value(root, path, name)
        # Annahme: Aufrufer hält self._lock
        self.backup_log.append({
            'root': root, 'path': path, 'name': name,
            'value': existing[0] if existing else None,
            'type': existing[1] if existing else None
        })
    
    def restore_all(self) -> Tuple[int, int]:
        """Stellt alle gesicherten Werte wieder her - überspringt None-Werte"""
        success = 0
        errors = 0
        
        with self._lock:
            for backup in reversed(self.backup_log):
                try:
                    # FIX: Überspringe Werte die vorher nicht existierten (None)
                    if backup['value'] is None:
                        success += 1  # Zählt als Erfolg (nichts zu tun)
                        continue
                    with winreg.OpenKey(backup['root'], backup['path'], 0, winreg.KEY_WRITE) as key:
                        winreg.SetValueEx(key, backup['name'], 0, backup['type'], backup['value'])
                    success += 1
                except (PermissionError, OSError):
                    errors += 1
            
            self.backup_log.clear()
        
        return success, errors
    
    def clear_backup_log(self) -> None:
        """Thread-safe clearing of backup log"""
        with self._lock:
            self.backup_log.clear()
    
    def get_backup_log_copy(self) -> List[Dict]:
        """Thread-safe copy of backup log"""
        with self._lock:
            return self.backup_log.copy()


class CommandExecutor:
    """Zentrale Subprocess-Abstraktion mit Timeout"""
    
    @staticmethod
    def execute(
        args: List[str],
        check: bool = False,
        capture_output: bool = True,
        silent: bool = False,
        timeout: int = 10
    ) -> CommandResult:
        """Fuehrt einen Befehl sicher aus mit Timeout"""
        if not args:
            return CommandResult(False, error_message="Empty command")
        
        # Fix: capture_output=True ist aequivalent zu stdout=PIPE, stderr=PIPE
        # Wir koennen NICHT beides gleichzeitig verwenden!
        try:
            if capture_output:
                # Standard: capture beide streams
                result = subprocess.run(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE if not silent else subprocess.DEVNULL,
                    text=True,
                    shell=False,
                    check=check,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=timeout
                )
            else:
                # Kein capture - nur Ausfuehren
                result = subprocess.run(
                    args,
                    shell=False,
                    check=check,
                    timeout=timeout
                )
            
            success = result.returncode == 0
            return CommandResult(
                success=success,
                stdout=result.stdout if capture_output else "",
                stderr=result.stderr if capture_output else "",
                returncode=result.returncode
            )
            
        except subprocess.TimeoutExpired:
            logger.warning(f"Command timed out: {' '.join(args)}")
            return CommandResult(False, error_message=f"Timeout after {timeout}s")
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            logger.error(f"Command error: {e}")
            return CommandResult(False, error_message=str(e))
    
    @classmethod
    def execute_batch(cls, commands: List[List[str]], continue_on_error: bool = True) -> Tuple[int, int, List[str]]:
        """Fuehrt mehrere Befehle aus"""
        success = 0
        errors = []
        
        for cmd in commands:
            result = cls.execute(cmd)
            if result.success:
                success += 1
            else:
                errors.append(f"{' '.join(cmd)}: {result.error_message}")
                if not continue_on_error:
                    break
        
        return success, len(commands), errors


class ProcessManager:
    """Prozess-Operationen mit crash-sicherer Validierung"""
    
    def __init__(self, process_list: Optional[List[str]] = None):
        self.process_list = process_list or ProcessLists.TO_KILL
        self._validate_list()
        self.killed: List[str] = []
    
    def _validate_list(self) -> None:
        """Validiert Prozessnamen - entfernt ungueltige, loggt Warnungen"""
        valid = []
        for proc in self.process_list:
            if ValidationPatterns.PROCESS_NAME.match(proc):
                valid.append(proc)
            else:
                logger.warning(f"Ungueltiger Prozessname uebersprungen: '{proc}'")
        
        if len(valid) < len(self.process_list):
            logger.info(f"{len(self.process_list) - len(valid)} ungueltige Prozesse entfernt")
        
        self.process_list = valid if valid else ["OneDrive.exe", "Teams.exe", "Chrome.exe"]
    
    def kill_all(self) -> List[str]:
        """Beendet alle konfigurierten Prozesse mit detailliertem Logging"""
        self.killed.clear()
        logger.info(f"Starting to kill {len(self.process_list)} processes...")
        
        for i, proc in enumerate(self.process_list, 1):
            logger.info(f"[{i}/{len(self.process_list)}] Killing {proc}...")
            try:
                # /F = Force, /IM = Image Name, /T = Terminate Tree
                result = CommandExecutor.execute(['taskkill', '/F', '/IM', proc, '/T'], timeout=3)
                if result.success:
                    self.killed.append(proc)
                    logger.info(f"  ✓ Killed: {proc}")
                elif "not found" in result.stderr.lower() or result.returncode == 128:
                    logger.info(f"  - Not running: {proc}")
                elif result.error_message:
                    logger.warning(f"  ✗ Failed: {proc} - {result.error_message}")
                else:
                    logger.warning(f"  ✗ Failed: {proc} (exit code: {result.returncode})")
            except Exception as e:
                logger.error(f"  ✗ Exception killing {proc}: {e}")
        
        logger.info(f"Process killing complete. Killed {len(self.killed)}/{len(self.process_list)}")
        return self.killed
    
    def restart_all(self) -> List[str]:
        """Startet beendete Prozesse neu - korrigiert: cmd /c start"""
        restarted = []
        for proc in self.killed[:]:
            try:
                # FIX: cmd /c start verwenden statt direkt 'start'
                result = CommandExecutor.execute(['cmd', '/c', 'start', '', proc], silent=True, timeout=5)
                if result.success:
                    restarted.append(proc)
            except Exception as e:
                logger.warning(f"  Failed to restart {proc}: {e}")
        self.killed.clear()
        return restarted


class ServiceManager:
    """Service-Operationen mit crash-sicherer Validierung"""
    
    def __init__(self, service_list: Optional[List[str]] = None):
        self.service_list = service_list or ProcessLists.TO_STOP
        self._validate_list()
        self.stopped: List[str] = []
    
    def _validate_list(self) -> None:
        """Validiert Service-Namen"""
        valid = []
        for svc in self.service_list:
            if ValidationPatterns.SERVICE_NAME.match(svc):
                valid.append(svc)
            else:
                logger.warning(f"Ungueltiger Service-Name: '{svc}'")
        
        self.service_list = valid if valid else ["WSearch", "SysMain", "DiagTrack"]
    
    def stop_all(self) -> List[str]:
        """Stoppt alle Services mit detailliertem Logging"""
        self.stopped.clear()
        logger.info(f"Starting to stop {len(self.service_list)} services...")
        
        for i, svc in enumerate(self.service_list, 1):
            logger.info(f"[{i}/{len(self.service_list)}] Stopping {svc}...")
            try:
                result = CommandExecutor.execute(['net', 'stop', svc, '/y'], silent=True, timeout=5)
                if result.success:
                    self.stopped.append(svc)
                    logger.info(f"  ✓ Stopped: {svc}")
                elif result.error_message:
                    logger.info(f"  - Could not stop {svc}: {result.error_message}")
                else:
                    logger.info(f"  - Could not stop {svc}")
            except Exception as e:
                logger.error(f"  ✗ Exception stopping {svc}: {e}")
        
        logger.info(f"Service stopping complete. Stopped {len(self.stopped)}/{len(self.service_list)}")
        return self.stopped
    
    def start_all(self) -> List[str]:
        """Startet gestoppte Services wieder mit Error-Handling"""
        started = []
        for svc in self.stopped:
            try:
                result = CommandExecutor.execute(['net', 'start', svc], silent=True, timeout=8)
                if result.success:
                    started.append(svc)
                    logger.info(f"  ✓ Started: {svc}")
                else:
                    logger.warning(f"  ✗ Failed to start {svc}: {result.error_message}")
            except Exception as e:
                logger.error(f"  ✗ Exception starting {svc}: {e}")
        self.stopped.clear()
        return started
    
    def configure_startup(self, service: str, mode: str = "disabled") -> bool:
        """Konfiguriert Service-Startmodus mit Timeout"""
        result = CommandExecutor.execute(['sc', 'config', service, f'start={mode}'], silent=True, timeout=5)
        return result.success


# =============================================================================
# HAUPTKLASSE
# =============================================================================

class SystemOptimizer:
    """Hauptklasse fuer System-Optimierungen"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path("config.json")
        self.config = self._load_config()
        self.registry = RegistryManager()
        self.processes = ProcessManager()
        self.services = ServiceManager()
        self.backup = BackupState()
    
    def _load_config(self) -> Dict:
        """Laedt Konfiguration mit Defaults und Typ-Validierung"""
        defaults = {
            "aggressive": False,
            "thermal_limit": 85,
            "fps_target": 60,
            "auto_restore": True
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Nur bekannte Keys mit korrektem Typ übernehmen
                    result = defaults.copy()
                    for key, value in config.items():
                        if key in defaults:
                            expected_type = type(defaults[key])
                            if isinstance(value, expected_type):
                                result[key] = value
                            else:
                                logger.warning(f"Config type mismatch for {key}: expected {expected_type.__name__}, got {type(value).__name__}")
                    return result
            except (json.JSONDecodeError, PermissionError, OSError) as e:
                logger.error(f"Config load error: {e}")
        
        return defaults
    
    def set_high_priority(self, pid: Optional[int] = None) -> bool:
        """Setzt Prozess-Prioritaet auf High"""
        pid = pid or os.getpid()
        try:
            handle = ctypes.windll.kernel32.OpenProcess(0x0200 | 0x0100, False, pid)
            if not handle:
                return False
            result = ctypes.windll.kernel32.SetPriorityClass(handle, 0x00000080)
            ctypes.windll.kernel32.CloseHandle(handle)
            return bool(result)
        except (AttributeError, OSError):
            return False
    
    def optimize_power_plan(self) -> bool:
        """Optimiert Power-Plan"""
        target = PowerPlanUUIDs.HIGH_PERFORMANCE if self.config.get("aggressive") else PowerPlanUUIDs.BALANCED
        
        commands = [
            ['powercfg', '/setactive', target],
            ['powercfg', '/change', 'monitor-timeout-ac', '0'],
            ['powercfg', '/change', 'disk-timeout-ac', '0'],
            ['powercfg', '/change', 'standby-timeout-ac', '0']
        ]
        
        success, total, _ = CommandExecutor.execute_batch(commands)
        return success == total
    
    def disable_visual_effects(self) -> bool:
        """Deaktiviert visuelle Effekte"""
        entries = [
            RegistryEntry(winreg.HKEY_CURRENT_USER, RegistryKeys.VISUAL_EFFECTS, "VisualFXSetting", 2, winreg.REG_DWORD),
            RegistryEntry(winreg.HKEY_CURRENT_USER, RegistryKeys.DESKTOP, "UserPreferencesMask", 
                         bytes([0x90, 0x12, 0x03, 0x80, 0x10, 0x00, 0x00, 0x00]), winreg.REG_BINARY)
        ]
        return all(self.registry.set_value(e) for e in entries)
    
    def optimize_gpu(self) -> List[str]:
        """GPU-Optimierungen - FIX: Korrekte Registry-Wurzel fuer jeden Pfad"""
        tweaks = []
        entries = [
            # (Pfad, Name, Wert, Tweak-Name, Registry-Wurzel)
            (RegistryKeys.GRAPHICS_DRIVERS, "HwSchMode", 2, "hardware_scheduling", winreg.HKEY_LOCAL_MACHINE),
            (RegistryKeys.GPU_PREFERENCES, "GpuPreference", "2;0", "gpu_preference", winreg.HKEY_CURRENT_USER),
            (RegistryKeys.PRIORITY_CONTROL, "Win32PrioritySeparation", 38, "priority_separation", winreg.HKEY_LOCAL_MACHINE),
        ]
        
        # FIX: Explizite Registry-Wurzel statt String-Matching
        for path, name, value, tweak_name, root in entries:
            entry = RegistryEntry(
                root, path, name, value,
                winreg.REG_DWORD if isinstance(value, int) else winreg.REG_SZ
            )
            if self.registry.set_value(entry):
                tweaks.append(tweak_name)
        
        return tweaks
    
    def optimize_network(self) -> bool:
        """Netzwerk-Optimierungen"""
        commands = [
            ['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=disabled'],
            ['netsh', 'int', 'tcp', 'set', 'global', 'rss=enabled'],
            ['netsh', 'interface', 'tcp', 'set', 'heuristics', 'disabled'],
            ['netsh', 'interface', 'tcp', 'set', 'global', 'timestamps=disabled']
        ]
        success, total, _ = CommandExecutor.execute_batch(commands)
        return success > 0
    
    def disable_windows_defender_rt(self) -> bool:
        """Deaktiviert Windows Defender RT"""
        commands = [
            ['reg', 'add', f'HKLM\\{RegistryKeys.DEFENDER_RT_PROTECTION}', '/v', 'DisableRealtimeMonitoring', '/t', 'REG_DWORD', '/d', '1', '/f'],
            ['reg', 'add', f'HKLM\\{RegistryKeys.DEFENDER_RT_PROTECTION}', '/v', 'DisableBehaviorMonitoring', '/t', 'REG_DWORD', '/d', '1', '/f'],
            ['reg', 'add', f'HKLM\\{RegistryKeys.DEFENDER_RT_PROTECTION}', '/v', 'DisableOnAccessProtection', '/t', 'REG_DWORD', '/d', '1', '/f']
        ]
        success, total, _ = CommandExecutor.execute_batch(commands)
        return success > 0
    
    def disable_superfetch(self) -> bool:
        """Deaktiviert Superfetch - nur SysMain Service"""
        # FIX: Stoppe NUR SysMain, nicht alle Services
        result = CommandExecutor.execute(['net', 'stop', 'SysMain', '/y'], silent=True, timeout=5)
        return self.services.configure_startup("SysMain", "disabled")
    
    def disable_game_dvr(self) -> bool:
        """Deaktiviert Game DVR - FIX: Korrekte Registry-Wurzeln"""
        entries = [
            (winreg.HKEY_CURRENT_USER, RegistryKeys.GAME_DVR, "AppCaptureEnabled", 0),
            (winreg.HKEY_CURRENT_USER, RegistryKeys.GAME_DVR, "GameDVR_Enabled", 0),
            (winreg.HKEY_LOCAL_MACHINE, RegistryKeys.GAME_DVR_POLICY, "AllowGameDVR", 0),
            (winreg.HKEY_CURRENT_USER, RegistryKeys.GAME_CONFIG_STORE, "GameDVR_FSEBehavior", 2),
        ]
        
        success = 0
        # FIX: Explizite root statt Tuple-Entpackung mit falschem root
        for root, path, name, value in entries:
            entry = RegistryEntry(root, path, name, value, winreg.REG_DWORD)
            if self.registry.set_value(entry):
                success += 1
        
        return success > 0
    
    def disable_fullscreen_optimizations(self) -> bool:
        """Deaktiviert Fullscreen-Optimierungen"""
        entries = [
            RegistryEntry(winreg.HKEY_CURRENT_USER, RegistryKeys.GAME_CONFIG_STORE, "GameDVR_FSEBehaviorMode", 2, winreg.REG_DWORD),
            RegistryEntry(winreg.HKEY_CURRENT_USER, RegistryKeys.GAME_CONFIG_STORE, "GameDVR_DSEBehavior", 2, winreg.REG_DWORD)
        ]
        return all(self.registry.set_value(e) for e in entries)
    
    def set_qos_packet_priority(self) -> bool:
        """Deaktiviert QoS Packet Priority"""
        entry = RegistryEntry(winreg.HKEY_LOCAL_MACHINE, RegistryKeys.TCPIP_PARAMETERS, "DisableQoS", 1, winreg.REG_DWORD)
        return self.registry.set_value(entry)
    
    def optimize_timer_resolution(self) -> bool:
        """Optimiert Timer-Resolution"""
        try:
            result = ctypes.windll.ntdll.NtSetTimerResolution(5000, True, ctypes.byref(ctypes.c_ulong()))
            return result == 0
        except (AttributeError, OSError):
            return False
    
    def clear_memory(self) -> bool:
        """Bereinigt RAM durch Leeren des Working Sets aller Prozesse"""
        logger.info("  [Substep] Clearing memory via EmptyWorkingSet...")
        
        # FIX: PowerShell Script als einzelne Zeile, korrekt escaped
        ps_script = '$sig="[DllImport(\"kernel32.dll\")]public static extern bool SetProcessWorkingSetSize(IntPtr h,int min,int max);";$t=Add-Type -MemberDefinition $sig -Name "M" -Namespace "W" -PassThru;Get-Process|ForEach-Object{try{$t::SetProcessWorkingSetSize($_.Handle,-1,-1)}catch{}}'
        
        result = CommandExecutor.execute([
            'powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_script
        ], timeout=15)
        
        if result.success:
            logger.info("  [Substep] Memory cleared successfully")
        else:
            logger.warning(f"  [Substep] Memory cleanup result: {result.error_message}")
        
        return result.success
    
    def optimize_full(self, options: Optional[Dict] = None) -> OptimizationResult:
        """Fuehrt alle Optimierungen durch mit detailliertem Logging"""
        options = options or {}
        result = OptimizationResult()
        
        self.registry.clear_backup_log()
        self.backup = BackupState()
        
        logger.info("=" * 50)
        logger.info("STARTING OPTIMIZATION")
        logger.info("=" * 50)
        logger.info(f"Options selected: {sum(options.values())}/14")
        
        if options.get("kill_apps", True):
            logger.info("[STEP 1/14] Killing background apps...")
            result.apps_killed = self.processes.kill_all()
            self.backup.killed_processes = result.apps_killed.copy()
        
        if options.get("stop_services", True):
            logger.info("[STEP 2/14] Stopping services...")
            result.services_stopped = self.services.stop_all()
            self.backup.stopped_services = result.services_stopped.copy()
        
        if options.get("high_priority", True):
            logger.info("[STEP 3/14] Setting high priority...")
            result.priority_set = self.set_high_priority()
            logger.info(f"  Priority set: {result.priority_set}")
        
        if options.get("power_plan", True):
            logger.info("[STEP 4/14] Optimizing power plan...")
            result.power_optimized = self.optimize_power_plan()
            # Verify power plan is active
            check_result = CommandExecutor.execute(['powercfg', '/getactivescheme'], capture_output=True, timeout=3)
            if PowerPlanUUIDs.HIGH_PERFORMANCE in check_result.stdout:
                logger.info("  ✓ Power plan verified: High Performance")
            else:
                logger.warning("  ⚠ Power plan may not be active - restart recommended")
            logger.info(f"  Power plan optimized: {result.power_optimized}")
        
        if options.get("visual_effects", True):
            logger.info("[STEP 5/14] Disabling visual effects...")
            result.visual_effects_disabled = self.disable_visual_effects()
            logger.info(f"  Visual effects disabled: {result.visual_effects_disabled}")
            # Explorer neu starten damit Änderungen sofort wirksam werden
            if result.visual_effects_disabled:
                logger.info("  Restarting Explorer to apply visual effects...")
                CommandExecutor.execute(['taskkill', '/F', '/IM', 'explorer.exe'], timeout=3, silent=True)
                time.sleep(0.5)
                CommandExecutor.execute(['cmd', '/c', 'start', 'explorer.exe'], timeout=5, silent=True)
                logger.info("  Explorer restarted")
        
        if options.get("gpu_tweaks", True):
            logger.info("[STEP 6/14] Applying GPU tweaks...")
            result.gpu_tweaks = self.optimize_gpu()
            logger.info(f"  GPU tweaks applied: {len(result.gpu_tweaks)}")
        
        if options.get("network", False):
            logger.info("[STEP 7/14] Optimizing network...")
            result.network_optimized = self.optimize_network()
            logger.info(f"  Network optimized: {result.network_optimized}")
        
        if options.get("defender", False):
            logger.info("[STEP 8/14] Disabling Windows Defender...")
            result.defender_disabled = self.disable_windows_defender_rt()
            logger.info(f"  Defender disabled: {result.defender_disabled}")
        
        if options.get("superfetch", False):
            logger.info("[STEP 9/14] Disabling Superfetch...")
            result.superfetch_disabled = self.disable_superfetch()
            logger.info(f"  Superfetch disabled: {result.superfetch_disabled}")
        
        if options.get("game_dvr", True):
            logger.info("[STEP 10/14] Disabling Game DVR...")
            result.game_dvr_disabled = self.disable_game_dvr()
            logger.info(f"  Game DVR disabled: {result.game_dvr_disabled}")
        
        if options.get("fullscreen_opt", True):
            logger.info("[STEP 11/14] Disabling fullscreen optimizations...")
            result.fullscreen_optimized = self.disable_fullscreen_optimizations()
            logger.info(f"  Fullscreen optimized: {result.fullscreen_optimized}")
        
        if options.get("qos", False):
            logger.info("[STEP 12/14] Setting QoS packet priority...")
            result.qos_optimized = self.set_qos_packet_priority()
            logger.info(f"  QoS optimized: {result.qos_optimized}")
        
        if options.get("timer_res", False):
            logger.info("[STEP 13/14] Optimizing timer resolution...")
            result.timer_optimized = self.optimize_timer_resolution()
            logger.info(f"  Timer optimized: {result.timer_optimized}")
        
        if options.get("clear_memory", False):
            logger.info("[STEP 14/14] Clearing memory...")
            result.memory_cleared = self.clear_memory()
            logger.info(f"  Memory cleared: {result.memory_cleared}")
        
        self.backup.registry_backup = self.registry.get_backup_log_copy()
        
        logger.info("=" * 50)
        logger.info("OPTIMIZATION COMPLETE")
        logger.info("=" * 50)
        logger.info(f"Errors: {len(result.errors)}")
        return result
    
    def restore(self) -> Dict:
        """Stellt System-Zustand wieder her mit detailliertem Error-Handling"""
        logger.info("Starting restore...")
        restored = {
            "processes_restarted": 0,
            "services_started": 0,
            "registry_restored": 0,
            "registry_errors": 0
        }
        
        try:
            # Power-Plan zurücksetzen
            result = CommandExecutor.execute(
                ['powercfg', '/setactive', PowerPlanUUIDs.BALANCED], 
                silent=True, timeout=5
            )
            if result.success:
                logger.info("  ✓ Power plan restored to Balanced")
        except Exception as e:
            logger.error(f"  ✗ Failed to restore power plan: {e}")
        
        # Prozesse neu starten
        try:
            restored["processes_restarted"] = len(self.processes.restart_all())
            logger.info(f"  ✓ Restarted {restored['processes_restarted']} processes")
        except Exception as e:
            logger.error(f"  ✗ Failed to restart processes: {e}")
        
        # Services starten
        try:
            restored["services_started"] = len(self.services.start_all())
            logger.info(f"  ✓ Started {restored['services_started']} services")
        except Exception as e:
            logger.error(f"  ✗ Failed to start services: {e}")
        
        # Registry wiederherstellen
        try:
            success, errors = self.registry.restore_all()
            restored["registry_restored"] = success
            restored["registry_errors"] = errors
            logger.info(f"  ✓ Registry: {success} restored, {errors} errors")
        except Exception as e:
            logger.error(f"  ✗ Failed to restore registry: {e}")
        
        logger.info(f"Restore complete: {restored}")
        return restored


# Export fuer Import
__all__ = ['SystemOptimizer', 'ProcessManager', 'ServiceManager', 'ValidationPatterns', 'ProcessLists']
