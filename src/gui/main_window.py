import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import yaml
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.excel_handler import ExcelHandler
from core.optimizer import PalletOptimizer
from data.models import Vehicle, Location, OptimizationResult


class PalletOptimizerDashboard:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.excel_handler = ExcelHandler()
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Store(id='optimization-results-store'),
            dcc.Store(id='stores-data-store'),
            dcc.Store(id='suppliers-data-store'),
            
            # Header
            html.Div([
                html.H1("=› Pallet Logistics Optimizer", 
                       className="text-center text-white mb-4",
                       style={'backgroundColor': '#2c3e50', 'padding': '20px', 'margin': '0'}),
            ]),
            
            # Main content
            html.Div([
                # Control Panel
                html.Div([
                    html.H3("=Ê Control Panel", className="mb-3"),
                    
                    # File Upload Section
                    html.Div([
                        html.H5("=Á Data Files"),
                        html.Div([
                            html.Label("Store Locations:"),
                            dcc.Upload(
                                id='upload-stores',
                                children=html.Div(['Drag and Drop or ', html.A('Select Store File')]),
                                style={
                                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                                    'borderWidth': '1px', 'borderStyle': 'dashed',
                                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                                }
                            ),
                        ], className="mb-3"),
                        
                        html.Div([
                            html.Label("Supplier Data:"),
                            dcc.Upload(
                                id='upload-suppliers',
                                children=html.Div(['Drag and Drop or ', html.A('Select Supplier File')]),
                                style={
                                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                                    'borderWidth': '1px', 'borderStyle': 'dashed',
                                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                                }
                            ),
                        ], className="mb-3"),
                    ], className="mb-4"),
                    
                    # Optimization Settings
                    html.Div([
                        html.H5("™ Settings"),
                        html.Div([
                            html.Label("Optimization Method:"),
                            dcc.RadioItems(
                                id='optimization-method',
                                options=[
                                    {'label': 'Heuristic (Fast)', 'value': 'heuristic'},
                                    {'label': 'Exact (Optimal)', 'value': 'exact'}
                                ],
                                value='heuristic',
                                className="mb-2"
                            ),
                        ]),
                        
                        html.Div([
                            html.Label("Number of Vehicles:"),
                            dcc.Slider(
                                id='num-vehicles',
                                min=1, max=10, step=1, value=3,
                                marks={i: str(i) for i in range(1, 11)},
                                className="mb-3"
                            ),
                        ]),
                    ], className="mb-4"),
                    
                    # Action Buttons
                    html.Div([
                        html.Button("= Load Sample Data", id="load-sample-btn", 
                                  className="btn btn-secondary me-2 mb-2", 
                                  style={'marginRight': '10px'}),
                        html.Button("=€ Run Optimization", id="optimize-btn", 
                                  className="btn btn-primary mb-2",
                                  style={'backgroundColor': '#e74c3c', 'borderColor': '#e74c3c'}),
                    ]),
                    
                    # Status
                    html.Div(id="status-message", className="mt-3"),
                    
                ], className="col-md-3", style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'minHeight': '100vh'}),
                
                # Results Panel
                html.Div([
                    # Summary Cards
                    html.Div(id="summary-cards", className="mb-4"),
                    
                    # Tabs for different views
                    dcc.Tabs(id="results-tabs", value='routes', children=[
                        dcc.Tab(label='=ú Routes', value='routes'),
                        dcc.Tab(label='=Ê Analytics', value='analytics'),
                        dcc.Tab(label='=Ë Data Tables', value='tables'),
                        dcc.Tab(label='<¯ Map View', value='map'),
                    ]),
                    
                    html.Div(id='tab-content')
                    
                ], className="col-md-9", style={'padding': '20px'}),
                
            ], className="row"),
            
        ], className="container-fluid")

    def setup_callbacks(self):
        
        @self.app.callback(
            [Output('stores-data-store', 'data'),
             Output('suppliers-data-store', 'data'),
             Output('status-message', 'children')],
            [Input('load-sample-btn', 'n_clicks')],
            prevent_initial_call=True
        )
        def load_sample_data(n_clicks):
            if n_clicks:
                try:
                    # Load sample data
                    stores = self.excel_handler.load_stores()
                    suppliers = self.excel_handler.load_suppliers()
                    
                    stores_data = []
                    for store in stores:
                        stores_data.append({
                            'id': store.id,
                            'name': store.name,
                            'city': store.location.city,
                            'state': store.location.state,
                            'demand_pallets': store.demand_pallets,
                            'latitude': store.location.latitude,
                            'longitude': store.location.longitude
                        })
                    
                    suppliers_data = []
                    for supplier in suppliers:
                        suppliers_data.append({
                            'id': supplier.id,
                            'name': supplier.name,
                            'city': supplier.location.city,
                            'state': supplier.location.state,
                            'available_pallets': supplier.available_pallets,
                            'cost_per_pallet': supplier.cost_per_pallet,
                            'latitude': supplier.location.latitude,
                            'longitude': supplier.location.longitude
                        })
                    
                    status = html.Div([
                        html.I(className="fas fa-check-circle text-success me-2"),
                        f" Loaded {len(stores)} stores and {len(suppliers)} suppliers"
                    ], className="alert alert-success")
                    
                    return stores_data, suppliers_data, status
                    
                except Exception as e:
                    status = html.Div([
                        html.I(className="fas fa-exclamation-triangle text-danger me-2"),
                        f"L Error loading data: {str(e)}"
                    ], className="alert alert-danger")
                    return [], [], status
            
            return dash.no_update, dash.no_update, dash.no_update
        
        @self.app.callback(
            [Output('optimization-results-store', 'data'),
             Output('status-message', 'children', allow_duplicate=True)],
            [Input('optimize-btn', 'n_clicks')],
            [State('stores-data-store', 'data'),
             State('suppliers-data-store', 'data'),
             State('optimization-method', 'value'),
             State('num-vehicles', 'value')],
            prevent_initial_call=True
        )
        def run_optimization(n_clicks, stores_data, suppliers_data, method, num_vehicles):
            if n_clicks and stores_data and suppliers_data:
                try:
                    # Convert data back to model objects
                    stores = []
                    for store_data in stores_data:
                        location = Location(
                            name=store_data['name'],
                            address="",
                            latitude=store_data['latitude'],
                            longitude=store_data['longitude'],
                            city=store_data['city'],
                            state=store_data['state'],
                            zip_code=""
                        )
                        from data.models import Store
                        store = Store(
                            id=store_data['id'],
                            name=store_data['name'],
                            location=location,
                            demand_pallets=store_data['demand_pallets']
                        )
                        stores.append(store)
                    
                    suppliers = []
                    for supplier_data in suppliers_data:
                        location = Location(
                            name=supplier_data['name'],
                            address="",
                            latitude=supplier_data['latitude'],
                            longitude=supplier_data['longitude'],
                            city=supplier_data['city'],
                            state=supplier_data['state'],
                            zip_code=""
                        )
                        from data.models import Supplier, PalletType
                        supplier = Supplier(
                            id=supplier_data['id'],
                            name=supplier_data['name'],
                            location=location,
                            available_pallets=supplier_data['available_pallets'],
                            cost_per_pallet=supplier_data['cost_per_pallet'],
                            lead_time_days=1,
                            capacity_per_day=100,
                            pallet_types=[PalletType.STANDARD]
                        )
                        suppliers.append(supplier)
                    
                    # Create vehicles
                    vehicles = []
                    for i in range(num_vehicles):
                        depot_location = Location(
                            name="depot",
                            address="Distribution Center",
                            latitude=41.8781,
                            longitude=-87.6298,
                            city="Chicago",
                            state="IL",
                            zip_code="60601"
                        )
                        vehicle = Vehicle(
                            id=f"truck_{i+1:02d}",
                            type="Standard Truck",
                            max_pallets=26,
                            max_weight=48000,
                            cost_per_mile=0.85,
                            cost_per_hour=35.0,
                            current_location=depot_location
                        )
                        vehicles.append(vehicle)
                    
                    # Run optimization
                    config = {
                        'solver': 'CBC',
                        'time_limit_seconds': 300,
                        'costs': {
                            'fuel_cost_per_mile': 0.65,
                            'driver_cost_per_hour': 25.0,
                            'warehouse_handling_cost': 15.0
                        }
                    }
                    
                    optimizer = PalletOptimizer(config)
                    
                    if method == 'heuristic':
                        depot_coords = (41.8781, -87.6298)
                        routes = optimizer.optimize_vehicle_routing_heuristic(stores, vehicles, depot_coords)
                        
                        total_cost = sum(route.total_cost for route in routes)
                        total_distance = sum(route.total_distance for route in routes)
                        total_time = sum(route.total_time for route in routes)
                        total_pallets = sum(route.pallets_delivered for route in routes)
                        total_capacity = sum(vehicle.max_pallets for vehicle in vehicles)
                        utilization = total_pallets / max(total_capacity, 1)
                        
                        result = OptimizationResult(
                            routes=routes,
                            total_cost=total_cost,
                            total_distance=total_distance,
                            total_time=total_time,
                            utilization_rate=utilization,
                            solver_status="Heuristic",
                            solve_time=0.1,
                            objective_value=total_cost
                        )
                    else:
                        result = optimizer.optimize_deliveries(stores, suppliers, vehicles)
                    
                    # Convert result to serializable format
                    routes_data = []
                    for route in result.routes:
                        routes_data.append({
                            'id': route.id,
                            'vehicle_id': route.vehicle_id,
                            'stops': route.stops,
                            'total_distance': route.total_distance,
                            'total_time': route.total_time,
                            'total_cost': route.total_cost,
                            'pallets_delivered': route.pallets_delivered
                        })
                    
                    results_data = {
                        'routes': routes_data,
                        'total_cost': result.total_cost,
                        'total_distance': result.total_distance,
                        'total_time': result.total_time,
                        'utilization_rate': result.utilization_rate,
                        'solver_status': result.solver_status,
                        'solve_time': result.solve_time,
                        'num_routes': len(result.routes)
                    }
                    
                    status = html.Div([
                        html.I(className="fas fa-check-circle text-success me-2"),
                        f"<¯ Optimization complete! Generated {len(routes_data)} routes with {result.utilization_rate:.1%} utilization"
                    ], className="alert alert-success")
                    
                    return results_data, status
                    
                except Exception as e:
                    status = html.Div([
                        html.I(className="fas fa-exclamation-triangle text-danger me-2"),
                        f"L Optimization failed: {str(e)}"
                    ], className="alert alert-danger")
                    return {}, status
            
            return dash.no_update, dash.no_update
        
        @self.app.callback(
            Output('summary-cards', 'children'),
            [Input('optimization-results-store', 'data')]
        )
        def update_summary_cards(results_data):
            if not results_data:
                return html.Div("=K Welcome! Load sample data and run optimization to see results.", 
                              className="alert alert-info")
            
            return html.Div([
                html.Div([
                    html.Div([
                        html.H3(f"${results_data['total_cost']:,.0f}", className="text-primary"),
                        html.P("Total Cost", className="mb-0")
                    ], className="card-body text-center")
                ], className="card col-md-2 me-2"),
                
                html.Div([
                    html.Div([
                        html.H3(f"{results_data['total_distance']:.0f}", className="text-info"),
                        html.P("Miles", className="mb-0")
                    ], className="card-body text-center")
                ], className="card col-md-2 me-2"),
                
                html.Div([
                    html.Div([
                        html.H3(f"{results_data['total_time']:.1f}", className="text-warning"),
                        html.P("Hours", className="mb-0")
                    ], className="card-body text-center")
                ], className="card col-md-2 me-2"),
                
                html.Div([
                    html.Div([
                        html.H3(f"{results_data['num_routes']}", className="text-success"),
                        html.P("Routes", className="mb-0")
                    ], className="card-body text-center")
                ], className="card col-md-2 me-2"),
                
                html.Div([
                    html.Div([
                        html.H3(f"{results_data['utilization_rate']:.1%}", className="text-danger"),
                        html.P("Utilization", className="mb-0")
                    ], className="card-body text-center")
                ], className="card col-md-2"),
                
            ], className="row")
        
        @self.app.callback(
            Output('tab-content', 'children'),
            [Input('results-tabs', 'value')],
            [State('optimization-results-store', 'data'),
             State('stores-data-store', 'data')]
        )
        def update_tab_content(active_tab, results_data, stores_data):
            if not results_data:
                return html.Div("No optimization results yet. Run optimization first!", 
                              className="alert alert-warning")
            
            if active_tab == 'routes':
                return self.create_routes_view(results_data)
            elif active_tab == 'analytics':
                return self.create_analytics_view(results_data)
            elif active_tab == 'tables':
                return self.create_tables_view(results_data)
            elif active_tab == 'map':
                return self.create_map_view(results_data, stores_data)
            
            return html.Div()
    
    def create_routes_view(self, results_data):
        routes_cards = []
        for i, route in enumerate(results_data['routes']):
            routes_cards.append(
                html.Div([
                    html.Div([
                        html.H5(f"=› {route['vehicle_id']}", className="card-title"),
                        html.P([
                            html.Strong("Route: "),
                            " ’ ".join(route['stops'])
                        ]),
                        html.P([
                            html.Strong("Distance: "), f"{route['total_distance']:.1f} miles"
                        ]),
                        html.P([
                            html.Strong("Cost: "), f"${route['total_cost']:.2f}"
                        ]),
                        html.P([
                            html.Strong("Pallets: "), f"{route['pallets_delivered']}"
                        ]),
                    ], className="card-body")
                ], className="card mb-3")
            )
        
        return html.Div([
            html.H4("=ú Optimized Routes"),
            html.Div(routes_cards)
        ])
    
    def create_analytics_view(self, results_data):
        # Create cost breakdown chart
        costs = ['Vehicle Cost', 'Fuel Cost', 'Labor Cost']
        values = [results_data['total_cost'] * 0.4, 
                 results_data['total_cost'] * 0.35, 
                 results_data['total_cost'] * 0.25]
        
        pie_chart = dcc.Graph(
            figure=px.pie(values=values, names=costs, title="Cost Breakdown")
        )
        
        # Route efficiency chart
        routes = results_data['routes']
        route_names = [r['vehicle_id'] for r in routes]
        distances = [r['total_distance'] for r in routes]
        costs = [r['total_cost'] for r in routes]
        
        bar_chart = dcc.Graph(
            figure=px.bar(x=route_names, y=distances, title="Distance by Route")
        )
        
        return html.Div([
            html.H4("=Ê Analytics Dashboard"),
            html.Div([
                html.Div([pie_chart], className="col-md-6"),
                html.Div([bar_chart], className="col-md-6"),
            ], className="row")
        ])
    
    def create_tables_view(self, results_data):
        routes_df = pd.DataFrame(results_data['routes'])
        
        return html.Div([
            html.H4("=Ë Data Tables"),
            html.H5("Routes Summary"),
            dash_table.DataTable(
                data=routes_df.to_dict('records'),
                columns=[
                    {'name': 'Vehicle', 'id': 'vehicle_id'},
                    {'name': 'Distance (mi)', 'id': 'total_distance', 'type': 'numeric', 'format': {'specifier': '.1f'}},
                    {'name': 'Time (hrs)', 'id': 'total_time', 'type': 'numeric', 'format': {'specifier': '.1f'}},
                    {'name': 'Cost ($)', 'id': 'total_cost', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                    {'name': 'Pallets', 'id': 'pallets_delivered', 'type': 'numeric'},
                ],
                style_cell={'textAlign': 'center'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'}
            )
        ])
    
    def create_map_view(self, results_data, stores_data):
        if not stores_data:
            return html.Div("Store location data not available for map view.", 
                          className="alert alert-warning")
        
        # Create a simple scatter plot as placeholder for map
        df_stores = pd.DataFrame(stores_data)
        
        map_fig = px.scatter(
            df_stores, x='longitude', y='latitude', 
            hover_name='name', size='demand_pallets',
            title="Store Locations and Demand"
        )
        
        return html.Div([
            html.H4("<¯ Geographic View"),
            dcc.Graph(figure=map_fig)
        ])
    
    def run(self, debug=True, port=8050):
        self.app.run_server(debug=debug, port=port, host='127.0.0.1')