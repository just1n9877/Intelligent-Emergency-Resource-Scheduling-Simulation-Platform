# Changelog

All notable changes are recorded here in project-phase order.

## GitHub Showcase Polish

- Reworked the README into a GitHub-first project homepage with badges, screenshots, quick start, architecture, algorithm flow, demo flow, and roadmap.
- Added placeholder screenshot assets for the six main product pages.
- Added a demo script, contributing guide, MIT license, Makefile commands, and a local acceptance checker.

## Graduate Interview Package

- Added a three-page Chinese project summary for quick review by interview teachers.
- Added a 10-slide defense presentation outline.
- Expanded interview questions and reference answers for system engineering, electronic information, algorithms, and future research discussion.
- Added English project pitch variants and bilingual resume bullets.

## Report Generation

- Added deterministic Markdown report generation that works without an API key.
- Added optional OpenAI-compatible report polishing with safe fallback.
- Included scenario description, algorithm configuration, metric comparison, bottleneck analysis, engineering recommendations, limitations, and future work.

## Algorithm Comparison

- Added multi-algorithm comparison across Greedy, Priority, Dijkstra-based, A*-based, and OR-Tools CVRP dispatch.
- Added metric explanations and weighted score ranking.
- Added comparison charts for distance, response time, completion rate, priority completion rate, and runtime.

## MVP

- Built a monorepo with FastAPI backend, Next.js frontend, Docker Compose, PostgreSQL/PostGIS, Redis, Celery worker, and pytest.
- Implemented core domain models for scenarios, nodes, edges, depots, vehicles, demands, dispatch plans, routes, simulation runs, metric results, and algorithm configs.
- Added six seeded civil emergency scheduling scenarios and the initial dashboard pages.
