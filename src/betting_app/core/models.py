from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@dataclass(frozen=True)
class Region:
    code: str
    label: str
    prize_by_matches: Mapping[int, int]


@dataclass(frozen=True)
class BetTicket:
    ticket_id: str
    created_at: str
    numbers: tuple[int, int, int, int]
    region: str


@dataclass(frozen=True)
class DrawResult:
    ticket_id: str
    created_at: str
    draw_numbers: tuple[int, int, int, int]
    matched_numbers: tuple[int, ...]
    matches: int
    prize: int
    region: str
