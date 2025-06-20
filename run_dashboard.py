#!/usr/bin/env python3

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.dashboard import PalletOptimizerDashboard

if __name__ == "__main__":
    print("Starting Pallet Logistics Optimizer Dashboard...")
    print("Opening web interface at: http://127.0.0.1:8050")
    print("Loading components...")
    
    dashboard = PalletOptimizerDashboard()
    dashboard.run(debug=True, port=8050)