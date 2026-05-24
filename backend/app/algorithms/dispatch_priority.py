from __future__ import annotations

import networkx as nx

from app.algorithms.dispatch_greedy import _route_demands
from app.algorithms.types import DemandInput, DispatchResult, VehicleInput


def priority_dispatch(
    graph: nx.DiGraph,
    vehicles: list[VehicleInput],
    demands: list[DemandInput],
    objective: str = "maximize_priority_completion",
) -> DispatchResult:
    ordered_demands = sorted(
        demands,
        key=lambda demand: (-demand.priority, demand.time_window_end_min or 10_000.0, demand.id),
    )
    return _route_demands(
        graph=graph,
        vehicles=vehicles,
        demands=ordered_demands,
        algorithm="priority",
        objective=objective,
        path_method="dijkstra",
    )

