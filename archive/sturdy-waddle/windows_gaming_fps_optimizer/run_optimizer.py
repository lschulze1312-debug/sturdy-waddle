#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Starter Script für Unified Gaming Optimizer
Production-ready mit Fehlerbehandlung und Logging
"""

import sys
import os
import traceback
import logging
from datetime import datetime

# Setup Logging
def setup_logging():
    """Richtet Logging ein"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"optimizer_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def check_dependencies():
    """Prüft alle Dependencies"""
    logger = logging.getLogger(__name__)
    
    required_modules = [
        'psutil',
        'numpy', 
        'cv2',  # OpenCV wird als cv2 importiert
        'win32api',
        'win32con',
        'win32process',
        'matplotlib',
        'json',
        'threading',
        'time',
        'subprocess'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module.startswith('win32'):
                import win32api
                logger.info(f"✅ {module} verfügbar")
            elif module == 'cv2':
                import cv2
                logger.info(f"✅ opencv-python verfügbar")
            else:
                __import__(module)
                logger.info(f"✅ {module} verfügbar")
        except ImportError:
            if module == 'cv2':
                missing_modules.append('opencv-python')
            else:
                missing_modules.append(module)
            logger.error(f"❌ {module} fehlt")
    
    if missing_modules:
        logger.error(f"Fehlende Module: {missing_modules}")
        logger.info("Installieren mit: pip install -r requirements.txt")
        return False
    
    return True

def check_system_compatibility():
    """Prüft System-Kompatibilität"""
    logger = logging.getLogger(__name__)
    
    try:
        import platform
        import psutil
        
        # OS Check
        if platform.system() != "Windows":
            logger.error(f"❌ Nicht-Windows System: {platform.system()}")
            return False
        
        logger.info(f"✅ {platform.system()} {platform.release()}")
        
        # Python Version
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            logger.error(f"❌ Python Version zu alt: {python_version}")
            return False
        
        logger.info(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # PowerShell Check
        try:
            import subprocess
            result = subprocess.run(["powershell", "-Command", "Get-Host"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("✅ PowerShell verfügbar")
            else:
                logger.warning("⚠️ PowerShell nicht verfügbar")
        except:
            logger.warning("⚠️ PowerShell Test fehlgeschlagen")
        
        # Memory Check
        memory = psutil.virtual_memory()
        if memory.total < 4 * 1024**3:  # Weniger als 4GB
            logger.warning(f"⚠️ Weniger als 4GB RAM: {memory.total / (1024**3):.1f}GB")
        else:
            logger.info(f"✅ {memory.total / (1024**3):.1f}GB RAM")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ System-Check Fehler: {e}")
        return False

def safe_import_unified_optimizer():
    """Sicherer Import des Unified Optimizers"""
    logger = logging.getLogger(__name__)
    
    try:
        # Pfade hinzufügen
        sys.path.insert(0, 'core')
        sys.path.insert(0, '../windows_gaming_driver_suite')
        
        # Import mit Fehlerbehandlung
        from unified_optimizer import UnifiedGamingOptimizer
        logger.info("✅ Unified Optimizer importiert")
        return UnifiedGamingOptimizer
        
    except ImportError as e:
        logger.error(f"❌ Import Fehler: {e}")
        logger.error("Stelle sicher, dass alle Dateien vorhanden sind:")
        logger.error("  - unified_optimizer.py")
        logger.error("  - core/real_time_optimizer.py")
        logger.error("  - core/system_monitor.py")
        logger.error("  - core/hardware_benchmark.py")
        logger.error("  - core/fsr_optimizer.py")
        return None
    except Exception as e:
        logger.error(f"❌ Unerwarteter Fehler: {e}")
        logger.error(traceback.format_exc())
        return None

def create_startup_config():
    """Erstellt Startup-Konfiguration"""
    config_file = "startup_config.json"
    
    default_config = {
        "auto_start_monitoring": True,
        "enable_fsr": True,
        "default_profile": "balanced",
        "log_level": "INFO",
        "performance_mode": "gaming",
        "show_system_info": True,
        "enable_auto_optimization": True
    }
    
    if not os.path.exists(config_file):
        import json
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            logging.getLogger(__name__).info(f"✅ Config erstellt: {config_file}")
        except Exception as e:
            logging.getLogger(__name__).error(f"❌ Config Erstellung fehlgeschlagen: {e}")
    
    return config_file

def main():
    """Hauptfunktion"""
    # Logging Setup
    logger = setup_logging()
    
    print("🚀 UNIFIED GAMING OPTIMIZER - STARTUP")
    print("="*60)
    logger.info("Unified Gaming Optimizer wird gestartet")
    
    try:
        # 1. Dependencies prüfen
        print("🔧 Dependencies prüfen...")
        if not check_dependencies():
            print("❌ Dependencies fehlen!")
            print("Installieren mit: pip install -r requirements.txt")
            input("Drücke Enter zum Beenden...")
            return 1
        
        # 2. System-Kompatibilität prüfen
        print("💻 System-Kompatibilität prüfen...")
        if not check_system_compatibility():
            print("❌ System nicht kompatibel!")
            input("Drücke Enter zum Beenden...")
            return 2
        
        # 3. Startup Config erstellen
        print("⚙️ Startup Konfiguration...")
        config_file = create_startup_config()
        
        # 4. Unified Optimizer importieren
        print("📦 Unified Optimizer laden...")
        UnifiedGamingOptimizer = safe_import_unified_optimizer()
        
        if not UnifiedGamingOptimizer:
            print("❌ Unified Optimizer konnte nicht geladen werden!")
            input("Drücke Enter zum Beenden...")
            return 3
        
        # 5. Optimizer starten
        print("🎮 Optimizer starten...")
        optimizer = UnifiedGamingOptimizer()
        
        print("✅ Alle Checks bestanden!")
        print("🚀 Optimizer wird gestartet...")
        print("="*60)
        
        # Starte Optimizer im Hauptthread
        try:
            optimizer.start()
            # Zeige Dashboard
            optimizer.show_menu()
        except KeyboardInterrupt:
            print("\n👋 Programm wird beendet...")
            logger.info("Programm durch Benutzer beendet")
        except Exception as e:
            print(f"❌ Laufzeitfehler: {e}")
            logger.error(f"Laufzeitfehler: {e}")
            logger.error(traceback.format_exc())
            input("Drücke Enter zum Beenden...")
            return 4
        finally:
            # Cleanup
            try:
                optimizer.stop()
                logger.info("Optimizer sauber beendet")
            except:
                pass
        
        print("✅ Optimizer beendet")
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 Startup abgebrochen")
        logger.info("Startup durch Benutzer abgebrochen")
        return 0
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        logger.error(f"Critical Error: {e}")
        logger.error(traceback.format_exc())
        print("\n📋 Fehler-Details:")
        print(traceback.format_exc())
        input("Drücke Enter zum Beenden...")
        return 5

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
