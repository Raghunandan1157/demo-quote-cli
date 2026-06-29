"""Orchestrating service layer."""
from __future__ import annotations

from typing import List, Optional, Sequence

from ..domain import Quote
from ..events import EventBus
from ..formatters import QuoteFormatter
from ..repositories import QuoteRepository
from ..strategies import SelectionStrategy


class QuoteService:
    """Orchestrates repository, strategy, and formatter collaborators."""

    def __init__(
        self,
        repository: QuoteRepository,
        strategy: SelectionStrategy,
        formatter: QuoteFormatter,
        bus: Optional[EventBus] = None,
    ) -> None:
        self._repository = repository
        self._strategy = strategy
        self._formatter = formatter
        self._bus = bus or EventBus()

    def _candidate_pool(self, tag: Optional[str]) -> Sequence[Quote]:
        pool = self._repository.by_tag(tag) if tag else self._repository.all()
        if not pool:
            raise LookupError(f"No quotes match the requested tag {tag!r}.")
        return pool

    def deliver(self, count: int, tag: Optional[str] = None) -> List[str]:
        """Select, announce, and render ``count`` quotes."""
        pool = self._candidate_pool(tag)
        chosen = self._strategy.select(pool, count)
        rendered: List[str] = []
        for quote in chosen:
            self._bus.publish(quote)
            rendered.append(self._formatter.render(quote))
        return rendered
