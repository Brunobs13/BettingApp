from __future__ import annotations

import random
from typing import Iterable

from betting_app.core.models import Region


DEFAULT_REGIONS: dict[str, Region] = {
    "EU": Region(
        code="EU",
        label="Europe",
        prize_by_matches={4: 2_000_000, 3: 50_000, 2: 10_000, 1: 500},
    ),
    "SA": Region(
        code="SA",
        label="South America",
        prize_by_matches={4: 1_000_000, 3: 50_000, 2: 10_000, 1: 500},
    ),
    "NA": Region(
        code="NA",
        label="North America",
        prize_by_matches={4: 2_500_000, 3: 60_000, 2: 12_000, 1: 600},
    ),
    "AP": Region(
        code="AP",
        label="Asia Pacific",
        prize_by_matches={4: 1_800_000, 3: 45_000, 2: 9_000, 1: 400},
    ),
}


class DrawEngine:
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def draw_numbers(self) -> tuple[int, int, int, int]:
        values = self._rng.sample(range(1, 100), 4)
        values.sort()
        return tuple(values)  # type: ignore[return-value]

    @staticmethod
    def matched_numbers(bet_numbers: Iterable[int], draw_numbers: Iterable[int]) -> tuple[int, ...]:
        return tuple(sorted(set(bet_numbers).intersection(set(draw_numbers))))
