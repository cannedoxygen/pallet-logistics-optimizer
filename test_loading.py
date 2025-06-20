#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data.excel_handler import ExcelHandler

print('=== TESTING EXCEL LOADING ===')
handler = ExcelHandler()

try:
    stores = handler.load_stores()
    print(f'✅ Successfully loaded {len(stores)} stores!')
    for store in stores[:2]:
        print(f'   - {store.name} (ID: {store.id})')
except Exception as e:
    print(f'❌ Store loading failed: {e}')

try:
    suppliers = handler.load_suppliers()
    print(f'✅ Successfully loaded {len(suppliers)} suppliers!')
    for supplier in suppliers[:2]:
        print(f'   - {supplier.name} (ID: {supplier.id})')
except Exception as e:
    print(f'❌ Supplier loading failed: {e}')

print('\n=== LOADING TEST COMPLETE ===')