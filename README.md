# Betting App Engine (Object-Oriented Refactor)

A production-grade modernization of an academic betting application.

## Project Overview
This repository transforms a monolithic Tkinter classroom project into a layered platform with:
- Domain-driven betting engine
- FastAPI backend service
- Interactive web dashboard
- Automated tests and CI pipeline
- Docker deployment and secure configuration patterns

## Business Problem
Academic prototypes usually demonstrate functionality but not operational quality. This refactor addresses:
- Maintainability (modular architecture)
- Security hygiene (no hardcoded credentials, env-driven config)
- Delivery readiness (CI/CD + Docker)
- Portfolio quality for technical interviews

## Architecture Diagram (Text)
```
[Interactive Dashboard - web/]
           |
           v
[FastAPI API Layer - src/betting_app/api]
           |
           v
[Application Service - betting_service.py]
           |
           v
[Domain Engine + Validators - core/*]
           |
           v
[Infrastructure Logging - JsonLineStorage]
```

## Tech Stack
- Python 3.11
- FastAPI + Uvicorn
- Pydantic
- Pytest
- Docker + Docker Compose
- GitHub Actions CI
- HTML/CSS/JavaScript dashboard

## Project Structure
```
.
├── src/betting_app/
│   ├── api/
│   ├── core/
│   ├── services/
│   └── infrastructure/
├── tests/
├── web/
├── configs/
├── docs/
├── scripts/
├── legacy/
├── Dockerfile
├── docker-compose.yml
└── Makefile
```

## Setup Instructions (Step-by-Step)
1. Clone:
```bash
git clone https://github.com/Brunobs13/BettingApp_Object-Oriented-Programming.git
cd BettingApp_Object-Oriented-Programming
```

2. Install dependencies:
```bash
./scripts/setup.sh
```

3. Run tests:
```bash
./scripts/test.sh
```

4. Run API and dashboard:
```bash
./scripts/run_api.sh
```

5. Open:
- Dashboard: `http://localhost:8080`
- Health: `http://localhost:8080/health`

## API Endpoints
- `GET /health`
- `GET /api/regions`
- `GET /api/state`
- `GET /api/metrics`
- `POST /api/bets/place`
- `POST /api/draw`
- `POST /api/reset`

## CI/CD Overview
Workflow (`.github/workflows/ci.yml`) runs on push/PR:
1. Install dependencies
2. Execute pytest suite
3. Enforce merge quality baseline

## Data Versioning Strategy
The current app is transactional and does not require dataset versioning. If future analytics data grows:
- Version large data with DVC
- Keep generated artifacts out of Git
- Track lineage metadata under `docs/`

## Model Tracking Strategy
This project does not train ML models. If predictive odds modeling is introduced:
- Use MLflow for experiment tracking
- Use DVC for feature dataset versioning
- Gate model promotions via CI checks

## Deployment Strategy
### Local Docker
```bash
docker compose up --build
```

### Cloud Hosting
Deploy the container to Render/Fly.io/Railway and expose port `8080`.

## Security Considerations
- No hardcoded API keys/secrets in code.
- Runtime settings loaded from environment variables.
- Event logs written to configurable path (`BETTING_LOG_PATH`).
- `.gitignore` includes `.env`, logs, artifacts, DVC cache and local build outputs.

## Lessons Learned
- Splitting domain rules from UI logic improves testability and extensibility.
- A service layer clarifies business flow and reduces API/controller complexity.
- Structured documentation elevates technical communication for interviews.

## Future Improvements
- Authentication and role-based access controls
- Multi-user bet sessions with persistent storage (PostgreSQL/Redis)
- WebSocket real-time updates
- Prometheus/OpenTelemetry observability
- Cloud deployment pipeline with staged environments
