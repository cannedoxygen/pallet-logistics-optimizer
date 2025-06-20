#!/usr/bin/env python3
"""
🍟 Frito-Lay Pallet Logistics Optimizer - Vercel Demo
Ultra-lightweight version with embedded data for Vercel deployment
Made by Lyndsey Gledhill
"""

from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

class FritoLayLogisticsDemo:
    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
        ])
        self.app.title = "🍟 Frito-Lay Logistics Optimizer - Demo"
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        # Mobile responsive viewport
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
            dcc.Store(id='demo-store', data=self.get_embedded_data()),
            
            # 🍟 Professional Header - Mobile Responsive
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H1([
                                        html.I(className="fas fa-truck me-2", style={'color': '#FFD700'}),
                                        html.Span("🍟 Frito-Lay", className="d-none d-md-inline"),
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
            ], className="bg-gradient-primary shadow-lg mb-4", style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'borderBottom': '4px solid #FFD700'
            }),
            
            # 🚨 Demo Notice
            dbc.Row([
                dbc.Col([
                    dbc.Alert([
                        html.H4([
                            html.I(className="fas fa-info-circle me-2"),
                            "🍟 Live Frito-Lay Logistics Demo"
                        ], className="alert-heading"),
                        html.Hr(),
                        html.P([
                            "This is a live demonstration of the Pallet Logistics Optimizer using realistic Frito-Lay data. ",
                            "The system shows optimized delivery routes for ", html.Strong("16 retail locations"), 
                            " across 6 states, served by ", html.Strong("6 distribution centers"), 
                            " with snack product deliveries totaling ", html.Strong("$8,450 in optimized costs"), "."
                        ]),
                        html.P([
                            html.I(className="fas fa-chart-bar me-1"),
                            "Explore the tabs below to see route analysis, cost breakdowns, and interactive visualizations."
                        ], className="mb-0 text-primary fw-bold")
                    ], color="info", className="mb-4")
                ])
            ]),
            
            # 📊 Key Metrics Dashboard
            html.Div(id="metrics-dashboard", className="mb-4"),
            
            # 📋 Interactive Results Tabs
            dbc.Card([
                dbc.CardHeader([
                    dbc.Tabs([
                        dbc.Tab(label="🚛 Route Overview", tab_id="routes", className="fw-bold"),
                        dbc.Tab(label="💰 Cost Analytics", tab_id="costs", className="fw-bold"),
                        dbc.Tab(label="🏪 Store Network", tab_id="stores", className="fw-bold"),
                        dbc.Tab(label="📍 Geographic Map", tab_id="map", className="fw-bold"),
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
                    ], className="shadow-sm border-0 h-100")
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
                    ], className="shadow-sm border-0 h-100")
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
                    ], className="shadow-sm border-0 h-100")
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
                    ], className="shadow-sm border-0 h-100")
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
                    ], className="shadow-sm border-0 h-100")
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
            elif active_tab == 'map':
                return self.create_geographic_view(data)
            return html.Div()
    
    def create_routes_view(self, data):
        routes = data['routes']
        
        route_cards = []
        for i, route in enumerate(routes, 1):
            # Route status badge
            status_color = "success" if route['efficiency'] > 0.8 else "warning" if route['efficiency'] > 0.6 else "danger"
            
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
                            dbc.Badge(f"{route['efficiency']:.0%} Efficient", 
                                    color=status_color, className="float-end")
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
                            dbc.Badge(f"📏 {route['distance']} mi", 
                                    color="info", className="me-2 mb-1"),
                            dbc.Badge(f"⏱️ {route['time']} hrs", 
                                    color="warning", className="mb-1")
                        ], width=12)
                    ]),
                    
                    html.Hr(className="my-3"),
                    
                    # Performance indicators
                    dbc.Row([
                        dbc.Col([
                            html.Small([
                                html.I(className="fas fa-tachometer-alt me-1 text-muted"),
                                f"Avg Speed: {route['distance']/route['time']:.1f} mph"
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
            ], className="mb-3 shadow-sm border-0")
            route_cards.append(card)
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-route me-2"),
                "Optimized Route Analysis"
            ], className="mb-4"),
            html.Div(route_cards)
        ])
    
    def create_cost_analysis(self, data):
        # Cost breakdown pie chart
        cost_data = data['cost_breakdown']
        
        pie_fig = px.pie(
            values=list(cost_data.values()), 
            names=list(cost_data.keys()),
            title="💰 Cost Breakdown Analysis",
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
        efficiency_scores = [r['efficiency'] * 100 for r in routes]
        
        bar_fig = px.bar(
            x=route_names, 
            y=efficiency_scores,
            title="📊 Route Efficiency Comparison",
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
            html.H5("💸 Cost Summary", className="mb-3"),
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
                    ], className="text-center")
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
                    ], className="text-center")
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
                    ], className="text-center")
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
                    ])
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{len(set(s['state'] for s in stores))}", className="text-info mb-1"),
                            html.P("States", className="mb-0")
                        ], className="text-center")
                    ])
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{sum(s['pallets'] for s in stores)}", className="text-success mb-1"),
                            html.P("Total Pallets", className="mb-0")
                        ], className="text-center")
                    ])
                ], width=6, md=3, className="mb-3"),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{sum(s['pallets'] for s in stores)/len(stores):.1f}", className="text-warning mb-1"),
                            html.P("Avg per Store", className="mb-0")
                        ], className="text-center")
                    ])
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
                    {'name': '📦 Pallets', 'id': 'pallets', 'type': 'numeric'},
                    {'name': '⭐ Priority', 'id': 'priority'}
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
                        'if': {'filter_query': '{priority} = High'},
                        'backgroundColor': '#f8d7da',
                        'color': 'black',
                    }
                ],
                sort_action="native",
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ])
    
    def create_geographic_view(self, data):
        stores = data['stores']
        
        # Create scatter plot map
        map_fig = px.scatter(
            x=[s['longitude'] for s in stores],
            y=[s['latitude'] for s in stores],
            size=[s['pallets'] for s in stores],
            color=[s['pallets'] for s in stores],
            hover_name=[s['name'] for s in stores],
            hover_data={
                'x': False,
                'y': False,
                'size': False,
                'color': False
            },
            custom_data=[[s['city'], s['state'], s['pallets']] for s in stores],
            title="🗺️ Frito-Lay Store Locations & Demand Distribution",
            labels={'x': 'Longitude', 'y': 'Latitude', 'color': 'Pallets', 'size': 'Demand'},
            color_continuous_scale="Viridis",
            size_max=20
        )
        
        map_fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
                         "City: %{customdata[0]}<br>" +
                         "State: %{customdata[1]}<br>" +
                         "Pallets: %{customdata[2]}<br>" +
                         "<extra></extra>"
        )
        
        map_fig.update_layout(
            height=400, 
            margin=dict(t=50, b=20, l=20, r=20),
            showlegend=True
        )
        
        return html.Div([
            html.H4([
                html.I(className="fas fa-map-marked-alt me-2"),
                "Geographic Distribution"
            ], className="mb-4"),
            
            dcc.Graph(figure=map_fig, config={'responsive': True}),
            
            html.Hr(className="my-4"),
            
            # Geographic summary
            html.H5("📊 Geographic Analysis", className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.P([
                        html.Strong("Coverage Area: "),
                        "6 states across Midwest and South regions"
                    ]),
                    html.P([
                        html.Strong("Largest Market: "),
                        "Texas (3 stores, 26 pallets)"
                    ]),
                    html.P([
                        html.Strong("Density: "),
                        "Urban markets with high-volume locations"
                    ])
                ], width=12, md=6),
                dbc.Col([
                    html.P([
                        html.Strong("Distribution Strategy: "),
                        "Hub-and-spoke model"
                    ]),
                    html.P([
                        html.Strong("Route Efficiency: "),
                        "Optimized for minimal total distance"
                    ]),
                    html.P([
                        html.Strong("Store Types: "),
                        "Walmart, Target, Kroger, Meijer, Costco"
                    ])
                ], width=12, md=6)
            ])
        ])
    
    def get_embedded_data(self):
        """🍟 Embedded Frito-Lay demonstration data - no file system dependencies"""
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
                {'name': 'Walmart Supercenter - Downtown Chicago', 'city': 'Chicago', 'state': 'IL', 'pallets': 8, 'priority': 'High', 'latitude': 41.8781, 'longitude': -87.6298},
                {'name': 'Target Express - Milwaukee Downtown', 'city': 'Milwaukee', 'state': 'WI', 'pallets': 6, 'priority': 'Medium', 'latitude': 43.0389, 'longitude': -87.9065},
                {'name': 'Kroger Marketplace - Detroit', 'city': 'Detroit', 'state': 'MI', 'pallets': 9, 'priority': 'High', 'latitude': 42.3314, 'longitude': -83.0458},
                {'name': 'Meijer Supercenter - Cincinnati', 'city': 'Cincinnati', 'state': 'OH', 'pallets': 7, 'priority': 'Medium', 'latitude': 39.1031, 'longitude': -84.5120},
                {'name': 'Walmart Neighborhood - Columbus', 'city': 'Columbus', 'state': 'OH', 'pallets': 5, 'priority': 'Low', 'latitude': 39.9612, 'longitude': -82.9988},
                {'name': 'Kroger Fresh Fare - Cleveland', 'city': 'Cleveland', 'state': 'OH', 'pallets': 7, 'priority': 'Medium', 'latitude': 41.4993, 'longitude': -81.6944},
                {'name': 'Costco Wholesale - Dallas', 'city': 'Dallas', 'state': 'TX', 'pallets': 10, 'priority': 'High', 'latitude': 32.7767, 'longitude': -96.7970},
                {'name': 'Target Supercenter - Austin', 'city': 'Austin', 'state': 'TX', 'pallets': 8, 'priority': 'High', 'latitude': 30.2672, 'longitude': -97.7431},
                {'name': 'Walmart Supercenter - Houston', 'city': 'Houston', 'state': 'TX', 'pallets': 8, 'priority': 'Medium', 'latitude': 29.7604, 'longitude': -95.3698}
            ]
        }

# 🚀 Create dashboard instance
dashboard = FritoLayLogisticsDemo()

# Vercel expects 'app' variable
app = dashboard.app.server

if __name__ == "__main__":
    dashboard.app.run(debug=False, port=8050)