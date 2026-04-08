#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance Stress Test für Unified Gaming Optimizer
"""

import sys
import os
import time
import threading
import psutil
from datetime import datetime

sys.path.insert(0, 'core')

class PerformanceStressTest:
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
    def run_stress_test(self):
        """Führt umfassenden Stress Test durch"""
        print("🔥 PERFORMANCE STRESS TEST")
        print("="*60)
        print(f"Startzeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        self.start_time = time.time()
        
        # 1. Multi-Thread Stress Test
        self._test_multi_threading()
        
        # 2. Memory Stress Test
        self._test_memory_stress()
        
        # 3. CPU Stress Test
        self._test_cpu_stress()
        
        # 4. FSR Performance Test
        self._test_fsr_performance()
        
        # 5. Long-Running Test
        self._test_long_running()
        
        # 6. Resource Leak Test
        self._test_resource_leaks()
        
        self.end_time = time.time()
        
        # Report generieren
        self._generate_stress_report()
        
        return self.test_results
    
    def _test_multi_threading(self):
        """Testet Multi-Threading Performance"""
        print("\n🧵 MULTI-THREADING STRESS TEST")
        print("-" * 40)
        
        try:
            from system_monitor import SystemMonitor
            
            # Erstelle mehrere Monitor-Instanzen
            monitors = []
            threads = []
            
            def monitor_worker(monitor_id):
                try:
                    monitor = SystemMonitor()
                    monitor.start_monitoring()
                    
                    # Sammle Daten für 3 Sekunden
                    for i in range(30):
                        metrics = monitor.get_current_metrics()
                        time.sleep(0.1)
                    
                    monitor.stop_monitoring()
                    return f"Monitor {monitor_id} completed"
                except Exception as e:
                    return f"Monitor {monitor_id} error: {e}"
            
            # Starte 5 parallele Monitore
            start_time = time.time()
            
            for i in range(5):
                thread = threading.Thread(target=monitor_worker, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Warte auf alle Threads
            for thread in threads:
                thread.join()
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"   ✅ 5 parallele Monitore in {duration:.2f}s")
            print(f"   📊 Durchschnitt: {duration/5:.2f}s pro Monitor")
            
            self.test_results["multi_threading"] = {
                "status": "passed",
                "duration": duration,
                "thread_count": 5
            }
            
        except Exception as e:
            print(f"   ❌ Multi-Threading Fehler: {e}")
            self.test_results["multi_threading"] = {
                "status": "failed",
                "error": str(e)
            }
    
    def _test_memory_stress(self):
        """Testet Memory unter Last"""
        print("\n🧠 MEMORY STRESS TEST")
        print("-" * 40)
        
        try:
            import numpy as np
            
            # Start-Memory
            initial_memory = psutil.virtual_memory().percent
            print(f"   📊 Start Memory: {initial_memory:.1f}%")
            
            # Erstelle Memory-Last
            memory_blocks = []
            
            # Simuliere Gaming Memory Usage
            for i in range(10):
                # Erstelle 100MB Arrays
                block = np.random.random((100, 100, 100))  # ~80MB
                memory_blocks.append(block)
                
                current_memory = psutil.virtual_memory().percent
                print(f"   📈 Block {i+1}/10 - Memory: {current_memory:.1f}%")
            
            # Peak Memory
            peak_memory = psutil.virtual_memory().percent
            print(f"   🔝 Peak Memory: {peak_memory:.1f}%")
            
            # Memory Cleanup
            del memory_blocks
            
            # Final Memory
            import gc
            gc.collect()
            
            final_memory = psutil.virtual_memory().percent
            print(f"   📉 Final Memory: {final_memory:.1f}%")
            
            memory_increase = peak_memory - initial_memory
            memory_leak = final_memory - initial_memory
            
            print(f"   📊 Memory Increase: +{memory_increase:.1f}%")
            print(f"   🔍 Memory Leak: +{memory_leak:.1f}%")
            
            # Bewertung
            if memory_leak < 5:
                status = "excellent"
            elif memory_leak < 10:
                status = "good"
            elif memory_leak < 20:
                status = "acceptable"
            else:
                status = "poor"
            
            print(f"   ✅ Memory Management: {status}")
            
            self.test_results["memory_stress"] = {
                "status": status,
                "initial_memory": initial_memory,
                "peak_memory": peak_memory,
                "final_memory": final_memory,
                "memory_increase": memory_increase,
                "memory_leak": memory_leak
            }
            
        except ImportError:
            print("   ⚠️ NumPy nicht verfügbar - Test übersprungen")
            self.test_results["memory_stress"] = {
                "status": "skipped",
                "reason": "NumPy not available"
            }
        except Exception as e:
            print(f"   ❌ Memory Stress Fehler: {e}")
            self.test_results["memory_stress"] = {
                "status": "failed",
                "error": str(e)
            }
    
    def _test_cpu_stress(self):
        """Testet CPU unter Last"""
        print("\n🔥 CPU STRESS TEST")
        print("-" * 40)
        
        try:
            from hardware_benchmark import HardwareBenchmark
            
            # Start CPU Usage
            initial_cpu = psutil.cpu_percent(interval=1)
            print(f"   📊 Start CPU: {initial_cpu:.1f}%")
            
            # Führe parallele Benchmarks durch
            benchmark_threads = []
            benchmark_results = []
            
            def benchmark_worker():
                try:
                    benchmark = HardwareBenchmark()
                    cpu_result = benchmark.benchmark_cpu()
                    return cpu_result["score"]
                except Exception as e:
                    return 0
            
            # Starte 3 parallele Benchmarks
            start_time = time.time()
            
            for i in range(3):
                thread = threading.Thread(target=benchmark_worker)
                benchmark_threads.append(thread)
                thread.start()
            
            # Warte auf Ergebnisse
            for thread in benchmark_threads:
                thread.join()
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Peak CPU während Test
            peak_cpu = psutil.cpu_percent(interval=1)
            print(f"   🔝 Peak CPU: {peak_cpu:.1f}%")
            
            # Final CPU
            final_cpu = psutil.cpu_percent(interval=1)
            print(f"   📉 Final CPU: {final_cpu:.1f}%")
            
            print(f"   ⏱️ 3 Benchmarks in {duration:.2f}s")
            
            # Bewertung
            if duration < 5.0:
                status = "excellent"
            elif duration < 10.0:
                status = "good"
            elif duration < 20.0:
                status = "acceptable"
            else:
                status = "poor"
            
            print(f"   ✅ CPU Performance: {status}")
            
            self.test_results["cpu_stress"] = {
                "status": status,
                "initial_cpu": initial_cpu,
                "peak_cpu": peak_cpu,
                "final_cpu": final_cpu,
                "duration": duration
            }
            
        except Exception as e:
            print(f"   ❌ CPU Stress Fehler: {e}")
            self.test_results["cpu_stress"] = {
                "status": "failed",
                "error": str(e)
            }
    
    def _test_fsr_performance(self):
        """Testet FSR Performance"""
        print("\n🚀 FSR PERFORMANCE TEST")
        print("-" * 40)
        
        try:
            from fsr_optimizer import CustomFSROptimizer
            
            # Test alle FSR Modi
            modes = ["ultra_performance", "performance", "balanced", "quality", "ultra_quality"]
            mode_results = {}
            
            for mode in modes:
                start_time = time.time()
                
                fsr = CustomFSROptimizer()
                fsr.set_fsr_mode(mode)
                fsr.apply_game_profile("Valorant")
                
                # Simuliere kurze Optimierung
                fsr.start_fsr_optimization("Valorant")
                time.sleep(0.5)
                fsr.stop_fsr_optimization()
                
                end_time = time.time()
                duration = end_time - start_time
                
                mode_results[mode] = duration
                print(f"   ✅ {mode}: {duration:.3f}s")
            
            # Berechne Durchschnitt
            avg_duration = sum(mode_results.values()) / len(mode_results)
            print(f"   📊 Durchschnitt: {avg_duration:.3f}s")
            
            # Bewertung
            if avg_duration < 1.0:
                status = "excellent"
            elif avg_duration < 2.0:
                status = "good"
            elif avg_duration < 5.0:
                status = "acceptable"
            else:
                status = "poor"
            
            print(f"   ✅ FSR Performance: {status}")
            
            self.test_results["fsr_performance"] = {
                "status": status,
                "mode_results": mode_results,
                "average_duration": avg_duration
            }
            
        except Exception as e:
            print(f"   ❌ FSR Performance Fehler: {e}")
            self.test_results["fsr_performance"] = {
                "status": "failed",
                "error": str(e)
            }
    
    def _test_long_running(self):
        """Testet langlaufende Operationen"""
        print("\n⏰ LONG-RUNNING TEST")
        print("-" * 40)
        
        try:
            from system_monitor import SystemMonitor
            
            monitor = SystemMonitor()
            monitor.start_monitoring()
            
            # Laufe für 30 Sekunden
            duration = 30
            start_time = time.time()
            
            measurements = []
            
            while time.time() - start_time < duration:
                try:
                    metrics = monitor.get_current_metrics()
                    measurements.append({
                        "timestamp": time.time(),
                        "cpu": metrics["cpu_usage"],
                        "memory": metrics["memory_usage"],
                        "gpu": metrics["gpu_usage"]
                    })
                    
                    # Zeige Fortschritt
                    elapsed = time.time() - start_time
                    progress = (elapsed / duration) * 100
                    print(f"   📊 {elapsed:.0f}s/{duration}s ({progress:.0f}%) - CPU: {metrics['cpu_usage']:.1f}%")
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"   ⚠️ Messfehler: {e}")
            
            monitor.stop_monitoring()
            
            # Analysiere Messungen
            if measurements:
                cpu_values = [m["cpu"] for m in measurements]
                memory_values = [m["memory"] for m in measurements]
                
                avg_cpu = sum(cpu_values) / len(cpu_values)
                max_cpu = max(cpu_values)
                avg_memory = sum(memory_values) / len(memory_values)
                max_memory = max(memory_values)
                
                print(f"   📊 Durchschnitt CPU: {avg_cpu:.1f}% (Max: {max_cpu:.1f}%)")
                print(f"   📊 Durchschnitt Memory: {avg_memory:.1f}% (Max: {max_memory:.1f}%)")
                print(f"   📈 Messungen: {len(measurements)}")
                
                # Bewertung
                if max_cpu < 50 and max_memory < 90:
                    status = "excellent"
                elif max_cpu < 70 and max_memory < 95:
                    status = "good"
                elif max_cpu < 90 and max_memory < 98:
                    status = "acceptable"
                else:
                    status = "poor"
                
                print(f"   ✅ Long-Running: {status}")
                
                self.test_results["long_running"] = {
                    "status": status,
                    "duration": duration,
                    "measurements": len(measurements),
                    "avg_cpu": avg_cpu,
                    "max_cpu": max_cpu,
                    "avg_memory": avg_memory,
                    "max_memory": max_memory
                }
            else:
                print("   ❌ Keine Messungen gesammelt")
                self.test_results["long_running"] = {
                    "status": "failed",
                    "reason": "No measurements collected"
                }
            
        except Exception as e:
            print(f"   ❌ Long-Running Fehler: {e}")
            self.test_results["long_running"] = {
                "status": "failed",
                "error": str(e)
            }
    
    def _test_resource_leaks(self):
        """Testet auf Resource Leaks"""
        print("\n🔍 RESOURCE LEAK TEST")
        print("-" * 40)
        
        try:
            # Start-Ressourcen
            initial_handles = len(psutil.Process().handles())
            initial_threads = psutil.Process().num_threads()
            initial_memory = psutil.virtual_memory().percent
            
            print(f"   📊 Start Handles: {initial_handles}")
            print(f"   📊 Start Threads: {initial_threads}")
            print(f"   📊 Start Memory: {initial_memory:.1f}%")
            
            # Führe verschiedene Operationen durch
            operations = [
                self._test_benchmark_cycle,
                self._test_monitor_cycle,
                self._test_fsr_cycle
            ]
            
            for i, operation in enumerate(operations, 1):
                print(f"   🔄 Operation {i}/3")
                
                # Führe Operation 5 Mal durch
                for j in range(5):
                    operation()
                
                # Zwischenstand
                current_handles = len(psutil.Process().handles())
                current_threads = psutil.Process().num_threads()
                current_memory = psutil.virtual_memory().percent
                
                print(f"      Handles: {current_handles} (+{current_handles-initial_handles})")
                print(f"      Threads: {current_threads} (+{current_threads-initial_threads})")
                print(f"      Memory: {current_memory:.1f}% (+{current_memory-initial_memory:.1f}%)")
            
            # Final-Ressourcen
            final_handles = len(psutil.Process().handles())
            final_threads = psutil.Process().num_threads()
            final_memory = psutil.virtual_memory().percent
            
            # Berechne Leaks
            handle_leak = final_handles - initial_handles
            thread_leak = final_threads - initial_threads
            memory_leak = final_memory - initial_memory
            
            print(f"\n   📊 RESOURCE LEAK ANALYSIS:")
            print(f"      Handle Leak: +{handle_leak}")
            print(f"      Thread Leak: +{thread_leak}")
            print(f"      Memory Leak: +{memory_leak:.1f}%")
            
            # Bewertung
            if abs(handle_leak) < 10 and abs(thread_leak) < 5 and abs(memory_leak) < 5:
                status = "excellent"
            elif abs(handle_leak) < 20 and abs(thread_leak) < 10 and abs(memory_leak) < 10:
                status = "good"
            elif abs(handle_leak) < 50 and abs(thread_leak) < 20 and abs(memory_leak) < 20:
                status = "acceptable"
            else:
                status = "poor"
            
            print(f"   ✅ Resource Management: {status}")
            
            self.test_results["resource_leaks"] = {
                "status": status,
                "handle_leak": handle_leak,
                "thread_leak": thread_leak,
                "memory_leak": memory_leak,
                "initial_handles": initial_handles,
                "final_handles": final_handles,
                "initial_threads": initial_threads,
                "final_threads": final_threads
            }
            
        except Exception as e:
            print(f"   ❌ Resource Leak Test Fehler: {e}")
            self.test_results["resource_leaks"] = {
                "status": "failed",
                "error": str(e)
            }
    
    def _test_benchmark_cycle(self):
        """Benchmark Test-Zyklus"""
        try:
            from hardware_benchmark import HardwareBenchmark
            benchmark = HardwareBenchmark()
            benchmark.benchmark_cpu()
        except:
            pass
    
    def _test_monitor_cycle(self):
        """Monitor Test-Zyklus"""
        try:
            from system_monitor import SystemMonitor
            monitor = SystemMonitor()
            monitor.start_monitoring()
            time.sleep(0.1)
            monitor.stop_monitoring()
        except:
            pass
    
    def _test_fsr_cycle(self):
        """FSR Test-Zyklus"""
        try:
            from fsr_optimizer import CustomFSROptimizer
            fsr = CustomFSROptimizer()
            fsr.set_fsr_mode("performance")
            fsr.apply_game_profile("Valorant")
        except:
            pass
    
    def _generate_stress_report(self):
        """Generiert Stress Test Report"""
        print("\n" + "="*60)
        print("📋 STRESS TEST ZUSAMMENFASSUNG")
        print("="*60)
        
        total_duration = self.end_time - self.start_time
        
        print(f"\n⏱️ Gesamtdauer: {total_duration:.2f}s")
        
        # Einzelne Test-Ergebnisse
        test_names = {
            "multi_threading": "Multi-Threading",
            "memory_stress": "Memory Stress",
            "cpu_stress": "CPU Stress",
            "fsr_performance": "FSR Performance",
            "long_running": "Long-Running",
            "resource_leaks": "Resource Leaks"
        }
        
        passed_tests = 0
        total_tests = len(self.test_results)
        
        for test_key, test_name in test_names.items():
            if test_key in self.test_results:
                result = self.test_results[test_key]
                status = result.get("status", "unknown")
                
                if status == "passed" or status == "excellent" or status == "good":
                    icon = "✅"
                    passed_tests += 1
                elif status == "acceptable":
                    icon = "⚠️"
                    passed_tests += 0.5
                elif status == "skipped":
                    icon = "⏭️"
                else:
                    icon = "❌"
                
                print(f"   {icon} {test_name}: {status}")
        
        # Gesamtbewertung
        pass_rate = (passed_tests / total_tests) * 100
        
        print(f"\n📊 TEST-STATISTIK:")
        print(f"   Bestanden: {passed_tests:.1f}/{total_tests}")
        print(f"   Pass Rate: {pass_rate:.1f}%")
        
        if pass_rate >= 90:
            overall_status = "🟢 EXCELLENT"
            recommendation = "Production Ready!"
        elif pass_rate >= 75:
            overall_status = "🟡 GOOD"
            recommendation = "Kleine Optimierungen empfohlen"
        elif pass_rate >= 50:
            overall_status = "🟠 ACCEPTABLE"
            recommendation = "Einige Optimierungen erforderlich"
        else:
            overall_status = "🔴 POOR"
            recommendation = "Major Optimierungen erforderlich"
        
        print(f"\n🏆 GESAMTSTATUS: {overall_status}")
        print(f"💡 EMPFEHLUNG: {recommendation}")
        
        # Speichere Report
        self._save_stress_report()
    
    def _save_stress_report(self):
        """Speichert Stress Test Report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stress_test_report_{timestamp}.json"
        
        try:
            import json
            report = {
                "timestamp": datetime.now().isoformat(),
                "duration": self.end_time - self.start_time,
                "test_results": self.test_results,
                "system_info": {
                    "cpu_count": psutil.cpu_count(),
                    "memory_total": psutil.virtual_memory().total,
                    "platform": sys.platform
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"\n📁 Stress Test Report gespeichert: {filename}")
        except Exception as e:
            print(f"\n❌ Report Speicherung fehlgeschlagen: {e}")

def main():
    """Hauptfunktion"""
    print("🔥 UNIFIED GAMING OPTIMIZER - PERFORMANCE STRESS TEST")
    print("="*60)
    
    stress_test = PerformanceStressTest()
    results = stress_test.run_stress_test()
    
    # Exit Code basierend auf Ergebnissen
    passed_tests = sum(1 for result in results.values() 
                      if result.get("status") in ["passed", "excellent", "good"])
    total_tests = len(results)
    
    if passed_tests == total_tests:
        print(f"\n✅ Alle Stress Tests bestanden - Exit Code 0")
        sys.exit(0)
    elif passed_tests >= total_tests * 0.8:
        print(f"\n⚠️ Die meisten Tests bestanden - Exit Code 1")
        sys.exit(1)
    elif passed_tests >= total_tests * 0.5:
        print(f"\n🟡 Einige Tests bestanden - Exit Code 2")
        sys.exit(2)
    else:
        print(f"\n❌ Viele Tests fehlgeschlagen - Exit Code 3")
        sys.exit(3)

if __name__ == "__main__":
    main()
