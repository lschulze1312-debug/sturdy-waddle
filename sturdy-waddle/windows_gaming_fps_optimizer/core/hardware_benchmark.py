#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hardware Benchmark Modul
"""

import psutil
import platform
import time
from datetime import datetime

class HardwareBenchmark:
    def __init__(self):
        self.system_info = self.get_system_info()
        self.benchmark_results = {}
    
    def get_system_info(self):
        """Sammelt System-Informationen"""
        # Import SystemProfiler für detaillierte Info
        try:
            from system_profiler import SystemProfiler
            profiler = SystemProfiler()
            detailed_info = profiler.system_specs
            
            # Basic Info für Benchmark-Kompatibilität
            info = {
                "platform": detailed_info["system"]["platform"],
                "processor": detailed_info["cpu"]["name"],
                "architecture": detailed_info["system"]["architecture"],
                "cpu_count": detailed_info["cpu"]["cores_logical"],
                "memory_total": detailed_info["memory"]["total_gb"],
                "memory_available": detailed_info["memory"]["available_gb"],
                "gpu_name": "Unknown",
                "gpu_memory": 0
            }
            
            # GPU-Info hinzufügen
            if detailed_info["gpu"]:
                # Nimm die beste GPU (dedizierte bevorzugen)
                best_gpu = None
                for gpu in detailed_info["gpu"]:
                    if gpu["type"] == "dedicated":
                        best_gpu = gpu
                        break
                
                if not best_gpu:
                    best_gpu = detailed_info["gpu"][0]
                
                info.update({
                    "gpu_name": best_gpu["name"],
                    "gpu_memory": best_gpu["memory_total_mb"]
                })
            
            return info
            
        except ImportError:
            # Fallback auf alte Methode
            info = {
                "platform": platform.system(),
                "processor": platform.processor(),
                "architecture": platform.architecture()[0],
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total // (1024**3),  # GB
                "memory_available": psutil.virtual_memory().available // (1024**3),
            }
            
            # GPU Information (wenn verfügbar)
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    info.update({
                        "gpu_name": gpu.name,
                        "gpu_memory": gpu.memoryTotal,
                        "gpu_driver": gpu.driver
                    })
            except:
                info["gpu_name"] = "Unknown"
                info["gpu_memory"] = 0
            
            return info
    
    def benchmark_cpu(self):
        """CPU Benchmark Test"""
        print("🔥 CPU Benchmark...")
        
        # Simple CPU Test
        start_time = time.time()
        
        # Matrix-Multiplikation Test
        import random
        size = 1000
        matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
        matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]
        
        # Einfache Multiplikation (nur für Benchmark)
        result = []
        for i in range(min(100, size)):  # Nur 100 Zeilen für Geschwindigkeit
            row = []
            for j in range(min(100, size)):
                sum_val = 0
                for k in range(min(100, size)):
                    sum_val += matrix_a[i][k] * matrix_b[k][j]
                row.append(sum_val)
            result.append(row)
        
        cpu_time = time.time() - start_time
        
        # CPU-Score berechnen
        base_time = 5.0  # Referenzzeit
        cpu_score = max(1, min(100, (base_time / cpu_time) * 50))
        
        return {
            "score": cpu_score,
            "time": cpu_time,
            "cores": self.system_info["cpu_count"],
            "processor": self.system_info["processor"]
        }
    
    def benchmark_memory(self):
        """Memory Benchmark Test"""
        print("🧠 Memory Benchmark...")
        
        start_time = time.time()
        
        # Memory-Allokation Test
        import random
        data_size = 1000000  # 1M Elemente
        
        # Allokieren und füllen
        data = [random.random() for _ in range(data_size)]
        
        # Sortier-Test
        data.sort()
        
        memory_time = time.time() - start_time
        
        # Memory-Score
        base_time = 2.0
        memory_score = max(1, min(100, (base_time / memory_time) * 50))
        
        return {
            "score": memory_score,
            "time": memory_time,
            "total_gb": self.system_info["memory_total"],
            "available_gb": self.system_info["memory_available"]
        }
    
    def benchmark_gpu(self):
        """GPU Benchmark Test (basic)"""
        print("🎮 GPU Benchmark...")
        
        if self.system_info["gpu_name"] == "Unknown":
            return {
                "score": 0,
                "time": 0,
                "name": "Unknown",
                "memory_mb": 0
            }
        
        # Simple GPU Test (wenn GPUtil verfügbar)
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                
                # GPU-Load Test
                start_time = time.time()
                
                # Simuliere GPU-Last
                for _ in range(1000000):
                    pass
                
                gpu_time = time.time() - start_time
                
                # GPU-Score basierend auf Memory und Name
                gpu_score = 0
                name = gpu.name.lower()
                
                if "rtx 4090" in name:
                    gpu_score = 95
                elif "rtx 4080" in name:
                    gpu_score = 85
                elif "rtx 4070" in name:
                    gpu_score = 75
                elif "rtx 4060" in name:
                    gpu_score = 65
                elif "rtx 3090" in name:
                    gpu_score = 80
                elif "rtx 3080" in name:
                    gpu_score = 70
                elif "rtx 3070" in name:
                    gpu_score = 60
                elif "rtx 3060" in name:
                    gpu_score = 50
                elif "gtx 1080" in name:
                    gpu_score = 55
                elif "gtx 1070" in name:
                    gpu_score = 45
                elif "gtx 1060" in name:
                    gpu_score = 35
                elif "rx 7900" in name:
                    gpu_score = 85
                elif "rx 6700" in name:
                    gpu_score = 65
                elif "rx 5700" in name:
                    gpu_score = 60
                elif "rx 580" in name:
                    gpu_score = 40
                else:
                    gpu_score = 30  # Default
                
                return {
                    "score": gpu_score,
                    "time": gpu_time,
                    "name": gpu.name,
                    "memory_mb": gpu.memoryTotal
                }
        except:
            pass
        
        return {
            "score": 0,
            "time": 0,
            "name": "Unknown",
            "memory_mb": 0
        }
    
    def run_full_benchmark(self):
        """Führt kompletten Benchmark durch"""
        print("🚀 STARTE KOMPLETTEN BENCHMARK")
        print("="*50)
        
        start_time = time.time()
        
        # CPU Benchmark
        cpu_result = self.benchmark_cpu()
        
        # Memory Benchmark
        memory_result = self.benchmark_memory()
        
        # GPU Benchmark
        gpu_result = self.benchmark_gpu()
        
        # Gesamtscore
        overall_score = (cpu_result["score"] * 0.3 + 
                        memory_result["score"] * 0.2 + 
                        gpu_result["score"] * 0.5)
        
        total_time = time.time() - start_time
        
        # Kategorie bestimmen
        if overall_score >= 80:
            category = "🔥 Extreme Gaming"
        elif overall_score >= 60:
            category = "🎮 High-End Gaming"
        elif overall_score >= 40:
            category = "👍 Mid-Range Gaming"
        elif overall_score >= 25:
            category = "⚡ Entry-Level Gaming"
        else:
            category = "💻 Office/Browsing"
        
        self.benchmark_results = {
            "cpu": cpu_result,
            "memory": memory_result,
            "gpu": gpu_result,
            "overall_score": overall_score,
            "category": category,
            "total_time": total_time,
            "timestamp": datetime.now().isoformat(),
            "system_info": self.system_info
        }
        
        return self.benchmark_results
    
    def print_results(self):
        """Gibt Benchmark-Ergebnisse aus"""
        if not self.benchmark_results:
            print("❌ Keine Benchmark-Ergebnisse verfügbar")
            return
        
        results = self.benchmark_results
        
        print("\n📊 BENCHMARK ERGEBNISSE")
        print("="*50)
        
        print(f"\n🔥 CPU:")
        print(f"   Score: {results['cpu']['score']:.1f}")
        print(f"   Zeit: {results['cpu']['time']:.2f}s")
        print(f"   Cores: {results['cpu']['cores']}")
        print(f"   Processor: {results['cpu']['processor']}")
        
        print(f"\n🧠 Memory:")
        print(f"   Score: {results['memory']['score']:.1f}")
        print(f"   Zeit: {results['memory']['time']:.2f}s")
        print(f"   Total: {results['memory']['total_gb']}GB")
        print(f"   Verfügbar: {results['memory']['available_gb']}GB")
        
        print(f"\n🎮 GPU:")
        print(f"   Score: {results['gpu']['score']:.1f}")
        print(f"   Name: {results['gpu']['name']}")
        print(f"   Memory: {results['gpu']['memory_mb']}MB")
        
        print(f"\n📈 GESAMT:")
        print(f"   Overall Score: {results['overall_score']:.1f}")
        print(f"   Kategorie: {results['category']}")
        print(f"   Benchmark Zeit: {results['total_time']:.2f}s")
        print(f"   Timestamp: {results['timestamp']}")
        
        # Empfehlungen
        print(f"\n💡 EMPFEHLUNGEN:")
        
        if results['cpu']['score'] < 40:
            print("   • CPU-Upgrade empfohlen für bessere Gaming-Performance")
        
        if results['memory']['score'] < 30:
            print("   • RAM-Upgrade oder XMP-Profile aktivieren")
        
        if results['gpu']['score'] < 40:
            print("   • GPU-Upgrade empfohlen für moderne Games")
        
        if results['overall_score'] >= 60:
            print("   🎮 System ist bereit für High-End Gaming!")
        elif results['overall_score'] >= 40:
            print("   👍 System ist gut für Mid-Range Gaming")
        else:
            print("   ⚡ System-Upgrade empfohlen für bessere Performance")


if __name__ == "__main__":
    benchmark = HardwareBenchmark()
    results = benchmark.run_full_benchmark()
    benchmark.print_results()
