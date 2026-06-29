"""Layered configuration cascade."""
from __future__ import annotations

import dataclasses
import logging
import os
from typing import Dict, Optional

from .theme import OutputTheme

logger = logging.getLogger("quote")


@dataclasses.dataclass
class Configuration:
    """Resolved runtime configuration assembled from a layered cascade."""

    count: int = 1
    theme: OutputTheme = OutputTheme.PLAIN
    seed: Optional[int] = None
    tag: Optional[str] = None
    unique: bool = False

    @classmethod
    def from_environment(cls) -> "Configuration":
        """Construct configuration defaults sourced from the environment."""
        cfg = cls()
        if (raw := os.environ.get("QUOTE_THEME")) is not None:
            try:
                cfg.theme = OutputTheme(raw.lower())
            except ValueError:
                logger.warning("Ignoring unknown QUOTE_THEME=%r", raw)
        if (raw := os.environ.get("QUOTE_SEED")) is not None:
            try:
                cfg.seed = int(raw)
            except ValueError:
                logger.warning("Ignoring non-integer QUOTE_SEED=%r", raw)
        return cfg

    def merged_with(self, overrides: Dict[str, object]) -> "Configuration":
        """Return a new Configuration with non-None overrides applied."""
        data = dataclasses.asdict(self)
        for key, value in overrides.items():
            if value is not None and key in data:
                data[key] = value
        if not isinstance(data["theme"], OutputTheme):
            data["theme"] = OutputTheme(data["theme"])
        return Configuration(**data)  # type: ignore[arg-type]
