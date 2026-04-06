#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test und Benchmark für Unified Gaming Optimizer
"""

import sys
import os
import time
from datetime import datetime

sys.path.insert(0, 'core')

from hardware_benchmark import HardwareBenchmark
from real_time_optimizer import RealTimeOptimizer
from system_monitor import SystemMonitor

def test_hardware_benchmark():
    """Testet Hardware-Benchmark"""
    print("🔥 TESTING HARDWARE BENCHMARK")
    print("="*50)
    
    benchmark = HardwareBenchmark()
    
    # System-Info
    print("\n📋 SYSTEM INFORMATION:")
    info = benchmark.system_info
    print(f"   Platform: {info['platform']}")
    print(f"   CPU: {info['processor']} ({info['cpu_count']} cores)")
    print(f"   Memory: {info['memory_total']}GB total, {info['memory_available']}GB available")
    print(f"   GPU: {info['gpu_name']} ({info['gpu_memory']}MB)")
    
    # Einzelne Benchmarks
    print("\n🧪 RUNNING INDIVIDUAL BENCHMARKS:")
    
    # CPU Benchmark
    cpu_result = benchmark.benchmark_cpu()
    print(f"   CPU Score: {cpu_result['score']:.1f} (Time: {cpu_result['time']:.2f}s)")
    
    # Memory Benchmark
    mem_result = benchmark.benchmark_memory()
    print(f"   Memory Score: {mem_result['score']:.1f} (Time: {mem_result['time']:.2f}s)")
    
    # GPU Benchmark
    gpu_result = benchmark.benchmark_gpu()
    print(f"   GPU Score: {gpu_result['score']:.1f} (Time: {gpu_result['time']:.2f}s)")
    
    # Gesamtergebnis
    overall_score = (cpu_result['score'] + mem_result['score'] + gpu_result['score']) / 3
    print(f"\n📊 OVERALL SCORE: {overall_score:.1f}/100")
    
    return {
        "cpu": cpu_result,
        "memory": mem_result,
        "gpu": gpu_result,
        "overall": overall_score
    }

def test_real_time_optimizer():
    """Testet Real-Time Optimizer"""
    print("\n🚀 TESTING REAL-TIME OPTIMIZER")
    print("="*50)
    
    optimizer = RealTimeOptimizer()
    
    # Starte Monitoring
    print("▶️ Starting monitoring...")
    optimizer.start_monitoring()
    
    # Warte 5 Sekunden für Datensammlung
    print("⏳ Collecting data for 5 seconds...")
    time.sleep(5)
    
    # Metriken abrufen
    metrics = optimizer.system_metrics
    print(f"\n📈 CURRENT METRICS:")
    print(f"   CPU Usage: {metrics['cpu_usage']:.1f}%")
    print(f"   Memory Usage: {metrics['memory_usage']:.1f}%")
    print(f"   GPU Usage: {metrics['gpu_usage']:.1f}%")
    print(f"   Temperature: {metrics['temperature']:.1f}°C")
    
    # Game-Erkennung
    detected_game = optimizer._detect_running_game()
    print(f"   Detected Game: {detected_game or 'None'}")
    
    # Performance-Report
    report = optimizer.get_performance_report()
    print(f"\n📋 PERFORMANCE REPORT:")
    print(f"   Optimization Level: {report['optimization_level']}")
    print(f"   Current Game: {report['current_game']}")
    print(f"   Recommendations: {len(report['recommendations'])}")
    
    # Stoppe Monitoring
    optimizer.stop_monitoring()
    print("⏹️ Monitoring stopped")
    
    return report

def test_system_monitor():
    """Testet System Monitor"""
    print("\n📊 TESTING SYSTEM MONITOR")
    print("="*50)
    
    monitor = SystemMonitor()
    
    # Starte Monitoring
    print("▶️ Starting system monitoring...")
    monitor.start_monitoring()
    
    # Warte 10 Sekunden für Datensammlung
    print("⏳ Collecting data for 10 seconds...")
    time.sleep(10)
    
    # Aktuelle Metriken
    current = monitor.get_current_metrics()
    print(f"\n📈 CURRENT METRICS:")
    print(f"   CPU: {current['cpu_usage']:.1f}%")
    print(f"   Memory: {current['memory_usage']:.1f}%")
    print(f"   GPU: {current['gpu_usage']:.1f}%")
    print(f"   Temperature: {current['temperature']:.1f}°C")
    
    # Performance-Zusammenfassung
    summary = monitor.get_performance_summary()
    print(f"\n📊 PERFORMANCE SUMMARY:")
    print(f"   Performance Score: {summary['performance_score']:.1f}/100")
    print(f"   Status: {summary['status']}")
    print(f"   CPU: Ø {summary['cpu']['average']:.1f}% | Peak {summary['cpu']['peak']:.1f}%")
    print(f"   Memory: Ø {summary['memory']['average']:.1f}% | Peak {summary['memory']['peak']:.1f}%")
    print(f"   GPU: Ø {summary['gpu']['average']:.1f}% | Peak {summary['gpu']['peak']:.1f}%")
    print(f"   Temperature: Ø {summary['temperature']['average']:.1f}°C | Peak {summary['temperature']['peak']:.1f}°C")
    print(f"   Active Alerts: {summary['alerts_count']}")
    
    # Alerts anzeigen
    if monitor.alerts:
        print(f"\n🚨 ALERTS:")
        for alert in monitor.alerts[-5:]:  # Letzte 5
            level_icon = "🔴" if alert["level"] == "critical" else "🟡"
            print(f"   {level_icon} {alert['component']}: {alert['message']}")
    
    # Stoppe Monitoring
    monitor.stop_monitoring()
    print("⏹️ System monitoring stopped")
    
    return summary

def run_comprehensive_test():
    """Führt umfassenden Test durch"""
    print("🎮 UNIFIED GAMING OPTIMIZER - COMPREHENSIVE TEST")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    results = {}
    
    try:
        # 1. Hardware Benchmark
        results['benchmark'] = test_hardware_benchmark()
        
        # 2. Real-Time Optimizer
        results['optimizer'] = test_real_time_optimizer()
        
        # 3. System Monitor
        results['monitor'] = test_system_monitor()
        
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        return None
    
    # Zusammenfassung
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    # Hardware Performance
    hw = results['benchmark']
    print(f"\n🔥 HARDWARE PERFORMANCE:")
    print(f"   CPU Score: {hw['cpu']['score']:.1f}/100")
    print(f"   Memory Score: {hw['memory']['score']:.1f}/100")
    print(f"   GPU Score: {hw['gpu']['score']:.1f}/100")
    print(f"   Overall Score: {hw['overall']:.1f}/100")
    
    # Performance-Kategorie
    if hw['overall'] >= 80:
        category = "🔥 Extreme Gaming"
    elif hw['overall'] >= 60:
        category = "🎮 High-End Gaming"
    elif hw['overall'] >= 40:
        category = "👍 Mid-Range Gaming"
    elif hw['overall'] >= 25:
        category = "⚡ Entry-Level Gaming"
    else:
        category = "💻 Office/Browsing"
    
    print(f"   Category: {category}")
    
    # System Performance
    sys_perf = results['monitor']
    print(f"\n📈 SYSTEM PERFORMANCE:")
    print(f"   Performance Score: {sys_perf['performance_score']:.1f}/100")
    print(f"   Status: {sys_perf['status'].upper()}")
    print(f"   Alerts: {sys_perf['alerts_count']}")
    
    # Optimizer Status
    opt = results['optimizer']
    print(f"\n🚀 OPTIMIZER STATUS:")
    print(f"   Optimization Level: {opt['optimization_level']}")
    print(f"   Active Game: {opt['current_game'] or 'None'}")
    print(f"   Recommendations: {len(opt['recommendations'])}")
    
    # Gesamtbewertung
    overall_hw = hw['overall']
    overall_sys = sys_perf['performance_score']
    combined_score = (overall_hw + overall_sys) / 2
    
    print(f"\n🏆 COMBINED SCORE: {combined_score:.1f}/100")
    
    # Empfehlungen
    print(f"\n💡 RECOMMENDATIONS:")
    if overall_hw < 50:
        print("   🔧 Hardware-Upgrade empfohlen")
    if sys_perf['performance_score'] < 60:
        print("   ⚡ System-Optimierung empfohlen")
    if opt['current_game']:
        print(f"   🎮 Gaming-Optimierung für {opt['current_game']} aktiv")
    else:
        print("   💻 Kein Game erkannt - Normalmodus")
    
    print(f"\n✅ TEST COMPLETED SUCCESSFULLY")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results

if __name__ == "__main__":
    results = run_comprehensive_test()
    
    if results:
        print(f"\n🎯 All tests passed! Ready for production use.")
    else:
        print(f"\n❌ Tests failed. Check the errors above.")
