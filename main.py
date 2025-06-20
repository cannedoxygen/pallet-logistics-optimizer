#!/usr/bin/env python3
"""
Frito-Lay Pallet Logistics Optimizer - Simple Flask Version
Made by Lyndsey Gledhill
"""

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frito-Lay Logistics Optimizer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
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
    </style>
</head>
<body>
    <div class="container-fluid bg-light min-vh-100">
        <!-- Header -->
        <div class="row">
            <div class="col">
                <div class="custom-header shadow-lg mb-4 py-4 px-4">
                    <div class="row">
                        <div class="col-12 col-md-8">
                            <h1 class="h3 h1-md text-white font-weight-bold mb-2">
                                <i class="fas fa-truck me-2" style="color: #FFD700;"></i>
                                <span class="d-none d-md-inline">Frito-Lay</span>
                                <span class="d-block d-md-inline">Logistics Optimizer</span>
                            </h1>
                            <p class="small lead-md text-white-75 mb-0">
                                <i class="fas fa-chart-line me-2" style="color: #FFD700;"></i>
                                Professional Route Optimization & Cost Analysis
                            </p>
                        </div>
                        <div class="col-12 col-md-4 text-end text-center text-md-end">
                            <span class="badge bg-warning mb-2 px-3 py-2">
                                <i class="fas fa-award me-1"></i>
                                Live Demo
                            </span>
                            <br>
                            <small class="text-white-75" style="font-size: 11px;">
                                <i class="fas fa-user-tie me-1"></i>
                                Made by Lyndsey Gledhill
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Demo Notice -->
        <div class="row">
            <div class="col">
                <div class="alert alert-info mb-4">
                    <h4 class="alert-heading">
                        <i class="fas fa-info-circle me-2"></i>
                        Live Frito-Lay Logistics Demo
                    </h4>
                    <hr>
                    <p>
                        This is a live demonstration of the Pallet Logistics Optimizer using realistic Frito-Lay data. 
                        The system shows optimized delivery routes for <strong>9 retail locations</strong> 
                        across 6 states, with snack product deliveries totaling <strong>$8,450 in optimized costs</strong>.
                    </p>
                </div>
            </div>
        </div>

        <!-- Metrics -->
        <div class="row g-3 mb-4">
            <div class="col-6 col-lg">
                <div class="card metrics-card shadow-sm border-0 h-100">
                    <div class="card-body text-center py-3">
                        <h3 class="text-primary mb-1">$8,450</h3>
                        <p class="text-muted mb-0 small">Total Cost</p>
                        <small class="text-success">
                            <i class="fas fa-arrow-down me-1"></i>
                            15% optimized
                        </small>
                    </div>
                </div>
            </div>
            <div class="col-6 col-lg">
                <div class="card metrics-card shadow-sm border-0 h-100">
                    <div class="card-body text-center py-3">
                        <h3 class="text-info mb-1">1,247</h3>
                        <p class="text-muted mb-0 small">Miles</p>
                        <small class="text-info">
                            <i class="fas fa-route me-1"></i>
                            3 routes
                        </small>
                    </div>
                </div>
            </div>
            <div class="col-6 col-lg">
                <div class="card metrics-card shadow-sm border-0 h-100">
                    <div class="card-body text-center py-3">
                        <h3 class="text-warning mb-1">18.2</h3>
                        <p class="text-muted mb-0 small">Hours</p>
                        <small class="text-warning">
                            <i class="fas fa-clock me-1"></i>
                            Delivery time
                        </small>
                    </div>
                </div>
            </div>
            <div class="col-6 col-lg">
                <div class="card metrics-card shadow-sm border-0 h-100">
                    <div class="card-body text-center py-3">
                        <h3 class="text-success mb-1">68</h3>
                        <p class="text-muted mb-0 small">Pallets</p>
                        <small class="text-success">
                            <i class="fas fa-boxes me-1"></i>
                            Delivered
                        </small>
                    </div>
                </div>
            </div>
            <div class="col-6 col-lg">
                <div class="card metrics-card shadow-sm border-0 h-100">
                    <div class="card-body text-center py-3">
                        <h3 class="text-danger mb-1">87%</h3>
                        <p class="text-muted mb-0 small">Efficiency</p>
                        <small class="text-danger">
                            <i class="fas fa-chart-line me-1"></i>
                            Fleet utilization
                        </small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="card shadow-lg border-0 mb-4">
            <div class="card-header">
                <ul class="nav nav-tabs card-header-tabs" id="mainTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active fw-bold" id="routes-tab" data-bs-toggle="tab" data-bs-target="#routes" type="button" role="tab">
                            🚛 Routes
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link fw-bold" id="costs-tab" data-bs-toggle="tab" data-bs-target="#costs" type="button" role="tab">
                            💰 Costs
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link fw-bold" id="stores-tab" data-bs-toggle="tab" data-bs-target="#stores" type="button" role="tab">
                            🏪 Stores
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link fw-bold" id="tolls-tab" data-bs-toggle="tab" data-bs-target="#tolls" type="button" role="tab">
                            🛣️ Tolls
                        </button>
                    </li>
                </ul>
            </div>
            <div class="card-body">
                <div class="tab-content" id="mainTabsContent">
                    <!-- Routes Tab -->
                    <div class="tab-pane fade show active" id="routes" role="tabpanel">
                        <h4><i class="fas fa-route me-2"></i>Optimized Route Analysis</h4>
                        
                        <!-- Route 1 -->
                        <div class="card route-card efficiency-high mb-3 shadow-sm border-0">
                            <div class="card-header">
                                <div class="row">
                                    <div class="col-8">
                                        <h5 class="mb-0 text-primary">
                                            <i class="fas fa-truck me-2"></i>Route 1: Truck_01
                                        </h5>
                                    </div>
                                    <div class="col-4 text-end">
                                        <span class="badge bg-success">88% Efficient</span>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <p><strong>🗺️ Route:</strong> Chicago DC → Walmart Chicago → Target Milwaukee → Kroger Detroit → Return</p>
                                <span class="badge bg-primary me-2">🚛 23 Pallets</span>
                                <span class="badge bg-success me-2">💰 $2,840</span>
                                <span class="badge bg-info me-2">📏 428 mi</span>
                                <span class="badge bg-warning">⏱️ 6.2 hrs</span>
                            </div>
                        </div>

                        <!-- Route 2 -->
                        <div class="card route-card efficiency-medium mb-3 shadow-sm border-0">
                            <div class="card-header">
                                <div class="row">
                                    <div class="col-8">
                                        <h5 class="mb-0 text-primary">
                                            <i class="fas fa-truck me-2"></i>Route 2: Truck_02
                                        </h5>
                                    </div>
                                    <div class="col-4 text-end">
                                        <span class="badge bg-warning">73% Efficient</span>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <p><strong>🗺️ Route:</strong> Cincinnati DC → Meijer Cincinnati → Walmart Columbus → Kroger Cleveland → Return</p>
                                <span class="badge bg-primary me-2">🚛 19 Pallets</span>
                                <span class="badge bg-success me-2">💰 $2,150</span>
                                <span class="badge bg-info me-2">📏 385 mi</span>
                                <span class="badge bg-warning">⏱️ 5.8 hrs</span>
                            </div>
                        </div>

                        <!-- Route 3 -->
                        <div class="card route-card efficiency-high mb-3 shadow-sm border-0">
                            <div class="card-header">
                                <div class="row">
                                    <div class="col-8">
                                        <h5 class="mb-0 text-primary">
                                            <i class="fas fa-truck me-2"></i>Route 3: Truck_03
                                        </h5>
                                    </div>
                                    <div class="col-4 text-end">
                                        <span class="badge bg-success">96% Efficient</span>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <p><strong>🗺️ Route:</strong> Dallas DC → Costco Dallas → Target Austin → Walmart Houston → Return</p>
                                <span class="badge bg-primary me-2">🚛 26 Pallets</span>
                                <span class="badge bg-success me-2">💰 $3,460</span>
                                <span class="badge bg-info me-2">📏 434 mi</span>
                                <span class="badge bg-warning">⏱️ 6.2 hrs</span>
                            </div>
                        </div>
                    </div>

                    <!-- Costs Tab -->
                    <div class="tab-pane fade" id="costs" role="tabpanel">
                        <h4><i class="fas fa-chart-pie me-2"></i>Cost Analytics</h4>
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <div class="card text-center">
                                    <div class="card-body">
                                        <h5>Vehicle Operations</h5>
                                        <h3 class="text-primary">$3,380</h3>
                                        <p class="text-muted">40.0% of total</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card text-center">
                                    <div class="card-body">
                                        <h5>Fuel Costs</h5>
                                        <h3 class="text-info">$2,958</h3>
                                        <p class="text-muted">35.0% of total</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card text-center">
                                    <div class="card-body">
                                        <h5>Labor Costs</h5>
                                        <h3 class="text-warning">$2,112</h3>
                                        <p class="text-muted">25.0% of total</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Stores Tab -->
                    <div class="tab-pane fade" id="stores" role="tabpanel">
                        <h4><i class="fas fa-store me-2"></i>Store Network</h4>
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>🏪 Store Name</th>
                                        <th>📍 City</th>
                                        <th>🗺️ State</th>
                                        <th>📦 Pallets</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td>Walmart Supercenter - Downtown Chicago</td><td>Chicago</td><td>IL</td><td>8</td></tr>
                                    <tr><td>Target Express - Milwaukee Downtown</td><td>Milwaukee</td><td>WI</td><td>6</td></tr>
                                    <tr><td>Kroger Marketplace - Detroit</td><td>Detroit</td><td>MI</td><td>9</td></tr>
                                    <tr><td>Meijer Supercenter - Cincinnati</td><td>Cincinnati</td><td>OH</td><td>7</td></tr>
                                    <tr><td>Walmart Neighborhood - Columbus</td><td>Columbus</td><td>OH</td><td>5</td></tr>
                                    <tr><td>Kroger Fresh Fare - Cleveland</td><td>Cleveland</td><td>OH</td><td>7</td></tr>
                                    <tr><td>Costco Wholesale - Dallas</td><td>Dallas</td><td>TX</td><td>10</td></tr>
                                    <tr><td>Target Supercenter - Austin</td><td>Austin</td><td>TX</td><td>8</td></tr>
                                    <tr><td>Walmart Supercenter - Houston</td><td>Houston</td><td>TX</td><td>8</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Tolls Tab -->
                    <div class="tab-pane fade" id="tolls" role="tabpanel">
                        <h4><i class="fas fa-road me-2"></i>Toll Rates</h4>
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>📍 From</th>
                                        <th>📍 To</th>
                                        <th>💰 Rate/Mile</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr><td>Chicago</td><td>Milwaukee</td><td>$0.150</td></tr>
                                    <tr><td>Indianapolis</td><td>Chicago</td><td>$0.120</td></tr>
                                    <tr><td>Columbus</td><td>Indianapolis</td><td>$0.140</td></tr>
                                    <tr><td>Detroit</td><td>Chicago</td><td>$0.180</td></tr>
                                    <tr><td>St. Louis</td><td>Chicago</td><td>$0.100</td></tr>
                                    <tr><td>Milwaukee</td><td>Detroit</td><td>$0.160</td></tr>
                                    <tr><td>Cincinnati</td><td>Columbus</td><td>$0.130</td></tr>
                                    <tr><td>Dallas</td><td>Austin</td><td>$0.110</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    '''
    return template

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)