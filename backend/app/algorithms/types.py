from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class NodeInput:
    id: int
    latitude: float
    longitude: float


@dataclass(frozen=True)
class EdgeInput:
    id: int
    source_node_id: int
    target_node_id: int
    distance_km: float
    speed_kmph: float
    congestion_factor: float
    is_blocked: bool


@dataclass(frozen=True)
class DepotInput:
    id: int
    node_id: int
    inventory_units: int


@dataclass(frozen=True)
class VehicleInput:
    id: int
    depot_id: int
    current_node_id: int
    capacity: int
    speed_kmph: float
    available: bool = True


@dataclass(frozen=True)
class DemandInput:
    id: int
    node_id: int
    quantity: int
    priority: int
    service_time_min: float
    time_window_start_min: float | None = None
    time_window_end_min: float | None = None


@dataclass
class RouteResult:
    vehicle_id: int
    node_path: list[int] = field(default_factory=list)
    demand_sequence: list[dict] = field(default_factory=list)
    distance_km: float = 0.0
    travel_time_min: float = 0.0
    load_units: int = 0


@dataclass
class DispatchResult:
    algorithm: str
    routes: list[RouteResult]
    unserved_demands: list[int]
    objective_value: float
    runtime_ms: float

