#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hardware Database - Erweiterte Hardware-Datenbank mit echten System-Spezifikationen
"""

# Deine System-Spezifikationen
USER_SYSTEM_SPECS = {
    "cpu": {
        "name": "AMD Ryzen 7 7735HS with Radeon Graphics",
        "cores_physical": 8,
        "cores_logical": 16,
        "frequency_max": 3201,
        "score": 85,  # High-End Laptop CPU
        "category": "high_end_mobile"
    },
    "gpu": {
        "integrated": {
            "name": "AMD Radeon(TM) Graphics",
            "memory_mb": 512,
            "type": "integrated",
            "score": 25
        },
        "dedicated": {
            "name": "AMD Radeon RX 7600S",
            "memory_mb": 4096,
            "type": "dedicated",
            "score": 70,  # Mid-High Range Gaming GPU
            "category": "mid_range_gaming"
        }
    },
    "memory": {
        "total_gb": 15.24,
        "type": "DDR5",  # Typisch für Ryzen 7000 Serie
        "speed_mhz": 4800,  # DDR5-4800 Standard
        "score": 60
    },
    "storage": {
        "type": "NVMe SSD",
        "capacity_gb": 928,
        "score": 80
    },
    "motherboard": {
        "manufacturer": "ASUSTeK COMPUTER INC.",
        "model": "ASUS TUF Gaming A16 FA617NS_FA617NS",
        "chipset": "AMD Ryzen 7000 Serie",
        "score": 70
    }
}

# Erweiterte Hardware-Datenbank
HARDWARE_DATABASE = {
    "cpus": {
        # Intel Desktop CPUs
        "Intel Core i3-12100": {"score": 40, "cores": 4, "threads": 8, "base_clock": 3.6, "boost_clock": 4.3, "category": "entry"},
        "Intel Core i5-12400": {"score": 55, "cores": 6, "threads": 12, "base_clock": 2.5, "boost_clock": 4.4, "category": "mid_range"},
        "Intel Core i5-13600K": {"score": 75, "cores": 14, "threads": 20, "base_clock": 3.5, "boost_clock": 5.1, "category": "high_end"},
        "Intel Core i7-12700K": {"score": 80, "cores": 12, "threads": 20, "base_clock": 3.6, "boost_clock": 4.9, "category": "high_end"},
        "Intel Core i9-13900K": {"score": 95, "cores": 24, "threads": 32, "base_clock": 3.0, "boost_clock": 5.8, "category": "extreme"},
        
        # AMD Desktop CPUs
        "AMD Ryzen 3 7330U": {"score": 35, "cores": 4, "threads": 8, "base_clock": 2.3, "boost_clock": 4.3, "category": "entry"},
        "AMD Ryzen 5 7600X": {"score": 70, "cores": 6, "threads": 12, "base_clock": 4.7, "boost_clock": 5.3, "category": "high_end"},
        "AMD Ryzen 7 7700X": {"score": 80, "cores": 8, "threads": 16, "base_clock": 4.5, "boost_clock": 5.4, "category": "high_end"},
        "AMD Ryzen 9 7950X": {"score": 95, "cores": 16, "threads": 32, "base_clock": 4.5, "boost_clock": 5.7, "category": "extreme"},
        
        # Mobile CPUs (deine Kategorie)
        "AMD Ryzen 7 7735HS": {"score": 85, "cores": 8, "threads": 16, "base_clock": 3.5, "boost_clock": 4.75, "category": "high_end_mobile"},
        "Intel Core i7-13700H": {"score": 80, "cores": 14, "threads": 20, "base_clock": 3.7, "boost_clock": 5.0, "category": "high_end_mobile"},
        "Intel Core i9-13900HX": {"score": 90, "cores": 24, "threads": 32, "base_clock": 3.9, "boost_clock": 5.4, "category": "extreme_mobile"},
        
        # Legacy CPUs (für Kompatibilität)
        "Intel Core i3-8100": {"score": 30, "cores": 4, "threads": 4, "base_clock": 3.6, "boost_clock": 3.6, "category": "legacy"},
        "Intel Core i5-8400": {"score": 45, "cores": 6, "threads": 6, "base_clock": 2.8, "boost_clock": 4.0, "category": "legacy"},
        "Intel Core i7-8700": {"score": 60, "cores": 6, "threads": 12, "base_clock": 3.2, "boost_clock": 4.6, "category": "legacy"},
        "Intel Core i9-9900": {"score": 75, "cores": 8, "threads": 16, "base_clock": 3.1, "boost_clock": 5.0, "category": "legacy"},
        "AMD Ryzen 3 1200": {"score": 25, "cores": 4, "threads": 4, "base_clock": 3.1, "boost_clock": 3.4, "category": "legacy"},
        "AMD Ryzen 5 2600": {"score": 50, "cores": 6, "threads": 12, "base_clock": 3.4, "boost_clock": 3.9, "category": "legacy"},
        "AMD Ryzen 7 2700": {"score": 65, "cores": 8, "threads": 16, "base_clock": 3.2, "boost_clock": 4.1, "category": "legacy"},
        "AMD Ryzen 9 3900": {"score": 80, "cores": 12, "threads": 24, "base_clock": 3.1, "boost_clock": 4.3, "category": "legacy"}
    },
    
    "gpus": {
        # NVIDIA RTX 40 Series
        "NVIDIA RTX 4050": {"score": 55, "vram": 6144, "memory_clock": 14000, "tdp": 120, "category": "entry_gaming"},
        "NVIDIA RTX 4060": {"score": 65, "vram": 8192, "memory_clock": 14000, "tdp": 115, "category": "mid_range_gaming"},
        "NVIDIA RTX 4060 Ti": {"score": 75, "vram": 8192, "memory_clock": 18000, "tdp": 160, "category": "high_end_gaming"},
        "NVIDIA RTX 4070": {"score": 80, "vram": 12288, "memory_clock": 21000, "tdp": 200, "category": "high_end_gaming"},
        "NVIDIA RTX 4070 Ti": {"score": 85, "vram": 12288, "memory_clock": 21000, "tdp": 285, "category": "extreme_gaming"},
        "NVIDIA RTX 4080": {"score": 90, "vram": 16384, "memory_clock": 23000, "tdp": 320, "category": "extreme_gaming"},
        "NVIDIA RTX 4090": {"score": 95, "vram": 24576, "memory_clock": 25000, "tdp": 450, "category": "extreme_gaming"},
        
        # AMD RX 7000 Series
        "AMD RX 7600": {"score": 60, "vram": 8192, "memory_clock": 18000, "tdp": 165, "category": "mid_range_gaming"},
        "AMD RX 7600 XT": {"score": 65, "vram": 16384, "memory_clock": 18000, "tdp": 190, "category": "mid_range_gaming"},
        "AMD RX 7700 XT": {"score": 75, "vram": 12288, "memory_clock": 19000, "tdp": 230, "category": "high_end_gaming"},
        "AMD RX 7800 XT": {"score": 80, "vram": 16384, "memory_clock": 19000, "tdp": 263, "category": "high_end_gaming"},
        "AMD RX 7900 XT": {"score": 85, "vram": 20480, "memory_clock": 20000, "tdp": 315, "category": "extreme_gaming"},
        "AMD RX 7900 XTX": {"score": 90, "vram": 24576, "memory_clock": 24000, "tdp": 355, "category": "extreme_gaming"},
        
        # Mobile GPUs (deine GPU)
        "AMD Radeon RX 7600S": {"score": 70, "vram": 4096, "memory_clock": 16000, "tdp": 75, "category": "mid_range_mobile"},
        "NVIDIA RTX 4060 Laptop": {"score": 68, "vram": 8192, "memory_clock": 14000, "tdp": 60, "category": "mid_range_mobile"},
        "NVIDIA RTX 4070 Laptop": {"score": 75, "vram": 8192, "memory_clock": 16000, "tdp": 80, "category": "high_end_mobile"},
        
        # Legacy GPUs
        "NVIDIA GTX 1050": {"score": 25, "vram": 2048, "memory_clock": 7000, "category": "legacy"},
        "NVIDIA GTX 1060": {"score": 40, "vram": 6072, "memory_clock": 8000, "category": "legacy"},
        "NVIDIA GTX 1070": {"score": 55, "vram": 8192, "memory_clock": 8000, "category": "legacy"},
        "NVIDIA GTX 1080": {"score": 70, "vram": 8192, "memory_clock": 10000, "category": "legacy"},
        "NVIDIA RTX 2060": {"score": 60, "vram": 6144, "memory_clock": 14000, "category": "legacy"},
        "NVIDIA RTX 2070": {"score": 75, "vram": 8192, "memory_clock": 14000, "category": "legacy"},
        "NVIDIA RTX 2080": {"score": 85, "vram": 8192, "memory_clock": 14000, "category": "legacy"},
        "AMD RX 570": {"score": 35, "vram": 4096, "memory_clock": 7000, "category": "legacy"},
        "AMD RX 580": {"score": 45, "vram": 8192, "memory_clock": 8000, "category": "legacy"},
        "AMD RX 590": {"score": 50, "vram": 8192, "memory_clock": 8000, "category": "legacy"},
        "AMD RX 5600": {"score": 65, "vram": 6144, "memory_clock": 14000, "category": "legacy"},
        "AMD RX 5700": {"score": 75, "vram": 8192, "memory_clock": 14000, "category": "legacy"}
    },
    
    "games": {
        # Competitive Shooters (High FPS Required)
        "CS:GO": {"cpu_req": 30, "gpu_req": 25, "ram_req": 4, "fps_target": 240, "category": "competitive"},
        "Valorant": {"cpu_req": 35, "gpu_req": 30, "ram_req": 4, "fps_target": 240, "category": "competitive"},
        "Apex Legends": {"cpu_req": 50, "gpu_req": 45, "ram_req": 8, "fps_target": 144, "category": "competitive"},
        "Overwatch 2": {"cpu_req": 45, "gpu_req": 40, "ram_req": 6, "fps_target": 144, "category": "competitive"},
        
        # Battle Royale
        "Fortnite": {"cpu_req": 50, "gpu_req": 55, "ram_req": 8, "fps_target": 144, "category": "battle_royale"},
        "PUBG": {"cpu_req": 60, "gpu_req": 65, "ram_req": 8, "fps_target": 60, "category": "battle_royale"},
        "Warzone": {"cpu_req": 70, "gpu_req": 75, "ram_req": 12, "fps_target": 120, "category": "battle_royale"},
        
        # AAA RPGs (High Quality)
        "Cyberpunk 2077": {"cpu_req": 80, "gpu_req": 85, "ram_req": 12, "fps_target": 60, "category": "aaa_rpg"},
        "The Witcher 3": {"cpu_req": 60, "gpu_req": 65, "ram_req": 8, "fps_target": 60, "category": "aaa_rpg"},
        "Elden Ring": {"cpu_req": 70, "gpu_req": 75, "ram_req": 12, "fps_target": 60, "category": "aaa_rpg"},
        "Starfield": {"cpu_req": 85, "gpu_req": 90, "ram_req": 16, "fps_target": 60, "category": "aaa_rpg"},
        
        # Racing Games
        "Forza Horizon 5": {"cpu_req": 70, "gpu_req": 75, "ram_req": 12, "fps_target": 60, "category": "racing"},
        "Assetto Corsa": {"cpu_req": 60, "gpu_req": 70, "ram_req": 8, "fps_target": 144, "category": "racing"},
        
        # Strategy Games
        "Civilization VI": {"cpu_req": 40, "gpu_req": 35, "ram_req": 8, "fps_target": 60, "category": "strategy"},
        "Age of Empires IV": {"cpu_req": 50, "gpu_req": 45, "ram_req": 8, "fps_target": 60, "category": "strategy"}
    }
}

# Game-spezifische Optimierungen für dein System
USER_SYSTEM_OPTIMIZATIONS = {
    "fortnite": {
        "recommended_settings": {
            "resolution": "1920x1080",
            "quality": "High",
            "shadows": "Medium",
            "effects": "High",
            "view_distance": "Epic",
            "post_processing": "Medium"
        },
        "expected_fps": 120,
        "optimization_tips": [
            "FidelityFX Super Resolution 1.0 für +20% FPS",
            "Epic Quality Settings mit DLSS",
            "120Hz Display für competitive advantage"
        ]
    },
    "valorant": {
        "recommended_settings": {
            "resolution": "1920x1080",
            "quality": "Low",
            "shadows": "Off",
            "effects": "Low",
            "ui": "Low"
        },
        "expected_fps": 240,
        "optimization_tips": [
            "Low Settings für maximale FPS",
            "Uncapped Framerate",
            "NVIDIA Reflex Latenz-Reduktion"
        ]
    },
    "cyberpunk_2077": {
        "recommended_settings": {
            "resolution": "1920x1080",
            "quality": "Medium",
            "ray_tracing": "Off",
            "fsr": "Ultra Performance",
            "textures": "High"
        },
        "expected_fps": 60,
        "optimization_tips": [
            "FSR 2.1 für +40% Performance",
            "Ray Tracing deaktivieren für +30% FPS",
            "Dynamic Resolution Scaling"
        ]
    }
}

def get_user_system_performance():
    """Berechnet Performance-Score für dein System"""
    cpu_score = USER_SYSTEM_SPECS["cpu"]["score"]
    gpu_score = USER_SYSTEM_SPECS["gpu"]["dedicated"]["score"]
    memory_score = USER_SYSTEM_SPECS["memory"]["score"]
    storage_score = USER_SYSTEM_SPECS["storage"]["score"]
    
    # Gewichteter Durchschnitt
    weights = {"cpu": 0.25, "gpu": 0.35, "memory": 0.15, "storage": 0.25}
    overall_score = (
        cpu_score * weights["cpu"] +
        gpu_score * weights["gpu"] +
        memory_score * weights["memory"] +
        storage_score * weights["storage"]
    )
    
    return {
        "cpu": cpu_score,
        "gpu": gpu_score,
        "memory": memory_score,
        "storage": storage_score,
        "overall": round(overall_score, 1),
        "category": get_performance_category(overall_score)
    }

def get_performance_category(score):
    """Gibt Performance-Kategorie zurück"""
    if score >= 85:
        return "🔥 Extreme Gaming"
    elif score >= 70:
        return "🎮 High-End Gaming"
    elif score >= 55:
        return "👍 Mid-Range Gaming"
    elif score >= 40:
        return "⚡ Entry-Level Gaming"
    else:
        return "💻 Office/Browsing"

def get_game_recommendations(game_name):
    """Gibt Game-spezifische Empfehlungen für dein System"""
    game_key = game_name.lower().replace(" ", "_").replace(":", "")
    
    if game_key in USER_SYSTEM_OPTIMIZATIONS:
        return USER_SYSTEM_OPTIMIZATIONS[game_key]
    
    # Generische Empfehlung basierend auf System-Score
    system_perf = get_user_system_performance()
    
    if system_perf["overall"] >= 70:
        return {
            "recommended_settings": "High/Ultra Settings",
            "expected_fps": "60+ FPS",
            "optimization_tips": ["Maximale Qualität genießen", "Ray Tracing aktivieren wenn unterstützt"]
        }
    elif system_perf["overall"] >= 55:
        return {
            "recommended_settings": "Medium/High Settings",
            "expected_fps": "45-60 FPS",
            "optimization_tips": ["Balanced Settings", "FSR/DLSS nutzen"]
        }
    else:
        return {
            "recommended_settings": "Low/Medium Settings",
            "expected_fps": "30-45 FPS",
            "optimization_tips": ["Low Settings für FPS", "Auflösung reduzieren"]
        }

if __name__ == "__main__":
    # System-Performance anzeigen
    perf = get_user_system_performance()
    print("🎮 DEIN SYSTEM PERFORMANCE")
    print("="*50)
    print(f"CPU: AMD Ryzen 7 7735HS - {perf['cpu']}/100")
    print(f"GPU: AMD Radeon RX 7600S - {perf['gpu']}/100")
    print(f"Memory: 15.24GB DDR5 - {perf['memory']}/100")
    print(f"Storage: 928GB NVMe SSD - {perf['storage']}/100")
    print(f"Overall: {perf['overall']}/100 - {perf['category']}")
    
    # Game-Empfehlungen
    print(f"\n🎯 GAME EMPFEHLUNGEN:")
    for game in ["Fortnite", "Valorant", "Cyberpunk 2077"]:
        rec = get_game_recommendations(game)
        print(f"\n{game}:")
        print(f"   Settings: {rec['recommended_settings']}")
        print(f"   FPS: {rec['expected_fps']}")
        print(f"   Tips: {', '.join(rec['optimization_tips'][:2])}")
