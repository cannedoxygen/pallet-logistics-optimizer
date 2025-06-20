import pulp
import numpy as np
from typing import Dict, List, Tuple, Optional
import time
from datetime import datetime
import uuid

from data.models import (
    Store, Supplier, Vehicle, Route, OptimizationResult, 
    RouteStatus, DistanceMatrix
)
from core.cost_calculator import CostCalculator
from utils.geo_utils import calculate_distance


class PalletOptimizer:
    def __init__(self, config: Dict):
        self.config = config
        self.solver_name = config.get('solver', 'CBC')
        self.time_limit = config.get('time_limit_seconds', 3600)
        self.mip_gap = config.get('mip_gap', 0.01)
        
        self.cost_calculator = CostCalculator(config.get('costs', {}))
        
    def optimize_deliveries(self, stores: List[Store], suppliers: List[Supplier], 
                          vehicles: List[Vehicle], 
                          distance_matrix: Optional[DistanceMatrix] = None) -> OptimizationResult:
        
        start_time = time.time()
        
        # Set up the optimization problem
        prob = pulp.LpProblem("Pallet_Delivery_Optimization", pulp.LpMinimize)
        
        # Decision variables
        # x[i][j][k] = 1 if vehicle k travels from location i to location j
        locations = ['depot'] + [store.location.name for store in stores]
        n_locations = len(locations)
        n_vehicles = len(vehicles)
        
        # Create decision variables
        x = {}
        for i in range(n_locations):
            for j in range(n_locations):
                for k in range(n_vehicles):
                    if i != j:  # Cannot travel from a location to itself
                        x[i, j, k] = pulp.LpVariable(f"x_{i}_{j}_{k}", cat='Binary')
        
        # Vehicle load variables
        load = {}
        for k in range(n_vehicles):
            for i in range(n_locations):
                load[k, i] = pulp.LpVariable(f"load_{k}_{i}", lowBound=0, cat='Integer')
        
        # Objective function: minimize total cost
        total_cost = 0
        
        for i in range(n_locations):
            for j in range(n_locations):
                for k in range(n_vehicles):
                    if i != j and (i, j, k) in x:
                        # Calculate cost for this arc
                        distance = self._get_distance(locations[i], locations[j], distance_matrix)
                        arc_cost = distance * vehicles[k].cost_per_mile
                        total_cost += arc_cost * x[i, j, k]
        
        prob += total_cost
        
        # Constraints
        
        # 1. Each store must be visited exactly once
        for j in range(1, n_locations):  # Skip depot (index 0)
            prob += pulp.lpSum([x[i, j, k] for i in range(n_locations) 
                               for k in range(n_vehicles) 
                               if i != j and (i, j, k) in x]) == 1
        
        # 2. Flow conservation: if a vehicle enters a location, it must leave
        for k in range(n_vehicles):
            for j in range(n_locations):
                inflow = pulp.lpSum([x[i, j, k] for i in range(n_locations) 
                                    if i != j and (i, j, k) in x])
                outflow = pulp.lpSum([x[j, i, k] for i in range(n_locations) 
                                     if i != j and (j, i, k) in x])
                prob += inflow == outflow
        
        # 3. Each vehicle starts and ends at depot
        for k in range(n_vehicles):
            # Must leave depot at most once
            prob += pulp.lpSum([x[0, j, k] for j in range(1, n_locations) 
                               if (0, j, k) in x]) <= 1
            # Must return to depot at most once
            prob += pulp.lpSum([x[j, 0, k] for j in range(1, n_locations) 
                               if (j, 0, k) in x]) <= 1
        
        # 4. Vehicle capacity constraints
        for k in range(n_vehicles):
            for i in range(n_locations):
                for j in range(n_locations):
                    if i != j and (i, j, k) in x:
                        if j > 0:  # Not depot
                            store_demand = stores[j-1].demand_pallets
                            prob += (load[k, j] >= load[k, i] + store_demand - 
                                   vehicles[k].max_pallets * (1 - x[i, j, k]))
                        else:  # Returning to depot
                            prob += load[k, j] == 0
        
        # 5. Initial load at depot
        for k in range(n_vehicles):
            prob += load[k, 0] == 0
        
        # 6. Load bounds
        for k in range(n_vehicles):
            for i in range(n_locations):
                prob += load[k, i] <= vehicles[k].max_pallets
        
        # Solve the problem
        solver = self._get_solver()
        prob.solve(solver)
        
        solve_time = time.time() - start_time
        
        # Extract solution
        routes = self._extract_routes(x, locations, vehicles, stores, prob.status)
        
        # Calculate results
        total_distance = sum(route.total_distance for route in routes)
        total_time = sum(route.total_time for route in routes)
        total_cost_result = sum(route.total_cost for route in routes)
        
        # Calculate utilization
        total_capacity = sum(vehicle.max_pallets for vehicle in vehicles if any(route.vehicle_id == vehicle.id for route in routes))
        total_used = sum(route.pallets_delivered for route in routes)
        utilization = total_used / max(total_capacity, 1) if total_capacity > 0 else 0
        
        result = OptimizationResult(
            routes=routes,
            total_cost=total_cost_result,
            total_distance=total_distance,
            total_time=total_time,
            utilization_rate=utilization,
            solver_status=pulp.LpStatus[prob.status],
            solve_time=solve_time,
            objective_value=pulp.value(prob.objective) if prob.objective else 0,
            gap=None
        )
        
        return result
    
    def optimize_supplier_assignment(self, stores: List[Store], 
                                   suppliers: List[Supplier]) -> Dict[str, str]:
        
        # Simple greedy assignment based on cost
        assignments = {}
        
        for store in stores:
            best_supplier = None
            best_cost = float('inf')
            
            for supplier in suppliers:
                if supplier.available_pallets >= store.demand_pallets:
                    cost = self.cost_calculator.calculate_supplier_assignment_cost(store, supplier)
                    
                    if cost < best_cost:
                        best_cost = cost
                        best_supplier = supplier
            
            if best_supplier:
                assignments[store.id] = best_supplier.id
                # Update supplier availability
                best_supplier.available_pallets -= store.demand_pallets
        
        return assignments
    
    def optimize_vehicle_routing_heuristic(self, stores: List[Store], 
                                         vehicles: List[Vehicle],
                                         depot_location: Tuple[float, float]) -> List[Route]:
        
        routes = []
        unassigned_stores = stores.copy()
        
        for vehicle in vehicles:
            if not unassigned_stores:
                break
                
            route_stores = []
            current_load = 0
            current_location = depot_location
            
            # Greedy nearest neighbor with capacity constraint
            while unassigned_stores and current_load < vehicle.max_pallets:
                nearest_store = None
                min_distance = float('inf')
                
                for store in unassigned_stores:
                    if current_load + store.demand_pallets <= vehicle.max_pallets:
                        distance = calculate_distance(
                            current_location[0], current_location[1],
                            store.location.latitude, store.location.longitude
                        )
                        
                        if distance < min_distance:
                            min_distance = distance
                            nearest_store = store
                
                if nearest_store:
                    route_stores.append(nearest_store)
                    current_load += nearest_store.demand_pallets
                    current_location = (nearest_store.location.latitude, 
                                      nearest_store.location.longitude)
                    unassigned_stores.remove(nearest_store)
                else:
                    break
            
            if route_stores:
                # Create route
                stops = ['depot'] + [store.location.name for store in route_stores] + ['depot']
                
                # Calculate route metrics
                total_distance = 0.0
                total_time = 0.0
                
                route_coords = [depot_location]
                for store in route_stores:
                    route_coords.append((store.location.latitude, store.location.longitude))
                route_coords.append(depot_location)
                
                for i in range(len(route_coords) - 1):
                    segment_distance = calculate_distance(
                        route_coords[i][0], route_coords[i][1],
                        route_coords[i+1][0], route_coords[i+1][1]
                    )
                    total_distance += segment_distance
                    total_time += segment_distance / 55.0  # 55 mph average
                
                route = Route(
                    id=f"route_{uuid.uuid4().hex[:8]}",
                    vehicle_id=vehicle.id,
                    stops=stops,
                    total_distance=total_distance,
                    total_time=total_time,
                    total_cost=total_distance * vehicle.cost_per_mile + total_time * vehicle.cost_per_hour,
                    pallets_delivered=current_load,
                    status=RouteStatus.PLANNED
                )
                
                routes.append(route)
        
        return routes
    
    def _get_solver(self):
        solver_map = {
            'CBC': pulp.PULP_CBC_CMD,
            'GLPK': pulp.GLPK_CMD,
            'CPLEX': pulp.CPLEX_CMD,
            'GUROBI': pulp.GUROBI_CMD
        }
        
        solver_class = solver_map.get(self.solver_name, pulp.PULP_CBC_CMD)
        
        try:
            if self.solver_name in ['CPLEX', 'GUROBI']:
                return solver_class(timeLimit=self.time_limit, mip=True, msg=1)
            else:
                return solver_class(timeLimit=self.time_limit, msg=1)
        except:
            # Fallback to CBC if other solvers are not available
            return pulp.PULP_CBC_CMD(timeLimit=self.time_limit, msg=1)
    
    def _get_distance(self, loc1: str, loc2: str, distance_matrix: Optional[DistanceMatrix]) -> float:
        if distance_matrix and (loc1, loc2) in distance_matrix.distances:
            return distance_matrix.distances[(loc1, loc2)]
        
        # Default distance if not in matrix
        return 50.0
    
    def _extract_routes(self, x_vars: Dict, locations: List[str], 
                       vehicles: List[Vehicle], stores: List[Store], 
                       status: int) -> List[Route]:
        
        routes = []
        
        if status != pulp.LpStatusOptimal:
            # If no optimal solution, return heuristic solution
            depot_coords = (41.8781, -87.6298)  # Default Chicago coordinates
            return self.optimize_vehicle_routing_heuristic(stores, vehicles, depot_coords)
        
        for k, vehicle in enumerate(vehicles):
            route_sequence = []
            current_loc = 0  # Start at depot
            
            # Follow the route for this vehicle
            while True:
                next_loc = None
                for j in range(len(locations)):
                    if (current_loc, j, k) in x_vars and pulp.value(x_vars[current_loc, j, k]) > 0.5:
                        next_loc = j
                        break
                
                if next_loc is None or next_loc == 0:  # Returned to depot or no next location
                    break
                    
                route_sequence.append(next_loc)
                current_loc = next_loc
            
            if route_sequence:
                stops = ['depot'] + [locations[i] for i in route_sequence] + ['depot']
                
                # Calculate route metrics (simplified)
                total_distance = len(route_sequence) * 50.0  # Estimate
                total_time = total_distance / 55.0
                pallets = sum(stores[i-1].demand_pallets for i in route_sequence if i > 0)
                
                route = Route(
                    id=f"route_{uuid.uuid4().hex[:8]}",
                    vehicle_id=vehicle.id,
                    stops=stops,
                    total_distance=total_distance,
                    total_time=total_time,
                    total_cost=total_distance * vehicle.cost_per_mile + total_time * vehicle.cost_per_hour,
                    pallets_delivered=pallets,
                    status=RouteStatus.PLANNED
                )
                
                routes.append(route)
        
        return routes