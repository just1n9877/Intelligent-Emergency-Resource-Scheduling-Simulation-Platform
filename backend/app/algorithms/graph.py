from __future__ import annotations

import math
import networkx as nx

from app.algorithms.types import EdgeInput, NodeInput


def travel_time_min(distance_km: float, speed_kmph: float, congestion_factor: float) -> float:
    effective_speed = max(speed_kmph, 1.0)
    return (distance_km / effective_speed) * 60.0 * max(congestion_factor, 1.0)


def build_graph(nodes: list[NodeInput], edges: list[EdgeInput]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(node.id, latitude=node.latitude, longitude=node.longitude)

    for edge in edges:
        if edge.is_blocked:
            continue
        graph.add_edge(
            edge.source_node_id,
            edge.target_node_id,
            distance_km=edge.distance_km,
            travel_time_min=travel_time_min(edge.distance_km, edge.speed_kmph, edge.congestion_factor),
            congestion_factor=edge.congestion_factor,
        )
    return graph


def euclidean_km(graph: nx.DiGraph, source: int, target: int) -> float:
    s = graph.nodes[source]
    t = graph.nodes[target]
    lat_km = (s["latitude"] - t["latitude"]) * 111.0
    lon_km = (s["longitude"] - t["longitude"]) * 111.0 * math.cos(math.radians(s["latitude"]))
    return math.sqrt(lat_km * lat_km + lon_km * lon_km)


def path_cost(graph: nx.DiGraph, path: list[int]) -> tuple[float, float]:
    distance = 0.0
    minutes = 0.0
    for source, target in zip(path, path[1:]):
        edge = graph[source][target]
        distance += float(edge["distance_km"])
        minutes += float(edge["travel_time_min"])
    return distance, minutes


def append_path(base_path: list[int], segment: list[int]) -> list[int]:
    if not segment:
        return base_path
    if not base_path:
        return list(segment)
    return base_path + segment[1:] if base_path[-1] == segment[0] else base_path + segment

