#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fehleranalyse und Bug Report für Unified Gaming Optimizer
"""

import sys
import os
import traceback
import json
from datetime import datetime
import subprocess

sys.path.insert(0, 'core')

class BugAnalyzer:
    def __init__(self):
        self.bugs_found = []
        self.warnings = []
        self.performance_issues = []
        self.system_compatibility = {}
        
    def run_comprehensive_analysis(self):
        """Führt umfassende Fehleranalyse durch"""
        print("🔍 UMFASSENDE FEHLERANALYSE")
        print("="*60)
        print(f"Startzeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 1. Import-Tests
        self._test_imports()
        
        # 2. System-Kompatibilität
        self._check_system_compatibility()
        
        # 3. Hardware-Erkennung
        self._test_hardware_detection()
        
        # 4. Performance-Tests
        self._test_performance_modules()
        
        # 5. FSR-Optimierung
        self._test_fsr_functionality()
        
        # 6. Unified Optimizer
        self._test_unified_optimizer()
        
        # 7. Speicher und Ressourcen
        self._test_memory_usage()
        
        # 8. Thread-Safety
        self._test_thread_safety()
        
        # Report generieren
        self._generate_bug_report()
        
        return self.bugs_found, self.warnings, self.performance_issues
    
    def _test_imports(self):
        """Testet alle Import-Module"""
        print("\n🔧 TESTING IMPORTS")
        print("-" * 30)
        
        modules_to_test = [
            ("hardware_benchmark", "HardwareBenchmark"),
            ("real_time_optimizer", "RealTimeOptimizer"),
            ("system_monitor", "SystemMonitor"),
            ("fsr_optimizer", "CustomFSROptimizer"),
            ("system_profiler", "SystemProfiler"),
            ("hardware_database", "get_user_system_performance")
        ]
        
        for module_name, class_name in modules_to_test:
            try:
                module = __import__(module_name)
                if hasattr(module, class_name):
                    print(f"   ✅ {module_name}.{class_name}")
                else:
                    error = f"❌ {module_name}.{class_name} nicht gefunden"
                    print(error)
                    self.bugs_found.append(error)
            except ImportError as e:
                error = f"❌ {module_name} Import Fehler: {e}"
                print(error)
                self.bugs_found.append(error)
            except Exception as e:
                error = f"⚠️ {module_name} Warnung: {e}"
                print(error)
                self.warnings.append(error)
    
    def _check_system_compatibility(self):
        """Prüft System-Kompatibilität"""
        print("\n💻 SYSTEM COMPATIBILITY")
        print("-" * 30)
        
        # Python Version
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 8:
            print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            error = f"❌ Python Version zu alt: {python_version}"
            print(error)
            self.bugs_found.append(error)
        
        # Windows Version
        try:
            import platform
            if platform.system() == "Windows":
                print(f"   ✅ {platform.system()} {platform.release()}")
            else:
                warning = f"⚠️ Nicht-Windows System: {platform.system()}"
                print(warning)
                self.warnings.append(warning)
        except Exception as e:
            error = f"❌ System-Erkennung Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
        
        # PowerShell Verfügbarkeit
        try:
            result = subprocess.run(["powershell", "-Command", "Get-Host"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("   ✅ PowerShell verfügbar")
            else:
                warning = "⚠️ PowerShell nicht verfügbar"
                print(warning)
                self.warnings.append(warning)
        except:
            warning = "⚠️ PowerShell Test fehlgeschlagen"
            print(warning)
            self.warnings.append(warning)
    
    def _test_hardware_detection(self):
        """Testet Hardware-Erkennung"""
        print("\n🖥️ HARDWARE DETECTION")
        print("-" * 30)
        
        try:
            from system_profiler import SystemProfiler
            profiler = SystemProfiler()
            
            specs = profiler.system_specs
            
            # CPU Detection
            if specs["cpu"]["name"] != "Unknown":
                print(f"   ✅ CPU erkannt: {specs['cpu']['name']}")
            else:
                warning = "⚠️ CPU nicht erkannt"
                print(warning)
                self.warnings.append(warning)
            
            # GPU Detection
            if specs["gpu"]:
                print(f"   ✅ {len(specs['gpu'])} GPU(s) erkannt")
                for i, gpu in enumerate(specs["gpu"]):
                    print(f"      GPU {i+1}: {gpu['name']}")
            else:
                warning = "⚠️ Keine GPU erkannt"
                print(warning)
                self.warnings.append(warning)
            
            # Memory Detection
            if specs["memory"]["total_gb"] > 0:
                print(f"   ✅ Memory: {specs['memory']['total_gb']}GB")
            else:
                error = "❌ Memory nicht erkannt"
                print(error)
                self.bugs_found.append(error)
                
        except Exception as e:
            error = f"❌ Hardware Detection Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
    
    def _test_performance_modules(self):
        """Testet Performance-Module"""
        print("\n📊 PERFORMANCE MODULES")
        print("-" * 30)
        
        # Hardware Benchmark
        try:
            from hardware_benchmark import HardwareBenchmark
            benchmark = HardwareBenchmark()
            
            # Test CPU Benchmark
            cpu_result = benchmark.benchmark_cpu()
            if cpu_result["score"] > 0:
                print(f"   ✅ CPU Benchmark: {cpu_result['score']:.1f}")
            else:
                error = "❌ CPU Benchmark Score 0"
                print(error)
                self.bugs_found.append(error)
            
            # Test Memory Benchmark
            mem_result = benchmark.benchmark_memory()
            if mem_result["score"] > 0:
                print(f"   ✅ Memory Benchmark: {mem_result['score']:.1f}")
            else:
                error = "❌ Memory Benchmark Score 0"
                print(error)
                self.bugs_found.append(error)
                
        except Exception as e:
            error = f"❌ Hardware Benchmark Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
        
        # System Monitor
        try:
            from system_monitor import SystemMonitor
            monitor = SystemMonitor()
            
            # Kurzer Test
            monitor.start_monitoring()
            import time
            time.sleep(2)
            
            current = monitor.get_current_metrics()
            if current["cpu_usage"] >= 0:
                print(f"   ✅ System Monitor: CPU {current['cpu_usage']:.1f}%")
            else:
                error = "❌ System Monitor CPU Fehler"
                print(error)
                self.bugs_found.append(error)
            
            monitor.stop_monitoring()
            
        except Exception as e:
            error = f"❌ System Monitor Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
    
    def _test_fsr_functionality(self):
        """Testet FSR Funktionalität"""
        print("\n🚀 FSR OPTIMIZER")
        print("-" * 30)
        
        try:
            from fsr_optimizer import CustomFSROptimizer
            fsr = CustomFSROptimizer()
            
            # Test Profile
            games = ["Fortnite", "Valorant", "Cyberpunk 2077"]
            for game in games:
                try:
                    fsr.apply_game_profile(game)
                    print(f"   ✅ FSR Profil für {game}")
                except Exception as e:
                    warning = f"⚠️ FSR Profil {game} Fehler: {e}"
                    print(warning)
                    self.warnings.append(warning)
            
            # Test Modi
            modes = ["ultra_performance", "performance", "balanced", "quality", "ultra_quality"]
            for mode in modes:
                try:
                    fsr.set_fsr_mode(mode)
                    print(f"   ✅ FSR Modus {mode}")
                except Exception as e:
                    warning = f"⚠️ FSR Modus {mode} Fehler: {e}"
                    print(warning)
                    self.warnings.append(warning)
            
        except Exception as e:
            error = f"❌ FSR Optimizer Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
    
    def _test_unified_optimizer(self):
        """Testet Unified Optimizer"""
        print("\n🎮 UNIFIED OPTIMIZER")
        print("-" * 30)
        
        try:
            from unified_optimizer import UnifiedGamingOptimizer
            optimizer = UnifiedGamingOptimizer()
            
            # Test Konfiguration
            if optimizer.config:
                print("   ✅ Konfiguration geladen")
            else:
                error = "❌ Konfiguration nicht geladen"
                print(error)
                self.bugs_found.append(error)
            
            # Test Profile
            if optimizer.profiles:
                print(f"   ✅ {len(optimizer.profiles)} Profile geladen")
            else:
                error = "❌ Keine Profile gefunden"
                print(error)
                self.bugs_found.append(error)
            
            # Test Game Profiles
            if optimizer.game_profiles:
                print(f"   ✅ {len(optimizer.game_profiles)} Game Profile geladen")
            else:
                error = "❌ Keine Game Profile gefunden"
                print(error)
                self.bugs_found.append(error)
            
        except Exception as e:
            error = f"❌ Unified Optimizer Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
    
    def _test_memory_usage(self):
        """Testet Speichernutzung"""
        print("\n🧠 MEMORY USAGE")
        print("-" * 30)
        
        try:
            import psutil
            
            # Aktuelle Memory-Nutzung
            memory = psutil.virtual_memory()
            print(f"   📊 Aktuell: {memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB ({memory.percent:.1f}%)")
            
            if memory.percent > 90:
                warning = f"⚠️ Hohe Memory-Nutzung: {memory.percent:.1f}%"
                print(warning)
                self.warnings.append(warning)
                self.performance_issues.append("High Memory Usage")
            
            # Test Memory-Leaks durch Modul-Import
            initial_memory = memory.percent
            
            # Importiere alle Module
            modules = ["hardware_benchmark", "real_time_optimizer", "system_monitor", "fsr_optimizer"]
            for module in modules:
                try:
                    __import__(module)
                except:
                    pass
            
            # Prüfe Memory nach Imports
            final_memory = psutil.virtual_memory().percent
            memory_increase = final_memory - initial_memory
            
            if memory_increase > 10:
                warning = f"⚠️ Memory Increase nach Imports: {memory_increase:.1f}%"
                print(warning)
                self.warnings.append(warning)
                self.performance_issues.append("Memory Leak in Imports")
            else:
                print(f"   ✅ Memory Increase: {memory_increase:.1f}%")
                
        except Exception as e:
            error = f"❌ Memory Test Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
    
    def _test_thread_safety(self):
        """Testet Thread-Safety"""
        print("\n🧵 THREAD SAFETY")
        print("-" * 30)
        
        try:
            import threading
            import time
            
            # Test System Monitor Thread
            from system_monitor import SystemMonitor
            
            monitor = SystemMonitor()
            errors = []
            
            def monitor_test():
                try:
                    monitor.start_monitoring()
                    time.sleep(1)
                    monitor.get_current_metrics()
                    monitor.stop_monitoring()
                except Exception as e:
                    errors.append(f"Monitor Thread Error: {e}")
            
            # Starte mehrere Threads
            threads = []
            for i in range(3):
                thread = threading.Thread(target=monitor_test)
                threads.append(thread)
                thread.start()
            
            # Warte auf alle Threads
            for thread in threads:
                thread.join()
            
            if errors:
                for error in errors:
                    print(f"   ❌ {error}")
                    self.bugs_found.append(error)
            else:
                print("   ✅ Thread-Safety Test bestanden")
                
        except Exception as e:
            error = f"❌ Thread-Safety Test Fehler: {e}"
            print(error)
            self.bugs_found.append(error)
    
    def _generate_bug_report(self):
        """Generiert detaillierten Bug Report"""
        print("\n" + "="*60)
        print("📋 BUG REPORT ZUSAMMENFASSUNG")
        print("="*60)
        
        print(f"\n🔍 CRITICAL BUGS ({len(self.bugs_found)}):")
        if self.bugs_found:
            for i, bug in enumerate(self.bugs_found, 1):
                print(f"   {i}. {bug}")
        else:
            print("   ✅ Keine Critical Bugs gefunden!")
        
        print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
        if self.warnings:
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        else:
            print("   ✅ Keine Warnungen!")
        
        print(f"\n📊 PERFORMANCE ISSUES ({len(self.performance_issues)}):")
        if self.performance_issues:
            for i, issue in enumerate(self.performance_issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("   ✅ Keine Performance-Probleme!")
        
        # Gesamtbewertung
        total_issues = len(self.bugs_found) + len(self.warnings) + len(self.performance_issues)
        
        if total_issues == 0:
            status = "🟢 PERFECT"
            recommendation = "Bereit für Production!"
        elif len(self.bugs_found) == 0:
            status = "🟡 GOOD"
            recommendation = "Kleine Optimierungen empfohlen"
        elif len(self.bugs_found) <= 2:
            status = "🟠 ACCEPTABLE"
            recommendation = "Bugs beheben vor Release"
        else:
            status = "🔴 CRITICAL"
            recommendation = "Major Bugs beheben erforderlich"
        
        print(f"\n🏆 GESAMTSTATUS: {status}")
        print(f"💡 EMPFEHLUNG: {recommendation}")
        
        # Speichere Report
        self._save_bug_report()
    
    def _save_bug_report(self):
        """Speichert Bug Report in Datei"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bug_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "critical_bugs": self.bugs_found,
            "warnings": self.warnings,
            "performance_issues": self.performance_issues,
            "system_info": self._get_system_info_for_report()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n📁 Bug Report gespeichert: {filename}")
        except Exception as e:
            print(f"\n❌ Bug Report Speicherung fehlgeschlagen: {e}")
    
    def _get_system_info_for_report(self):
        """Sammelt System-Info für Report"""
        try:
            import platform
            import psutil
            
            return {
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available
            }
        except:
            return {"error": "System Info nicht verfügbar"}

def main():
    """Hauptfunktion"""
    print("🔍 UNIFIED GAMING OPTIMIZER - FEHLERANALYSE")
    print("="*60)
    
    analyzer = BugAnalyzer()
    bugs, warnings, performance_issues = analyzer.run_comprehensive_analysis()
    
    # Exit Code basierend auf Ergebnissen
    if len(bugs) > 0:
        print(f"\n❌ {len(bugs)} Critical Bugs gefunden - Exit Code 1")
        sys.exit(1)
    elif len(warnings) > 5:
        print(f"\n⚠️ {len(warnings)} Warnungen gefunden - Exit Code 2")
        sys.exit(2)
    elif len(performance_issues) > 0:
        print(f"\n📊 {len(performance_issues)} Performance Issues - Exit Code 3")
        sys.exit(3)
    else:
        print(f"\n✅ Alle Tests bestanden - Exit Code 0")
        sys.exit(0)

if __name__ == "__main__":
    main()
