import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from data.models import (
    Store, Supplier, Vehicle, Route, Location, 
    CostBreakdown, TollSegment, DistanceMatrix
)
from utils.geo_utils import calculate_distance, calculate_travel_time


class CostCalculator:
    def __init__(self, config: Dict):
        self.fuel_cost_per_mile = config.get('fuel_cost_per_mile', 0.65)
        self.driver_cost_per_hour = config.get('driver_cost_per_hour', 25.0)
        self.warehouse_handling_cost = config.get('warehouse_handling_cost', 15.0)
        self.default_toll_rate = config.get('default_toll_rate', 0.15)
        
        self.toll_rates: Dict[Tuple[str, str], float] = {}
        self.distance_matrix: Optional[DistanceMatrix] = None
    
    def set_toll_rates(self, toll_rates: Dict[Tuple[str, str], float]):
        self.toll_rates = toll_rates
    
    def set_distance_matrix(self, distance_matrix: DistanceMatrix):
        self.distance_matrix = distance_matrix
    
    def calculate_distance_cost(self, from_location: str, to_location: str, 
                               vehicle: Vehicle) -> float:
        distance = self._get_distance(from_location, to_location)
        return distance * vehicle.cost_per_mile
    
    def calculate_time_cost(self, from_location: str, to_location: str, 
                           vehicle: Vehicle) -> float:
        travel_time = self._get_travel_time(from_location, to_location)
        return travel_time * vehicle.cost_per_hour
    
    def calculate_toll_cost(self, from_location: str, to_location: str) -> float:
        toll_key = (from_location, to_location)
        reverse_key = (to_location, from_location)
        
        if toll_key in self.toll_rates:
            distance = self._get_distance(from_location, to_location)
            return distance * self.toll_rates[toll_key]
        elif reverse_key in self.toll_rates:
            distance = self._get_distance(from_location, to_location)
            return distance * self.toll_rates[reverse_key]
        else:
            distance = self._get_distance(from_location, to_location)
            return distance * self.default_toll_rate
    
    def calculate_handling_cost(self, num_pallets: int) -> float:
        return num_pallets * self.warehouse_handling_cost
    
    def calculate_route_cost(self, route: Route, vehicle: Vehicle, 
                           stores: List[Store]) -> CostBreakdown:
        total_fuel_cost = 0.0
        total_driver_cost = 0.0
        total_toll_cost = 0.0
        total_distance = 0.0
        total_time = 0.0
        
        # Calculate costs for each segment of the route
        for i in range(len(route.stops) - 1):
            from_stop = route.stops[i]
            to_stop = route.stops[i + 1]
            
            # Distance and time
            distance = self._get_distance(from_stop, to_stop)
            travel_time = self._get_travel_time(from_stop, to_stop)
            
            total_distance += distance
            total_time += travel_time
            
            # Fuel cost
            total_fuel_cost += distance * self.fuel_cost_per_mile
            
            # Driver cost
            total_driver_cost += travel_time * self.driver_cost_per_hour
            
            # Toll cost
            total_toll_cost += self.calculate_toll_cost(from_stop, to_stop)
        
        # Handling cost
        handling_cost = self.calculate_handling_cost(route.pallets_delivered)
        
        total_cost = total_fuel_cost + total_driver_cost + total_toll_cost + handling_cost
        
        cost_breakdown = CostBreakdown(
            fuel_cost=total_fuel_cost,
            driver_cost=total_driver_cost,
            toll_cost=total_toll_cost,
            handling_cost=handling_cost,
            total_cost=total_cost,
            cost_per_pallet=total_cost / max(route.pallets_delivered, 1),
            cost_per_mile=total_cost / max(total_distance, 1)
        )
        
        return cost_breakdown
    
    def calculate_supplier_assignment_cost(self, store: Store, supplier: Supplier) -> float:
        base_cost = supplier.cost_per_pallet * store.demand_pallets
        
        # Add distance-based transportation cost estimate
        distance = calculate_distance(
            store.location.latitude, store.location.longitude,
            supplier.location.latitude, supplier.location.longitude
        )
        transportation_cost = distance * self.fuel_cost_per_mile * 0.5  # Estimate
        
        # Reliability penalty
        reliability_penalty = (1.0 - supplier.reliability_score) * base_cost * 0.1
        
        # Priority bonus/penalty
        priority_factor = 1.0 + (store.priority - 1) * 0.05
        
        total_cost = (base_cost + transportation_cost + reliability_penalty) * priority_factor
        
        return total_cost
    
    def calculate_consolidation_savings(self, routes: List[Route], 
                                      stores: List[Store]) -> Dict[str, float]:
        savings = {}
        
        # Calculate savings from consolidating deliveries
        for route in routes:
            if len(route.stops) > 2:  # More than just depot and one store
                individual_costs = 0.0
                
                # Calculate cost if each store was served individually
                depot = route.stops[0]
                for stop in route.stops[1:]:
                    store = next((s for s in stores if s.location.name == stop), None)
                    if store:
                        individual_distance = self._get_distance(depot, stop) * 2  # Round trip
                        individual_cost = individual_distance * self.fuel_cost_per_mile
                        individual_costs += individual_cost
                
                # Actual route cost
                actual_cost = route.total_cost
                
                # Savings
                route_savings = individual_costs - actual_cost
                savings[route.id] = max(0, route_savings)
        
        return savings
    
    def estimate_optimization_potential(self, current_routes: List[Route], 
                                      stores: List[Store]) -> Dict[str, float]:
        metrics = {}
        
        # Calculate current utilization
        total_capacity = sum(26 for _ in current_routes)  # Assuming 26 pallet capacity
        total_used = sum(route.pallets_delivered for route in current_routes)
        utilization = total_used / max(total_capacity, 1)
        
        # Estimate potential savings
        if utilization < 0.8:
            potential_savings = len(current_routes) * 0.15 * 1000  # 15% savings per route
            metrics['potential_cost_savings'] = potential_savings
            metrics['current_utilization'] = utilization
            metrics['target_utilization'] = 0.85
            metrics['consolidation_opportunities'] = len(current_routes) - math.ceil(len(current_routes) * 0.85)
        
        return metrics
    
    def _get_distance(self, from_location: str, to_location: str) -> float:
        if self.distance_matrix:
            key = (from_location, to_location)
            if key in self.distance_matrix.distances:
                return self.distance_matrix.distances[key]
        
        # Default estimation if no distance matrix available
        return 50.0  # Default 50 miles
    
    def _get_travel_time(self, from_location: str, to_location: str) -> float:
        if self.distance_matrix:
            key = (from_location, to_location)
            if key in self.distance_matrix.travel_times:
                return self.distance_matrix.travel_times[key]
        
        # Default estimation: distance / average speed
        distance = self._get_distance(from_location, to_location)
        return distance / 55.0  # 55 mph average speed