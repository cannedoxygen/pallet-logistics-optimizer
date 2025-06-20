#!/usr/bin/env python3
"""
Vercel entry point for Pallet Logistics Optimizer
"""
import os
import sys

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from src.gui.professional_dashboard import ProfessionalPalletDashboard

# Create the dashboard instance
dashboard = ProfessionalPalletDashboard()

# Vercel expects the app to be available as 'app'
app = dashboard.app.server

if __name__ == "__main__":
    dashboard.run(debug=False, port=8050)