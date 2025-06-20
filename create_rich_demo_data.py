#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
import random
import numpy as np

def create_rich_demo_data():
    """Create comprehensive demonstration data for Frito-Lay logistics"""
    
    data_dir = Path("data/input")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("🍟 Creating comprehensive Frito-Lay demonstration data...")
    
    # Expanded Store Locations - Major retail chains across multiple states
    stores_data = [
        # Walmart Locations
        {'store_id': 'WM001', 'name': 'Walmart Supercenter - Downtown Chicago', 'address': '100 N State St', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60601', 'latitude': 41.8781, 'longitude': -87.6298, 'demand_pallets': 45, 'priority': 1, 'contact_info': 'manager@walmart-chicago.com'},
        {'store_id': 'WM002', 'name': 'Walmart Supercenter - Schaumburg', 'address': '1555 N Roselle Rd', 'city': 'Schaumburg', 'state': 'IL', 'zip_code': '60195', 'latitude': 42.0334, 'longitude': -88.0834, 'demand_pallets': 52, 'priority': 1, 'contact_info': 'ops@walmart-schaumburg.com'},
        {'store_id': 'WM003', 'name': 'Walmart Supercenter - Milwaukee West', 'address': '3355 S 27th St', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53215', 'latitude': 43.0189, 'longitude': -87.9464, 'demand_pallets': 38, 'priority': 1, 'contact_info': 'mgr@walmart-milwaukee.com'},
        
        # Target Locations
        {'store_id': 'TG001', 'name': 'Target Express - Milwaukee Downtown', 'address': '250 E Wisconsin Ave', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53202', 'latitude': 43.0389, 'longitude': -87.9065, 'demand_pallets': 32, 'priority': 2, 'contact_info': 'contact@target-milwaukee.com'},
        {'store_id': 'TG002', 'name': 'Target - Naperville', 'address': '3155 W Jefferson Ave', 'city': 'Naperville', 'state': 'IL', 'zip_code': '60564', 'latitude': 41.7508, 'longitude': -88.1535, 'demand_pallets': 29, 'priority': 2, 'contact_info': 'team@target-naperville.com'},
        {'store_id': 'TG003', 'name': 'Target - Indianapolis Circle Centre', 'address': '49 W Maryland St', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46204', 'latitude': 39.7684, 'longitude': -86.1581, 'demand_pallets': 35, 'priority': 2, 'contact_info': 'mgmt@target-indy.com'},
        
        # Kroger Locations
        {'store_id': 'KR001', 'name': 'Kroger Fresh Market - Indianapolis', 'address': '455 E Market St', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46202', 'latitude': 39.7684, 'longitude': -86.1581, 'demand_pallets': 38, 'priority': 1, 'contact_info': 'manager@kroger-indy.com'},
        {'store_id': 'KR002', 'name': 'Kroger Plus - Columbus', 'address': '1275 Olentangy River Rd', 'city': 'Columbus', 'state': 'OH', 'zip_code': '43212', 'latitude': 40.0150, 'longitude': -83.0186, 'demand_pallets': 41, 'priority': 1, 'contact_info': 'ops@kroger-columbus.com'},
        {'store_id': 'KR003', 'name': 'Kroger Marketplace - Cincinnati', 'address': '7800 Factory Shop Blvd', 'city': 'Cincinnati', 'state': 'OH', 'zip_code': '45069', 'latitude': 39.3210, 'longitude': -84.4877, 'demand_pallets': 44, 'priority': 1, 'contact_info': 'store@kroger-cincy.com'},
        
        # Meijer Locations
        {'store_id': 'MJ001', 'name': 'Meijer Supermarket - Grand Rapids', 'address': '3825 28th St SE', 'city': 'Grand Rapids', 'state': 'MI', 'zip_code': '49512', 'latitude': 42.9634, 'longitude': -85.6681, 'demand_pallets': 41, 'priority': 2, 'contact_info': 'team@meijer-gr.com'},
        {'store_id': 'MJ002', 'name': 'Meijer - Lansing', 'address': '6200 S Pennsylvania Ave', 'city': 'Lansing', 'state': 'MI', 'zip_code': '48911', 'latitude': 42.6875, 'longitude': -84.5467, 'demand_pallets': 33, 'priority': 2, 'contact_info': 'mgr@meijer-lansing.com'},
        
        # Costco Locations
        {'store_id': 'CS001', 'name': 'Costco Wholesale - St. Louis', 'address': '1234 Veterans Memorial Pkwy', 'city': 'St. Louis', 'state': 'MO', 'zip_code': '63146', 'latitude': 38.6270, 'longitude': -90.1994, 'demand_pallets': 65, 'priority': 1, 'contact_info': 'bulk@costco-stlouis.com'},
        {'store_id': 'CS002', 'name': 'Costco Wholesale - Schaumburg', 'address': '1818 McConnor Pkwy', 'city': 'Schaumburg', 'state': 'IL', 'zip_code': '60173', 'latitude': 42.0450, 'longitude': -88.0767, 'demand_pallets': 72, 'priority': 1, 'contact_info': 'ops@costco-schaumburg.com'},
        
        # Additional chains for variety
        {'store_id': 'CV001', 'name': 'CVS Pharmacy Plus - Detroit', 'address': '789 Woodward Ave', 'city': 'Detroit', 'state': 'MI', 'zip_code': '48226', 'latitude': 42.3314, 'longitude': -83.0458, 'demand_pallets': 22, 'priority': 3, 'contact_info': 'pharm@cvs-detroit.com'},
        {'store_id': 'DG001', 'name': 'Dollar General - Springfield', 'address': '123 S Main St', 'city': 'Springfield', 'state': 'IL', 'zip_code': '62701', 'latitude': 39.7817, 'longitude': -89.6501, 'demand_pallets': 19, 'priority': 3, 'contact_info': 'store@dg-springfield.com'},
        {'store_id': 'SA001', 'name': 'Save-A-Lot - Rockford', 'address': '456 E State St', 'city': 'Rockford', 'state': 'IL', 'zip_code': '61104', 'latitude': 42.2711, 'longitude': -89.0940, 'demand_pallets': 28, 'priority': 2, 'contact_info': 'mgmt@sal-rockford.com'}
    ]
    
    # Expanded Frito-Lay Distribution Centers
    suppliers_data = [
        {'supplier_id': 'FL_CHICAGO_001', 'name': 'Frito-Lay Chicago Primary Distribution Center', 'address': '5000 S Cicero Ave', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60632', 'latitude': 41.7886, 'longitude': -87.7505, 'available_pallets': 280, 'cost_per_pallet': 125.50, 'lead_time_days': 1, 'capacity_per_day': 300, 'reliability_score': 0.985, 'contact_info': 'dispatch@fritolay-chicago.com'},
        {'supplier_id': 'FL_INDY_002', 'name': 'Frito-Lay Indianapolis Regional Hub', 'address': '3200 Industrial Blvd', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46241', 'latitude': 39.7173, 'longitude': -86.2944, 'available_pallets': 245, 'cost_per_pallet': 118.75, 'lead_time_days': 1, 'capacity_per_day': 250, 'reliability_score': 0.972, 'contact_info': 'indy@fritolay.com'},
        {'supplier_id': 'FL_MILWAUKEE_003', 'name': 'Frito-Lay Milwaukee Distribution', 'address': '7800 W Lincoln Ave', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53218', 'latitude': 43.0731, 'longitude': -87.9673, 'available_pallets': 195, 'cost_per_pallet': 135.25, 'lead_time_days': 1, 'capacity_per_day': 180, 'reliability_score': 0.961, 'contact_info': 'milwaukee@fritolay.com'},
        {'supplier_id': 'FL_STLOUIS_004', 'name': 'Frito-Lay St. Louis Fulfillment Center', 'address': '1100 Distribution Way', 'city': 'St. Louis', 'state': 'MO', 'zip_code': '63110', 'latitude': 38.5598, 'longitude': -90.2023, 'available_pallets': 210, 'cost_per_pallet': 142.00, 'lead_time_days': 2, 'capacity_per_day': 200, 'reliability_score': 0.958, 'contact_info': 'stlouis@fritolay.com'},
        {'supplier_id': 'FL_COLUMBUS_005', 'name': 'Frito-Lay Columbus Distribution Center', 'address': '4500 Eastgate Dr', 'city': 'Columbus', 'state': 'OH', 'zip_code': '43230', 'latitude': 39.9612, 'longitude': -82.8988, 'available_pallets': 165, 'cost_per_pallet': 128.90, 'lead_time_days': 1, 'capacity_per_day': 175, 'reliability_score': 0.978, 'contact_info': 'columbus@fritolay.com'},
        {'supplier_id': 'FL_DETROIT_006', 'name': 'Frito-Lay Detroit Metro Distribution', 'address': '25000 Industrial Dr', 'city': 'Detroit', 'state': 'MI', 'zip_code': '48210', 'latitude': 42.3598, 'longitude': -83.0023, 'available_pallets': 185, 'cost_per_pallet': 131.75, 'lead_time_days': 1, 'capacity_per_day': 190, 'reliability_score': 0.968, 'contact_info': 'detroit@fritolay.com'}
    ]
    
    # Expanded Historical Orders with realistic Frito-Lay products
    frito_products = ['Lay\'s Classic', 'Doritos Nacho Cheese', 'Cheetos Crunchy', 'Fritos Original', 'Tostitos Scoops', 'Ruffles Original', 'SunChips Original', 'Smartfood Popcorn']
    
    orders_data = []
    for i in range(1, 26):  # 25 historical orders
        store = random.choice(stores_data)
        supplier = random.choice(suppliers_data)
        product_mix = random.sample(frito_products, random.randint(2, 4))
        
        orders_data.append({
            'order_id': f'FL_2024_{i:03d}',
            'store_id': store['store_id'],
            'supplier_id': supplier['supplier_id'],
            'quantity': random.randint(15, 55),
            'requested_date': f'2024-0{random.randint(1, 2)}-{random.randint(10, 28):02d}',
            'priority': random.randint(1, 3),
            'special_instructions': random.choice([
                'Loading dock 3', 'Weekend delivery OK', 'Call on arrival', 
                'Fragile - handle with care', 'Rush order', 'Standard delivery',
                'Morning delivery preferred', 'Back entrance only'
            ]),
            'product_mix': ', '.join(product_mix)
        })
    
    # Comprehensive Toll Rates
    toll_data = [
        {'from_location': 'Chicago', 'to_location': 'Milwaukee', 'rate_per_mile': 0.15},
        {'from_location': 'Indianapolis', 'to_location': 'Chicago', 'rate_per_mile': 0.12},
        {'from_location': 'Columbus', 'to_location': 'Indianapolis', 'rate_per_mile': 0.14},
        {'from_location': 'Detroit', 'to_location': 'Chicago', 'rate_per_mile': 0.18},
        {'from_location': 'St. Louis', 'to_location': 'Chicago', 'rate_per_mile': 0.10},
        {'from_location': 'Milwaukee', 'to_location': 'Chicago', 'rate_per_mile': 0.13},
        {'from_location': 'Grand Rapids', 'to_location': 'Detroit', 'rate_per_mile': 0.16},
        {'from_location': 'Cincinnati', 'to_location': 'Columbus', 'rate_per_mile': 0.11}
    ]
    
    # Create Excel files
    print(f"📊 Creating {len(stores_data)} store locations...")
    stores_df = pd.DataFrame(stores_data)
    stores_df.to_excel(data_dir / 'store_locations.xlsx', index=False)
    
    print(f"🏭 Creating {len(suppliers_data)} distribution centers...")
    suppliers_df = pd.DataFrame(suppliers_data)
    suppliers_df.to_excel(data_dir / 'supplier_data.xlsx', index=False)
    
    print(f"📦 Creating {len(orders_data)} historical orders...")
    orders_df = pd.DataFrame(orders_data)
    orders_df.to_excel(data_dir / 'historical_orders.xlsx', index=False)
    
    print(f"🛣️ Creating {len(toll_data)} toll routes...")
    toll_df = pd.DataFrame(toll_data)
    toll_df.to_excel(data_dir / 'toll_rates.xlsx', index=False)
    
    print("\n🎯 COMPREHENSIVE FRITO-LAY DEMO DATA CREATED!")
    print(f"✅ {len(stores_data)} retail locations across 6 states")
    print(f"✅ {len(suppliers_data)} Frito-Lay distribution centers")
    print(f"✅ {len(orders_data)} historical delivery records")
    print(f"✅ {len(toll_data)} interstate toll routes")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🚚 FRITO-LAY COMPREHENSIVE DEMO DATA GENERATOR")
    print("=" * 60)
    
    create_rich_demo_data()
    
    print("\n" + "=" * 60)
    print("🍟 READY FOR PROFESSIONAL DEMONSTRATION!")
    print("=" * 60)