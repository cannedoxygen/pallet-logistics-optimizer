import math
import requests
from typing import Dict, List, Tuple, Optional
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return geodesic((lat1, lon1), (lat2, lon2)).miles


def calculate_travel_time(lat1: float, lon1: float, lat2: float, lon2: float, 
                         avg_speed_mph: float = 55.0) -> float:
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    return distance / avg_speed_mph


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def geocode_address(address: str, geocoder_api_key: Optional[str] = None) -> Tuple[float, float]:
    try:
        geolocator = Nominatim(user_agent="pallet_optimizer")
        location = geolocator.geocode(address)
        
        if location:
            return location.latitude, location.longitude
        else:
            raise ValueError(f"Could not geocode address: {address}")
    
    except Exception as e:
        raise ValueError(f"Geocoding failed for {address}: {str(e)}")


def calculate_distance_matrix(locations: List[Tuple[float, float]], 
                            api_key: Optional[str] = None) -> Dict[Tuple[int, int], float]:
    distance_matrix = {}
    
    for i, loc1 in enumerate(locations):
        for j, loc2 in enumerate(locations):
            if i != j:
                distance = calculate_distance(loc1[0], loc1[1], loc2[0], loc2[1])
                distance_matrix[(i, j)] = distance
            else:
                distance_matrix[(i, j)] = 0.0
    
    return distance_matrix


def calculate_time_matrix(locations: List[Tuple[float, float]], 
                         avg_speed_mph: float = 55.0) -> Dict[Tuple[int, int], float]:
    time_matrix = {}
    
    for i, loc1 in enumerate(locations):
        for j, loc2 in enumerate(locations):
            if i != j:
                travel_time = calculate_travel_time(loc1[0], loc1[1], loc2[0], loc2[1], avg_speed_mph)
                time_matrix[(i, j)] = travel_time
            else:
                time_matrix[(i, j)] = 0.0
    
    return time_matrix


def find_nearest_locations(target_lat: float, target_lon: float, 
                          locations: List[Tuple[str, float, float]], 
                          n: int = 5) -> List[Tuple[str, float]]:
    distances = []
    
    for name, lat, lon in locations:
        distance = calculate_distance(target_lat, target_lon, lat, lon)
        distances.append((name, distance))
    
    distances.sort(key=lambda x: x[1])
    return distances[:n]


def calculate_route_distance(route_coordinates: List[Tuple[float, float]]) -> float:
    total_distance = 0.0
    
    for i in range(len(route_coordinates) - 1):
        lat1, lon1 = route_coordinates[i]
        lat2, lon2 = route_coordinates[i + 1]
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        total_distance += distance
    
    return total_distance


def get_bounding_box(locations: List[Tuple[float, float]]) -> Tuple[float, float, float, float]:
    if not locations:
        return 0.0, 0.0, 0.0, 0.0
    
    lats = [loc[0] for loc in locations]
    lons = [loc[1] for loc in locations]
    
    return min(lats), max(lats), min(lons), max(lons)


def is_within_radius(center_lat: float, center_lon: float, 
                    target_lat: float, target_lon: float, 
                    radius_miles: float) -> bool:
    distance = calculate_distance(center_lat, center_lon, target_lat, target_lon)
    return distance <= radius_miles


def calculate_centroid(locations: List[Tuple[float, float]]) -> Tuple[float, float]:
    if not locations:
        return 0.0, 0.0
    
    avg_lat = sum(loc[0] for loc in locations) / len(locations)
    avg_lon = sum(loc[1] for loc in locations) / len(locations)
    
    return avg_lat, avg_lon


def optimize_depot_location(store_locations: List[Tuple[float, float]], 
                           weights: Optional[List[float]] = None) -> Tuple[float, float]:
    if not store_locations:
        return 0.0, 0.0
    
    if weights is None:
        weights = [1.0] * len(store_locations)
    
    if len(weights) != len(store_locations):
        weights = [1.0] * len(store_locations)
    
    total_weight = sum(weights)
    
    weighted_lat = sum(loc[0] * weight for loc, weight in zip(store_locations, weights))
    weighted_lon = sum(loc[1] * weight for loc, weight in zip(store_locations, weights))
    
    optimal_lat = weighted_lat / total_weight
    optimal_lon = weighted_lon / total_weight
    
    return optimal_lat, optimal_lon