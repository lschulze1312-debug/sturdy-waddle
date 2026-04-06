#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Script - Einfacher Start für Gaming Optimizer
"""

import sys
import os

def quick_start():
    """Quick Start Funktion"""
    print("🎮 UNIFIED GAMING OPTIMIZER - QUICK START")
    print("="*50)
    
    # Wechsle zum richtigen Verzeichnis
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"📁 Arbeitsverzeichnis: {os.getcwd()}")
    
    # Prüfe ob Hauptdatei existiert
    if not os.path.exists("run_optimizer.py"):
        print("❌ run_optimizer.py nicht gefunden!")
        print("Stelle sicher, dass du im richtigen Verzeichnis bist.")
        input("Drücke Enter zum Beenden...")
        return
    
    # Starte Hauptprogramm
    try:
        print("🚀 Starte Gaming Optimizer...")
        os.system("python run_optimizer.py")
    except KeyboardInterrupt:
        print("\n👋 Programm beendet")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        input("Drücke Enter zum Beenden...")

if __name__ == "__main__":
    quick_start()
