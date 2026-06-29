"""Unique (sample-without-replacement) selection strategy."""
from __future__ import annotations

import random
from typing import List, Sequence

from ..domain import Quote


class UniqueSelectionStrategy:
    """Selects distinct quotes, sampling without replacement where possible."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def select(self, pool: Sequence[Quote], count: int) -> List[Quote]:
        k = min(count, len(pool))
        return self._rng.sample(list(pool), k)
