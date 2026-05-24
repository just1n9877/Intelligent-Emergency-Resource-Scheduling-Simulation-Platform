from __future__ import annotations

import time
import networkx as nx

from app.algorithms.graph import append_path, path_cost
from app.algorithms.shortest_path import find_path
from app.algorithms.types import DemandInput, DispatchResult, RouteResult, VehicleInput


def _edge_weight_for_objective(objective: str) -> str:
    return "distance_km" if objective == "minimize_total_distance" else "travel_time_min"


def _route_demands(
    *,
    graph: nx.DiGraph,
    vehicles: list[VehicleInput],
    demands: list[DemandInput],
    algorithm: str,
    objective: str,
    path_method: str = "dijkstra",
) -> DispatchResult:
    started = time.perf_counter()
    weight = _edge_weight_for_objective(objective)
    states: dict[int, RouteResult] = {
        vehicle.id: RouteResult(vehicle_id=vehicle.id, node_path=[vehicle.current_node_id])
        for vehicle in vehicles
        if vehicle.available
    }
    remaining_capacity = {vehicle.id: vehicle.capacity for vehicle in vehicles if vehicle.available}
    current_node = {vehicle.id: vehicle.current_node_id for vehicle in vehicles if vehicle.available}
    unserved: list[int] = []

    for demand in demands:
        candidates: list[tuple[float, int, list[int], float, float]] = []
        for vehicle_id, capacity in remaining_capacity.items():
            if demand.quantity > capacity:
                continue
            try:
                path = find_path(graph, current_node[vehicle_id], demand.node_id, path_method, weight)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            distance_km, travel_min = path_cost(graph, path)
            priority_bonus = max(demand.priority, 1)
            score = travel_min / priority_bonus if objective == "maximize_priority_completion" else travel_min
            if objective == "minimize_total_distance":
                score = distance_km
            candidates.append((score, vehicle_id, path, distance_km, travel_min))

        if not candidates:
            unserved.append(demand.id)
            continue

        _, vehicle_id, path, distance_km, travel_min = min(candidates, key=lambda item: item[0])
        route = states[vehicle_id]
        arrival_time = route.travel_time_min + travel_min
        route.node_path = append_path(route.node_path, path)
        route.distance_km += distance_km
        route.travel_time_min = arrival_time + demand.service_time_min
        route.load_units += demand.quantity
        route.demand_sequence.append(
            {
                "demand_id": demand.id,
                "node_id": demand.node_id,
                "quantity": demand.quantity,
                "priority": demand.priority,
                "arrival_time_min": round(arrival_time, 2),
                "service_time_min": demand.service_time_min,
                "delayed": demand.time_window_end_min is not None and arrival_time > demand.time_window_end_min,
            }
        )
        remaining_capacity[vehicle_id] -= demand.quantity
        current_node[vehicle_id] = demand.node_id

    routes = [route for route in states.values() if route.demand_sequence]
    objective_value = sum(route.distance_km for route in routes)
    if objective == "minimize_total_response_time":
        objective_value = sum(
            item["arrival_time_min"] for route in routes for item in route.demand_sequence
        )
    if objective == "maximize_priority_completion":
        objective_value = -sum(item["priority"] for route in routes for item in route.demand_sequence)
    if objective == "weighted_multi_objective":
        objective_value = sum(route.distance_km + 0.2 * route.travel_time_min for route in routes) + 10 * len(unserved)

    return DispatchResult(
        algorithm=algorithm,
        routes=routes,
        unserved_demands=unserved,
        objective_value=round(objective_value, 3),
        runtime_ms=round((time.perf_counter() - started) * 1000.0, 3),
    )


def greedy_dispatch(
    graph: nx.DiGraph,
    vehicles: list[VehicleInput],
    demands: list[DemandInput],
    objective: str = "minimize_total_distance",
    path_method: str = "dijkstra",
    algorithm_name: str | None = None,
) -> DispatchResult:
    return _route_demands(
        graph=graph,
        vehicles=vehicles,
        demands=sorted(demands, key=lambda demand: demand.id),
        algorithm=algorithm_name or ("greedy" if path_method == "dijkstra" else "astar"),
        objective=objective,
        path_method=path_method,
    )
