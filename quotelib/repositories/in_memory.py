"""In-memory repository backed by a curated corpus."""
from __future__ import annotations

from typing import ClassVar, Sequence, Tuple

from ..domain import Quote
from .base import QuoteRepository


class InMemoryQuoteRepository(QuoteRepository):
    """A repository backed by a hard-coded, curated corpus."""

    _CORPUS: ClassVar[Tuple[Quote, ...]] = (
        Quote("Talk is cheap. Show me the code.", "Linus Torvalds", ("pragmatism",)),
        Quote("Programs must be written for people to read.", "Harold Abelson",
              ("readability",)),
        Quote("Premature optimization is the root of all evil.", "Donald Knuth",
              ("performance",)),
        Quote("Simplicity is the soul of efficiency.", "Austin Freeman",
              ("simplicity",)),
        Quote("First, solve the problem. Then, write the code.", "John Johnson",
              ("process",)),
        Quote("Code is like humor. When you have to explain it, it's bad.",
              "Cory House", ("readability",)),
    )

    def all(self) -> Sequence[Quote]:
        return self._CORPUS
