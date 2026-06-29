"""Abstract formatter and registry."""
from __future__ import annotations

import abc
from typing import ClassVar, Dict, Optional

from ..config import OutputTheme
from ..domain import Quote


class QuoteFormatter(abc.ABC):
    """Renders a Quote into a presentable string."""

    registry: ClassVar[Dict[OutputTheme, type["QuoteFormatter"]]] = {}

    def __init_subclass__(cls, theme: Optional[OutputTheme] = None, **kw: object):
        super().__init_subclass__(**kw)
        if theme is not None:
            QuoteFormatter.registry[theme] = cls

    @classmethod
    def for_theme(cls, theme: OutputTheme) -> "QuoteFormatter":
        impl = cls.registry.get(theme)
        if impl is None:  # pragma: no cover - defensive
            raise KeyError(f"No formatter registered for theme {theme!r}")
        return impl()

    @abc.abstractmethod
    def render(self, quote: Quote) -> str:
        ...
