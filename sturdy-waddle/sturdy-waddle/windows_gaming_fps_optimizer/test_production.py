#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Test - Testet die production-ready Version
"""

import sys
import os
import time
import traceback

def test_imports():
    """Testet alle Imports"""
    print("🔧 TESTING IMPORTS")
    print("-" * 30)
    
    try:
        sys.path.insert(0, 'core')
        
        # Test Core Module
        from real_time_optimizer import RealTimeOptimizer
        print("   ✅ RealTimeOptimizer")
        
        from system_monitor import SystemMonitor
        print("   ✅ SystemMonitor")
        
        from hardware_benchmark import HardwareBenchmark
        print("   ✅ HardwareBenchmark")
        
        from fsr_optimizer import CustomFSROptimizer
        print("   ✅ CustomFSROptimizer")
        
        # Test Unified Optimizer
        from unified_optimizer import UnifiedGamingOptimizer
        print("   ✅ UnifiedGamingOptimizer")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import Fehler: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Testet grundlegende Funktionalität"""
    print("\n🎮 TESTING BASIC FUNCTIONALITY")
    print("-" * 30)
    
    try:
        from unified_optimizer import UnifiedGamingOptimizer
        
        # Erstelle Optimizer
        optimizer = UnifiedGamingOptimizer()
        print("   ✅ Optimizer erstellt")
        
        # Test Konfiguration
        if optimizer.config:
            print("   ✅ Konfiguration geladen")
        else:
            print("   ❌ Konfiguration nicht geladen")
            return False
        
        # Test Profile
        if optimizer.profiles:
            print(f"   ✅ {len(optimizer.profiles)} Profile")
        else:
            print("   ❌ Keine Profile")
            return False
        
        # Test Hardware Benchmark
        print("   🔥 Hardware Benchmark...")
        hw_result = optimizer.hardware_benchmark.run_full_benchmark()
        if hw_result:
            print(f"   ✅ Benchmark Score: {hw_result.get('overall_score', 0):.1f}")
        else:
            print("   ❌ Benchmark fehlgeschlagen")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Funktions-Test Fehler: {e}")
        traceback.print_exc()
        return False

def test_fsr_functionality():
    """Testet FSR Funktionalität"""
    print("\n🚀 TESTING FSR FUNCTIONALITY")
    print("-" * 30)
    
    try:
        from fsr_optimizer import CustomFSROptimizer
        
        fsr = CustomFSROptimizer()
        print("   ✅ FSR Optimizer erstellt")
        
        # Test Modi
        modes = ["ultra_performance", "performance", "balanced"]
        for mode in modes:
            fsr.set_fsr_mode(mode)
            print(f"   ✅ FSR Modus: {mode}")
        
        # Test Game Profile
        games = ["Valorant", "Fortnite"]
        for game in games:
            fsr.apply_game_profile(game)
            print(f"   ✅ Game Profil: {game}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ FSR Test Fehler: {e}")
        traceback.print_exc()
        return False

def test_system_monitoring():
    """Testet System Monitoring"""
    print("\n📊 TESTING SYSTEM MONITORING")
    print("-" * 30)
    
    try:
        from system_monitor import SystemMonitor
        
        monitor = SystemMonitor()
        print("   ✅ System Monitor erstellt")
        
        # Kurzer Test
        monitor.start_monitoring()
        time.sleep(2)
        
        metrics = monitor.get_current_metrics()
        if metrics:
            print(f"   ✅ Metrics: CPU {metrics['cpu_usage']:.1f}%")
        else:
            print("   ❌ Keine Metrics")
            return False
        
        monitor.stop_monitoring()
        print("   ✅ Monitoring gestoppt")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Monitoring Test Fehler: {e}")
        traceback.print_exc()
        return False

def main():
    """Hauptfunktion"""
    print("🧪 PRODUCTION TEST")
    print("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("FSR Functionality", test_fsr_functionality),
        ("System Monitoring", test_system_monitoring)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 TEST RESULTS: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - PRODUCTION READY!")
        return 0
    elif passed >= total * 0.8:
        print("⚠️ MOST TESTS PASSED - NEARLY READY")
        return 1
    else:
        print("❌ MANY TESTS FAILED - NOT READY")
        return 2

if __name__ == "__main__":
    exit_code = main()
    input("\nDrücke Enter zum Beenden...")
    sys.exit(exit_code)
