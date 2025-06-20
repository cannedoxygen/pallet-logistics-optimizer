#!/usr/bin/env python3
"""
🍟 Frito-Lay Pallet Logistics Optimizer - Vercel API Handler
WSGI-compatible entry point for Vercel serverless deployment
Made by Lyndsey Gledhill
"""

from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px

class FritoLayLogisticsDemo:
    def __init__(self):
        self.app = Dash(__name__, 
                       external_stylesheets=[
                           dbc.themes.BOOTSTRAP,
                           "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
                       ],
                       requests_pathname_prefix="/")
        self.app.title = "🍟 Frito-Lay Logistics Optimizer"
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
            
            # 🍟 Header
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1([
                            "🍟 Frito-Lay Logistics Optimizer"
                        ], className="text-white text-center py-4"),
                        html.P([
                            "Made by Lyndsey Gledhill"
                        ], className="text-white-75 text-center")
                    ])
                ])
            ], className="bg-primary mb-4"),
            
            # 📊 Metrics
            html.Div(id="metrics-dashboard", className="mb-4"),
            
            # 📋 Results Tabs
            dbc.Card([
                dbc.CardHeader([
                    dbc.Tabs([
                        dbc.Tab(label="Routes", tab_id="routes"),
                        dbc.Tab(label="Costs", tab_id="costs"),
                        dbc.Tab(label="Stores", tab_id="stores"),
                    ], id="main-tabs", active_tab="routes")
                ]),
                dbc.CardBody([
                    html.Div(id='tab-content')
                ])
            ])
        ], fluid=True)

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
                            html.H3(f"${metrics['total_cost']:,}", className="text-primary"),
                            html.P("Total Cost", className="text-muted")
                        ], className="text-center")
                    ])
                ], width=12, md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['total_distance']:,}", className="text-info"),
                            html.P("Miles", className="text-muted")
                        ], className="text-center")
                    ])
                ], width=12, md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['total_pallets']}", className="text-success"),
                            html.P("Pallets", className="text-muted")
                        ], className="text-center")
                    ])
                ], width=12, md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{metrics['efficiency']:.0%}", className="text-warning"),
                            html.P("Efficiency", className="text-muted")
                        ], className="text-center")
                    ])
                ], width=12, md=3)
            ])
            
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
            return html.Div()
    
    def create_routes_view(self, data):
        routes = data['routes']
        
        route_cards = []
        for i, route in enumerate(routes, 1):
            card = dbc.Card([
                dbc.CardBody([
                    html.H5(f"Route {i}: {route['vehicle']}", className="text-primary"),
                    html.P(" → ".join(route['stops']), className="text-monospace small"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge(f"{route['pallets']} Pallets", color="primary", className="me-2"),
                            dbc.Badge(f"${route['cost']:,}", color="success")
                        ])
                    ])
                ])
            ], className="mb-3")
            route_cards.append(card)
        
        return html.Div(route_cards)
    
    def create_cost_analysis(self, data):
        cost_data = data['cost_breakdown']
        
        pie_fig = px.pie(
            values=list(cost_data.values()), 
            names=list(cost_data.keys()),
            title="Cost Breakdown"
        )
        
        return dcc.Graph(figure=pie_fig)
    
    def create_stores_view(self, data):
        stores = data['stores']
        
        return dash_table.DataTable(
            data=stores,
            columns=[
                {'name': 'Store', 'id': 'name'},
                {'name': 'City', 'id': 'city'},
                {'name': 'State', 'id': 'state'},
                {'name': 'Pallets', 'id': 'pallets'}
            ],
            style_table={'overflowX': 'auto'}
        )
    
    def get_embedded_data(self):
        return {
            'summary': {
                'total_cost': 8450,
                'total_distance': 1247,
                'total_pallets': 68,
                'efficiency': 0.87
            },
            'routes': [
                {
                    'vehicle': 'Truck_01',
                    'stops': ['Chicago DC', 'Walmart Chicago', 'Target Milwaukee', 'Return'],
                    'pallets': 23,
                    'cost': 2840
                },
                {
                    'vehicle': 'Truck_02',
                    'stops': ['Cincinnati DC', 'Meijer Cincinnati', 'Walmart Columbus', 'Return'],
                    'pallets': 19,
                    'cost': 2150
                },
                {
                    'vehicle': 'Truck_03',
                    'stops': ['Dallas DC', 'Costco Dallas', 'Target Austin', 'Return'],
                    'pallets': 26,
                    'cost': 3460
                }
            ],
            'cost_breakdown': {
                'Vehicle Operations': 3380,
                'Fuel Costs': 2958,
                'Labor Costs': 2112
            },
            'stores': [
                {'name': 'Walmart Chicago', 'city': 'Chicago', 'state': 'IL', 'pallets': 8},
                {'name': 'Target Milwaukee', 'city': 'Milwaukee', 'state': 'WI', 'pallets': 6},
                {'name': 'Kroger Detroit', 'city': 'Detroit', 'state': 'MI', 'pallets': 9},
                {'name': 'Meijer Cincinnati', 'city': 'Cincinnati', 'state': 'OH', 'pallets': 7},
                {'name': 'Walmart Columbus', 'city': 'Columbus', 'state': 'OH', 'pallets': 5},
                {'name': 'Costco Dallas', 'city': 'Dallas', 'state': 'TX', 'pallets': 10},
                {'name': 'Target Austin', 'city': 'Austin', 'state': 'TX', 'pallets': 8}
            ]
        }

# Create dashboard instance
dashboard = FritoLayLogisticsDemo()

# Vercel handler function
def handler(request, response):
    return dashboard.app.server(request, response)

# For direct access
app = dashboard.app.server

if __name__ == "__main__":
    dashboard.app.run(debug=False, port=8050)