from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


SUPPORTED_ALGORITHMS = {"greedy", "priority", "dijkstra", "astar", "ortools_cvrp", "vrptw"}


class ApiResponse(BaseModel):
    success: bool = True
    message: str = "ok"
    data: object | None = None


class ScenarioCreate(BaseModel):
    name: str = Field(min_length=3, max_length=160)
    description: str = ""
    scenario_type: str = "custom"


class ScenarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    scenario_type: str
    created_at: datetime
    updated_at: datetime
    node_count: int = 0
    edge_count: int = 0
    vehicle_count: int = 0
    demand_count: int = 0
    priority_distribution: dict[str, int] = Field(default_factory=dict)
    congested_edge_count: int = 0
    blocked_edge_count: int = 0
    expected_challenge: str = ""


class NodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    latitude: float
    longitude: float
    node_type: str


class EdgeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_node_id: int
    target_node_id: int
    distance_km: float
    speed_kmph: float
    congestion_factor: float
    is_blocked: bool


class DepotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    node_id: int
    name: str
    inventory_units: int


class VehicleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    depot_id: int
    current_node_id: int
    name: str
    capacity: int
    speed_kmph: float
    available: bool


class DemandRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    node_id: int
    name: str
    quantity: int
    priority: int
    time_window_start_min: float | None
    time_window_end_min: float | None
    service_time_min: float


class NetworkRead(BaseModel):
    nodes: list[NodeRead]
    edges: list[EdgeRead]
    depots: list[DepotRead]
    vehicles: list[VehicleRead]
    demands: list[DemandRead]


class RunRequest(BaseModel):
    algorithm: str = Field(default="greedy", pattern="^(greedy|priority|dijkstra|astar|ortools_cvrp|vrptw)$")
    objective: str = "minimize_total_distance"
    parameters: dict = Field(default_factory=dict)


class CompareRequest(BaseModel):
    algorithms: list[str] = Field(default_factory=lambda: ["greedy", "priority", "ortools_cvrp"])
    objective: str = "weighted_multi_objective"
    parameters: dict = Field(default_factory=dict)

    @field_validator("algorithms")
    @classmethod
    def validate_algorithms(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("At least one algorithm is required")
        unsupported = sorted(set(value) - SUPPORTED_ALGORITHMS)
        if unsupported:
            raise ValueError(f"Unsupported algorithms: {', '.join(unsupported)}")
        return value


class SimulationRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_id: int
    status: str
    algorithms: list[str]
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class RouteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dispatch_plan_id: int
    vehicle_id: int
    sequence_index: int
    node_path: list[int]
    demand_sequence: list[dict]
    distance_km: float
    travel_time_min: float
    load_units: int


class MetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    simulation_run_id: int
    dispatch_plan_id: int
    metric_name: str
    metric_value: float
    unit: str


class ReportRead(BaseModel):
    run_id: int
    markdown: str
    generated_by: str
