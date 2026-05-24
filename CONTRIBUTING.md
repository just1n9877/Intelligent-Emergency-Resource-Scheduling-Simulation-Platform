# Contributing

Thanks for improving this project. The repository is intentionally structured for interview review and reproducible experiments, so changes should stay small, explainable, and testable.

## Code Structure

- `backend/app/algorithms/`: graph construction, shortest paths, dispatch algorithms, and metrics.
- `backend/app/api/`: FastAPI route handlers.
- `backend/app/models/`: SQLAlchemy domain models.
- `backend/app/seeds/`: deterministic experiment scenarios.
- `backend/app/tests/`: pytest tests for algorithms, APIs, seed data, and reports.
- `frontend/src/app/`: Next.js pages for scenarios, network, simulation, results, and reports.
- `docs/`: system design, algorithm design, technical report, interview materials, and demo assets.

## Start the Project

```bash
cp .env.example .env
make dev
```

Open:

- Frontend: http://localhost:3000
- Swagger: http://localhost:8000/docs

## Run Tests

```bash
make test
```

Backend-only:

```bash
cd backend
DATABASE_URL=sqlite+pysqlite:// AUTO_SEED_DEFAULTS=false python -m pytest -q
```

Frontend build:

```bash
cd frontend
npm run build
```

## Lint and Acceptance Check

```bash
make lint
python scripts/check_project.py
```

`scripts/check_project.py` expects the Docker stack to be running for service health checks. It also runs backend pytest with SQLite.

## Contribution Guidelines

- Do not change public API shapes unless the README, docs, tests, and frontend client are updated together.
- Do not replace implemented algorithms with hard-coded demo results.
- Keep Roadmap items clearly labeled as future work.
- Add or update tests when changing algorithm, API, seed, or report behavior.
- Keep README screenshots honest: placeholders must remain clearly labeled until replaced by real screenshots.
