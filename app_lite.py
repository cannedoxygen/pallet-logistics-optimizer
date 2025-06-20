#!/usr/bin/env python3
"""
Lightweight Vercel entry point for Pallet Logistics Optimizer Demo
This version shows demo data without heavy optimization libraries
"""
import os
import sys
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import yaml

class LightweightPalletDashboard:
    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
        ])
        self.app.title = "Pallet Logistics Optimizer - Demo"
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
            dcc.Store(id='demo-results-store', data=self.get_demo_data()),
            
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
                                        html.Span("Professional Route Optimization Demo", className="d-none d-md-inline"),
                                        html.Span("Route Optimization Demo", className="d-block d-md-none")
                                    ], className="small lead-md text-white-75 mb-0")
                                ])
                            ], width=12, md=8),
                            dbc.Col([
                                html.Div([
                                    dbc.Badge([
                                        html.I(className="fas fa-award me-1"),
                                        "Demo Version"
                                    ], color="warning", className="mb-2 px-2 px-md-3 py-1 py-md-2", style={'fontSize': '12px'}),
                                    html.Br(className="d-none d-md-block"),
                                    html.Small([
                                        html.I(className="fas fa-shield-alt me-1"),
                                        html.Span("Frito-Lay Demo", className="d-block d-md-none"),
                                        html.Span("Frito-Lay Sample Data", className="d-none d-md-inline")
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
            
            # Demo Notice
            dbc.Row([
                dbc.Col([
                    dbc.Alert([
                        html.H4("🍟 Frito-Lay Logistics Demo", className="alert-heading"),
                        html.Hr(),
                        html.P([
                            "This is a demonstration of the Pallet Logistics Optimizer using Frito-Lay sample data. ",
                            "The demo shows optimized delivery routes for 16 retail locations across 6 states, ",
                            "served by 6 distribution centers with realistic snack product deliveries."
                        ]),
                        html.P([
                            html.Strong("Note: "),
                            "This lightweight version shows pre-calculated results for demonstration purposes. ",
                            "The full version includes real-time optimization capabilities."
                        ], className="mb-0 text-muted")
                    ], color="info", className="mb-4")
                ])
            ]),
            
            # Key Metrics
            html.Div(id="demo-metrics", className="mb-4"),
            
            # Results Tabs
            dbc.Card([
                dbc.CardHeader([
                    dbc.Tabs([
                        dbc.Tab(label="Route Overview", tab_id="overview", className="fw-bold"),
                        dbc.Tab(label="Cost Analysis", tab_id="costs", className="fw-bold"),
                        dbc.Tab(label="Store Locations", tab_id="locations", className="fw-bold"),
                    ], id="demo-tabs", active_tab="overview")
                ]),
                dbc.CardBody([
                    html.Div(id='demo-content', className="p-3")
                ])
            ], className="shadow-sm")
        ], fluid=True, className="bg-light min-vh-100")

    def setup_callbacks(self):
        @self.app.callback(
            Output('demo-metrics', 'children'),
            [Input('demo-results-store', 'data')]
        )
        def update_metrics(demo_data):
            cards = dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("$8,450", className="text-primary mb-1 h4 h3-md"),
                            html.P("Total Cost", className="text-muted mb-0 small")
                        ], className="text-center py-2")
                    ], className="shadow-sm border-0")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("1,247", className="text-info mb-1 h4 h3-md"),
                            html.P("Miles", className="text-muted mb-0 small")
                        ], className="text-center py-2")
                    ], className="shadow-sm border-0")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("18.2", className="text-warning mb-1 h4 h3-md"),
                            html.P("Hours", className="text-muted mb-0 small")
                        ], className="text-center py-2")
                    ], className="shadow-sm border-0")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("3", className="text-success mb-1 h4 h3-md"),
                            html.P("Routes", className="text-muted mb-0 small")
                        ], className="text-center py-2")
                    ], className="shadow-sm border-0")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("87%", className="text-danger mb-1 h4 h3-md"),
                            html.P("Efficiency", className="text-muted mb-0 small")
                        ], className="text-center py-2")
                    ], className="shadow-sm border-0")
                ], width=6, lg=True, className="mb-2 mb-lg-0"),
            ], className="g-2 g-lg-3")
            
            return cards
        
        @self.app.callback(
            Output('demo-content', 'children'),
            [Input('demo-tabs', 'active_tab')]
        )
        def update_demo_content(active_tab):
            if active_tab == 'overview':
                return self.create_overview()
            elif active_tab == 'costs':
                return self.create_cost_analysis()
            elif active_tab == 'locations':
                return self.create_locations_view()
            return html.Div()
    
    def create_overview(self):
        routes = [
            {
                'vehicle': 'Truck_01',
                'route': 'Chicago DC → Walmart Chicago → Target Milwaukee → Kroger Detroit → Return',
                'pallets': 23,
                'cost': '$2,840',
                'distance': '428 miles',
                'time': '6.2 hours'
            },
            {
                'vehicle': 'Truck_02', 
                'route': 'Cincinnati DC → Meijer Cincinnati → Walmart Columbus → Kroger Cleveland → Return',
                'pallets': 19,
                'cost': '$2,150',
                'distance': '385 miles',
                'time': '5.8 hours'
            },
            {
                'vehicle': 'Truck_03',
                'route': 'Dallas DC → Costco Dallas → Target Austin → Walmart Houston → Return',
                'pallets': 26,
                'cost': '$3,460',
                'distance': '434 miles',
                'time': '6.2 hours'
            }
        ]
        
        cards = []
        for route in routes:
            card = dbc.Card([
                dbc.CardHeader([
                    html.H5(f"Vehicle: {route['vehicle']}", className="mb-0 text-primary")
                ]),
                dbc.CardBody([
                    html.P(route['route'], className="text-monospace small mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge(f"{route['pallets']} Pallets", color="primary", className="me-2"),
                            dbc.Badge(route['cost'], color="success")
                        ], width=12, md=8),
                        dbc.Col([
                            html.Small(f"{route['distance']} • {route['time']}", className="text-muted")
                        ], width=12, md=4)
                    ])
                ])
            ], className="mb-3 shadow-sm")
            cards.append(card)
        
        return html.Div([
            html.H4("Optimized Route Overview", className="mb-4"),
            html.Div(cards)
        ])
    
    def create_cost_analysis(self):
        # Cost breakdown chart
        costs = ['Vehicle Operations', 'Fuel Costs', 'Labor Costs']
        values = [3380, 2958, 2112]
        
        pie_fig = px.pie(values=values, names=costs, 
                        title="Cost Breakdown Analysis",
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        pie_fig.update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20))
        
        # Route costs bar chart
        vehicles = ['Truck_01', 'Truck_02', 'Truck_03']
        route_costs = [2840, 2150, 3460]
        
        bar_fig = px.bar(x=vehicles, y=route_costs,
                        title="Cost by Vehicle Route",
                        labels={'x': 'Vehicle', 'y': 'Cost ($)'},
                        color=route_costs,
                        color_continuous_scale="Viridis")
        bar_fig.update_layout(height=350, margin=dict(t=50, b=50, l=50, r=20))
        
        return html.Div([
            html.H4("Cost Analytics Dashboard", className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=pie_fig, config={'responsive': True})
                ], width=12, lg=6, className="mb-3 mb-lg-0"),
                dbc.Col([
                    dcc.Graph(figure=bar_fig, config={'responsive': True})
                ], width=12, lg=6)
            ])
        ])
    
    def create_locations_view(self):
        stores = [
            {'name': 'Walmart Supercenter - Chicago', 'state': 'IL', 'pallets': 8},
            {'name': 'Target Express - Milwaukee', 'state': 'WI', 'pallets': 6},
            {'name': 'Kroger Marketplace - Detroit', 'state': 'MI', 'pallets': 9},
            {'name': 'Meijer - Cincinnati', 'state': 'OH', 'pallets': 7},
            {'name': 'Walmart - Columbus', 'state': 'OH', 'pallets': 5},
            {'name': 'Kroger - Cleveland', 'state': 'OH', 'pallets': 7},
            {'name': 'Costco Wholesale - Dallas', 'state': 'TX', 'pallets': 10},
            {'name': 'Target - Austin', 'state': 'TX', 'pallets': 8},
            {'name': 'Walmart - Houston', 'state': 'TX', 'pallets': 8}
        ]
        
        return html.Div([
            html.H4("Store Locations & Demand", className="mb-4"),
            dash_table.DataTable(
                data=stores,
                columns=[
                    {'name': 'Store Name', 'id': 'name'},
                    {'name': 'State', 'id': 'state'},
                    {'name': 'Pallets Delivered', 'id': 'pallets', 'type': 'numeric'}
                ],
                style_cell={'textAlign': 'left', 'fontFamily': 'Arial', 'fontSize': '14px'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)'
                    }
                ],
                page_size=10
            )
        ])
    
    def get_demo_data(self):
        return {
            'total_cost': 8450,
            'total_distance': 1247,
            'total_time': 18.2,
            'num_routes': 3,
            'efficiency': 0.87
        }

# Create the dashboard instance
dashboard = LightweightPalletDashboard()

# Vercel expects the app to be available as 'app'
app = dashboard.app.server

if __name__ == "__main__":
    dashboard.app.run(debug=False, port=8050)