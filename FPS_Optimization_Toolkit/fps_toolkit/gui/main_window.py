import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ModernButton(tk.Button):
    def __init__(self, master, text, command, color, **kwargs):
        super().__init__(
            master, text=text, command=command,
            bg=color, fg="white", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", padx=20, pady=10, **kwargs
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.default_bg = color
    
    def _on_enter(self, e):
        self["bg"] = self._lighten(self.default_bg)
    
    def _on_leave(self, e):
        self["bg"] = self.default_bg
    
    @staticmethod
    def _lighten(hex_color):
        return hex_color


class ModernCheckbutton(tk.Checkbutton):
    def __init__(self, master, text, variable, **kwargs):
        super().__init__(
            master, text=text, variable=variable,
            bg="#252526", fg="white", font=("Segoe UI", 9),
            selectcolor="#00ff88", activebackground="#252526",
            activeforeground="white", anchor="w", **kwargs
        )


class DummyMonitor:
    """Dummy monitor when real monitor fails to initialize"""
    def is_admin(self):
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
    
    def get_all_info(self):
        class DummyInfo:
            pass
        cpu = DummyInfo()
        cpu.name = "Unknown CPU"
        gpu = DummyInfo()
        gpu.name = "Unknown GPU"
        ram = DummyInfo()
        ram.total_gb = 0
        ram.available_gb = 0
        return {"cpu": cpu, "gpu": gpu, "ram": ram}
    
    def get_cpu_info(self):
        class DummyInfo:
            pass
        info = DummyInfo()
        info.usage = 0
        return info
    
    def get_ram_info(self):
        class DummyInfo:
            pass
        info = DummyInfo()
        info.usage_percent = 0
        return info
    
    def get_temps(self):
        class DummyTemps:
            pass
        temps = DummyTemps()
        temps.cpu = None
        temps.gpu = None
        return temps


class MainWindow:
    def __init__(self):
        # LAZY INITIALIZATION
        self._opt = None
        self._mon = None
        self._active = False
        self._lock = threading.Lock()  # Thread-Safety Lock
        
        self._log_early("MainWindow.__init__ starting...")
        
        # ROOT WINDOW
        self.root = tk.Tk()
        self.root.title("FPS Optimization Toolkit v2.0")
        self.root.geometry("800x650")
        self.root.minsize(750, 600)
        self.root.configure(bg="#1e1e1e")
        
        self._log_early("Tk root created")
        
        # Checkbox-Variablen
        self.check_vars = {
            "kill_apps": tk.BooleanVar(value=True),
            "stop_services": tk.BooleanVar(value=True),
            "high_priority": tk.BooleanVar(value=True),
            "power_plan": tk.BooleanVar(value=True),
            "visual_effects": tk.BooleanVar(value=True),
            "gpu_tweaks": tk.BooleanVar(value=True),
            "clear_memory": tk.BooleanVar(value=False),
            "network": tk.BooleanVar(value=False),
            "defender": tk.BooleanVar(value=False),
            "superfetch": tk.BooleanVar(value=False),
            "game_dvr": tk.BooleanVar(value=True),
            "fullscreen_opt": tk.BooleanVar(value=True),
            "qos": tk.BooleanVar(value=False),
            "timer_res": tk.BooleanVar(value=False),
        }
        
        self._center_window()
        self._log_early("Building UI...")
        self._build_ui()
        self._log_early("UI built, updating system info...")
        self._update_system_info()
        self._log_early("Starting monitoring...")
        self._start_monitoring()
        self._log_early("MainWindow.__init__ complete")

    @property
    def opt(self):
        """Lazy initialization of SystemOptimizer"""
        if self._opt is None:
            self._log_early("Creating SystemOptimizer (lazy)...")
            try:
                from fps_toolkit.core.optimizer import SystemOptimizer
                self._opt = SystemOptimizer()
                self._log_early("SystemOptimizer created successfully")
            except Exception as e:
                self._log_early(f"ERROR creating SystemOptimizer: {e}")
                import traceback
                self._log_early(traceback.format_exc())
                raise
        return self._opt
    
    @property
    def mon(self):
        """Lazy initialization of SystemMonitor"""
        if self._mon is None:
            self._log_early("Creating SystemMonitor (lazy)...")
            try:
                from fps_toolkit.core.monitor import SystemMonitor
                self._mon = SystemMonitor()
                self._log_early("SystemMonitor created successfully")
            except Exception as e:
                self._log_early(f"ERROR creating SystemMonitor: {e}")
                self._mon = DummyMonitor()
                self._log_early("Using DummyMonitor as fallback")
        return self._mon
    
    def _log_early(self, msg):
        """Early logging with immediate flush"""
        logger.info(f"[EARLY] {msg}")
        for handler in logger.handlers:
            if hasattr(handler, 'flush'):
                handler.flush()

    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#252526", height=60)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        tk.Label(header, text="FPS OPTIMIZATION TOOLKIT",
                font=("Segoe UI", 18, "bold"), bg="#252526", fg="#00ff88").pack(pady=15)

        # Main content
        content = tk.Frame(self.root, bg="#1e1e1e")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Left panel
        left_panel = tk.Frame(content, bg="#252526", bd=1, relief=tk.FLAT)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # System Info
        tk.Label(left_panel, text="SYSTEM INFO", font=("Segoe UI", 11, "bold"),
                bg="#252526", fg="white").pack(pady=10)

        self.sys_frame = tk.Frame(left_panel, bg="#252526")
        self.sys_frame.pack(fill="x", padx=15, pady=5)

        self.sys_labels = {}
        for key, label in [("cpu", "CPU"), ("gpu", "GPU"), ("ram", "RAM")]:
            row = tk.Frame(self.sys_frame, bg="#252526")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{label}:", bg="#252526", fg="#aaaaaa",
                    font=("Segoe UI", 9), width=8, anchor="w").pack(side="left")
            lbl = tk.Label(row, text="--", bg="#252526", fg="white",
                         font=("Segoe UI", 9), anchor="w")
            lbl.pack(side="left", fill="x", expand=True)
            self.sys_labels[key] = lbl

        # Usage bars
        self.usage_frame = tk.Frame(left_panel, bg="#252526")
        self.usage_frame.pack(fill="x", padx=15, pady=10)
        
        self.usage_bars = {}
        for key, label in [("cpu", "CPU Usage"), ("ram", "RAM Usage")]:
            tk.Label(self.usage_frame, text=label, bg="#252526", fg="#aaaaaa",
                    font=("Segoe UI", 8)).pack(anchor="w", pady=(5,0))
            bar_frame = tk.Frame(self.usage_frame, bg="#3c3c3c", height=8)
            bar_frame.pack(fill="x", pady=(2,5))
            bar_frame.pack_propagate(False)
            bar = tk.Frame(bar_frame, bg="#00ff88", width=0)
            bar.pack(side="left", fill="y")
            self.usage_bars[key] = bar

        # Temps
        tk.Label(left_panel, text="TEMPERATURES", font=("Segoe UI", 10, "bold"),
                bg="#252526", fg="white").pack(pady=(15,5))
        
        self.temp_frame = tk.Frame(left_panel, bg="#252526")
        self.temp_frame.pack(fill="x", padx=15)
        
        self.temp_cpu = tk.Label(self.temp_frame, text="CPU: --C", bg="#252526",
                                fg="white", font=("Segoe UI", 10))
        self.temp_cpu.pack(side="left", padx=5)
        
        self.temp_gpu = tk.Label(self.temp_frame, text="GPU: --C", bg="#252526",
                                fg="white", font=("Segoe UI", 10))
        self.temp_gpu.pack(side="left", padx=5)

        # Checkboxes
        checkbox_frame = tk.LabelFrame(left_panel, text="OPTIMIERUNGEN AUSWaeHLEN",
                                       bg="#252526", fg="white",
                                       font=("Segoe UI", 10, "bold"),
                                       padx=10, pady=5)
        checkbox_frame.pack(fill="x", padx=15, pady=15)
        
        cb_frame = tk.Frame(checkbox_frame, bg="#252526")
        cb_frame.pack(fill="x")
        
        left_cb = tk.Frame(cb_frame, bg="#252526")
        left_cb.pack(side="left", fill="y", expand=True)
        
        right_cb = tk.Frame(cb_frame, bg="#252526")
        right_cb.pack(side="right", fill="y", expand=True)
        
        # Basis
        tk.Label(left_cb, text="Basis", bg="#252526", fg="#00ff88",
                font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", pady=(0,5))
        
        ModernCheckbutton(left_cb, "Hintergrund-Apps beenden", self.check_vars["kill_apps"]).pack(fill="x", pady=2)
        ModernCheckbutton(left_cb, "Services stoppen", self.check_vars["stop_services"]).pack(fill="x", pady=2)
        ModernCheckbutton(left_cb, "Hohe Prioritaet setzen", self.check_vars["high_priority"]).pack(fill="x", pady=2)
        ModernCheckbutton(left_cb, "Power-Plan optimieren", self.check_vars["power_plan"]).pack(fill="x", pady=2)
        ModernCheckbutton(left_cb, "Visuelle Effekte deaktivieren", self.check_vars["visual_effects"]).pack(fill="x", pady=2)
        ModernCheckbutton(left_cb, "GPU-Tweaks", self.check_vars["gpu_tweaks"]).pack(fill="x", pady=2)
        
        # Erweitert
        tk.Label(right_cb, text="Erweitert", bg="#252526", fg="#00ff88",
                font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", pady=(0,5))
        
        ModernCheckbutton(right_cb, "Speicher bereinigen", self.check_vars["clear_memory"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "Netzwerk optimieren", self.check_vars["network"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "Windows Defender RT deakt.", self.check_vars["defender"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "Superfetch deaktivieren", self.check_vars["superfetch"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "Game DVR deaktivieren", self.check_vars["game_dvr"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "Fullscreen-Optimierung", self.check_vars["fullscreen_opt"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "QoS Packet Priority", self.check_vars["qos"]).pack(fill="x", pady=2)
        ModernCheckbutton(right_cb, "Timer-Resolution", self.check_vars["timer_res"]).pack(fill="x", pady=2)

        # Button frame
        btn_select_frame = tk.Frame(checkbox_frame, bg="#252526")
        btn_select_frame.pack(fill="x", pady=(10,0))
        
        tk.Button(btn_select_frame, text="Alle auswaehlen", command=self._select_all,
                 bg="#3c3c3c", fg="white", relief=tk.FLAT, cursor="hand2",
                 font=("Segoe UI", 8)).pack(side="left", padx=5)
        
        tk.Button(btn_select_frame, text="Keine auswaehlen", command=self._select_none,
                 bg="#3c3c3c", fg="white", relief=tk.FLAT, cursor="hand2",
                 font=("Segoe UI", 8)).pack(side="left", padx=5)
        
        tk.Button(btn_select_frame, text="Nur Basis", command=self._select_basic,
                 bg="#3c3c3c", fg="white", relief=tk.FLAT, cursor="hand2",
                 font=("Segoe UI", 8)).pack(side="left", padx=5)

        # Right panel
        right_panel = tk.Frame(content, bg="#252526", width=250)
        right_panel.pack(side="right", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="CONTROLS", font=("Segoe UI", 11, "bold"),
                bg="#252526", fg="white").pack(pady=10)

        btn_frame = tk.Frame(right_panel, bg="#252526")
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.optimize_btn = ModernButton(btn_frame, "OPTIMIZE NOW",
                                        self._on_optimize, "#28a745")
        self.optimize_btn.pack(fill="x", pady=5)

        self.restore_btn = ModernButton(btn_frame, "RESTORE",
                                        self._on_restore, "#dc3545")
        self.restore_btn.pack(fill="x", pady=5)
        self.restore_btn.config(state="disabled")

        # Log area
        tk.Label(right_panel, text="LOG", font=("Segoe UI", 10, "bold"),
                bg="#252526", fg="white").pack(pady=(20,5))
        
        self.log_area = scrolledtext.ScrolledText(
            right_panel, height=12, bg="#1e1e1e", fg="#cccccc",
            font=("Consolas", 9), relief=tk.FLAT, wrap=tk.WORD
        )
        self.log_area.pack(fill="both", expand=True, padx=15, pady=5)
        self.log_area.config(state="disabled")

        # Status bar
        self.status_bar = tk.Label(
            self.root, text="Ready - Select optimizations and click OPTIMIZE NOW",
            bd=0, relief=tk.FLAT, anchor="w", font=("Segoe UI", 9),
            bg="#007acc", fg="white", padx=10, pady=5
        )
        self.status_bar.pack(side="bottom", fill="x")

        # Admin warning
        if not self.mon.is_admin():
            self._log("WARNING: Not running as administrator. Some features will be limited.")
            self._log("Right-click -> Run as Administrator for full functionality.")

    def _select_all(self):
        for var in self.check_vars.values():
            var.set(True)

    def _select_none(self):
        for var in self.check_vars.values():
            var.set(False)

    def _select_basic(self):
        for key, var in self.check_vars.items():
            if key in ["kill_apps", "stop_services", "high_priority", "power_plan",
                      "visual_effects", "gpu_tweaks", "game_dvr", "fullscreen_opt"]:
                var.set(True)
            else:
                var.set(False)

    def _update_system_info(self):
        try:
            info = self.mon.get_all_info()
            
            cpu = info["cpu"]
            self.sys_labels["cpu"].config(text=f"{cpu.name[:35]}" if len(cpu.name) > 35 else cpu.name)
            
            gpu = info["gpu"]
            self.sys_labels["gpu"].config(text=f"{gpu.name[:35]}" if len(gpu.name) > 35 else gpu.name)
            
            ram = info["ram"]
            self.sys_labels["ram"].config(text=f"{ram.total_gb} GB ({ram.available_gb} GB free)")
        except Exception as e:
            logger.error(f"Error updating system info: {e}")

    def _start_monitoring(self):
        def monitor():
            while True:
                try:
                    # Check if root window still exists
                    if not self.root.winfo_exists():
                        break
                    
                    cpu_info = self.mon.get_cpu_info()
                    ram_info = self.mon.get_ram_info()
                    temps = self.mon.get_temps()
                    
                    # FIX: Use after() for thread-safe GUI updates
                    self.root.after(0, lambda c=cpu_info, r=ram_info, t=temps: self._update_ui(c, r, t))
                    
                    time.sleep(2)
                except Exception:
                    time.sleep(2)
        
        threading.Thread(target=monitor, daemon=True).start()
    
    def _update_ui(self, cpu_info, ram_info, temps):
        """Thread-safe UI update"""
        try:
            # Update usage bars
            cpu_width = min(int(cpu_info.usage), 100)
            self.usage_bars["cpu"].config(
                width=int(self.usage_frame.winfo_width() * cpu_width / 100))
            self.usage_bars["cpu"].config(
                bg="#ff4444" if cpu_info.usage > 80 else "#00ff88")
            
            ram_width = min(int(ram_info.usage_percent), 100)
            self.usage_bars["ram"].config(
                width=int(self.usage_frame.winfo_width() * ram_width / 100))
            
            # Update temps
            cpu_temp = temps.cpu or "--"
            gpu_temp = temps.gpu or "--"
            
            cpu_color = "#ff4444" if temps.cpu and temps.cpu > 80 else "#00ff88" if temps.cpu and temps.cpu < 60 else "#ffaa00"
            self.temp_cpu.config(text=f"CPU: {cpu_temp}C", fg=cpu_color)
            self.temp_gpu.config(text=f"GPU: {gpu_temp}C")
        except Exception:
            pass  # Ignore GUI update errors

    def _log(self, message):
        self.log_area.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert("end", f"[{timestamp}] {message}\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def _get_selected_options(self):
        return {key: var.get() for key, var in self.check_vars.items()}

    def _on_optimize(self):
        options = self._get_selected_options()
        
        if not any(options.values()):
            messagebox.showwarning("No Selection", "Please select at least one optimization option.")
            return
        
        self.optimize_btn.config(state="disabled")
        self.status_bar.config(text="Optimizing system...")
        self._log(f"Starting optimization with {sum(options.values())} options selected...")
        self._log("Check fps_optimizer.log for detailed progress...")

        def run():
            import time
            start_time = time.time()
            try:
                logger.info(f"[GUI Thread] Starting optimization thread")
                results = self.opt.optimize_full(options)
                elapsed = time.time() - start_time
                logger.info(f"[GUI Thread] Optimization completed in {elapsed:.1f}s")
                
                self.root.after(0, lambda: self._on_optimize_done(results))
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"[GUI Thread] Optimization failed after {elapsed:.1f}s: {e}")
                import traceback
                logger.error(traceback.format_exc())
                self.root.after(0, lambda: self._on_optimize_error(str(e)))

        threading.Thread(target=run, daemon=True).start()

    def _on_optimize_done(self, results):
        """Called when optimization is complete"""
        with self._lock:
            self._active = True
        self.optimize_btn.config(state="disabled")
        self.restore_btn.config(state="normal")
        
        self._log("Optimization complete!")
        
        # Pruefe ob Neustart empfohlen wird
        needs_restart = any([
            results.visual_effects_disabled,
            results.game_dvr_disabled,
            results.fullscreen_optimized,
            results.power_optimized,
            results.gpu_tweaks,
            results.defender_disabled,
            results.superfetch_disabled
        ])
        
        message = "System optimization completed successfully!"
        if needs_restart:
            message += "\n\n For some changes to take full effect, a system restart is recommended."
        
        messagebox.showinfo("Optimization Complete", message)

        # Access dataclass attributes
        try:
            if results.apps_killed:
                self._log(f"  - {len(results.apps_killed)} background processes terminated")
            if results.services_stopped:
                self._log(f"  - {len(results.services_stopped)} services stopped")
            if results.power_optimized:
                self._log("  - Power plan set to High Performance")
            if results.visual_effects_disabled:
                self._log("  - Visual effects disabled")
            if results.gpu_tweaks:
                self._log(f"  - GPU tweaks applied: {', '.join(results.gpu_tweaks)}")
            if results.network_optimized:
                self._log("  - Network optimized")
            if results.defender_disabled:
                self._log("  - Windows Defender RT disabled")
            if results.superfetch_disabled:
                self._log("  - Superfetch disabled")
            if results.game_dvr_disabled:
                self._log("  - Game DVR disabled")
            if results.fullscreen_optimized:
                self._log("  - Fullscreen optimizations disabled")
            if results.qos_optimized:
                self._log("  - QoS packet priority set")
            if results.timer_optimized:
                self._log("  - Timer resolution optimized")
            if results.memory_cleared:
                self._log("  - Memory cleared")
            
            if results.errors:
                self._log(f"  - {len(results.errors)} errors occurred")
            
            success_count = sum([
                bool(results.apps_killed),
                bool(results.services_stopped),
                results.power_optimized,
                results.priority_set,
                results.visual_effects_disabled,
                bool(results.gpu_tweaks),
                results.network_optimized,
                results.defender_disabled,
                results.superfetch_disabled,
                results.game_dvr_disabled,
                results.fullscreen_optimized,
                results.qos_optimized,
                results.timer_optimized,
                results.memory_cleared
            ])
            
            self.status_bar.config(text=f"Optimized: {success_count} optimizations applied")
            
        except Exception as e:
            logger.error(f"Error in _on_optimize_done: {e}")
            self._log(f"Error processing results: {e}")
        finally:
            with self._lock:
                self._active = True  # Optimization is active (completed)

    def _on_optimize_error(self, error):
        self.optimize_btn.config(state="normal")
        self.status_bar.config(text="Optimization failed")
        self._log(f"ERROR: {error}")
        messagebox.showerror("Error", f"Optimization failed:\n{error}")

    def _on_restore(self):
        self.restore_btn.config(state="disabled")
        self.status_bar.config(text="Restoring system...")
        self._log("Restoring system state...")

        def run():
            try:
                restored = self.opt.restore()
                self.root.after(0, lambda: self._on_restore_done(restored))
            except Exception as e:
                self.root.after(0, lambda: self._on_restore_error(str(e)))

        threading.Thread(target=run, daemon=True).start()

    def _on_restore_done(self, restored):
        self.optimize_btn.config(state="normal")
        self.restore_btn.config(state="disabled")
        
        # FIX: Correct dictionary keys from restore() method
        procs = restored.get("processes_restarted", 0)
        svcs = restored.get("services_started", 0)
        
        self._log(f"Restore complete!")
        self._log(f"  - {procs} processes restarted")
        self._log(f"  - {svcs} services started")
        
        self.status_bar.config(text="System restored - Select optimizations to optimize again")

    def _on_restore_error(self, error):
        self.restore_btn.config(state="normal")
        self._log(f"Restore ERROR: {error}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
