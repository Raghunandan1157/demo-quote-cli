"""The Quote value object."""
from __future__ import annotations

import dataclasses
from typing import Tuple


@dataclasses.dataclass(frozen=True, order=True)
class Quote:
    """An immutable value object representing a single quotation."""

    text: str
    author: str
    tags: Tuple[str, ...] = dataclasses.field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("A Quote must have non-empty text.")
        if not self.author:
            object.__setattr__(self, "author", "Anonymous")

    @property
    def fingerprint(self) -> int:
        """A stable identity hash, useful for de-duplication strategies."""
        return hash((self.text, self.author))
