# Algorithm Design

## Graph Modeling

The road network is modeled as a directed weighted graph `G=(V,E)`.

- Node: intersection, depot location, vehicle start, or demand point.
- Edge: directed road segment with distance, speed, congestion factor, and blocked status.
- Blocked edges are stored in the database but removed from the algorithm graph.
- Congestion changes travel-time cost:

```text
travel_time_min = distance_km / speed_kmph * 60 * congestion_factor
```

The same graph supports shortest-path routing and vehicle dispatch.

## Unified Algorithm I/O

Input:

- `graph`: NetworkX directed graph.
- `vehicles`: id, start node, capacity, speed, availability.
- `demands`: id, node, quantity, priority, service time, time window.
- `objective`: distance, response time, priority completion, or weighted objective.
- `parameters`: vehicle count, demand scale, congestion ratio.

Output:

- route list.
- served demand ids.
- unserved demand ids.
- node path for each vehicle.
- total distance and travel time.
- objective value.
- runtime milliseconds.
- metrics for comparison.

## Dijkstra-based Dispatch

Core idea: use Dijkstra shortest paths as the routing subroutine, then assign each demand to the feasible vehicle with the best immediate travel score.

Best suited for:

- Stable road networks.
- Transparent baseline comparison.
- Explaining shortest-path fundamentals.

Advantages:

- Deterministic and easy to explain.
- Works with any non-negative edge weight.
- Reliable baseline for routing.

Limitations:

- Dispatch remains greedy, so it may miss globally better vehicle-demand sequences.

Complexity:

```text
Shortest path: O((V + E) log V)
Dispatch loop: O(D * K * shortest_path_cost)
```

where `D` is demand count and `K` is vehicle count.

## A*-based Dispatch

Core idea: use A* for vehicle-to-demand path planning. The heuristic is geographic distance between two nodes.

Best suited for:

- Larger spatial graphs where target direction matters.
- Cases where routing speed is important.

Advantages:

- Can expand fewer nodes than Dijkstra when the heuristic is informative.
- Still uses real edge weights for final path cost.

Limitations:

- Heuristic quality affects performance.
- In this MVP, dispatch sequencing is still greedy.

Complexity:

```text
Worst case: O((V + E) log V)
Typical case: fewer expanded nodes than Dijkstra with a useful heuristic
```

## Greedy Dispatch

Core idea: process demands in deterministic id order. For each demand, choose the feasible vehicle with enough remaining capacity and the shortest immediate path.

Best suited for:

- Fast baseline.
- Normal scenarios with balanced capacity.
- Demonstrating a simple decision rule.

Advantages:

- Very fast.
- Easy to debug.
- Produces readable route decisions.

Limitations:

- Local optimum only.
- May serve low-priority demands before urgent ones.
- Early assignments may cause later unserved demands.

Complexity:

```text
O(D * K * shortest_path_cost)
```

## Priority-based Dispatch

Core idea: sort demands by priority descending, then by time-window deadline, then demand id. Assignment still uses shortest feasible path.

Best suited for:

- High Priority Rescue Scenario.
- Medical or emergency response cases where urgency matters more than route distance.

Advantages:

- Improves high-priority completion.
- Easy to defend in system-engineering interviews.

Limitations:

- May increase total distance.
- Can reduce low-priority completion under resource shortage.

Complexity:

```text
Sort: O(D log D)
Dispatch: O(D * K * shortest_path_cost)
```

## OR-Tools CVRP

Core idea: formulate the dispatch problem as a Capacitated Vehicle Routing Problem. The solver receives a shortest-path distance matrix, vehicle capacities, and demand quantities.

Best suited for:

- Capacity-constrained logistics.
- Resource Shortage Scenario.
- Algorithm comparison baseline.
- More complex constraints in future VRPTW extensions.

Advantages:

- Uses a mature operations research solver.
- Handles capacity constraints globally.
- Easier to extend to time windows, penalties, multiple depots, and drop costs.

Limitations:

- Needs distance-matrix construction.
- Runtime can grow with problem size.
- Solver output may require post-processing back to road-node paths.

Complexity:

CVRP is NP-hard. OR-Tools uses heuristics and local search rather than exhaustive enumeration. In practice, the MVP uses a time limit to keep experiments interactive.

Why OR-Tools is better for complex constraints:

- It natively supports dimensions such as capacity, time, distance, and slack.
- It can add penalties for dropped demands.
- It supports local-search metaheuristics.
- It separates model constraints from search strategy, which is easier to explain and extend than handcrafted nested logic.

## Objectives

- `minimize_total_distance`: reduce total route kilometers.
- `minimize_total_response_time`: reduce arrival time.
- `maximize_priority_completion`: prioritize urgent demands.
- `weighted_multi_objective`: combine distance, response time, completion, and unserved penalties.

## Metrics

- `total_distance`: total vehicle travel distance.
- `average_response_time`: average arrival time.
- `max_response_time`: worst-case arrival time.
- `completion_rate`: served demands divided by all demands.
- `priority_completion_rate`: priority-weighted served ratio.
- `vehicle_utilization`: served load divided by available vehicle capacity.
- `delayed_demands`: served demands arriving after deadline.
- `unserved_demands`: demands not assigned to any route.
- `algorithm_runtime_ms`: execution time.

## Weighted Score

The comparison module computes an interpretable score:

```text
score =
0.30 * completion_rate
+ 0.25 * priority_completion_rate
+ 0.20 * normalized_response_time_score
+ 0.15 * normalized_distance_score
+ 0.10 * normalized_runtime_score
```

Normalization:

- Completion metrics are already ratios in `[0, 1]`.
- For lower-is-better metrics such as distance, response time, and runtime:

```text
normalized_score = 1 - (value - min_value) / (max_value - min_value)
```

If all algorithms have the same value, the normalized score is `1.0`.

Weight meaning:

- Completion and priority completion dominate because emergency systems value service success first.
- Response time is next because delay can matter more than distance.
- Distance and runtime remain important engineering efficiency indicators.
