from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.reports import generate_report
from app.schemas import CompareRequest, RunRequest, ScenarioCreate
from app.services.scenario_service import (
    create_scenario,
    get_scenario_or_none,
    list_scenario_summaries,
    load_network,
    scenario_summary,
    seed_scenario,
)
from app.services.simulation_service import (
    get_metrics_for_run,
    get_routes_for_run,
    get_run,
    latest_comparison,
    run_algorithms,
)

router = APIRouter()


def ok(data=None, message: str = "ok") -> dict:
    return {"success": True, "message": message, "data": jsonable_encoder(data)}


@router.get("/health")
def health() -> dict:
    return ok({"status": "healthy", "service": "emergency-scheduling-api"})


@router.get("/scenarios")
def list_scenarios(db: Session = Depends(get_db)) -> dict:
    return ok(list_scenario_summaries(db))


@router.post("/scenarios", status_code=201)
def create_scenario_endpoint(payload: ScenarioCreate, db: Session = Depends(get_db)) -> dict:
    scenario = create_scenario(db, payload)
    return ok(scenario_summary(db, scenario), "scenario_created")


@router.get("/scenarios/{scenario_id}")
def get_scenario(scenario_id: int, db: Session = Depends(get_db)) -> dict:
    scenario = get_scenario_or_none(db, scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ok(scenario_summary(db, scenario))


@router.post("/scenarios/{scenario_id}/seed")
def seed_scenario_endpoint(scenario_id: int, db: Session = Depends(get_db)) -> dict:
    scenario = seed_scenario(db, scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ok(scenario_summary(db, scenario), "scenario_seeded")


@router.get("/scenarios/{scenario_id}/network")
def get_network(scenario_id: int, db: Session = Depends(get_db)) -> dict:
    if get_scenario_or_none(db, scenario_id) is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ok(load_network(db, scenario_id))


@router.get("/scenarios/{scenario_id}/demands")
def get_demands(scenario_id: int, db: Session = Depends(get_db)) -> dict:
    if get_scenario_or_none(db, scenario_id) is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ok(load_network(db, scenario_id)["demands"])


@router.get("/scenarios/{scenario_id}/vehicles")
def get_vehicles(scenario_id: int, db: Session = Depends(get_db)) -> dict:
    if get_scenario_or_none(db, scenario_id) is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ok(load_network(db, scenario_id)["vehicles"])


@router.post("/scenarios/{scenario_id}/run")
def run_scenario(scenario_id: int, payload: RunRequest, db: Session = Depends(get_db)) -> dict:
    try:
        run = run_algorithms(db, scenario_id, [payload.algorithm], payload.objective, payload.parameters)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ok(run, "simulation_completed")


@router.get("/simulation-runs/{run_id}")
def read_run(run_id: int, db: Session = Depends(get_db)) -> dict:
    run = get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return ok(run)


@router.get("/simulation-runs/{run_id}/routes")
def read_routes(run_id: int, db: Session = Depends(get_db)) -> dict:
    if get_run(db, run_id) is None:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return ok(get_routes_for_run(db, run_id))


@router.get("/simulation-runs/{run_id}/metrics")
def read_metrics(run_id: int, db: Session = Depends(get_db)) -> dict:
    if get_run(db, run_id) is None:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return ok(get_metrics_for_run(db, run_id))


@router.post("/scenarios/{scenario_id}/compare")
def compare_algorithms(scenario_id: int, payload: CompareRequest, db: Session = Depends(get_db)) -> dict:
    try:
        run = run_algorithms(db, scenario_id, payload.algorithms, payload.objective, payload.parameters)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ok(run, "comparison_completed")


@router.get("/scenarios/{scenario_id}/comparison")
def get_comparison(scenario_id: int, db: Session = Depends(get_db)) -> dict:
    if get_scenario_or_none(db, scenario_id) is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ok(latest_comparison(db, scenario_id))


@router.post("/reports/{run_id}/generate")
def generate_report_endpoint(run_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        markdown, generated_by = generate_report(db, run_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ok({"run_id": run_id, "markdown": markdown, "generated_by": generated_by}, "report_generated")
