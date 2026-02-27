import os
from fastapi.testclient import TestClient

from betting_app.api.app import create_app


def test_health_endpoint(tmp_path):
    os.environ["BETTING_LOG_PATH"] = str(tmp_path / "events.jsonl")
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_place_bet_and_draw(tmp_path):
    os.environ["BETTING_LOG_PATH"] = str(tmp_path / "events.jsonl")
    os.environ["BETTING_RANDOM_SEED"] = "15"

    app = create_app()
    client = TestClient(app)

    place = client.post(
        "/api/bets/place",
        json={"numbers": [1, 2, 3, 4], "region": "EU"},
    )
    assert place.status_code == 200

    draw = client.post("/api/draw")
    assert draw.status_code == 200
    assert "result" in draw.json()
