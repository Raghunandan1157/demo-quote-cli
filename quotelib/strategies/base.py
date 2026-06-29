"""Selection strategy protocol."""
from __future__ import annotations

from typing import List, Protocol, Sequence, runtime_checkable

from ..domain import Quote


@runtime_checkable
class SelectionStrategy(Protocol):
    """A pluggable policy for choosing quotes from a candidate pool."""

    def select(self, pool: Sequence[Quote], count: int) -> List[Quote]:
        ...
