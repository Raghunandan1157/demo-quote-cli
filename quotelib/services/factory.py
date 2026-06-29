"""Service factory wiring collaborators from configuration."""
from __future__ import annotations

import logging
import random
from typing import Optional

from ..config import Configuration
from ..events import EventBus
from ..formatters import QuoteFormatter
from ..repositories import InMemoryQuoteRepository, QuoteRepository
from ..strategies import (
    RandomSelectionStrategy,
    SelectionStrategy,
    UniqueSelectionStrategy,
)
from .service import QuoteService

logger = logging.getLogger("quote")


class ServiceFactory:
    """Assembles a fully-wired :class:`QuoteService` from configuration."""

    def __init__(self, repository: Optional[QuoteRepository] = None) -> None:
        self._repository = repository or InMemoryQuoteRepository()

    def create(self, config: Configuration) -> QuoteService:
        rng = random.Random(config.seed)
        strategy: SelectionStrategy = (
            UniqueSelectionStrategy(rng)
            if config.unique
            else RandomSelectionStrategy(rng)
        )
        formatter = QuoteFormatter.for_theme(config.theme)
        bus = EventBus()
        bus.subscribe(lambda q: logger.debug("Delivering quote by %s", q.author))
        return QuoteService(self._repository, strategy, formatter, bus)
