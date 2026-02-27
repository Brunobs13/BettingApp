from betting_app.core.engine import DrawEngine
from betting_app.infrastructure.storage import JsonLineStorage
from betting_app.services.betting_service import BettingService


def make_service(tmp_path):
    storage = JsonLineStorage(str(tmp_path / "events.jsonl"))
    draw_engine = DrawEngine(seed=7)
    return BettingService(storage=storage, draw_engine=draw_engine)


def test_place_and_draw_flow(tmp_path):
    service = make_service(tmp_path)

    placed = service.place_bet([5, 12, 23, 45], "EU")
    assert placed["ticket"]["region"] == "EU"

    draw = service.draw()
    result = draw["result"]
    assert sorted(result["draw_numbers"]) == result["draw_numbers"]
    assert 0 <= result["matches"] <= 4
    assert result["prize"] >= 0


def test_duplicate_numbers_rejected(tmp_path):
    service = make_service(tmp_path)

    try:
        service.place_bet([2, 2, 10, 11], "EU")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "unique" in str(exc).lower()


def test_draw_without_pending_bet_fails(tmp_path):
    service = make_service(tmp_path)

    try:
        service.draw()
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "no pending bet" in str(exc).lower()
