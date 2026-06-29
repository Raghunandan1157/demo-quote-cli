"""Abstract repository boundary."""
from __future__ import annotations

import abc
from typing import Iterator, Sequence

from ..domain import Quote


class QuoteRepository(abc.ABC):
    """Abstract persistence boundary for quotations."""

    @abc.abstractmethod
    def all(self) -> Sequence[Quote]:
        ...

    def by_tag(self, tag: str) -> Sequence[Quote]:
        """Filter quotes whose tag set contains ``tag`` (case-insensitive)."""
        needle = tag.lower()
        return [q for q in self.all() if needle in (t.lower() for t in q.tags)]

    def __len__(self) -> int:
        return len(self.all())

    def __iter__(self) -> Iterator[Quote]:
        return iter(self.all())
