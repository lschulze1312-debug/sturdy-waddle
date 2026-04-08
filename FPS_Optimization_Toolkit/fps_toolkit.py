#!/usr/bin/env python3
"""
FPS Optimization Toolkit
Professionelles Windows-Gaming-Optimierungstool
"""

from fps_toolkit.core.optimizer import SystemOptimizer
from fps_toolkit.gui.main_window import MainWindow


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
