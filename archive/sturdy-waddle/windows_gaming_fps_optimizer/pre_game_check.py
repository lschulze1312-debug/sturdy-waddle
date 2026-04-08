#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Game System Check - Kompletter Test vor dem Gaming
"""

import os
import sys
import time
import json
import psutil
import subprocess
from datetime import datetime

sys.path.insert(0, 'core')

class PreGameSystemCheck:
    """Führt kompletten System-Check vor dem Gaming durch"""
    
    def __init__(self):
        self.test_results = {}
        self.all_passed = True
        self.warnings = []
        
    def run_all_tests(self):
        """Führt alle Tests durch"""
        print("="*70)
        print("🎮 PRE-GAME SYSTEM CHECK")
        print("="*70)
        print(f"Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # 1. Import Tests
        self._test_imports()
        
        # 2. System Info
        self._test_system_info()
        
        # 3. Thermal Protection Test
        self._test_thermal_protection()
        
        # 4. Borderlands 4 Config Test
        self._test_borderlands4_config()
        
        # 5. GPU Software Optimizations Test
        self._test_gpu_software_opt()
        
        # 6. Background Optimizer Test
        self._test_background_optimizer()
        
        # 7. FSR Optimizer Test
        self._test_fsr_optimizer()
        
        # 8. DirectX 12 Optimizer Test
        self._test_dx12_optimizer()
        
        # 9. System Performance Test
        self._test_system_performance()
        
        # 10. Pre-Game Readiness Report
        self._generate_readiness_report()
    
    def _test_imports(self):
        """Test 1: Alle Module können importiert werden"""
        print("\n📦 TEST 1: Modul-Importe...")
        
        modules = [
            'real_time_optimizer',
            'system_monitor',
            'hardware_benchmark',
            'fsr_optimizer',
            'directx12_optimizer_safe',
            'background_process_optimizer',
            'ue5_stability_optimizer',
            'thermal_protection',
            'gpu_software_optimizer'
        ]
        
        passed = 0
        failed = 0
        
        for module in modules:
            try:
                __import__(module)
                print(f"   ✅ {module}")
                passed += 1
            except Exception as e:
                print(f"   ❌ {module}: {e}")
                failed += 1
                self.all_passed = False
        
        self.test_results['imports'] = {'passed': passed, 'failed': failed}
        print(f"   Ergebnis: {passed}/{len(modules)} Module OK")
    
    def _test_system_info(self):
        """Test 2: System-Informationen"""
        print("\n💻 TEST 2: System-Informationen...")
        
        try:
            # CPU
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory
            memory = psutil.virtual_memory()
            
            # Disk
            disk = psutil.disk_usage('/')
            
            info = {
                'cpu_cores': cpu_count,
                'cpu_freq': cpu_freq.current if cpu_freq else 0,
                'cpu_usage': cpu_usage,
                'memory_total_gb': memory.total / (1024**3),
                'memory_used_gb': memory.used / (1024**3),
                'memory_percent': memory.percent,
                'disk_free_gb': disk.free / (1024**3),
                'disk_percent': disk.percent
            }
            
            print(f"   ✅ CPU: {info['cpu_cores']} Kerne @ {info['cpu_freq']:.0f}MHz")
            print(f"   ✅ CPU-Last: {info['cpu_usage']:.1f}%")
            print(f"   ✅ RAM: {info['memory_used_gb']:.1f}/{info['memory_total_gb']:.1f} GB ({info['memory_percent']:.0f}%)")
            print(f"   ✅ Disk: {info['disk_free_gb']:.1f} GB frei")
            
            # Check if system is ready
            ready = True
            if info['memory_percent'] > 85:
                self.warnings.append("⚠️ RAM fast voll - Browser tabs schließen!")
                ready = False
            if info['disk_free_gb'] < 10:
                self.warnings.append("⚠️ Wenig Speicherplatz!")
                ready = False
            if info['cpu_usage'] > 50:
                self.warnings.append("⚠️ Hohe CPU-Last - Hintergrund-Apps schließen!")
                ready = False
            
            self.test_results['system_info'] = {'status': 'OK', 'ready': ready, 'data': info}
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['system_info'] = {'status': 'ERROR', 'error': str(e)}
            self.all_passed = False
    
    def _test_thermal_protection(self):
        """Test 3: Thermal Protection"""
        print("\n🌡️ TEST 3: Thermal Protection...")
        
        try:
            from thermal_protection import ThermalProtectionManager
            
            thermal = ThermalProtectionManager()
            status = thermal.get_thermal_status()
            
            # Check if laptop detected
            is_laptop = thermal.is_laptop
            
            print(f"   ✅ Thermal Protection initialisiert")
            print(f"   🖥️ System-Typ: {'Laptop' if is_laptop else 'Desktop'}")
            print(f"   🌡️ Aktuelle Temp: {status['current_temp']:.1f}°C" if status['current_temp'] > 0 else "   ⚠️ Temperatur nicht verfügbar")
            
            # Laptop-specific thresholds
            if is_laptop:
                print(f"   ✅ Laptop-Grenzwerte: 80°C/88°C/93°C/96°C")
            else:
                print(f"   ✅ Desktop-Grenzwerte: 70°C/80°C/85°C/90°C")
            
            self.test_results['thermal'] = {
                'status': 'OK',
                'is_laptop': is_laptop,
                'temp': status['current_temp'],
                'safe': status['safe_to_proceed']
            }
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['thermal'] = {'status': 'ERROR', 'error': str(e)}
            self.all_passed = False
    
    def _test_borderlands4_config(self):
        """Test 4: Borderlands 4 Konfiguration"""
        print("\n🎮 TEST 4: Borderlands 4 Konfiguration...")
        
        try:
            # Check if UE5 config exists
            config_paths = [
                os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Config\\WindowsNoEditor\\Engine.ini"),
                os.path.expandvars("%LOCALAPPDATA%\\Borderlands4\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini")
            ]
            
            configs_found = 0
            for path in config_paths:
                if os.path.exists(path):
                    configs_found += 1
                    print(f"   ✅ {os.path.basename(path)} gefunden")
                else:
                    print(f"   ⚠️ {os.path.basename(path)} nicht gefunden")
            
            if configs_found == 0:
                self.warnings.append("⚠️ Borderlands 4 Config fehlt - borderlands4_autofix.py ausführen!")
            
            self.test_results['borderlands4'] = {
                'status': 'OK' if configs_found > 0 else 'WARNING',
                'configs_found': configs_found
            }
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['borderlands4'] = {'status': 'ERROR', 'error': str(e)}
    
    def _test_gpu_software_opt(self):
        """Test 5: GPU Software Optimizations"""
        print("\n🎨 TEST 5: GPU Software Optimizations...")
        
        try:
            from gpu_software_optimizer import GPUDriverIndependentOptimizer
            
            # Check if module can be instantiated
            gpu_opt = GPUDriverIndependentOptimizer()
            
            print(f"   ✅ GPU Software Optimizer bereit")
            print(f"   ✅ {len(gpu_opt.optimizations_applied)} Optimierungen verfügbar")
            
            self.test_results['gpu_software'] = {'status': 'OK'}
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['gpu_software'] = {'status': 'ERROR', 'error': str(e)}
    
    def _test_background_optimizer(self):
        """Test 6: Background Process Optimizer"""
        print("\n🔧 TEST 6: Background Process Optimizer...")
        
        try:
            from background_process_optimizer import BackgroundProcessOptimizer
            
            bg_opt = BackgroundProcessOptimizer()
            
            print(f"   ✅ Background Optimizer bereit")
            print(f"   ✅ Kann {len(bg_opt.background_apps)} Apps verwalten")
            
            self.test_results['background'] = {'status': 'OK'}
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['background'] = {'status': 'ERROR', 'error': str(e)}
    
    def _test_fsr_optimizer(self):
        """Test 7: FSR Optimizer"""
        print("\n🚀 TEST 7: FSR Optimizer...")
        
        try:
            from fsr_optimizer import CustomFSROptimizer
            
            fsr = CustomFSROptimizer()
            
            print(f"   ✅ FSR Optimizer bereit")
            print(f"   ✅ Profile: {len(fsr.game_profiles)} Games")
            
            # Check Borderlands 4 profile
            if 'borderlands_4' in fsr.game_profiles:
                print(f"   ✅ Borderlands 4 FSR-Profil vorhanden")
            
            self.test_results['fsr'] = {'status': 'OK'}
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['fsr'] = {'status': 'ERROR', 'error': str(e)}
    
    def _test_dx12_optimizer(self):
        """Test 8: DirectX 12 Optimizer"""
        print("\n🎮 TEST 8: DirectX 12 Optimizer...")
        
        try:
            from directx12_optimizer_safe import DirectX12OptimizerSafe
            
            dx12 = DirectX12OptimizerSafe()
            
            print(f"   ✅ DirectX 12 Optimizer bereit")
            print(f"   ✅ {len(dx12.game_profiles)} Game-Profile")
            
            # Check Borderlands 4 profile
            if 'borderlands_4' in dx12.game_profiles:
                print(f"   ✅ Borderlands 4 DX12-Profil vorhanden")
            
            self.test_results['dx12'] = {'status': 'OK'}
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['dx12'] = {'status': 'ERROR', 'error': str(e)}
    
    def _test_system_performance(self):
        """Test 9: System Performance Check"""
        print("\n⚡ TEST 9: System Performance...")
        
        try:
            # Quick performance check
            start = time.time()
            
            # CPU benchmark (simple)
            cpu_score = 0
            for i in range(1000000):
                cpu_score += i * i
            
            cpu_time = time.time() - start
            
            # Memory test
            mem = psutil.virtual_memory()
            
            print(f"   ✅ CPU-Test: {cpu_time:.3f}s (schnell={cpu_time < 1.0})")
            print(f"   ✅ RAM: {mem.available / (1024**3):.1f} GB verfügbar")
            
            # Check if gaming-ready
            gaming_ready = cpu_time < 2.0 and mem.available > (2 * 1024**3)
            
            if not gaming_ready:
                self.warnings.append("⚠️ System etwas langsam - Hintergrund-Apps schließen!")
            
            self.test_results['performance'] = {
                'status': 'OK',
                'gaming_ready': gaming_ready,
                'cpu_time': cpu_time,
                'ram_available_gb': mem.available / (1024**3)
            }
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            self.test_results['performance'] = {'status': 'ERROR', 'error': str(e)}
    
    def _generate_readiness_report(self):
        """Generiert Pre-Game Readiness Report"""
        print("\n" + "="*70)
        print("📋 PRE-GAME READINESS REPORT")
        print("="*70)
        
        # Count results
        passed = sum(1 for r in self.test_results.values() if r.get('status') == 'OK')
        total = len(self.test_results)
        
        print(f"\n✅ TESTS BESTANDEN: {passed}/{total}")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️ WARNUNGEN ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        # System status
        print(f"\n🖥️ SYSTEM-STATUS:")
        
        # Thermal
        thermal = self.test_results.get('thermal', {})
        if thermal.get('is_laptop'):
            print(f"   🖥️ Laptop-Modus: AKTIV (80°C/88°C/93°C/96°C)")
        
        # Ready to game?
        ready = self.all_passed and len(self.warnings) == 0
        
        print(f"\n{'='*70}")
        if ready:
            print("🎉 SYSTEM BEREIT FÜR GAMING!")
            print("✅ Alle Tests bestanden")
            print("✅ Keine Warnungen")
            print("✅ Du kannst jetzt Borderlands 4 starten!")
            print("\n🚀 Empfohlener Start:")
            print("   1. python run_optimizer.py")
            print("   2. Borderlands 4 starten")
            print("   3. Genießen!")
        else:
            print("⚠️ SYSTEM NICHT OPTIMAL BEREIT")
            print("❌ Einige Tests fehlgeschlagen oder Warnungen vorhanden")
            print("\n🔧 Empfohlene Aktionen:")
            print("   1. Warnungen oben beheben")
            print("   2. python borderlands4_autofix.py ausführen")
            print("   3. PC neu starten")
            print("   4. Test wiederholen")
        
        print(f"{'='*70}")
        
        # Save report
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'tests_passed': passed,
                'tests_total': total,
                'warnings': self.warnings,
                'ready': ready,
                'results': self.test_results
            }
            
            filename = f"pre_game_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n📁 Report gespeichert: {filename}")
            
        except Exception as e:
            print(f"\n❌ Report Speicherung fehlgeschlagen: {e}")

if __name__ == "__main__":
    check = PreGameSystemCheck()
    check.run_all_tests()
    
    input("\n🖱️ Drücke Enter zum Beenden...")
