# English Project Pitch

## 30-second Version

I built an Intelligent Emergency Resource Scheduling and Simulation Platform for civil emergency logistics. The system models an urban road network as a weighted graph, represents depots, vehicles, demands, congestion, and blocked roads, then runs dispatch algorithms such as Greedy, Priority-based dispatch, Dijkstra-based routing, A* routing, and OR-Tools CVRP. It records routes and metrics, compares algorithms, and generates an experiment report. The goal is to demonstrate a complete system engineering loop from modeling to optimization, simulation, evaluation, and full-stack implementation.

## 1-minute Version

This project is a full-stack platform for civil emergency resource scheduling. I model the city as a directed weighted graph, where nodes represent intersections or demand locations, and edges represent roads with distance, speed, congestion factor, and blocked status. On top of this graph, the system models depots, vehicles, vehicle capacity, demand quantity, priority, service time, and time-window evaluation.

The backend is built with FastAPI, SQLAlchemy, Pydantic, PostgreSQL/PostGIS, Redis/Celery, NetworkX, and OR-Tools. The frontend is built with Next.js, TypeScript, Tailwind CSS, shadcn/ui, and Recharts. The platform supports seeded benchmark scenarios, route visualization, simulation control, algorithm comparison, metrics dashboard, and deterministic markdown report generation. For me, the main value is that it connects system engineering, operations research, path planning, simulation evaluation, and real software engineering.

## 3-minute Version

My project is called Intelligent Emergency Resource Scheduling and Simulation Platform. It focuses on civil emergency logistics, such as urban relief supply delivery or campus medical material scheduling. I chose this topic because it is a typical system engineering problem: there are multiple interacting elements, including a road network, depots, vehicles, demand points, road states, resource constraints, objectives, and evaluation metrics.

The mathematical model starts from a directed weighted graph. Each edge has distance, speed, congestion factor, and blocked status. Travel time is calculated from distance, speed, and congestion. If an edge is blocked, it is excluded from the algorithm graph. Vehicles have capacity and current location. Demands have quantity, priority, service time, and time-window information. The core decision is to assign demands to vehicles, determine service sequences, and generate road-node paths.

The algorithm layer contains several comparable methods. Dijkstra and A* are used for path planning. Greedy Dispatch is a fast baseline that assigns each demand to the nearest feasible vehicle. Priority Dispatch sorts demands by urgency before assignment. OR-Tools CVRP provides an operations research baseline for capacity-constrained vehicle routing. All algorithms are evaluated using the same metrics: total distance, average response time, max response time, completion rate, priority completion rate, vehicle utilization, delayed demands, unserved demands, and runtime.

The engineering implementation is a real full-stack system. The backend uses FastAPI, SQLAlchemy, Pydantic, PostgreSQL/PostGIS, Redis/Celery, NetworkX, OR-Tools, and pytest. The frontend uses Next.js, TypeScript, Tailwind CSS, shadcn/ui, and Recharts. The system provides scenario management, network visualization, simulation control, result dashboard, algorithm comparison charts, weighted score ranking, and deterministic report generation. If an OpenAI-compatible API key is configured, the report can be polished by an LLM, but the project works without any external AI service.

The current implementation is an MVP, so it does not yet include real-time dynamic re-optimization or full hard-constraint VRPTW. However, it already demonstrates the complete loop of system modeling, optimization, simulation, evaluation, and engineering delivery. This is why I think it is a meaningful project for electronic information and system engineering study.

## Follow-up Q&A Version

**Q: Why is this project not just a dashboard?**  
A: The dashboard is only the interface. The core is the data model, graph construction, dispatch algorithms, persisted simulation runs, comparable metrics, and experiment reports. The frontend consumes real backend results.

**Q: What algorithms are actually implemented?**  
A: The project implements Dijkstra shortest path, A* with a geographic heuristic, Greedy Dispatch, Priority-based Dispatch, and OR-Tools CVRP. OR-Tools may fall back to priority dispatch when the capacity-constrained model is infeasible.

**Q: What is the main system engineering idea?**  
A: I treat emergency scheduling as a complex system. I define system components, constraints, objectives, algorithms, simulation metrics, and feedback reports instead of optimizing a single isolated route.

**Q: What is the weighted score used for?**  
A: It provides an explainable decision-support score. Completion rate and priority completion have the highest weights because emergency scenarios care first about serving demands, especially urgent demands. Response time, distance, and runtime are also considered.

**Q: What are the limitations?**  
A: The current version uses static seeded scenarios, grid-based road networks, and time-window evaluation rather than full VRPTW. Future work includes rolling-horizon re-optimization, real map data, full VRPTW, and batch experiment management.
