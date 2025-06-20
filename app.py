#!/usr/bin/env python3
"""
Frito-Lay Pallet Logistics Optimizer - Complete Demo
Professional route optimization and cost analysis dashboard
Made by Lyndsey Gledhill
"""

from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

class FritoLayLogisticsDemo:
    def __init__(self):
        self.app = Dash(__name__, 
                       external_stylesheets=[
                           dbc.themes.BOOTSTRAP,
                           "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
                       ])
        self.app.title = "Frito-Lay Logistics Optimizer - Demo"
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        # Mobile responsive viewport with custom CSS
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <style>
                .custom-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                    border-bottom: 4px solid #FFD700;
                }
                .metrics-card {
                    transition: all 0.3s ease;
                    border: none !important;
                }
                .metrics-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
                }
                .route-card {
                    transition: all 0.2s ease;
                    border-left: 4px solid #007bff;
                }
                .route-card:hover {
                    transform: translateX(5px);
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }
                .efficiency-high { border-left-color: #28a745 !important; }
                .efficiency-medium { border-left-color: #ffc107 !important; }
                .efficiency-low { border-left-color: #dc3545 !important; }
                .bg-gradient-primary {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                }
                .animate-fade-in {
                    animation: fadeIn 0.6s ease-in;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                </style>
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
            dcc.Store(id='demo-store', data=self.get_embedded_data()),
            
            # Professional Header - Mobile Responsive
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H1([
                                        html.I(className="fas fa-truck me-2", style={'color': '#FFD700'}),
                                        html.Span("Frito-Lay", className="d-none d-md-inline"),
                                        html.Span("Logistics Optimizer", className="d-block d-md-inline")
                                    ], className="h3 h1-md text-white font-weight-bold mb-2"),
                                    html.P([
                                        html.I(className="fas fa-chart-line me-2", style={'color': '#FFD700'}),
                                        html.Span("Professional Route Optimization & Cost Analysis", className="d-none d-md-inline"),
                                        html.Span("Route Optimization Demo", className="d-block d-md-none")
                                    ], className="small lead-md text-white-75 mb-0")
                                ])
                            ], width=12, md=8),
                            dbc.Col([
                                html.Div([
                                    dbc.Badge([
                                        html.I(className="fas fa-award me-1"),
                                        "Enterprise Demo"
                                    ], color="warning", className="mb-2 px-2 px-md-3 py-1 py-md-2", style={'fontSize': '12px'}),
                                    html.Br(className="d-none d-md-block"),
                                    html.Small([
                                        html.I(className="fas fa-shield-alt me-1"),
                                        html.Span("Live Demo", className="d-block d-md-none"),
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
            ], className="custom-header shadow-lg mb-4"),
            
            # Demo Notice
            dbc.Row([
                dbc.Col([
                    dbc.Alert([
                        html.H4([
                            html.I(className="fas fa-info-circle me-2"),
                            "Live Frito-Lay Logistics Demo"
                        ], className="alert-heading"),
                        html.Hr(),
                        html.P([
                            "This is a live demonstration of the Pallet Logistics Optimizer using realistic Frito-Lay data. ",
                            "The system shows optimized delivery routes for ", html.Strong("9 retail locations"), 
                            " across 6 states, with snack product deliveries totaling ", html.Strong("$8,450 in optimized costs"), "."
                        ]),
                        html.P([
                            html.I(className="fas fa-chart-bar me-1"),
                            "Explore the tabs below to see route analysis, cost breakdowns, and interactive visualizations."
                        ], className="mb-0 text-primary fw-bold")
                    ], color="info", className="mb-4 animate-fade-in")
                ])
            ]),
            
            # Metrics
            html.Div(id="metrics-dashboard", className="mb-4"),
            
            # Results Tabs
            dbc.Card([
                dbc.CardHeader([
                    dbc.Tabs([
                        dbc.Tab(label="🚛 Route Overview", tab_id="routes", className="fw-bold"),
                        dbc.Tab(label="💰 Cost Analytics", tab_id="costs", className="fw-bold"),
                        dbc.Tab(label="🏪 Store Network", tab_id="stores", className="fw-bold"),
                        dbc.Tab(label="🛣️ Toll Rates", tab_id="tolls", className="fw-bold"),
                        dbc.Tab(label="📦 Orders History", tab_id="orders", className="fw-bold"),
                        dbc.Tab(label="🏭 Suppliers", tab_id="suppliers", className="fw-bold"),
                    ], id="main-tabs", active_tab="routes")
                ]),
                dbc.CardBody([
                    html.Div(id='tab-content', className="p-2 p-md-3")
                ])
            ], className="shadow-lg border-0")
        ], fluid=True, className="bg-light min-vh-100")

    def setup_callbacks(self):
        @self.app.callback(
            Output('metrics-dashboard', 'children'),
            [Input('demo-store', 'data')]
        )
        def update_metrics(data):
            metrics = data['summary']
            
            cards = dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"${metrics['total_cost']:,}", 
                                   className="text-primary mb-1 h4 h3-md"),
                            html.P("Total Cost", className="text-muted mb-0 small"),
                            html.Small([
                                html.I(className="fas fa-arrow-down me-1 text-success"),
                                "15% optimized"
                            ], className="text-success")
                        ], className="text-center py-2")
                    ], className="metrics-card shadow-sm border-0 h-100")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['total_distance']:,}", 
                                   className="text-info mb-1 h4 h3-md"),
                            html.P("Miles", className="text-muted mb-0 small"),
                            html.Small([
                                html.I(className="fas fa-route me-1"),
                                f"{len(data['routes'])} routes"
                            ], className="text-info")
                        ], className="text-center py-2")
                    ], className="metrics-card shadow-sm border-0 h-100")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['total_time']:.1f}", 
                                   className="text-warning mb-1 h4 h3-md"),
                            html.P("Hours", className="text-muted mb-0 small"),
                            html.Small([
                                html.I(className="fas fa-clock me-1"),
                                "Delivery time"
                            ], className="text-warning")
                        ], className="text-center py-2")
                    ], className="metrics-card shadow-sm border-0 h-100")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['total_pallets']}", 
                                   className="text-success mb-1 h4 h3-md"),
                            html.P("Pallets", className="text-muted mb-0 small"),
                            html.Small([
                                html.I(className="fas fa-boxes me-1"),
                                "Delivered"
                            ], className="text-success")
                        ], className="text-center py-2")
                    ], className="metrics-card shadow-sm border-0 h-100")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['efficiency']:.0%}", 
                                   className="text-danger mb-1 h4 h3-md"),
                            html.P("Efficiency", className="text-muted mb-0 small"),
                            html.Small([
                                html.I(className="fas fa-chart-line me-1"),
                                "Fleet utilization"
                            ], className="text-danger")
                        ], className="text-center py-2")
                    ], className="metrics-card shadow-sm border-0 h-100")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
            ], className="g-2 g-lg-3")
            
            return cards
        
        @self.app.callback(
            Output('tab-content', 'children'),
            [Input('main-tabs', 'active_tab')],
            [State('demo-store', 'data')]
        )
        def update_content(active_tab, data):
            if active_tab == 'routes':
                return self.create_routes_view(data)
            elif active_tab == 'costs':
                return self.create_cost_analysis(data)
            elif active_tab == 'stores':
                return self.create_stores_view(data)
            elif active_tab == 'tolls':
                return self.create_toll_rates_view(data)
            elif active_tab == 'orders':
                return self.create_orders_history_view(data)
            elif active_tab == 'suppliers':
                return self.create_suppliers_view(data)
            return html.Div()
    
    def create_routes_view(self, data):
        routes = data['routes']
        
        route_cards = []
        for i, route in enumerate(routes, 1):
            # Determine efficiency class for styling
            efficiency = route.get('efficiency', 0.7)
            if efficiency > 0.8:
                efficiency_class = "efficiency-high"
                efficiency_color = "success"
            elif efficiency > 0.6:
                efficiency_class = "efficiency-medium"  
                efficiency_color = "warning"
            else:
                efficiency_class = "efficiency-low"
                efficiency_color = "danger"
            
            card = dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            html.H5([
                                html.I(className="fas fa-truck me-2"),
                                f"Route {i}: {route['vehicle']}"
                            ], className="mb-0 text-primary")
                        ], width=12, md=8),
                        dbc.Col([
                            dbc.Badge(f"{efficiency:.0%} Efficient", 
                                    color=efficiency_color, className="float-end")
                        ], width=12, md=4, className="text-end mt-2 mt-md-0")
                    ])
                ]),
                dbc.CardBody([
                    # Route sequence
                    html.Div([
                        html.Strong("🗺️ Route Sequence:"),
                        html.P(" → ".join(route['stops']), 
                              className="text-monospace small mb-3 ms-3")
                    ]),
                    
                    # Key metrics row
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge(f"🚛 {route['pallets']} Pallets", 
                                    color="primary", className="me-2 mb-1"),
                            dbc.Badge(f"💰 ${route['cost']:,}", 
                                    color="success", className="me-2 mb-1"),
                            dbc.Badge(f"📏 {route.get('distance', 400)} mi", 
                                    color="info", className="me-2 mb-1"),
                            dbc.Badge(f"⏱️ {route.get('time', 6)} hrs", 
                                    color="warning", className="mb-1")
                        ], width=12)
                    ]),
                    
                    html.Hr(className="my-3"),
                    
                    # Performance indicators
                    dbc.Row([
                        dbc.Col([
                            html.Small([
                                html.I(className="fas fa-tachometer-alt me-1 text-muted"),
                                f"Avg Speed: {route.get('distance', 400)/route.get('time', 6):.1f} mph"
                            ], className="text-muted")
                        ], width=12, sm=6),
                        dbc.Col([
                            html.Small([
                                html.I(className="fas fa-dollar-sign me-1 text-muted"),
                                f"Cost per Pallet: ${route['cost']/route['pallets']:.0f}"
                            ], className="text-muted")
                        ], width=12, sm=6)
                    ])
                ])
            ], className=f"route-card {efficiency_class} mb-3 shadow-sm border-0")
            route_cards.append(card)
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-route me-2"),
                "Optimized Route Analysis"
            ], className="mb-4"),
            html.Div(route_cards)
        ])
    
    def create_cost_analysis(self, data):
        cost_data = data['cost_breakdown']
        
        pie_fig = px.pie(
            values=list(cost_data.values()), 
            names=list(cost_data.keys()),
            title="Cost Breakdown Analysis",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        )
        pie_fig.update_layout(
            height=350, 
            margin=dict(t=50, b=20, l=20, r=20),
            font=dict(size=12)
        )
        
        # Route efficiency comparison
        routes = data['routes']
        route_names = [f"Route {i+1}" for i in range(len(routes))]
        efficiency_scores = [route.get('efficiency', 0.7) * 100 for route in routes]
        
        bar_fig = px.bar(
            x=route_names, 
            y=efficiency_scores,
            title="Route Efficiency Comparison",
            labels={'x': 'Route', 'y': 'Efficiency (%)'},
            color=efficiency_scores,
            color_continuous_scale="RdYlGn"
        )
        bar_fig.update_layout(
            height=350, 
            margin=dict(t=50, b=50, l=50, r=20),
            showlegend=False
        )
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-chart-pie me-2"),
                "Cost Analytics Dashboard"
            ], className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=pie_fig, config={'responsive': True})
                ], width=12, lg=6, className="mb-3 mb-lg-0"),
                dbc.Col([
                    dcc.Graph(figure=bar_fig, config={'responsive': True})
                ], width=12, lg=6)
            ]),
            
            # Cost summary cards
            html.Hr(className="my-4"),
            html.H5("Cost Summary", className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Vehicle Operations", className="card-title"),
                            html.H4(f"${cost_data['Vehicle Operations']:,}", 
                                   className="text-primary"),
                            html.P(f"{cost_data['Vehicle Operations']/sum(cost_data.values()):.1%} of total", 
                                  className="text-muted small mb-0")
                        ])
                    ], className="text-center metrics-card")
                ], width=12, md=4, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Fuel Costs", className="card-title"),
                            html.H4(f"${cost_data['Fuel Costs']:,}", 
                                   className="text-info"),
                            html.P(f"{cost_data['Fuel Costs']/sum(cost_data.values()):.1%} of total", 
                                  className="text-muted small mb-0")
                        ])
                    ], className="text-center metrics-card")
                ], width=12, md=4, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Labor Costs", className="card-title"),
                            html.H4(f"${cost_data['Labor Costs']:,}", 
                                   className="text-warning"),
                            html.P(f"{cost_data['Labor Costs']/sum(cost_data.values()):.1%} of total", 
                                  className="text-muted small mb-0")
                        ])
                    ], className="text-center metrics-card")
                ], width=12, md=4, className="mb-3")
            ])
        ])
    
    def create_stores_view(self, data):
        stores = data['stores']
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-store me-2"),
                "Frito-Lay Store Network"
            ], className="mb-4"),
            
            # Store statistics
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{len(stores)}", className="text-primary mb-1"),
                            html.P("Total Stores", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{len(set(s['state'] for s in stores))}", className="text-info mb-1"),
                            html.P("States", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{sum(s['pallets'] for s in stores)}", className="text-success mb-1"),
                            html.P("Total Pallets", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{sum(s['pallets'] for s in stores)/len(stores):.1f}", className="text-warning mb-1"),
                            html.P("Avg per Store", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3")
            ]),
            
            html.Hr(className="my-4"),
            
            # Store data table
            dash_table.DataTable(
                data=stores,
                columns=[
                    {'name': '🏪 Store Name', 'id': 'name'},
                    {'name': '📍 City', 'id': 'city'},
                    {'name': '🗺️ State', 'id': 'state'},
                    {'name': '📦 Pallets', 'id': 'pallets', 'type': 'numeric'}
                ],
                style_cell={
                    'textAlign': 'left', 
                    'fontFamily': 'Arial', 
                    'fontSize': '14px',
                    'padding': '12px'
                },
                style_header={
                    'backgroundColor': '#f8f9fa', 
                    'fontWeight': 'bold',
                    'border': '1px solid #dee2e6'
                },
                style_data={
                    'border': '1px solid #dee2e6'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)'
                    }
                ],
                sort_action="native",
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ])
    
    def create_toll_rates_view(self, data):
        toll_rates = [
            {'from_location': 'Chicago', 'to_location': 'Milwaukee', 'rate_per_mile': 0.15},
            {'from_location': 'Indianapolis', 'to_location': 'Chicago', 'rate_per_mile': 0.12},
            {'from_location': 'Columbus', 'to_location': 'Indianapolis', 'rate_per_mile': 0.14},
            {'from_location': 'Detroit', 'to_location': 'Chicago', 'rate_per_mile': 0.18},
            {'from_location': 'St. Louis', 'to_location': 'Chicago', 'rate_per_mile': 0.10},
            {'from_location': 'Milwaukee', 'to_location': 'Detroit', 'rate_per_mile': 0.16},
            {'from_location': 'Cincinnati', 'to_location': 'Columbus', 'rate_per_mile': 0.13},
            {'from_location': 'Dallas', 'to_location': 'Austin', 'rate_per_mile': 0.11}
        ]
        
        avg_rate = sum(rate['rate_per_mile'] for rate in toll_rates) / len(toll_rates)
        max_rate = max(toll_rates, key=lambda x: x['rate_per_mile'])
        min_rate = min(toll_rates, key=lambda x: x['rate_per_mile'])
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-road me-2"),
                "Toll Rates Analysis"
            ], className="mb-4"),
            
            # Summary metrics
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"${avg_rate:.3f}", className="text-primary mb-1"),
                            html.P("Average Rate/Mile", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"${max_rate['rate_per_mile']:.3f}", className="text-danger mb-1"),
                            html.P("Highest Rate", className="mb-0"),
                            html.Small(f"{max_rate['from_location']} → {max_rate['to_location']}", className="text-muted")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"${min_rate['rate_per_mile']:.3f}", className="text-success mb-1"),
                            html.P("Lowest Rate", className="mb-0"),
                            html.Small(f"{min_rate['from_location']} → {min_rate['to_location']}", className="text-muted")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{len(toll_rates)}", className="text-info mb-1"),
                            html.P("Total Routes", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3")
            ]),
            
            html.Hr(className="my-4"),
            
            # Toll rates table
            dash_table.DataTable(
                data=toll_rates,
                columns=[
                    {'name': '📍 From Location', 'id': 'from_location'},
                    {'name': '📍 To Location', 'id': 'to_location'},
                    {'name': '💰 Rate per Mile', 'id': 'rate_per_mile', 'type': 'numeric', 'format': {'specifier': '$.3f'}}
                ],
                style_cell={
                    'textAlign': 'left', 
                    'fontFamily': 'Arial', 
                    'fontSize': '14px',
                    'padding': '12px'
                },
                style_header={
                    'backgroundColor': '#f8f9fa', 
                    'fontWeight': 'bold',
                    'border': '1px solid #dee2e6'
                },
                style_data={
                    'border': '1px solid #dee2e6'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)'
                    },
                    {
                        'if': {'filter_query': '{rate_per_mile} > 0.15'},
                        'backgroundColor': '#f8d7da',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{rate_per_mile} < 0.12'},
                        'backgroundColor': '#d1eddf',
                        'color': 'black'
                    }
                ],
                sort_action="native",
                style_table={'overflowX': 'auto'}
            )
        ])
    
    def create_orders_history_view(self, data):
        orders = [
            {'order_id': 'FL_2024_001', 'store_id': 'WM_CHI_001', 'quantity': 45, 'priority': 'High', 'product_mix': 'Cheetos Crunchy, Lay\'s Classic'},
            {'order_id': 'FL_2024_002', 'store_id': 'TG_MIL_002', 'quantity': 32, 'priority': 'Medium', 'product_mix': 'Ruffles Original, Smartfood Popcorn'},
            {'order_id': 'FL_2024_003', 'store_id': 'KR_DET_003', 'quantity': 58, 'priority': 'High', 'product_mix': 'Cheetos Crunchy, Fritos Original'},
            {'order_id': 'FL_2024_004', 'store_id': 'MJ_CIN_004', 'quantity': 28, 'priority': 'Low', 'product_mix': 'Fritos Original, Smartfood Popcorn'},
            {'order_id': 'FL_2024_005', 'store_id': 'WM_COL_005', 'quantity': 41, 'priority': 'Medium', 'product_mix': 'Doritos Nacho Cheese, Lay\'s Classic'},
            {'order_id': 'FL_2024_006', 'store_id': 'CS_DAL_006', 'quantity': 67, 'priority': 'High', 'product_mix': 'Cheetos Flamin\' Hot, Lay\'s BBQ'},
            {'order_id': 'FL_2024_007', 'store_id': 'TG_AUS_007', 'quantity': 39, 'priority': 'Medium', 'product_mix': 'Fritos Scoops, Ruffles Cheddar'},
            {'order_id': 'FL_2024_008', 'store_id': 'WM_HOU_008', 'quantity': 52, 'priority': 'High', 'product_mix': 'Doritos Cool Ranch, Cheetos Puffs'}
        ]
        
        total_quantity = sum(order['quantity'] for order in orders)
        high_priority = len([o for o in orders if o['priority'] == 'High'])
        avg_order_size = total_quantity / len(orders)
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-history me-2"),
                "Orders History Dashboard"
            ], className="mb-4"),
            
            # Order statistics
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{len(orders)}", className="text-primary mb-1"),
                            html.P("Total Orders", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{total_quantity}", className="text-success mb-1"),
                            html.P("Total Quantity", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{high_priority}", className="text-danger mb-1"),
                            html.P("High Priority", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{avg_order_size:.1f}", className="text-info mb-1"),
                            html.P("Avg Order Size", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3")
            ]),
            
            html.Hr(className="my-4"),
            
            # Orders table
            dash_table.DataTable(
                data=orders,
                columns=[
                    {'name': '📋 Order ID', 'id': 'order_id'},
                    {'name': '🏪 Store ID', 'id': 'store_id'},
                    {'name': '📦 Quantity', 'id': 'quantity', 'type': 'numeric'},
                    {'name': '🚨 Priority', 'id': 'priority'},
                    {'name': 'Product Mix', 'id': 'product_mix'}
                ],
                style_cell={
                    'textAlign': 'left', 
                    'fontFamily': 'Arial', 
                    'fontSize': '14px',
                    'padding': '12px',
                    'maxWidth': '200px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_header={
                    'backgroundColor': '#f8f9fa', 
                    'fontWeight': 'bold',
                    'border': '1px solid #dee2e6'
                },
                style_data={
                    'border': '1px solid #dee2e6',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)'
                    },
                    {
                        'if': {'filter_query': '{priority} = High'},
                        'backgroundColor': '#f8d7da',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{priority} = Low'},
                        'backgroundColor': '#d1eddf',
                        'color': 'black'
                    }
                ],
                sort_action="native",
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ])
    
    def create_suppliers_view(self, data):
        suppliers = [
            {'name': 'Frito-Lay Chicago Distribution Center', 'city': 'Chicago', 'state': 'IL', 'available_pallets': 250, 'cost_per_pallet': 85, 'reliability_score': 98},
            {'name': 'Frito-Lay Indianapolis Hub', 'city': 'Indianapolis', 'state': 'IN', 'available_pallets': 180, 'cost_per_pallet': 82, 'reliability_score': 95},
            {'name': 'Frito-Lay Milwaukee Center', 'city': 'Milwaukee', 'state': 'WI', 'available_pallets': 120, 'cost_per_pallet': 87, 'reliability_score': 92},
            {'name': 'Frito-Lay St. Louis Facility', 'city': 'St. Louis', 'state': 'MO', 'available_pallets': 200, 'cost_per_pallet': 80, 'reliability_score': 96},
            {'name': 'Frito-Lay Columbus Distribution', 'city': 'Columbus', 'state': 'OH', 'available_pallets': 160, 'cost_per_pallet': 83, 'reliability_score': 94},
            {'name': 'Frito-Lay Dallas Mega Center', 'city': 'Dallas', 'state': 'TX', 'available_pallets': 300, 'cost_per_pallet': 78, 'reliability_score': 99}
        ]
        
        total_pallets = sum(s['available_pallets'] for s in suppliers)
        avg_cost = sum(s['cost_per_pallet'] for s in suppliers) / len(suppliers)
        avg_reliability = sum(s['reliability_score'] for s in suppliers) / len(suppliers)
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-industry me-2"),
                "Frito-Lay Supplier Network"
            ], className="mb-4"),
            
            # Supplier statistics
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{len(suppliers)}", className="text-primary mb-1"),
                            html.P("Active Suppliers", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{total_pallets:,}", className="text-success mb-1"),
                            html.P("Total Capacity", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"${avg_cost:.0f}", className="text-warning mb-1"),
                            html.P("Avg Cost/Pallet", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{avg_reliability:.1f}%", className="text-info mb-1"),
                            html.P("Avg Reliability", className="mb-0")
                        ], className="text-center")
                    ], className="metrics-card")
                ], width=6, md=3, className="mb-3")
            ]),
            
            html.Hr(className="my-4"),
            
            # Suppliers table
            dash_table.DataTable(
                data=suppliers,
                columns=[
                    {'name': '🏭 Supplier Name', 'id': 'name'},
                    {'name': '📍 City', 'id': 'city'},
                    {'name': '🗺️ State', 'id': 'state'},
                    {'name': '📦 Available Pallets', 'id': 'available_pallets', 'type': 'numeric'},
                    {'name': '💰 Cost per Pallet', 'id': 'cost_per_pallet', 'type': 'numeric', 'format': {'specifier': '$'}},
                    {'name': '⭐ Reliability Score', 'id': 'reliability_score', 'type': 'numeric', 'format': {'specifier': '.0%'}}
                ],
                style_cell={
                    'textAlign': 'left', 
                    'fontFamily': 'Arial', 
                    'fontSize': '14px',
                    'padding': '12px',
                    'maxWidth': '200px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_header={
                    'backgroundColor': '#f8f9fa', 
                    'fontWeight': 'bold',
                    'border': '1px solid #dee2e6'
                },
                style_data={
                    'border': '1px solid #dee2e6',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)'
                    },
                    {
                        'if': {'filter_query': '{reliability_score} > 97'},
                        'backgroundColor': '#d1eddf',
                        'color': 'black'
                    },
                    {
                        'if': {'filter_query': '{cost_per_pallet} < 82'},
                        'backgroundColor': '#cce5ff',
                        'color': 'black'
                    }
                ],
                sort_action="native",
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ])

    def get_embedded_data(self):
        return {
            'summary': {
                'total_cost': 8450,
                'total_distance': 1247,
                'total_time': 18.2,
                'total_pallets': 68,
                'efficiency': 0.87
            },
            'routes': [
                {
                    'vehicle': 'Truck_01',
                    'stops': ['Chicago DC', 'Walmart Chicago', 'Target Milwaukee', 'Kroger Detroit', 'Return'],
                    'pallets': 23,
                    'cost': 2840,
                    'distance': 428,
                    'time': 6.2,
                    'efficiency': 0.88
                },
                {
                    'vehicle': 'Truck_02',
                    'stops': ['Cincinnati DC', 'Meijer Cincinnati', 'Walmart Columbus', 'Kroger Cleveland', 'Return'],
                    'pallets': 19,
                    'cost': 2150,
                    'distance': 385,
                    'time': 5.8,
                    'efficiency': 0.73
                },
                {
                    'vehicle': 'Truck_03',
                    'stops': ['Dallas DC', 'Costco Dallas', 'Target Austin', 'Walmart Houston', 'Return'],
                    'pallets': 26,
                    'cost': 3460,
                    'distance': 434,
                    'time': 6.2,
                    'efficiency': 0.96
                }
            ],
            'cost_breakdown': {
                'Vehicle Operations': 3380,
                'Fuel Costs': 2958,
                'Labor Costs': 2112
            },
            'stores': [
                {'name': 'Walmart Supercenter - Downtown Chicago', 'city': 'Chicago', 'state': 'IL', 'pallets': 8},
                {'name': 'Target Express - Milwaukee Downtown', 'city': 'Milwaukee', 'state': 'WI', 'pallets': 6},
                {'name': 'Kroger Marketplace - Detroit', 'city': 'Detroit', 'state': 'MI', 'pallets': 9},
                {'name': 'Meijer Supercenter - Cincinnati', 'city': 'Cincinnati', 'state': 'OH', 'pallets': 7},
                {'name': 'Walmart Neighborhood - Columbus', 'city': 'Columbus', 'state': 'OH', 'pallets': 5},
                {'name': 'Kroger Fresh Fare - Cleveland', 'city': 'Cleveland', 'state': 'OH', 'pallets': 7},
                {'name': 'Costco Wholesale - Dallas', 'city': 'Dallas', 'state': 'TX', 'pallets': 10},
                {'name': 'Target Supercenter - Austin', 'city': 'Austin', 'state': 'TX', 'pallets': 8},
                {'name': 'Walmart Supercenter - Houston', 'city': 'Houston', 'state': 'TX', 'pallets': 8}
            ]
        }

# Create dashboard instance
dashboard = FritoLayLogisticsDemo()

# Vercel expects 'app' variable
app = dashboard.app.server

if __name__ == "__main__":
    dashboard.app.run(debug=False, port=8050)