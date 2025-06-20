#!/usr/bin/env python3

import sys
import os
import webbrowser
import time
from threading import Timer

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.professional_dashboard import ProfessionalPalletDashboard

def open_browser():
    """Open the web browser after a short delay to ensure server is running"""
    webbrowser.open('http://127.0.0.1:8051')

if __name__ == "__main__":
    print("=" * 60)
    print("   PALLET LOGISTICS OPTIMIZER - PROFESSIONAL EDITION")
    print("=" * 60)
    print("🚀 Starting professional dashboard...")
    print("🌐 Web interface will open at: http://127.0.0.1:8051")
    print("📊 Loading business analytics components...")
    print()
    print("📋 Instructions:")
    print("   1. Click 'Load Sample Data' to begin")
    print("   2. Adjust optimization settings as needed")
    print("   3. Click 'Run Optimization' to generate routes")
    print("   4. Explore results in the analytics dashboard")
    print()
    print("⏳ Starting server... (Press Ctrl+C to stop)")
    print("-" * 60)
    
    # Start the dashboard
    dashboard = ProfessionalPalletDashboard()
    
    # Open browser after 2 seconds
    timer = Timer(2.0, open_browser)
    timer.start()
    
    try:
        dashboard.run(debug=False, port=8051)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped. Thank you for using Pallet Logistics Optimizer!")
        sys.exit(0)