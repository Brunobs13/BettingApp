from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from betting_app.core.engine import DEFAULT_REGIONS, DrawEngine
from betting_app.core.models import BetTicket, DrawResult, Region
from betting_app.core.validators import normalize_numbers
from betting_app.infrastructure.storage import JsonLineStorage


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


class BettingService:
    def __init__(
        self,
        storage: JsonLineStorage,
        regions: dict[str, Region] | None = None,
        draw_engine: DrawEngine | None = None,
    ) -> None:
        self._storage = storage
        self._regions = regions or DEFAULT_REGIONS
        self._draw_engine = draw_engine or DrawEngine()

        self._pending_bet: BetTicket | None = None
        self._history: list[DrawResult] = []

        self._metrics: dict[str, int | str] = {
            "started_at": _utc_now(),
            "bets_placed": 0,
            "draws_processed": 0,
            "wins_count": 0,
            "total_prize_paid": 0,
            "errors": 0,
        }

    def list_regions(self) -> list[dict[str, Any]]:
        return [
            {
                "code": region.code,
                "label": region.label,
                "prize_by_matches": dict(region.prize_by_matches),
            }
            for region in self._regions.values()
        ]

    def place_bet(self, numbers: list[int], region_code: str) -> dict[str, Any]:
        code = region_code.strip().upper()
        if code not in self._regions:
            self._metrics["errors"] = int(self._metrics["errors"]) + 1
            raise ValueError(f"Unknown region code: {region_code}")

        if self._pending_bet is not None:
            self._metrics["errors"] = int(self._metrics["errors"]) + 1
            raise ValueError("A pending bet already exists. Run draw or reset first.")

        normalized = normalize_numbers(numbers)

        ticket = BetTicket(
            ticket_id=str(uuid4()),
            created_at=_utc_now(),
            numbers=normalized,
            region=code,
        )

        self._pending_bet = ticket
        self._metrics["bets_placed"] = int(self._metrics["bets_placed"]) + 1

        self._storage.write_event(
            {
                "type": "bet_placed",
                "timestamp": _utc_now(),
                "ticket": asdict(ticket),
            }
        )

        return {
            "message": "Bet placed successfully",
            "ticket": self._ticket_to_dict(ticket),
            "state": self.state(),
        }

    def draw(self) -> dict[str, Any]:
        ticket = self._pending_bet
        if ticket is None:
            self._metrics["errors"] = int(self._metrics["errors"]) + 1
            raise ValueError("No pending bet. Place a bet first.")

        draw_numbers = self._draw_engine.draw_numbers()
        matched = DrawEngine.matched_numbers(ticket.numbers, draw_numbers)
        matches = len(matched)

        region = self._regions[ticket.region]
        prize = int(region.prize_by_matches.get(matches, 0))

        result = DrawResult(
            ticket_id=ticket.ticket_id,
            created_at=_utc_now(),
            draw_numbers=draw_numbers,
            matched_numbers=matched,
            matches=matches,
            prize=prize,
            region=ticket.region,
        )

        self._history.insert(0, result)
        self._pending_bet = None

        self._metrics["draws_processed"] = int(self._metrics["draws_processed"]) + 1
        if prize > 0:
            self._metrics["wins_count"] = int(self._metrics["wins_count"]) + 1
            self._metrics["total_prize_paid"] = int(self._metrics["total_prize_paid"]) + prize

        self._storage.write_event(
            {
                "type": "draw_processed",
                "timestamp": _utc_now(),
                "ticket": self._ticket_to_dict(ticket),
                "result": self._result_to_dict(result),
            }
        )

        return {
            "message": "Draw processed",
            "result": self._result_to_dict(result),
            "state": self.state(),
        }

    def reset(self) -> dict[str, Any]:
        self._pending_bet = None
        self._history.clear()

        self._metrics = {
            "started_at": _utc_now(),
            "bets_placed": 0,
            "draws_processed": 0,
            "wins_count": 0,
            "total_prize_paid": 0,
            "errors": 0,
        }

        self._storage.write_event(
            {
                "type": "session_reset",
                "timestamp": _utc_now(),
            }
        )

        return {
            "message": "Session reset",
            "state": self.state(),
        }

    def metrics(self) -> dict[str, Any]:
        output = dict(self._metrics)
        output["timestamp"] = _utc_now()
        output["history_count"] = len(self._history)
        return output

    def state(self) -> dict[str, Any]:
        return {
            "pending_bet": self._ticket_to_dict(self._pending_bet) if self._pending_bet else None,
            "history": [self._result_to_dict(item) for item in self._history[:20]],
            "regions": self.list_regions(),
        }

    @staticmethod
    def _ticket_to_dict(ticket: BetTicket) -> dict[str, Any]:
        return {
            "ticket_id": ticket.ticket_id,
            "created_at": ticket.created_at,
            "numbers": list(ticket.numbers),
            "region": ticket.region,
        }

    @staticmethod
    def _result_to_dict(result: DrawResult) -> dict[str, Any]:
        return {
            "ticket_id": result.ticket_id,
            "created_at": result.created_at,
            "draw_numbers": list(result.draw_numbers),
            "matched_numbers": list(result.matched_numbers),
            "matches": result.matches,
            "prize": result.prize,
            "region": result.region,
        }
