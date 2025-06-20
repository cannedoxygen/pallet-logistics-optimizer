from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum


class PalletType(Enum):
    STANDARD = "standard"
    EURO = "euro"
    CUSTOM = "custom"


class RouteStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Location:
    name: str
    address: str
    latitude: float
    longitude: float
    city: str
    state: str
    zip_code: str
    contact_info: Optional[str] = None


@dataclass
class Store:
    id: str
    name: str
    location: Location
    demand_pallets: int
    delivery_window_start: Optional[datetime] = None
    delivery_window_end: Optional[datetime] = None
    priority: int = 1
    special_requirements: List[str] = field(default_factory=list)


@dataclass
class Supplier:
    id: str
    name: str
    location: Location
    available_pallets: int
    cost_per_pallet: float
    lead_time_days: int
    capacity_per_day: int
    reliability_score: float = 1.0
    pallet_types: List[PalletType] = field(default_factory=lambda: [PalletType.STANDARD])


@dataclass
class Vehicle:
    id: str
    type: str
    max_pallets: int
    max_weight: int
    cost_per_mile: float
    cost_per_hour: float
    current_location: Optional[Location] = None
    available: bool = True


@dataclass
class Route:
    id: str
    vehicle_id: str
    stops: List[str]
    total_distance: float
    total_time: float
    total_cost: float
    pallets_delivered: int
    status: RouteStatus = RouteStatus.PLANNED
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Order:
    id: str
    store_id: str
    supplier_id: str
    quantity: int
    pallet_type: PalletType
    requested_date: datetime
    priority: int = 1
    special_instructions: Optional[str] = None


@dataclass
class TollSegment:
    from_location: str
    to_location: str
    rate_per_mile: float
    flat_rate: Optional[float] = None


@dataclass
class DistanceMatrix:
    locations: List[str]
    distances: Dict[Tuple[str, str], float]
    travel_times: Dict[Tuple[str, str], float]


@dataclass
class OptimizationResult:
    routes: List[Route]
    total_cost: float
    total_distance: float
    total_time: float
    utilization_rate: float
    solver_status: str
    solve_time: float
    objective_value: float
    gap: Optional[float] = None


@dataclass
class CostBreakdown:
    fuel_cost: float
    driver_cost: float
    toll_cost: float
    handling_cost: float
    total_cost: float
    cost_per_pallet: float
    cost_per_mile: float