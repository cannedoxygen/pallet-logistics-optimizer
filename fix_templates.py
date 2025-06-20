#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data.excel_handler import ExcelHandler

# Remove old templates
import shutil
try:
    shutil.rmtree('excel_templates')
    print("🗑️  Removed old template files")
except:
    pass

# Create new templates with correct column names
handler = ExcelHandler()
handler.create_template_files()
print("✅ Template files regenerated with correct 'name' columns!")