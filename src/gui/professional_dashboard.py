import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
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


class ProfessionalPalletDashboard:
    def __init__(self):
        # Initialize with Bootstrap theme and FontAwesome icons
        self.app = dash.Dash(__name__, external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
        ])
        self.app.title = "Pallet Logistics Optimizer - Professional Edition"
        self.excel_handler = ExcelHandler()
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        # Add viewport meta tag for mobile responsiveness
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
        
        self.app.layout = dbc.Container([
            dcc.Store(id='optimization-results-store'),
            dcc.Store(id='stores-data-store'),
            dcc.Store(id='suppliers-data-store'),
            
            # Enhanced Header - Mobile Responsive
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H1([
                                        html.I(className="fas fa-truck me-2", style={'color': '#FFD700'}),
                                        html.Span("Pallet Logistics", className="d-none d-md-inline"),
                                        html.Span("Optimizer", className="d-block d-md-inline")
                                    ], className="h3 h1-md text-white font-weight-bold mb-2"),
                                    html.P([
                                        html.I(className="fas fa-chart-line me-2", style={'color': '#FFD700'}),
                                        html.Span("Professional Route Optimization & Cost Analysis", className="d-none d-md-inline"),
                                        html.Span("Route Optimization Platform", className="d-block d-md-none")
                                    ], className="small lead-md text-white-75 mb-0")
                                ])
                            ], width=12, md=8),
                            dbc.Col([
                                html.Div([
                                    dbc.Badge([
                                        html.I(className="fas fa-award me-1"),
                                        "Enterprise"
                                    ], color="warning", className="mb-2 px-2 px-md-3 py-1 py-md-2", style={'fontSize': '12px'}),
                                    html.Br(className="d-none d-md-block"),
                                    html.Small([
                                        html.I(className="fas fa-shield-alt me-1"),
                                        html.Span("Secure • Reliable", className="d-block d-md-none"),
                                        html.Span("Secure • Scalable • Reliable", className="d-none d-md-inline")
                                    ], className="text-white-50"),
                                    html.Br(),
                                    html.Small([
                                        html.I(className="fas fa-user-tie me-1"),
                                        "Made by Lyndsey Gledhill"
                                    ], className="text-white-75", style={'fontSize': '11px'})
                                ], className="text-end text-center text-md-end")
                            ], width=12, md=4)
                        ])
                    ], className="py-3 py-md-4 px-3 px-md-4")
                ])
            ], className="bg-gradient-primary shadow-lg mb-4", style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'borderBottom': '4px solid #FFD700'
            }),
            
            # Instructions Panel
            dbc.Row([
                dbc.Col([
                    dbc.Alert([
                        html.H4("Quick Start Guide", className="alert-heading"),
                        html.Hr(),
                        html.Ol([
                            html.Li("Click 'Load Sample Data' to use demonstration data"),
                            html.Li("Adjust optimization settings in the control panel"),
                            html.Li("Click 'Run Optimization' to generate optimal routes"),
                            html.Li("Review results in the analytics dashboard below"),
                            html.Li("Export results using the download options")
                        ], className="mb-2"),
                        html.P([
                            html.Strong("For custom data: "),
                            "Place your Excel files in the data/input directory. Use the provided templates for proper formatting."
                        ], className="mb-0 text-muted")
                    ], color="info", className="mb-4")
                ])
            ]),
            
            # Main Content - Mobile Responsive
            dbc.Row([
                # Control Panel
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5("Control Panel", className="mb-0 text-primary")
                        ]),
                        dbc.CardBody([
                            # Data Management Section
                            html.Div([
                                html.H6("Data Management", className="text-secondary mb-3"),
                                dbc.ButtonGroup([
                                    dbc.Button("Load Sample Data", 
                                             id="load-sample-btn",
                                             color="outline-primary",
                                             className="me-2"),
                                    dbc.Button("Export Templates", 
                                             color="outline-secondary",
                                             size="sm")
                                ], className="mb-3 d-flex"),
                            ]),
                            
                            html.Hr(),
                            
                            # Optimization Settings
                            html.Div([
                                html.H6("Optimization Settings", className="text-secondary mb-3"),
                                
                                html.Label("Method", className="form-label fw-bold"),
                                dbc.RadioItems(
                                    id='optimization-method',
                                    options=[
                                        {"label": "Heuristic (Fast - Recommended)", "value": "heuristic"},
                                        {"label": "Exact Optimization (Slower)", "value": "exact"}
                                    ],
                                    value="heuristic",
                                    className="mb-3"
                                ),
                                
                                html.Label("Fleet Size", className="form-label fw-bold"),
                                html.P("Number of vehicles available for routing", 
                                       className="text-muted small mb-2"),
                                dcc.Slider(
                                    id='num-vehicles',
                                    min=1, max=10, step=1, value=3,
                                    marks={i: {'label': str(i), 'style': {'font-size': '12px'}} 
                                          for i in range(1, 11)},
                                    className="mb-4"
                                ),
                                
                                html.Div([
                                    dbc.Button("Run Optimization", 
                                             id="optimize-btn",
                                             color="success",
                                             size="lg",
                                             className="w-100")
                                ]),
                            ]),
                            
                            html.Hr(),
                            
                            # Status Section
                            html.Div([
                                html.H6("Status", className="text-secondary mb-2"),
                                html.Div(id="status-message")
                            ])
                        ])
                    ], className="shadow-sm")
                ], width=12, lg=4, className="mb-4 mb-lg-0"),
                
                # Results Panel
                dbc.Col([
                    # Key Metrics Cards
                    html.Div(id="metrics-cards", className="mb-4"),
                    
                    # Results Tabs
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Tabs([
                                dbc.Tab(label="Route Analysis", tab_id="routes", 
                                       className="fw-bold"),
                                dbc.Tab(label="Cost Analytics", tab_id="analytics", 
                                       className="fw-bold"),
                                dbc.Tab(label="Data Tables", tab_id="tables", 
                                       className="fw-bold"),
                                dbc.Tab(label="Geographic View", tab_id="map", 
                                       className="fw-bold"),
                            ], id="results-tabs", active_tab="routes")
                        ]),
                        dbc.CardBody([
                            html.Div(id='tab-content', className="p-3")
                        ])
                    ], className="shadow-sm")
                ], width=12, lg=8)
            ])
        ], fluid=True, className="bg-light min-vh-100")

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
                    print("🔍 DEBUG: Starting load_sample_data")
                    print(f"🔍 DEBUG: Excel handler type: {type(self.excel_handler)}")
                    
                    print("🔍 DEBUG: Loading stores...")
                    stores = self.excel_handler.load_stores()
                    print(f"🔍 DEBUG: Loaded {len(stores)} stores successfully")
                    
                    print("🔍 DEBUG: Loading suppliers...")
                    suppliers = self.excel_handler.load_suppliers()
                    print(f"🔍 DEBUG: Loaded {len(suppliers)} suppliers successfully")
                    
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
                    
                    status = dbc.Alert([
                        html.I(className="bi bi-check-circle-fill me-2"),
                        f"Successfully loaded {len(stores)} stores and {len(suppliers)} suppliers"
                    ], color="success", dismissable=True)
                    
                    print("🔍 DEBUG: Successfully completed load_sample_data")
                    return stores_data, suppliers_data, status
                    
                except Exception as e:
                    import traceback
                    error_details = traceback.format_exc()
                    print(f"🔍 DEBUG: ERROR in load_sample_data: {str(e)}")
                    print(f"🔍 DEBUG: Full traceback:\n{error_details}")
                    
                    status = dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        f"Error loading data: {str(e)}"
                    ], color="danger", dismissable=True)
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
                    # Show processing status
                    processing_status = dbc.Alert([
                        "⚙️ Processing optimization... This may take a few moments."
                    ], color="info")
                    
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
                    
                    status = dbc.Alert([
                        html.I(className="bi bi-check-circle-fill me-2"),
                        html.Div([
                            html.Strong("Optimization Complete!"),
                            html.Br(),
                            f"Generated {len(routes_data)} optimal routes with {result.utilization_rate:.1%} fleet utilization"
                        ])
                    ], color="success", dismissable=True)
                    
                    return results_data, status
                    
                except Exception as e:
                    status = dbc.Alert([
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        f"Optimization failed: {str(e)}"
                    ], color="danger", dismissable=True)
                    return {}, status
            
            return dash.no_update, dash.no_update
        
        @self.app.callback(
            Output('metrics-cards', 'children'),
            [Input('optimization-results-store', 'data')]
        )
        def update_metrics_cards(results_data):
            if not results_data:
                return dbc.Alert([
                    html.H4("Welcome to Pallet Logistics Optimizer", className="alert-heading"),
                    html.P("Load your data and run optimization to view comprehensive analytics and route planning results.", 
                           className="mb-0")
                ], color="light", className="text-center")
            
            cards = dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2(f"${results_data['total_cost']:,.0f}", 
                                   className="text-primary mb-1"),
                            html.P("Total Cost", className="text-muted mb-0 small")
                        ], className="text-center")
                    ], className="shadow-sm border-0")
                ], width=True),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2(f"{results_data['total_distance']:.0f}", 
                                   className="text-info mb-1"),
                            html.P("Miles", className="text-muted mb-0 small")
                        ], className="text-center")
                    ], className="shadow-sm border-0")
                ], width=True),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2(f"{results_data['total_time']:.1f}", 
                                   className="text-warning mb-1"),
                            html.P("Hours", className="text-muted mb-0 small")
                        ], className="text-center")
                    ], className="shadow-sm border-0")
                ], width=True),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2(f"{results_data['num_routes']}", 
                                   className="text-success mb-1"),
                            html.P("Routes", className="text-muted mb-0 small")
                        ], className="text-center")
                    ], className="shadow-sm border-0")
                ], width=True),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2(f"{results_data['utilization_rate']:.1%}", 
                                   className="text-danger mb-1"),
                            html.P("Utilization", className="text-muted mb-0 small")
                        ], className="text-center")
                    ], className="shadow-sm border-0")
                ], width=True),
            ], className="g-3")
            
            return cards
        
        @self.app.callback(
            Output('tab-content', 'children'),
            [Input('results-tabs', 'active_tab')],
            [State('optimization-results-store', 'data'),
             State('stores-data-store', 'data')]
        )
        def update_tab_content(active_tab, results_data, stores_data):
            if not results_data:
                return dbc.Alert([
                    html.H5("No Results Available", className="alert-heading"),
                    html.P("Please load data and run optimization to view results.", className="mb-0")
                ], color="warning")
            
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
        route_cards = []
        for i, route in enumerate(results_data['routes']):
            card = dbc.Card([
                dbc.CardHeader([
                    html.H5(f"Vehicle: {route['vehicle_id']}", className="mb-0 text-primary")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Strong("Route Sequence:"),
                            html.P(" → ".join(route['stops']), className="text-monospace small")
                        ], width=8),
                        dbc.Col([
                            dbc.Badge(f"{route['pallets_delivered']} Pallets", 
                                    color="primary", className="mb-1"),
                            html.Br(),
                            dbc.Badge(f"${route['total_cost']:.0f}", 
                                    color="success")
                        ], width=4, className="text-end")
                    ]),
                    html.Hr(className="my-2"),
                    dbc.Row([
                        dbc.Col([
                            html.Small(f"Distance: {route['total_distance']:.1f} miles", 
                                     className="text-muted")
                        ], width=6),
                        dbc.Col([
                            html.Small(f"Time: {route['total_time']:.1f} hours", 
                                     className="text-muted")
                        ], width=6)
                    ])
                ])
            ], className="mb-3 shadow-sm border-0")
            route_cards.append(card)
        
        return html.Div([
            html.H4("Route Analysis", className="mb-4"),
            html.Div(route_cards)
        ])
    
    def create_analytics_view(self, results_data):
        # Cost breakdown pie chart
        costs = ['Vehicle Operations', 'Fuel Costs', 'Labor Costs']
        values = [results_data['total_cost'] * 0.4, 
                 results_data['total_cost'] * 0.35, 
                 results_data['total_cost'] * 0.25]
        
        pie_fig = px.pie(values=values, names=costs, 
                        title="Cost Breakdown Analysis",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        pie_fig.update_layout(showlegend=True, height=350, margin=dict(t=50, b=20, l=20, r=20))
        
        # Route efficiency bar chart
        routes = results_data['routes']
        route_names = [r['vehicle_id'] for r in routes]
        distances = [r['total_distance'] for r in routes]
        costs = [r['total_cost'] for r in routes]
        
        bar_fig = px.bar(x=route_names, y=distances, 
                        title="Distance by Vehicle Route",
                        labels={'x': 'Vehicle', 'y': 'Distance (miles)'},
                        color=distances,
                        color_continuous_scale="Blues")
        bar_fig.update_layout(showlegend=False, height=350, margin=dict(t=50, b=50, l=50, r=20))
        
        return html.Div([
            html.H4("Cost Analytics", className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=pie_fig, config={'responsive': True})
                ], width=12, lg=6, className="mb-3 mb-lg-0"),
                dbc.Col([
                    dcc.Graph(figure=bar_fig, config={'responsive': True})
                ], width=12, lg=6)
            ])
        ])
    
    def create_tables_view(self, results_data):
        routes_df = pd.DataFrame(results_data['routes'])
        
        return html.Div([
            html.H4("Data Tables", className="mb-4"),
            dash_table.DataTable(
                data=routes_df.to_dict('records'),
                columns=[
                    {'name': 'Vehicle', 'id': 'vehicle_id'},
                    {'name': 'Distance (mi)', 'id': 'total_distance', 'type': 'numeric', 
                     'format': {'specifier': '.1f'}},
                    {'name': 'Time (hrs)', 'id': 'total_time', 'type': 'numeric', 
                     'format': {'specifier': '.1f'}},
                    {'name': 'Cost ($)', 'id': 'total_cost', 'type': 'numeric', 
                     'format': {'specifier': '.2f'}},
                    {'name': 'Pallets', 'id': 'pallets_delivered', 'type': 'numeric'},
                ],
                style_cell={'textAlign': 'center', 'fontFamily': 'Arial'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold',
                            'border': '1px solid #dee2e6'},
                style_data={'border': '1px solid #dee2e6'},
                sort_action="native",
                page_size=10
            )
        ])
    
    def create_map_view(self, results_data, stores_data):
        if not stores_data:
            return dbc.Alert("Store location data not available for geographic view.", 
                           color="warning")
        
        df_stores = pd.DataFrame(stores_data)
        
        map_fig = px.scatter(
            df_stores, x='longitude', y='latitude', 
            hover_name='name', size='demand_pallets',
            title="Store Locations and Demand Distribution",
            labels={'longitude': 'Longitude', 'latitude': 'Latitude'},
            color='demand_pallets',
            color_continuous_scale="Viridis"
        )
        map_fig.update_layout(height=400, margin=dict(t=50, b=20, l=20, r=20))
        
        return html.Div([
            html.H4("Geographic View", className="mb-4"),
            dcc.Graph(figure=map_fig, config={'responsive': True})
        ])
    
    def run(self, debug=True, port=8050):
        self.app.run(debug=debug, port=port, host='127.0.0.1')