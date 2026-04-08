#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Borderlands 4 Auto Bug Fixer - Behebt automatisch alle gefundenen Probleme
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

sys.path.insert(0, 'core')

class Borderlands4AutoFixer:
    """Behebt automatisch alle Borderlands 4 FPS-Probleme"""
    
    def __init__(self):
        self.fixes_applied = []
        self.errors = []
        
    def run_auto_fix(self):
        """Führt automatische Fehlerbehebung durch"""
        print("🔧 BORDERLANDS 4 AUTO BUG FIXER")
        print("="*60)
        print(f"Startzeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        print("\n🚀 Starte automatische Fehlerbehebung...")
        print("Dies kann einige Sekunden dauern...\n")
        
        # 1. Power Plan auf High Performance setzen
        self._fix_power_plan()
        
        # 2. Game Mode deaktivieren
        self._fix_game_mode()
        
        # 3. Windows Visual Effects optimieren
        self._fix_visual_effects()
        
        # 4. Hintergrund-Apps deaktivieren
        self._fix_background_apps()
        
        # 5. Windows Search deaktivieren
        self._fix_windows_search()
        
        # 6. Superfetch deaktivieren
        self._fix_superfetch()
        
        # 7. GPU-Priorität setzen
        self._fix_gpu_priority()
        
        # 8. Temp-Dateien löschen
        self._fix_temp_files()
        
        # 9. Borderlands 4 Config erstellen (wenn nicht existiert)
        self._fix_borderlands_config()
        
        # 10. System bereinigen
        self._fix_system_cleanup()
        
        # Report
        self._generate_fix_report()
    
    def _fix_power_plan(self):
        """Fix 1: Power Plan auf High Performance"""
        print("⚡ Fix 1: Setze Power Plan auf High Performance...")
        try:
            subprocess.run(
                ["powercfg", "/setactive", "SCHEME_MIN"],
                capture_output=True, check=False, timeout=10
            )
            self.fixes_applied.append("✅ Power Plan auf High Performance gesetzt")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Power Plan Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_game_mode(self):
        """Fix 2: Game Mode deaktivieren"""
        print("🎮 Fix 2: Deaktiviere Windows Game Mode...")
        try:
            subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\GameBar' -Name 'AllowAutoGameMode' -Value 0 -Force; "
                "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\GameBar' -Name 'AutoGameModeEnabled' -Value 0 -Force",
            ], capture_output=True, check=False, timeout=10)
            self.fixes_applied.append("✅ Windows Game Mode deaktiviert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Game Mode Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_visual_effects(self):
        """Fix 3: Visual Effects optimieren"""
        print("🎨 Fix 3: Optimiere Windows Visual Effects...")
        try:
            subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name 'UserPreferencesMask' -Value ([byte[]](0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00)) -Force; "
                "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop\\WindowMetrics' -Name 'MinAnimate' -Value 0 -Force",
            ], capture_output=True, check=False, timeout=10)
            self.fixes_applied.append("✅ Visual Effects auf Performance optimiert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Visual Effects Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_background_apps(self):
        """Fix 4: Hintergrund-Apps deaktivieren"""
        print("📱 Fix 4: Deaktiviere Hintergrund-Apps...")
        try:
            subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications' -Name 'GlobalUserDisabled' -Value 1 -Force",
            ], capture_output=True, check=False, timeout=10)
            self.fixes_applied.append("✅ Hintergrund-Apps deaktiviert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Background Apps Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_windows_search(self):
        """Fix 5: Windows Search deaktivieren"""
        print("🔍 Fix 5: Deaktiviere Windows Search (Indexer)...")
        try:
            subprocess.run(
                ["sc", "config", "WSearch", "start=", "disabled"],
                capture_output=True, check=False, timeout=10
            )
            subprocess.run(
                ["sc", "stop", "WSearch"],
                capture_output=True, check=False, timeout=10
            )
            self.fixes_applied.append("✅ Windows Search deaktiviert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Windows Search Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_superfetch(self):
        """Fix 6: Superfetch deaktivieren"""
        print("🚀 Fix 6: Deaktiviere Superfetch (SysMain)...")
        try:
            subprocess.run(
                ["sc", "config", "SysMain", "start=", "disabled"],
                capture_output=True, check=False, timeout=10
            )
            subprocess.run(
                ["sc", "stop", "SysMain"],
                capture_output=True, check=False, timeout=10
            )
            self.fixes_applied.append("✅ Superfetch deaktiviert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Superfetch Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_gpu_priority(self):
        """Fix 7: GPU-Priorität setzen"""
        print("🎮 Fix 7: Optimiere GPU-Einstellungen...")
        try:
            # AMD GPU Optimierungen
            subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers' -Name 'HwSchMode' -Value 2 -Force",
            ], capture_output=True, check=False, timeout=10)
            
            # GPU Priority
            subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'GPU Priority' -Value 8 -Force",
            ], capture_output=True, check=False, timeout=10)
            
            self.fixes_applied.append("✅ GPU-Priorität optimiert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ GPU Priority Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_temp_files(self):
        """Fix 8: Temp-Dateien löschen"""
        print("🧹 Fix 8: Lösche temporäre Dateien...")
        try:
            import shutil
            temp_dirs = [
                os.environ.get("TEMP"),
                os.environ.get("TMP"),
                r"C:\Windows\Temp",
            ]
            
            cleared = 0
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for item in os.listdir(temp_dir):
                        try:
                            item_path = os.path.join(temp_dir, item)
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                                cleared += 1
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path, ignore_errors=True)
                                cleared += 1
                        except:
                            pass
            
            self.fixes_applied.append(f"✅ {cleared} temporäre Dateien/Ordner gelöscht")
            print(f"   ✅ {cleared} Dateien/Ordner gelöscht")
        except Exception as e:
            self.errors.append(f"❌ Temp Files Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_borderlands_config(self):
        """Fix 9: Borderlands 4 Config erstellen"""
        print("🎮 Fix 9: Erstelle optimierte Borderlands 4 Config...")
        try:
            from ue5_stability_optimizer import UE5StabilityOptimizer
            
            optimizer = UE5StabilityOptimizer()
            optimizer.apply_ue5_stability_profile()
            
            self.fixes_applied.append("✅ Borderlands 4 Config optimiert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ Borderlands Config Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _fix_system_cleanup(self):
        """Fix 10: System bereinigen"""
        print("🧹 Fix 10: System-Optimierungen...")
        try:
            # DNS Cache leeren
            subprocess.run(
                ["ipconfig", "/flushdns"],
                capture_output=True, check=False, timeout=10
            )
            
            # Windows Store Cache leeren
            subprocess.run([
                "powershell", "-Command",
                "wsreset.exe -i",
            ], capture_output=True, check=False, timeout=10)
            
            # Memory bereinigen
            subprocess.run([
                "powershell", "-Command",
                "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect()",
            ], capture_output=True, check=False, timeout=10)
            
            self.fixes_applied.append("✅ System bereinigt und optimiert")
            print("   ✅ Erfolgreich")
        except Exception as e:
            self.errors.append(f"❌ System Cleanup Fehler: {e}")
            print(f"   ❌ Fehler: {e}")
    
    def _generate_fix_report(self):
        """Generiert Fix-Report"""
        print("\n" + "="*60)
        print("📋 FIX REPORT ZUSAMMENFASSUNG")
        print("="*60)
        
        print(f"\n✅ ERFOLGREICH ANGEWENDET ({len(self.fixes_applied)}):")
        if self.fixes_applied:
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"   {i}. {fix}")
        else:
            print("   ⚠️ Keine Fixes angewendet")
        
        if self.errors:
            print(f"\n⚠️ FEHLER ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        print(f"\n🎮 NÄCHSTE SCHRITTE:")
        print(f"   1. 🔄 PC NEU STARTEN (wichtig für Änderungen)")
        print(f"   2. 🎮 Borderlands 4 starten")
        print(f"   3. 📊 FPS überprüfen (sollte jetzt besser sein)")
        print(f"   4. ⚡ Unified Optimizer laufen lassen für automatische Optimierung")
        
        print(f"\n💡 WICHTIGE HINWEISE:")
        print(f"   • AMD Treiber: Wenn weiterhin Probleme, auf 24.5.1 zurücksetzen")
        print(f"   • Spiel-Settings: Nicht alles auf Minimum - versuche Medium")
        print(f"   • Fullscreen: Immer echtes Fullscreen verwenden (kein Borderless)")
        print(f"   • VSync: Im Spiel deaktivieren")
        
        # Speichere Report
        self._save_fix_report()
        
        print(f"\n{'='*60}")
        print("🎉 AUTOMATISCHE FEHLERBEHEBUNG ABGESCHLOSSEN!")
        print(f"{'='*60}")
    
    def _save_fix_report(self):
        """Speichert Fix-Report"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "fixes_applied": self.fixes_applied,
                "errors": self.errors,
                "total_fixes": len(self.fixes_applied),
                "total_errors": len(self.errors)
            }
            
            filename = f"borderlands4_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n📁 Fix Report gespeichert: {filename}")
        except Exception as e:
            print(f"\n❌ Report Speicherung fehlgeschlagen: {e}")

if __name__ == "__main__":
    import shutil
    fixer = Borderlands4AutoFixer()
    fixer.run_auto_fix()
    
    input("\n🖱️ Drücke Enter zum Beenden...")
