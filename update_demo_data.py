#!/usr/bin/env python3

import sys
import os
import pandas as pd
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_enhanced_sample_data():
    """Create comprehensive demonstration Excel files"""
    
    data_dir = Path("data/input")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Enhanced Store Locations Data
    stores_data = [
        {
            'store_id': 'WM001', 'name': 'Walmart Supercenter - Downtown', 
            'address': '100 Main St', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60601',
            'latitude': 41.8781, 'longitude': -87.6298, 'demand_pallets': 45,
            'store_type': 'Supercenter', 'priority': 'High', 'delivery_window': '6AM-10PM'
        },
        {
            'store_id': 'TG002', 'name': 'Target Express - Midtown', 
            'address': '250 State St', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53202',
            'latitude': 43.0389, 'longitude': -87.9065, 'demand_pallets': 32,
            'store_type': 'Express', 'priority': 'Medium', 'delivery_window': '7AM-9PM'
        },
        {
            'store_id': 'HD003', 'name': 'Home Depot - Northside', 
            'address': '1575 N Milwaukee Ave', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60647',
            'latitude': 41.9093, 'longitude': -87.6878, 'demand_pallets': 28,
            'store_type': 'Home Improvement', 'priority': 'High', 'delivery_window': '5AM-11PM'
        },
        {
            'store_id': 'KG004', 'name': 'Kroger Fresh Market', 
            'address': '455 E Ohio St', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46202',
            'latitude': 39.7684, 'longitude': -86.1581, 'demand_pallets': 38,
            'store_type': 'Grocery', 'priority': 'High', 'delivery_window': '4AM-12AM'
        },
        {
            'store_id': 'MJ005', 'name': 'Meijer Supermarket', 
            'address': '3825 S Port Ave', 'city': 'Corpus Christi', 'state': 'TX', 'zip_code': '78415',
            'latitude': 27.7003, 'longitude': -97.3384, 'demand_pallets': 41,
            'store_type': 'Supermarket', 'priority': 'Medium', 'delivery_window': '6AM-10PM'
        },
        {
            'store_id': 'CV006', 'name': 'CVS Pharmacy Plus', 
            'address': '789 Michigan Ave', 'city': 'Detroit', 'state': 'MI', 'zip_code': '48226',
            'latitude': 42.3314, 'longitude': -83.0458, 'demand_pallets': 22,
            'store_type': 'Pharmacy', 'priority': 'Low', 'delivery_window': '8AM-8PM'
        },
        {
            'store_id': 'WG007', 'name': 'Walgreens Express', 
            'address': '123 Broadway St', 'city': 'Nashville', 'state': 'TN', 'zip_code': '37203',
            'latitude': 36.1627, 'longitude': -86.7816, 'demand_pallets': 19,
            'store_type': 'Pharmacy', 'priority': 'Low', 'delivery_window': '9AM-7PM'
        },
        {
            'store_id': 'CS008', 'name': 'Costco Wholesale', 
            'address': '1234 Veterans Pkwy', 'city': 'St. Louis', 'state': 'MO', 'zip_code': '63146',
            'latitude': 38.6270, 'longitude': -90.1994, 'demand_pallets': 65,
            'store_type': 'Wholesale', 'priority': 'High', 'delivery_window': '5AM-11PM'
        }
    ]
    
    # Enhanced Supplier Data
    suppliers_data = [
        {
            'supplier_id': 'SUP_ACME_001', 'name': 'ACME Distribution Center', 
            'address': '5000 Industrial Blvd', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60632',
            'latitude': 41.7886, 'longitude': -87.7505, 'available_pallets': 180,
            'cost_per_pallet': 125.50, 'lead_time_days': 1, 'capacity_per_day': 200,
            'supplier_type': 'Primary', 'reliability_score': 98.5, 'quality_rating': 'A+'
        },
        {
            'supplier_id': 'SUP_METRO_002', 'name': 'Metro Logistics Hub', 
            'address': '3200 Commerce Dr', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46241',
            'latitude': 39.7173, 'longitude': -86.2944, 'available_pallets': 145,
            'cost_per_pallet': 118.75, 'lead_time_days': 2, 'capacity_per_day': 150,
            'supplier_type': 'Secondary', 'reliability_score': 95.2, 'quality_rating': 'A'
        },
        {
            'supplier_id': 'SUP_SWIFT_003', 'name': 'Swift Supply Chain Solutions', 
            'address': '7800 Logistics Ln', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53218',
            'latitude': 43.0731, 'longitude': -87.9673, 'available_pallets': 95,
            'cost_per_pallet': 135.25, 'lead_time_days': 1, 'capacity_per_day': 120,
            'supplier_type': 'Premium', 'reliability_score': 99.1, 'quality_rating': 'A+'
        },
        {
            'supplier_id': 'SUP_RAPID_004', 'name': 'Rapid Response Warehouse', 
            'address': '1100 Distribution Way', 'city': 'Detroit', 'state': 'MI', 'zip_code': '48210',
            'latitude': 42.3598, 'longitude': -83.0023, 'available_pallets': 110,
            'cost_per_pallet': 142.00, 'lead_time_days': 1, 'capacity_per_day': 140,
            'supplier_type': 'Express', 'reliability_score': 97.8, 'quality_rating': 'A'
        }
    ]
    
    # Historical Orders Data
    historical_orders = [
        {
            'order_id': 'ORD_2024_001', 'date': '2024-01-15', 'store_id': 'WM001', 
            'supplier_id': 'SUP_ACME_001', 'pallets_ordered': 42, 'pallets_delivered': 42,
            'delivery_cost': 5285.00, 'delivery_time_hours': 3.5, 'distance_miles': 28.3,
            'order_priority': 'High', 'delivery_status': 'On Time'
        },
        {
            'order_id': 'ORD_2024_002', 'date': '2024-01-16', 'store_id': 'TG002', 
            'supplier_id': 'SUP_SWIFT_003', 'pallets_ordered': 30, 'pallets_delivered': 30,
            'delivery_cost': 4057.50, 'delivery_time_hours': 2.8, 'distance_miles': 15.7,
            'order_priority': 'Medium', 'delivery_status': 'On Time'
        },
        {
            'order_id': 'ORD_2024_003', 'date': '2024-01-17', 'store_id': 'CS008', 
            'supplier_id': 'SUP_ACME_001', 'pallets_ordered': 60, 'pallets_delivered': 58,
            'delivery_cost': 7290.00, 'delivery_time_hours': 5.2, 'distance_miles': 42.1,
            'order_priority': 'High', 'delivery_status': 'Late'
        },
        {
            'order_id': 'ORD_2024_004', 'date': '2024-01-18', 'store_id': 'HD003', 
            'supplier_id': 'SUP_METRO_002', 'pallets_ordered': 25, 'pallets_delivered': 25,
            'delivery_cost': 2968.75, 'delivery_time_hours': 4.1, 'distance_miles': 35.9,
            'order_priority': 'High', 'delivery_status': 'On Time'
        }
    ]
    
    # Toll Rates Data
    toll_rates = [
        {
            'route_segment': 'I-90 Chicago to Milwaukee', 'toll_rate_per_mile': 0.15,
            'segment_length_miles': 92.3, 'vehicle_class': 'Class 8 Truck',
            'time_of_day_multiplier': 1.0, 'peak_hours': '7AM-9AM, 4PM-6PM'
        },
        {
            'route_segment': 'I-65 Indianapolis Corridor', 'toll_rate_per_mile': 0.12,
            'segment_length_miles': 45.7, 'vehicle_class': 'Class 8 Truck',
            'time_of_day_multiplier': 1.2, 'peak_hours': '6AM-9AM, 3PM-7PM'
        },
        {
            'route_segment': 'I-94 Detroit Metro Area', 'toll_rate_per_mile': 0.18,
            'segment_length_miles': 28.9, 'vehicle_class': 'Class 8 Truck',
            'time_of_day_multiplier': 1.5, 'peak_hours': '6AM-10AM, 3PM-8PM'
        },
        {
            'route_segment': 'I-70 St. Louis Bypass', 'toll_rate_per_mile': 0.10,
            'segment_length_miles': 67.2, 'vehicle_class': 'Class 8 Truck',
            'time_of_day_multiplier': 0.8, 'peak_hours': 'None'
        }
    ]
    
    # Create Excel files with professional formatting
    print("🏗️  Creating enhanced demonstration data files...")
    
    # Store locations
    stores_df = pd.DataFrame(stores_data)
    with pd.ExcelWriter(data_dir / 'store_locations.xlsx', engine='openpyxl') as writer:
        stores_df.to_excel(writer, sheet_name='Store_Locations', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Store_Locations']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # Supplier data
    suppliers_df = pd.DataFrame(suppliers_data)
    with pd.ExcelWriter(data_dir / 'supplier_data.xlsx', engine='openpyxl') as writer:
        suppliers_df.to_excel(writer, sheet_name='Supplier_Data', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Supplier_Data']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # Historical orders
    orders_df = pd.DataFrame(historical_orders)
    with pd.ExcelWriter(data_dir / 'historical_orders.xlsx', engine='openpyxl') as writer:
        orders_df.to_excel(writer, sheet_name='Historical_Orders', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Historical_Orders']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # Toll rates
    toll_df = pd.DataFrame(toll_rates)
    with pd.ExcelWriter(data_dir / 'toll_rates.xlsx', engine='openpyxl') as writer:
        toll_df.to_excel(writer, sheet_name='Toll_Rates', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Toll_Rates']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print("✅ Enhanced demonstration files created successfully!")
    print(f"📊 Store Locations: {len(stores_data)} professional retail locations")
    print(f"🏭 Suppliers: {len(suppliers_data)} distribution centers with ratings")
    print(f"📈 Historical Orders: {len(historical_orders)} sample delivery records")
    print(f"🛣️  Toll Rates: {len(toll_rates)} route segments with pricing")
    
    return {
        'stores': len(stores_data),
        'suppliers': len(suppliers_data),
        'orders': len(historical_orders),
        'toll_segments': len(toll_rates)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚚 PALLET LOGISTICS OPTIMIZER - DEMO DATA GENERATOR")
    print("=" * 60)
    
    stats = create_enhanced_sample_data()
    
    print("\n" + "=" * 60)
    print("✨ ENHANCED DEMONSTRATION DATA READY FOR TESTING")
    print("=" * 60)
    print("Files created in: data/input/")
    print("Ready for optimization analysis!")