# Technical Overview - Betting App Engine

## 1) Deep Architectural Explanation

### Flow
1. User places bet via dashboard (`POST /api/bets/place`).
2. API validates payload and delegates to `BettingService`.
3. Service normalizes bet numbers and stores pending ticket.
4. User triggers draw (`POST /api/draw`).
5. Draw engine samples unique numbers and computes matched values.
6. Service resolves prize by selected region and records event history.
7. Dashboard fetches updated state/metrics and renders results.

### Key Decisions
- Domain rules isolated in `core/` for high cohesion.
- Service layer orchestrates state transitions and business rules.
- Infrastructure layer handles persistence abstraction (`JsonLineStorage`).
- API remains thin and focused on transport concerns.

### Trade-offs
- In-memory session state is simple and fast but not shared across instances.
- JSONL logging is lightweight but not query-optimized for analytics.
- Polling dashboard is simpler than WebSocket streaming but less real-time.

### Alternatives
- PostgreSQL persistence for multi-user durability.
- Event-driven architecture (Kafka/Redis streams) for higher scale.
- WebSocket frontend for lower-latency updates.

## 2) Junior Interview Questions
1. Why did you use a service layer?
- To separate business orchestration from HTTP and UI concerns.

2. How is input validated?
- Domain validator enforces exactly 4 unique integers in range 1..99.

3. How are prizes computed?
- Region-specific payout table keyed by match count.

4. Why maintain a pending bet concept?
- It preserves game flow and avoids inconsistent multi-draw behavior.

5. How do you test this project?
- Unit tests for domain/service plus API tests with FastAPI TestClient.

## 3) Senior Interview Questions
1. How would you scale this to multiple users?
- Introduce account/session IDs, persistent storage, and stateless API workers.

2. How would you harden reliability?
- Add retries for storage writes, structured error taxonomy, and idempotency keys.

3. How would you implement observability?
- OpenTelemetry traces, Prometheus metrics, and centralized log aggregation.

4. How would you secure the API?
- Add JWT auth, rate limiting, input abuse protections, and audit controls.

5. How would you prepare multi-environment deployment?
- Environment-specific config overlays, secret manager integration, and staged CI/CD pipelines.

## 4) Critical Code Sections

### `src/betting_app/core/validators.py`
- Ensures strict bet format and domain constraints.
- Interview angle: guardrails and defensive programming.

### `src/betting_app/services/betting_service.py`
- Central business orchestration and metrics accounting.
- Interview angle: transactional state design and consistency.

### `src/betting_app/api/app.py`
- Endpoint definitions and API-to-service translation.
- Interview angle: error mapping and interface stability.

### `web/app.js`
- Client-side orchestration of user actions and live rendering.
- Interview angle: front-end state sync and UX feedback loops.
