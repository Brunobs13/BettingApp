from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from betting_app.core.engine import DrawEngine
from betting_app.infrastructure.storage import JsonLineStorage
from betting_app.services.betting_service import BettingService


class PlaceBetRequest(BaseModel):
    numbers: list[int] = Field(..., min_length=4, max_length=4)
    region: str = Field(..., min_length=2, max_length=8)


class DrawResponse(BaseModel):
    message: str
    result: dict[str, Any]
    state: dict[str, Any]


def create_app() -> FastAPI:
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logger = logging.getLogger("betting.api")

    storage_path = os.getenv("BETTING_LOG_PATH", "artifacts/events.jsonl")
    seed = os.getenv("BETTING_RANDOM_SEED")
    draw_engine = DrawEngine(seed=int(seed)) if seed else DrawEngine()

    service = BettingService(
        storage=JsonLineStorage(storage_path),
        draw_engine=draw_engine,
    )

    app = FastAPI(title="Betting App Engine", version="1.0.0")

    repo_root = Path(__file__).resolve().parents[3]
    web_root = repo_root / "web"

    if web_root.exists():
        app.mount("/assets", StaticFiles(directory=web_root), name="assets")

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "betting-app-engine",
            "storage_path": storage_path,
        }

    @app.get("/api/regions")
    def regions() -> dict[str, Any]:
        return {"regions": service.list_regions()}

    @app.get("/api/state")
    def state() -> dict[str, Any]:
        return service.state()

    @app.get("/api/metrics")
    def metrics() -> dict[str, Any]:
        return service.metrics()

    @app.post("/api/bets/place")
    def place_bet(payload: PlaceBetRequest) -> dict[str, Any]:
        try:
            return service.place_bet(numbers=payload.numbers, region_code=payload.region)
        except ValueError as exc:
            logger.warning("failed to place bet: %s", exc)
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/api/draw", response_model=DrawResponse)
    def draw() -> dict[str, Any]:
        try:
            return service.draw()
        except ValueError as exc:
            logger.warning("failed to process draw: %s", exc)
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/api/reset")
    def reset() -> dict[str, Any]:
        return service.reset()

    @app.get("/")
    def root() -> FileResponse:
        index_file = web_root / "index.html"
        if not index_file.exists():
            raise HTTPException(status_code=404, detail="dashboard not available")
        return FileResponse(index_file)

    return app


app = create_app()
