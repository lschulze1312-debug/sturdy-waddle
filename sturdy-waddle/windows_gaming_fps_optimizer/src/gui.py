import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

from optimizer import Optimizer
from system import SystemInfo


class FPSOptimizerGUI:
    def __init__(self):
        self.opt = Optimizer()
        self.sys = SystemInfo()
        self.root = tk.Tk()
        self.root.title("FPS Optimizer")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.active = False
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="FPS Optimizer", font=("Arial", 16, "bold")).pack(pady=10)

        info_frame = tk.LabelFrame(self.root, text="System", padx=10, pady=5)
        info_frame.pack(fill="x", padx=20, pady=5)

        self.sys_labels = {}
        for key in ["cpu", "gpu", "ram"]:
            lbl = tk.Label(info_frame, text=f"{key.upper()}: --", anchor="w")
            lbl.pack(fill="x")
            self.sys_labels[key] = lbl

        self.temp_label = tk.Label(info_frame, text="Temps: --", anchor="w")
        self.temp_label.pack(fill="x")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        self.opt_btn = tk.Button(btn_frame, text="Optimieren", command=self._optimize,
                                 bg="#4CAF50", fg="white", width=15, height=2)
        self.opt_btn.pack(side="left", padx=5)

        self.restore_btn = tk.Button(btn_frame, text="Wiederherstellen", command=self._restore,
                                      bg="#f44336", fg="white", width=15, height=2, state="disabled")
        self.restore_btn.pack(side="left", padx=5)

        self.status = tk.Label(self.root, text="Bereit", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status.pack(side="bottom", fill="x")

        self._update_sys_info()
        self._start_monitoring()

    def _update_sys_info(self):
        info = self.sys.all()
        self.sys_labels["cpu"].config(text=f"CPU: {info['cpu']['name'][:30]}...")
        self.sys_labels["gpu"].config(text=f"GPU: {info['gpu']['name'][:30]}...")
        self.sys_labels["ram"].config(text=f"RAM: {info['ram']['total_gb']} GB")

    def _start_monitoring(self):
        def monitor():
            while True:
                temps = self.sys.temperatures()
                cpu_temp = temps.get("cpu") or "--"
                gpu_temp = temps.get("gpu") or "--"
                self.temp_label.config(text=f"Temps: CPU {cpu_temp}°C | GPU {gpu_temp}°C")
                time.sleep(3)
        threading.Thread(target=monitor, daemon=True).start()

    def _optimize(self):
        if not self.sys.is_admin():
            messagebox.showwarning("Hinweis", "Programm als Administrator ausführen für volle Funktionalität")

        self.status.config(text="Optimiere...")
        self.opt_btn.config(state="disabled")

        def run():
            results = self.opt.optimize_full()
            killed = len(results.get("apps_killed", []))
            stopped = len(results.get("services_stopped", []))
            self.root.after(0, lambda: self._on_optimize_done(killed, stopped))

        threading.Thread(target=run, daemon=True).start()

    def _on_optimize_done(self, killed, stopped):
        self.active = True
        self.opt_btn.config(state="disabled")
        self.restore_btn.config(state="normal")
        self.status.config(text=f"Fertig: {killed} Apps, {stopped} Services")
        messagebox.showinfo("Erledigt", f"{killed} Hintergrund-Apps beendet\n{stopped} Services gestoppt")

    def _restore(self):
        self.status.config(text="Stelle wieder her...")
        def run():
            self.opt.restore()
            self.root.after(0, self._on_restore_done)
        threading.Thread(target=run, daemon=True).start()

    def _on_restore_done(self):
        self.active = False
        self.opt_btn.config(state="normal")
        self.restore_btn.config(state="disabled")
        self.status.config(text="Wiederhergestellt")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FPSOptimizerGUI()
    app.run()
