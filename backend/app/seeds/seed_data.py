from __future__ import annotations

import math
from sqlalchemy import delete, func, select, text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Demand, Depot, Edge, Node, Scenario, Vehicle


SCENARIO_PROFILES = {
    "normal": {
        "name": "Normal Scenario",
        "description": "Baseline benchmark: normal demand scale, balanced depot coverage, and passable roads.",
        "expected_challenge": "Serves as the control group for distance, response time, and utilization comparison.",
    },
    "congestion": {
        "name": "Congestion Scenario",
        "description": "Urban-center links have elevated congestion factors while roads remain passable.",
        "expected_challenge": "Tests whether algorithms avoid slow center corridors and reduce response time under traffic pressure.",
    },
    "surge": {
        "name": "Demand Surge Scenario",
        "description": "Additional demand points appear with tighter time windows and larger quantities.",
        "expected_challenge": "Tests scalability and completion-rate robustness when workload rises suddenly.",
    },
    "shortage": {
        "name": "Resource Shortage Scenario",
        "description": "Vehicle count, capacity, and depot inventory are intentionally constrained.",
        "expected_challenge": "Forces unserved-demand tradeoffs and highlights capacity bottlenecks.",
    },
    "blocked": {
        "name": "Blocked Road Scenario",
        "description": "Critical links around the city center are blocked and must be routed around.",
        "expected_challenge": "Tests graph connectivity, blocked-edge handling, and route detour quality.",
    },
    "high_priority": {
        "name": "High Priority Rescue Scenario",
        "description": "High-priority rescue tasks are clustered in the east and south of the network.",
        "expected_challenge": "Tests whether priority-aware dispatch improves urgent-task completion.",
    },
}

DEFAULT_SCENARIOS = [
    (profile["name"], profile["description"], scenario_type)
    for scenario_type, profile in SCENARIO_PROFILES.items()
]


def _distance_km(a: Node, b: Node) -> float:
    lat_km = (a.latitude - b.latitude) * 111.0
    lon_km = (a.longitude - b.longitude) * 111.0 * math.cos(math.radians(a.latitude))
    return round(math.sqrt(lat_km * lat_km + lon_km * lon_km), 3)


def _reset_scenario_children(db: Session, scenario_id: int) -> None:
    for model in (Demand, Vehicle, Depot, Edge, Node):
        db.execute(delete(model).where(model.scenario_id == scenario_id))


def populate_scenario(db: Session, scenario: Scenario) -> Scenario:
    _reset_scenario_children(db, scenario.id)
    db.flush()

    base_lat, base_lon = 39.980, 116.310
    node_by_grid: dict[tuple[int, int], Node] = {}
    for row in range(5):
        for col in range(5):
            node = Node(
                scenario_id=scenario.id,
                name=f"N{row}-{col}",
                latitude=base_lat + row * 0.006,
                longitude=base_lon + col * 0.007,
                node_type="intersection",
            )
            db.add(node)
            node_by_grid[(row, col)] = node
    db.flush()

    def add_edge(source: Node, target: Node, blocked: bool = False, congestion: float = 1.0) -> None:
        db.add(
            Edge(
                scenario_id=scenario.id,
                source_node_id=source.id,
                target_node_id=target.id,
                distance_km=_distance_km(source, target),
                speed_kmph=36.0,
                congestion_factor=congestion,
                is_blocked=blocked,
            )
        )

    for row in range(5):
        for col in range(5):
            source = node_by_grid[(row, col)]
            for d_row, d_col in ((1, 0), (0, 1)):
                neighbor_key = (row + d_row, col + d_col)
                if neighbor_key not in node_by_grid:
                    continue
                target = node_by_grid[neighbor_key]
                center_link = row in (1, 2) and col in (1, 2)
                east_west_bypass = row in (2, 3) and col in (2, 3)
                congestion = 1.0
                if scenario.scenario_type == "congestion" and center_link:
                    congestion = 2.4
                if scenario.scenario_type == "high_priority" and east_west_bypass:
                    congestion = 1.6
                blocked = scenario.scenario_type == "blocked" and (row, col, d_row, d_col) in {
                    (2, 1, 0, 1),
                    (2, 2, 0, 1),
                    (1, 2, 1, 0),
                    (2, 2, 1, 0),
                }
                add_edge(source, target, blocked, congestion)
                add_edge(target, source, blocked, congestion)

    depot_inventory = (240, 220)
    if scenario.scenario_type == "shortage":
        depot_inventory = (70, 60)
    depot_a = Depot(
        scenario_id=scenario.id,
        node_id=node_by_grid[(0, 0)].id,
        name="Northwest Relief Depot",
        inventory_units=depot_inventory[0],
    )
    depot_b = Depot(
        scenario_id=scenario.id,
        node_id=node_by_grid[(4, 4)].id,
        name="Southeast Medical Depot",
        inventory_units=depot_inventory[1],
    )
    db.add_all([depot_a, depot_b])
    db.flush()

    vehicle_specs = [(depot_a, (0, 0), 45), (depot_a, (0, 0), 35), (depot_b, (4, 4), 40)]
    if scenario.scenario_type == "surge":
        vehicle_specs.append((depot_b, (4, 4), 45))
    if scenario.scenario_type == "shortage":
        vehicle_specs = [(depot_a, (0, 0), 25), (depot_b, (4, 4), 20)]
    for idx, (depot, grid, capacity) in enumerate(vehicle_specs, start=1):
        db.add(
            Vehicle(
                scenario_id=scenario.id,
                depot_id=depot.id,
                current_node_id=node_by_grid[grid].id,
                name=f"Vehicle-{idx}",
                capacity=capacity,
                speed_kmph=34.0,
                available=True,
            )
        )

    demand_specs = [
        ((0, 4), 12, 3, 45.0),
        ((1, 3), 18, 5, 35.0),
        ((2, 2), 15, 4, 50.0),
        ((3, 1), 10, 2, 80.0),
        ((4, 0), 20, 4, 65.0),
        ((3, 4), 16, 3, 70.0),
    ]
    if scenario.scenario_type == "shortage":
        demand_specs = [
            ((0, 4), 18, 3, 45.0),
            ((1, 3), 22, 5, 35.0),
            ((2, 2), 20, 4, 50.0),
            ((3, 1), 16, 2, 80.0),
            ((4, 0), 25, 4, 65.0),
            ((3, 4), 18, 3, 70.0),
        ]
    if scenario.scenario_type == "blocked":
        demand_specs = [
            ((0, 4), 12, 3, 42.0),
            ((1, 4), 16, 4, 45.0),
            ((2, 3), 18, 5, 48.0),
            ((3, 1), 12, 3, 75.0),
            ((4, 0), 20, 4, 80.0),
            ((4, 2), 14, 3, 70.0),
        ]
    if scenario.scenario_type == "high_priority":
        demand_specs = [
            ((1, 3), 12, 5, 32.0),
            ((1, 4), 14, 5, 36.0),
            ((2, 4), 16, 5, 40.0),
            ((3, 3), 12, 5, 44.0),
            ((4, 2), 18, 4, 55.0),
            ((0, 2), 10, 2, 80.0),
            ((3, 0), 12, 3, 78.0),
        ]
    if scenario.scenario_type == "surge":
        demand_specs += [
            ((1, 1), 22, 5, 35.0),
            ((2, 4), 18, 5, 42.0),
            ((4, 2), 15, 4, 55.0),
        ]
    for idx, (grid, quantity, priority, due_min) in enumerate(demand_specs, start=1):
        db.add(
            Demand(
                scenario_id=scenario.id,
                node_id=node_by_grid[grid].id,
                name=f"Demand-{idx}",
                quantity=quantity,
                priority=priority,
                time_window_start_min=0.0,
                time_window_end_min=due_min,
                service_time_min=6.0 + priority,
            )
        )

    _sync_postgis_columns(db, scenario.id)
    return scenario


def _sync_postgis_columns(db: Session, scenario_id: int) -> None:
    if db.bind is None or db.bind.dialect.name != "postgresql":
        return
    has_geom = db.scalar(
        text(
            """
            SELECT EXISTS (
              SELECT 1 FROM information_schema.columns
              WHERE table_name = 'nodes' AND column_name = 'geom'
            )
            """
        )
    )
    if not has_geom:
        return
    db.execute(
        text(
            """
            UPDATE nodes
            SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
            WHERE scenario_id = :scenario_id
            """
        ),
        {"scenario_id": scenario_id},
    )
    db.execute(
        text(
            """
            UPDATE edges e
            SET geom = ST_MakeLine(s.geom, t.geom)
            FROM nodes s, nodes t
            WHERE e.source_node_id = s.id
              AND e.target_node_id = t.id
              AND e.scenario_id = :scenario_id
            """
        ),
        {"scenario_id": scenario_id},
    )


def seed_default_scenarios(db: Session) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for name, description, scenario_type in DEFAULT_SCENARIOS:
        scenario = db.scalar(select(Scenario).where(Scenario.name == name))
        if scenario is None:
            scenario = Scenario(name=name, description=description, scenario_type=scenario_type)
            db.add(scenario)
            db.flush()
            populate_scenario(db, scenario)
        else:
            node_count = db.scalar(select(func.count(Node.id)).where(Node.scenario_id == scenario.id)) or 0
            edge_count = db.scalar(select(func.count(Edge.id)).where(Edge.scenario_id == scenario.id)) or 0
            vehicle_count = db.scalar(select(func.count(Vehicle.id)).where(Vehicle.scenario_id == scenario.id)) or 0
            demand_count = db.scalar(select(func.count(Demand.id)).where(Demand.scenario_id == scenario.id)) or 0
            if min(node_count, edge_count, vehicle_count, demand_count) == 0:
                populate_scenario(db, scenario)
        scenarios.append(scenario)
    db.commit()
    return scenarios


def main() -> None:
    with SessionLocal() as db:
        seed_default_scenarios(db)


if __name__ == "__main__":
    main()
