#!/usr/bin/env python3
"""
Test script to verify the Load Sample Data functionality works correctly.
This will test the exact same path that the dashboard uses.
"""
import sys
import os
import traceback

# Add src to path for imports (same as dashboard)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data.excel_handler import ExcelHandler

def test_load_sample_data():
    """Test the exact same code path that the dashboard Load Sample Data button uses"""
    print("🧪 Testing Load Sample Data functionality...")
    print("=" * 60)
    
    try:
        # This is the exact same code from professional_dashboard.py line 208
        excel_handler = ExcelHandler()
        print("✅ Excel handler created successfully")
        
        # Load stores (line 208 in dashboard)
        print("\n📍 Loading stores...")
        stores = excel_handler.load_stores()
        print(f"✅ Successfully loaded {len(stores)} stores")
        
        # Display store information (same as dashboard lines 212-221)
        stores_data = []
        for store in stores:
            store_info = {
                'id': store.id,
                'name': store.name,
                'city': store.location.city,
                'state': store.location.state,
                'demand_pallets': store.demand_pallets,
                'latitude': store.location.latitude,
                'longitude': store.location.longitude
            }
            stores_data.append(store_info)
            print(f"   Store: {store.name} ({store.location.city}, {store.location.state})")
        
        # Load suppliers (line 209 in dashboard)
        print("\n🏭 Loading suppliers...")
        suppliers = excel_handler.load_suppliers()
        print(f"✅ Successfully loaded {len(suppliers)} suppliers")
        
        # Display supplier information (same as dashboard lines 223-234)
        suppliers_data = []
        for supplier in suppliers:
            supplier_info = {
                'id': supplier.id,
                'name': supplier.name,
                'city': supplier.location.city,
                'state': supplier.location.state,
                'available_pallets': supplier.available_pallets,
                'cost_per_pallet': supplier.cost_per_pallet,
                'latitude': supplier.location.latitude,
                'longitude': supplier.location.longitude
            }
            suppliers_data.append(supplier_info)
            print(f"   Supplier: {supplier.name} ({supplier.location.city}, {supplier.location.state})")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS: Load Sample Data test completed without errors!")
        print(f"📊 Summary: {len(stores)} stores, {len(suppliers)} suppliers loaded")
        print("✅ No 'store_name' errors detected!")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()
        print("\n" + "=" * 60)
        return False

if __name__ == "__main__":
    success = test_load_sample_data()
    sys.exit(0 if success else 1)