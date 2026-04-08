    
    def _bg_optimizer_menu(self):
        """Background Process Optimizer Menü"""
        print(f"\n🔧 HINTERGRUNDPROZESSE OPTIMIERUNG")
        print("="*50)
        
        print(f"Status: {'🟢 AKTIV' if self.bg_optimizer.active else '🔴 INAKTIV'}")
        if self.bg_optimizer.active:
            report = self.bg_optimizer.get_optimization_report()
            print(f"Deaktivierte Services: {report['disabled_services']}")
            print(f"Beendete Prozesse: {report['killed_processes']}")
            print(f"System-Auslastung: CPU {report['system_metrics']['cpu_after']:.1f}%, Memory {report['system_metrics']['memory_after']:.1f}%")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] Optimierung starten/stoppen")
        print("   [2] Services verwalten")
        print("   [3] Temp-Dateien löschen")
        print("   [4] Windows-Einstellungen optimieren")
        print("   [5] Status anzeigen")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self._toggle_bg_optimizer()
        elif choice == "2":
            self._manage_services_menu()
        elif choice == "3":
            self._clear_temp_files_manual()
        elif choice == "4":
            self._optimize_windows_settings_menu()
        elif choice == "5":
            self.bg_optimizer.print_status()
        elif choice == "0":
            return
    
    def _toggle_bg_optimizer(self):
        """Background Process Optimizer starten/stoppen"""
        if self.bg_optimizer.active:
            self.bg_optimizer.stop_optimization()
            print("⏹️ Hintergrundprozess-Optimierung gestoppt")
        else:
            self.bg_optimizer.start_optimization()
            print("▶️ Hintergrundprozess-Optimierung gestartet")
    
    def _manage_services_menu(self):
        """Services-Verwaltung Menü"""
        print(f"\n⚙️ SERVICES VERWALTEN")
        print("="*50)
        
        print(f"Unnötige Services die deaktiviert werden:")
        for i, service in enumerate(self.bg_optimizer.unnecessary_services[:10], 1):
            print(f"   {i}. {service}")
        
        if len(self.bg_optimizer.unnecessary_services) > 10:
            print(f"   ... und {len(self.bg_optimizer.unnecessary_services) - 10} weitere")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] Alle Services deaktivieren")
        print("   [2] Services wiederherstellen")
        print("   [3] Gaming-Modus aktivieren")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self.bg_optimizer._optimize_services()
            print("✅ Services deaktiviert")
        elif choice == "2":
            self.bg_optimizer._restore_services()
            print("✅ Services wiederhergestellt")
        elif choice == "3":
            self.bg_optimizer.optimization_settings["disable_windows_update"] = True
            self.bg_optimizer.optimization_settings["disable_superfetch"] = True
            self.bg_optimizer.optimization_settings["disable_windows_search"] = True
            self.bg_optimizer._optimize_services()
            self.bg_optimizer._optimize_windows_settings()
            print("✅ Gaming-Modus aktiviert - Alle unnötigen Services deaktiviert")
        elif choice == "0":
            return
    
    def _clear_temp_files_manual(self):
        """Temp-Dateien manuell löschen"""
        print(f"\n🧹 TEMP-DATEIEN LÖSCHEN")
        print("="*50)
        
        print("Lösche temporäre Dateien...")
        self.bg_optimizer._clear_temp_files()
    
    def _optimize_windows_settings_menu(self):
        """Windows-Einstellungen optimieren"""
        print(f"\n⚙️ WINDOWS-EINSTELLUNGEN OPTIMIEREN")
        print("="*50)
        
        print(f"Aktuelle Einstellungen:")
        for setting, enabled in self.bg_optimizer.optimization_settings.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {setting.replace('_', ' ').title()}")
        
        print(f"\n🔧 OPTIONEN:")
        print("   [1] Alle Einstellungen optimieren")
        print("   [2] Visual Effects optimieren")
        print("   [3] Hintergrund-Apps deaktivieren")
        print("   [4] Power Plan optimieren")
        print("   [0] Zurück")
        
        choice = input(f"\nWähle Option: ").strip()
        
        if choice == "1":
            self.bg_optimizer._optimize_windows_settings()
            print("✅ Alle Windows-Einstellungen optimiert")
        elif choice == "2":
            self.bg_optimizer._optimize_visual_effects()
            print("✅ Visual Effects optimiert")
        elif choice == "3":
            self.bg_optimizer._disable_background_apps()
            print("✅ Hintergrund-Apps deaktiviert")
        elif choice == "4":
            self.bg_optimizer._optimize_power_plan()
            print("✅ Power Plan optimiert")
        elif choice == "0":
            return

