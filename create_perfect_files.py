#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_perfect_excel_files():
    """Create Excel files with EXACT column structure the code expects"""
    
    data_dir = Path("data/input")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔧 Creating Excel files with EXACT expected column structure...")
    
    # Store locations - EXACT columns the code expects
    stores_data = [
        {
            'store_id': 'WM001',
            'name': 'Walmart Supercenter - Downtown Chicago',  # EXACT: 'name' not 'store_name'
            'address': '100 N State St',
            'city': 'Chicago',
            'state': 'IL',
            'zip_code': '60601',
            'latitude': 41.8781,
            'longitude': -87.6298,
            'demand_pallets': 45,
            'priority': 1,  # EXACT: integer not text
            'contact_info': 'manager@walmart.com'
        },
        {
            'store_id': 'TG002',
            'name': 'Target Express - Milwaukee Downtown',
            'address': '250 E Wisconsin Ave',
            'city': 'Milwaukee',
            'state': 'WI',
            'zip_code': '53202',
            'latitude': 43.0389,
            'longitude': -87.9065,
            'demand_pallets': 32,
            'priority': 2,
            'contact_info': 'contact@target.com'
        },
        {
            'store_id': 'KR003',
            'name': 'Kroger Fresh Market - Indianapolis',
            'address': '455 E Market St',
            'city': 'Indianapolis',
            'state': 'IN',
            'zip_code': '46202',
            'latitude': 39.7684,
            'longitude': -86.1581,
            'demand_pallets': 38,
            'priority': 1,
            'contact_info': 'manager@kroger.com'
        },
        {
            'store_id': 'CS004',
            'name': 'Costco Wholesale - St. Louis',
            'address': '1234 Veterans Memorial Pkwy',
            'city': 'St. Louis',
            'state': 'MO',
            'zip_code': '63146',
            'latitude': 38.6270,
            'longitude': -90.1994,
            'demand_pallets': 65,
            'priority': 1,
            'contact_info': 'bulk@costco.com'
        }
    ]
    
    # Supplier data - EXACT columns the code expects
    suppliers_data = [
        {
            'supplier_id': 'FL_CHICAGO_001',
            'name': 'Frito-Lay Chicago Distribution Center',  # EXACT: 'name' not 'supplier_name'
            'address': '5000 S Cicero Ave',
            'city': 'Chicago',
            'state': 'IL',
            'zip_code': '60632',
            'latitude': 41.7886,
            'longitude': -87.7505,
            'available_pallets': 180,
            'cost_per_pallet': 125.50,
            'lead_time_days': 1,
            'capacity_per_day': 200,
            'reliability_score': 0.985,
            'contact_info': 'dispatch@fritolay.com'
        },
        {
            'supplier_id': 'FL_INDY_002',
            'name': 'Frito-Lay Indianapolis Regional Hub',
            'address': '3200 Industrial Blvd',
            'city': 'Indianapolis',
            'state': 'IN',
            'zip_code': '46241',
            'latitude': 39.7173,
            'longitude': -86.2944,
            'available_pallets': 145,
            'cost_per_pallet': 118.75,
            'lead_time_days': 1,
            'capacity_per_day': 150,
            'reliability_score': 0.972,
            'contact_info': 'indy@fritolay.com'
        }
    ]
    
    # Historical orders - EXACT columns the code expects
    orders_data = [
        {
            'order_id': 'FL_2024_001',
            'store_id': 'WM001',
            'supplier_id': 'FL_CHICAGO_001',
            'quantity': 42,  # EXACT: 'quantity' not 'pallets_ordered'
            'requested_date': '2024-01-15',  # EXACT: 'requested_date' not 'date'
            'priority': 1,  # EXACT: integer not text
            'special_instructions': 'Loading dock 3'
        },
        {
            'order_id': 'FL_2024_002',
            'store_id': 'TG002',
            'supplier_id': 'FL_INDY_002',
            'quantity': 30,
            'requested_date': '2024-01-16',
            'priority': 2,
            'special_instructions': 'Weekend delivery OK'
        }
    ]
    
    # Toll rates - EXACT columns the code expects
    toll_data = [
        {
            'from_location': 'Chicago',  # EXACT: 'from_location' not 'route_segment'
            'to_location': 'Milwaukee',  # EXACT: 'to_location'
            'rate_per_mile': 0.15       # EXACT: 'rate_per_mile' not 'toll_rate_per_mile'
        },
        {
            'from_location': 'Indianapolis',
            'to_location': 'Chicago',
            'rate_per_mile': 0.12
        }
    ]
    
    # Create Excel files
    stores_df = pd.DataFrame(stores_data)
    stores_df.to_excel(data_dir / 'store_locations.xlsx', index=False)
    print(f"✅ Created store_locations.xlsx with columns: {list(stores_df.columns)}")
    
    suppliers_df = pd.DataFrame(suppliers_data)
    suppliers_df.to_excel(data_dir / 'supplier_data.xlsx', index=False)
    print(f"✅ Created supplier_data.xlsx with columns: {list(suppliers_df.columns)}")
    
    orders_df = pd.DataFrame(orders_data)
    orders_df.to_excel(data_dir / 'historical_orders.xlsx', index=False)
    print(f"✅ Created historical_orders.xlsx with columns: {list(orders_df.columns)}")
    
    toll_df = pd.DataFrame(toll_data)
    toll_df.to_excel(data_dir / 'toll_rates.xlsx', index=False)
    print(f"✅ Created toll_rates.xlsx with columns: {list(toll_df.columns)}")
    
    print("\n🎯 ALL FILES CREATED WITH EXACT EXPECTED STRUCTURE!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🚨 EMERGENCY FIX: CREATING PERFECT EXCEL FILES")
    print("=" * 60)
    
    create_perfect_excel_files()
    
    print("\n" + "=" * 60)
    print("✅ PERFECT FILES READY - EXACT COLUMN MATCHES!")
    print("=" * 60)