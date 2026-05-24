# Technical Report

## 1. Project Background

Emergency resource scheduling is a typical complex system problem. A city emergency manager must allocate limited vehicles and supplies to distributed demand points under road congestion, blocked roads, vehicle capacity, service time, and urgency constraints.

This project uses a public civil emergency logistics scenario. It is designed for system engineering, routing optimization, simulation evaluation, and full-stack engineering demonstration.

## 2. Problem Definition

Given a road network graph, depots, vehicles, and emergency demands, the system generates vehicle routes that satisfy capacity constraints and maximize service quality under road-state constraints.

Inputs:

- Road graph `G=(V,E)`.
- Depot inventory and vehicle initial positions.
- Demand quantity, priority, service time, and time window.
- Edge distance, speed, congestion factor, and blocked state.

Outputs:

- Vehicle-demand assignment.
- Vehicle node paths.
- Served, delayed, and unserved demand lists.
- Route distance, response time, completion metrics.
- Algorithm comparison and experiment report.

## 3. Mathematical Modeling

Each road edge has an effective travel-time cost:

```text
t_ij = distance_ij / speed_ij * 60 * congestion_factor_ij
```

Vehicle capacity constraint:

```text
sum demand_quantity served by vehicle k <= capacity_k
```

Priority completion:

```text
priority_completion_rate =
sum(priority_i for served demands) / sum(priority_i for all demands)
```

The experimental weighted score is:

```text
score =
0.30 * completion_rate
+ 0.25 * priority_completion_rate
+ 0.20 * normalized_response_time_score
+ 0.15 * normalized_distance_score
+ 0.10 * normalized_runtime_score
```

For lower-is-better metrics, normalization uses min-max inversion across compared algorithms.

## 4. System Design

The platform is a monorepo:

- `frontend/`: Next.js dashboard.
- `backend/`: FastAPI API, algorithms, simulation, reports.
- `docs/`: algorithm design, technical report, interview questions.
- `docker-compose.yml`: PostgreSQL/PostGIS, Redis, backend, worker, frontend.

The backend persists every experiment as `SimulationRun`, `DispatchPlan`, `Route`, and `MetricResult`, making algorithm comparison reproducible.

## 5. Experiment Design

The project includes six standard benchmark scenarios:

| Scenario | Experimental Purpose | Expected Challenge |
| --- | --- | --- |
| Normal Scenario | Control group | Balanced distance, response time, and utilization. |
| Congestion Scenario | Road travel-time stress | Avoid congested center corridors. |
| Demand Surge Scenario | Workload growth | Maintain completion rate under more demand. |
| Resource Shortage Scenario | Capacity stress | Trade off unserved demands and priority completion. |
| Blocked Road Scenario | Network disruption | Route around critical blocked links. |
| High Priority Rescue Scenario | Urgency stress | Serve clustered high-priority demands early. |

The experimental workflow is:

1. Select one scenario.
2. Run Greedy, Priority, Dijkstra-based, A*-based, and OR-Tools CVRP.
3. Persist routes and metrics.
4. Compare algorithms with raw metrics and weighted score.
5. Generate a deterministic markdown report.

## 6. Algorithm Comparison

Compared algorithms:

- Greedy Dispatch: fast local baseline.
- Priority Dispatch: urgency-aware heuristic.
- Dijkstra-based Dispatch: shortest-path baseline.
- A*-based Dispatch: heuristic path planning baseline.
- OR-Tools CVRP: capacity-constrained operations research baseline.

The comparison table includes:

- total distance.
- average and max response time.
- completion rate.
- priority completion rate.
- vehicle utilization.
- delayed and unserved demand counts.
- runtime.
- weighted score.

## 7. Experiment Result Interpretation

Important interpretation patterns:

- If `completion_rate` is high but `priority_completion_rate` is low, the algorithm served easy tasks but missed urgent ones.
- If `total_distance` is low but `average_response_time` is high, congestion or service order may be poor.
- If `unserved_demands` is high in Resource Shortage Scenario, the bottleneck is capacity rather than path planning.
- If OR-Tools improves completion but costs more runtime, it is a quality-latency tradeoff.
- If Priority Dispatch wins in High Priority Rescue Scenario, the scenario validates urgency-aware scheduling.

## 8. Engineering Implementation

Key engineering features:

- SQLAlchemy 2.x typed models.
- Alembic migration with PostGIS extension.
- Deterministic research benchmark seed data.
- Unified API response envelope.
- OpenAPI documentation.
- Pytest algorithm, seed, report, and API tests.
- Docker Compose for frontend, backend, PostgreSQL/PostGIS, Redis, and worker.
- Optional OpenAI-compatible report generation with deterministic fallback.

## 9. Limitations and Improvements

Current limitations:

- Dynamic demand updates are not yet rolling-horizon optimized.
- Full hard VRPTW constraints are planned but not yet complete.
- SVG visualization is stable but not a geographic tile map.
- Real traffic feeds are represented by scenario parameters.

Future work:

- Online re-optimization with vehicle current positions.
- Full VRPTW and demand drop penalties in OR-Tools.
- Stochastic traffic simulation.
- MapLibre/Leaflet map layer.
- PDF report export and experiment archive bundles.

## 10. Interview Discussion Points

- Why this is a system engineering problem.
- How graph modeling maps real emergency scheduling.
- Difference between path planning and vehicle routing.
- Why heuristic methods and OR-Tools are both useful.
- How metrics and weighted score support decision analysis.
