#!/usr/bin/env python3

import sys
import os
import pandas as pd
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_frito_lay_sample_data():
    """Create Frito-Lay themed demonstration Excel files"""
    
    data_dir = Path("data/input")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Frito-Lay Store Locations (Retail Partners)
    stores_data = [
        {
            'store_id': 'WM001', 'name': 'Walmart Supercenter - Downtown Chicago', 
            'address': '100 N State St', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60601',
            'latitude': 41.8781, 'longitude': -87.6298, 'demand_pallets': 45,
            'store_type': 'Supercenter', 'priority': 'High', 'delivery_window': '6AM-10PM'
        },
        {
            'store_id': 'TG002', 'name': 'Target Express - Milwaukee Downtown', 
            'address': '250 E Wisconsin Ave', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53202',
            'latitude': 43.0389, 'longitude': -87.9065, 'demand_pallets': 32,
            'store_type': 'Express', 'priority': 'Medium', 'delivery_window': '7AM-9PM'
        },
        {
            'store_id': 'KR003', 'name': 'Kroger Fresh Market - Indianapolis', 
            'address': '455 E Market St', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46202',
            'latitude': 39.7684, 'longitude': -86.1581, 'demand_pallets': 38,
            'store_type': 'Grocery', 'priority': 'High', 'delivery_window': '4AM-12AM'
        },
        {
            'store_id': 'MJ004', 'name': 'Meijer Supermarket - Grand Rapids', 
            'address': '3825 28th St SE', 'city': 'Grand Rapids', 'state': 'MI', 'zip_code': '49512',
            'latitude': 42.9634, 'longitude': -85.6681, 'demand_pallets': 41,
            'store_type': 'Supermarket', 'priority': 'Medium', 'delivery_window': '6AM-10PM'
        },
        {
            'store_id': 'CS005', 'name': 'Costco Wholesale - St. Louis', 
            'address': '1234 Veterans Memorial Pkwy', 'city': 'St. Louis', 'state': 'MO', 'zip_code': '63146',
            'latitude': 38.6270, 'longitude': -90.1994, 'demand_pallets': 65,
            'store_type': 'Wholesale', 'priority': 'High', 'delivery_window': '5AM-11PM'
        },
        {
            'store_id': 'CV006', 'name': 'CVS Pharmacy Plus - Detroit', 
            'address': '789 Woodward Ave', 'city': 'Detroit', 'state': 'MI', 'zip_code': '48226',
            'latitude': 42.3314, 'longitude': -83.0458, 'demand_pallets': 22,
            'store_type': 'Pharmacy', 'priority': 'Low', 'delivery_window': '8AM-8PM'
        },
        {
            'store_id': 'DG007', 'name': 'Dollar General - Springfield', 
            'address': '123 S Main St', 'city': 'Springfield', 'state': 'IL', 'zip_code': '62701',
            'latitude': 39.7817, 'longitude': -89.6501, 'demand_pallets': 19,
            'store_type': 'Discount', 'priority': 'Low', 'delivery_window': '9AM-7PM'
        },
        {
            'store_id': 'SA008', 'name': 'Save-A-Lot - Rockford', 
            'address': '456 E State St', 'city': 'Rockford', 'state': 'IL', 'zip_code': '61104',
            'latitude': 42.2711, 'longitude': -89.0940, 'demand_pallets': 28,
            'store_type': 'Grocery', 'priority': 'Medium', 'delivery_window': '7AM-9PM'
        }
    ]
    
    # Frito-Lay Distribution Centers
    suppliers_data = [
        {
            'supplier_id': 'FL_CHICAGO_001', 'name': 'Frito-Lay Chicago Distribution Center', 
            'address': '5000 S Cicero Ave', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60632',
            'latitude': 41.7886, 'longitude': -87.7505, 'available_pallets': 180,
            'cost_per_pallet': 125.50, 'lead_time_days': 1, 'capacity_per_day': 200,
            'supplier_type': 'Primary DC', 'reliability_score': 98.5, 'quality_rating': 'A+'
        },
        {
            'supplier_id': 'FL_INDY_002', 'name': 'Frito-Lay Indianapolis Regional Hub', 
            'address': '3200 Industrial Blvd', 'city': 'Indianapolis', 'state': 'IN', 'zip_code': '46241',
            'latitude': 39.7173, 'longitude': -86.2944, 'available_pallets': 145,
            'cost_per_pallet': 118.75, 'lead_time_days': 1, 'capacity_per_day': 150,
            'supplier_type': 'Regional DC', 'reliability_score': 97.2, 'quality_rating': 'A+'
        },
        {
            'supplier_id': 'FL_MILWAUKEE_003', 'name': 'Frito-Lay Milwaukee Distribution', 
            'address': '7800 W Lincoln Ave', 'city': 'Milwaukee', 'state': 'WI', 'zip_code': '53218',
            'latitude': 43.0731, 'longitude': -87.9673, 'available_pallets': 95,
            'cost_per_pallet': 135.25, 'lead_time_days': 1, 'capacity_per_day': 120,
            'supplier_type': 'Satellite DC', 'reliability_score': 96.1, 'quality_rating': 'A'
        },
        {
            'supplier_id': 'FL_STLOUIS_004', 'name': 'Frito-Lay St. Louis Fulfillment Center', 
            'address': '1100 Distribution Way', 'city': 'St. Louis', 'state': 'MO', 'zip_code': '63110',
            'latitude': 38.5598, 'longitude': -90.2023, 'available_pallets': 110,
            'cost_per_pallet': 142.00, 'lead_time_days': 2, 'capacity_per_day': 140,
            'supplier_type': 'Express DC', 'reliability_score': 95.8, 'quality_rating': 'A'
        }
    ]
    
    # Historical Frito-Lay Orders
    historical_orders = [
        {
            'order_id': 'FL_2024_001', 'date': '2024-01-15', 'store_id': 'WM001', 
            'supplier_id': 'FL_CHICAGO_001', 'pallets_ordered': 42, 'pallets_delivered': 42,
            'delivery_cost': 5285.00, 'delivery_time_hours': 3.5, 'distance_miles': 28.3,
            'order_priority': 'High', 'delivery_status': 'On Time', 'product_mix': 'Lay\'s, Doritos, Cheetos'
        },
        {
            'order_id': 'FL_2024_002', 'date': '2024-01-16', 'store_id': 'TG002', 
            'supplier_id': 'FL_MILWAUKEE_003', 'pallets_ordered': 30, 'pallets_delivered': 30,
            'delivery_cost': 4057.50, 'delivery_time_hours': 2.8, 'distance_miles': 15.7,
            'order_priority': 'Medium', 'delivery_status': 'On Time', 'product_mix': 'Fritos, Tostitos, Ruffles'
        },
        {
            'order_id': 'FL_2024_003', 'date': '2024-01-17', 'store_id': 'CS005', 
            'supplier_id': 'FL_STLOUIS_004', 'pallets_ordered': 60, 'pallets_delivered': 58,
            'delivery_cost': 7290.00, 'delivery_time_hours': 5.2, 'distance_miles': 42.1,
            'order_priority': 'High', 'delivery_status': 'Late', 'product_mix': 'Mixed Variety Packs'
        },
        {
            'order_id': 'FL_2024_004', 'date': '2024-01-18', 'store_id': 'KR003', 
            'supplier_id': 'FL_INDY_002', 'pallets_ordered': 35, 'pallets_delivered': 35,
            'delivery_cost': 4158.75, 'delivery_time_hours': 2.1, 'distance_miles': 18.9,
            'order_priority': 'High', 'delivery_status': 'On Time', 'product_mix': 'Lay\'s, Cheetos, SunChips'
        },
        {
            'order_id': 'FL_2024_005', 'date': '2024-01-19', 'store_id': 'MJ004', 
            'supplier_id': 'FL_CHICAGO_001', 'pallets_ordered': 38, 'pallets_delivered': 38,
            'delivery_cost': 4968.00, 'delivery_time_hours': 4.3, 'distance_miles': 35.2,
            'order_priority': 'Medium', 'delivery_status': 'On Time', 'product_mix': 'Doritos, Fritos, Smartfood'
        }
    ]
    
    # Transportation Toll Rates for Frito-Lay Routes
    toll_rates = [
        {
            'route_segment': 'I-90 Chicago to Milwaukee Corridor', 'toll_rate_per_mile': 0.15,
            'segment_length_miles': 92.3, 'vehicle_class': 'Class 8 Delivery Truck',
            'time_of_day_multiplier': 1.0, 'peak_hours': '7AM-9AM, 4PM-6PM'
        },
        {
            'route_segment': 'I-65 Indianapolis Distribution Route', 'toll_rate_per_mile': 0.12,
            'segment_length_miles': 45.7, 'vehicle_class': 'Class 8 Delivery Truck',
            'time_of_day_multiplier': 1.2, 'peak_hours': '6AM-9AM, 3PM-7PM'
        },
        {
            'route_segment': 'I-94 Michigan Delivery Network', 'toll_rate_per_mile': 0.18,
            'segment_length_miles': 28.9, 'vehicle_class': 'Class 8 Delivery Truck',
            'time_of_day_multiplier': 1.5, 'peak_hours': '6AM-10AM, 3PM-8PM'
        },
        {
            'route_segment': 'I-70 St. Louis Supply Chain Route', 'toll_rate_per_mile': 0.10,
            'segment_length_miles': 67.2, 'vehicle_class': 'Class 8 Delivery Truck',
            'time_of_day_multiplier': 0.8, 'peak_hours': 'None'
        }
    ]
    
    # Create Excel files with professional formatting
    print("🍟 Creating Frito-Lay demonstration data files...")
    
    # Store locations
    stores_df = pd.DataFrame(stores_data)
    with pd.ExcelWriter(data_dir / 'store_locations.xlsx', engine='openpyxl') as writer:
        stores_df.to_excel(writer, sheet_name='Frito_Lay_Retail_Partners', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Frito_Lay_Retail_Partners']
        
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
        suppliers_df.to_excel(writer, sheet_name='Frito_Lay_Distribution_Centers', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Frito_Lay_Distribution_Centers']
        
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
        orders_df.to_excel(writer, sheet_name='Frito_Lay_Order_History', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Frito_Lay_Order_History']
        
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
        toll_df.to_excel(writer, sheet_name='Frito_Lay_Route_Tolls', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Frito_Lay_Route_Tolls']
        
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
    
    print("✅ Frito-Lay demonstration files created successfully!")
    print(f"🏪 Retail Partners: {len(stores_data)} major retail locations")
    print(f"🏭 Distribution Centers: {len(suppliers_data)} Frito-Lay facilities")
    print(f"📦 Historical Orders: {len(historical_orders)} snack delivery records")
    print(f"🛣️  Route Segments: {len(toll_rates)} delivery corridors")
    
    return {
        'stores': len(stores_data),
        'suppliers': len(suppliers_data),
        'orders': len(historical_orders),
        'toll_segments': len(toll_rates)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🍟 FRITO-LAY PALLET LOGISTICS OPTIMIZER")
    print("=" * 60)
    
    stats = create_frito_lay_sample_data()
    
    print("\n" + "=" * 60)
    print("🚚 FRITO-LAY DEMONSTRATION DATA READY")
    print("=" * 60)
    print("Files created in: data/input/")
    print("Ready for snack delivery optimization!")