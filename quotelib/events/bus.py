"""A minimal synchronous publish/subscribe dispatcher."""
from __future__ import annotations

import logging
from typing import Callable, List

from ..domain import Quote

logger = logging.getLogger("quote")

Observer = Callable[[Quote], None]


class EventBus:
    """A minimal synchronous publish/subscribe dispatcher."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def publish(self, quote: Quote) -> None:
        for observer in self._observers:
            try:
                observer(quote)
            except Exception:  # pragma: no cover
                logger.exception("Observer %r raised; continuing", observer)
