"""Random selection strategy."""
from __future__ import annotations

import random
from typing import List, Sequence

from ..domain import Quote


class RandomSelectionStrategy:
    """Selects quotes uniformly at random, allowing repetition."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def select(self, pool: Sequence[Quote], count: int) -> List[Quote]:
        return [self._rng.choice(pool) for _ in range(count)]
