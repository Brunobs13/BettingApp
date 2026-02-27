# Portfolio Ready Material

## LinkedIn Version (Short)
Refactored a monolithic academic betting app into a production-ready platform with modular Python architecture, FastAPI backend, interactive dashboard, automated tests, CI/CD workflow, and Docker deployment.

## CV Version (Technical)
Professionalized an OOP betting project by:
- Re-architecting into domain/service/infrastructure/API layers
- Implementing strict input validation and region-based prize logic
- Building a live web dashboard for bet placement and draw analytics
- Adding pytest suite, CI checks, Docker packaging, and operational scripts
- Producing technical audit and interview-ready documentation

## 60-Second Pitch
I transformed an academic Tkinter betting app into a production-style engineering project. I separated business rules into a domain layer, added a service layer for game flow, exposed the system with FastAPI, and built an interactive web dashboard for live bet and draw operations. I also added testing, CI, Docker, and full technical documentation. The final result demonstrates both software architecture maturity and practical delivery standards expected in real teams.

## 5-Minute Technical Pitch
The original repository mixed UI and business logic in a single file and lacked testing and deployment structure. I redesigned it into layered architecture: `core` for domain rules, `services` for orchestration, `infrastructure` for event logging, and `api` for HTTP transport. This made rule validation explicit and testable.

I implemented deterministic draw behavior support through optional seeding, region-specific payout models, and stateful session control with pending bet constraints. On top of that, I built an interactive web console that visualizes pending bets, draw outputs, prize outcomes, and operational metrics.

For production readiness, I added automated tests with pytest, CI workflow in GitHub Actions, Docker artifacts, environment-based configuration, and improved repository hygiene. If scaling to production, the next step would be persistent multi-user session storage and observability instrumentation.
