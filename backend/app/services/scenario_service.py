from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.algorithms.types import DemandInput, DepotInput, EdgeInput, NodeInput, VehicleInput
from app.models import Demand, Depot, Edge, Node, Scenario, Vehicle
from app.schemas import ScenarioCreate
from app.seeds.seed_data import SCENARIO_PROFILES, populate_scenario


def create_scenario(db: Session, payload: ScenarioCreate) -> Scenario:
    scenario = Scenario(
        name=payload.name,
        description=payload.description,
        scenario_type=payload.scenario_type,
    )
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    return scenario


def get_scenario_or_none(db: Session, scenario_id: int) -> Scenario | None:
    return db.get(Scenario, scenario_id)


def scenario_summary(db: Session, scenario: Scenario) -> dict:
    priorities = db.execute(
        select(Demand.priority, func.count(Demand.id))
        .where(Demand.scenario_id == scenario.id)
        .group_by(Demand.priority)
        .order_by(Demand.priority.desc())
    ).all()
    profile = SCENARIO_PROFILES.get(scenario.scenario_type, {})
    return {
        "id": scenario.id,
        "name": scenario.name,
        "description": scenario.description,
        "scenario_type": scenario.scenario_type,
        "created_at": scenario.created_at,
        "updated_at": scenario.updated_at,
        "node_count": db.scalar(select(func.count(Node.id)).where(Node.scenario_id == scenario.id)) or 0,
        "edge_count": db.scalar(select(func.count(Edge.id)).where(Edge.scenario_id == scenario.id)) or 0,
        "vehicle_count": db.scalar(select(func.count(Vehicle.id)).where(Vehicle.scenario_id == scenario.id)) or 0,
        "demand_count": db.scalar(select(func.count(Demand.id)).where(Demand.scenario_id == scenario.id)) or 0,
        "priority_distribution": {str(priority): count for priority, count in priorities},
        "congested_edge_count": db.scalar(
            select(func.count(Edge.id)).where(Edge.scenario_id == scenario.id, Edge.congestion_factor > 1.0)
        )
        or 0,
        "blocked_edge_count": db.scalar(
            select(func.count(Edge.id)).where(Edge.scenario_id == scenario.id, Edge.is_blocked.is_(True))
        )
        or 0,
        "expected_challenge": profile.get("expected_challenge", "Custom scenario for ad-hoc experiment design."),
    }


def list_scenario_summaries(db: Session) -> list[dict]:
    scenarios = db.scalars(select(Scenario).order_by(Scenario.id)).all()
    return [scenario_summary(db, scenario) for scenario in scenarios]


def seed_scenario(db: Session, scenario_id: int) -> Scenario | None:
    scenario = db.get(Scenario, scenario_id)
    if scenario is None:
        return None
    populate_scenario(db, scenario)
    db.commit()
    db.refresh(scenario)
    return scenario


def load_network(db: Session, scenario_id: int) -> dict:
    return {
        "nodes": list(db.scalars(select(Node).where(Node.scenario_id == scenario_id).order_by(Node.id)).all()),
        "edges": list(db.scalars(select(Edge).where(Edge.scenario_id == scenario_id).order_by(Edge.id)).all()),
        "depots": list(db.scalars(select(Depot).where(Depot.scenario_id == scenario_id).order_by(Depot.id)).all()),
        "vehicles": list(db.scalars(select(Vehicle).where(Vehicle.scenario_id == scenario_id).order_by(Vehicle.id)).all()),
        "demands": list(db.scalars(select(Demand).where(Demand.scenario_id == scenario_id).order_by(Demand.id)).all()),
    }


def algorithm_inputs(db: Session, scenario_id: int) -> tuple[list[NodeInput], list[EdgeInput], list[DepotInput], list[VehicleInput], list[DemandInput]]:
    network = load_network(db, scenario_id)
    nodes = [NodeInput(n.id, n.latitude, n.longitude) for n in network["nodes"]]
    edges = [
        EdgeInput(e.id, e.source_node_id, e.target_node_id, e.distance_km, e.speed_kmph, e.congestion_factor, e.is_blocked)
        for e in network["edges"]
    ]
    depots = [DepotInput(d.id, d.node_id, d.inventory_units) for d in network["depots"]]
    vehicles = [
        VehicleInput(v.id, v.depot_id, v.current_node_id, v.capacity, v.speed_kmph, v.available)
        for v in network["vehicles"]
    ]
    demands = [
        DemandInput(
            d.id,
            d.node_id,
            d.quantity,
            d.priority,
            d.service_time_min,
            d.time_window_start_min,
            d.time_window_end_min,
        )
        for d in network["demands"]
    ]
    return nodes, edges, depots, vehicles, demands
