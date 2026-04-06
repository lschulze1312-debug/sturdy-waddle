#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gui import FPSOptimizerGUI


def main():
    app = FPSOptimizerGUI()
    app.run()


if __name__ == "__main__":
    main()
