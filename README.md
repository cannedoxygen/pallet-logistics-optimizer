# Pallet Logistics Optimizer

A comprehensive logistics optimization system for pallet routing and supply chain management.

## Features

- **Route Optimization**: Vehicle routing problem solving with capacity constraints
- **Cost Calculation**: Comprehensive cost modeling including fuel, labor, tolls, and handling
- **Supplier Assignment**: Optimal supplier-to-store assignment based on cost and constraints
- **Excel Integration**: Import/export data through Excel files
- **Multiple Solvers**: Support for CBC, CPLEX, GUROBI, and GLPK optimization solvers
- **Visualization**: Route visualization and cost analysis dashboards
- **Real-time Analysis**: Performance metrics and optimization potential assessment

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Sample Data**
   ```bash
   python scripts/generate_sample_data.py
   ```

3. **Run Optimization**
   ```bash
   python scripts/run_optimization.py --method heuristic
   ```

## Project Structure

```
pallet/
   config.yaml              # Configuration settings
   requirements.txt          # Python dependencies
   data/                    # Data files
      input/              # Input Excel files
      output/             # Optimization results
   src/                    # Source code
      core/               # Optimization algorithms
      data/               # Data models and handlers
      utils/              # Utility functions
      analysis/           # Analysis modules
      gui/                # GUI components
      visualization/      # Visualization tools
   scripts/                # Executable scripts
   tests/                  # Test files
   docs/                   # Documentation
```

## Configuration

Edit `config.yaml` to customize:
- Cost parameters (fuel, labor, tolls)
- Solver settings and time limits
- File paths and output preferences
- Vehicle constraints

## Usage Examples

### Basic Optimization
```bash
python scripts/run_optimization.py
```

### With Custom Data Files
```bash
python scripts/run_optimization.py --stores my_stores.xlsx --suppliers my_suppliers.xlsx
```

### Exact Optimization (slower but optimal)
```bash
python scripts/run_optimization.py --method exact
```

## Input Data Format

### Store Locations (store_locations.xlsx)
- store_id, store_name, address, city, state, zip_code
- latitude, longitude, demand_pallets, priority

### Supplier Data (supplier_data.xlsx)
- supplier_id, supplier_name, address, city, state, zip_code
- latitude, longitude, available_pallets, cost_per_pallet
- lead_time_days, capacity_per_day, reliability_score

## Output

The system generates Excel reports with:
- Optimized routes for each vehicle
- Cost breakdowns and performance metrics
- Summary statistics and KPIs
- Route visualization data

## Dependencies

- pandas, numpy: Data manipulation
- openpyxl: Excel file handling
- pulp: Linear programming solver
- geopy: Geographic calculations
- matplotlib, plotly: Visualization
- dash: Web dashboard (optional)

## License

MIT License