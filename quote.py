#!/usr/bin/env python3
"""An over-engineered, enterprise-grade, infinitely-extensible quotation
delivery subsystem.

What was once a six-line script is now a fully abstracted, pattern-saturated
framework featuring repositories, strategies, formatters, a plugin registry,
an event bus, dependency injection, and a layered configuration cascade.

Backwards compatible with the original CLI:

    python3 quote.py            # one quote
    python3 quote.py -n 3       # three quotes
"""
from __future__ import annotations

import abc
import argparse
import dataclasses
import enum
import functools
import logging
import os
import random
import sys
import textwrap
from typing import (
    Callable,
    ClassVar,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    runtime_checkable,
)

__version__ = "2.0.0-enterprise"

logger = logging.getLogger("quote")


# --------------------------------------------------------------------------- #
# Domain model
# --------------------------------------------------------------------------- #
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


# --------------------------------------------------------------------------- #
# Configuration cascade
# --------------------------------------------------------------------------- #
class OutputTheme(enum.Enum):
    """Enumerates supported rendering themes."""

    PLAIN = "plain"
    FANCY = "fancy"
    BANNER = "banner"
    JSON = "json"


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
        # asdict() flattens the enum; restore it.
        if not isinstance(data["theme"], OutputTheme):
            data["theme"] = OutputTheme(data["theme"])
        return Configuration(**data)  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# Repository layer (data access abstraction)
# --------------------------------------------------------------------------- #
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


# --------------------------------------------------------------------------- #
# Selection strategies (strategy pattern)
# --------------------------------------------------------------------------- #
@runtime_checkable
class SelectionStrategy(Protocol):
    """A pluggable policy for choosing quotes from a candidate pool."""

    def select(self, pool: Sequence[Quote], count: int) -> List[Quote]:
        ...


class RandomSelectionStrategy:
    """Selects quotes uniformly at random, allowing repetition."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def select(self, pool: Sequence[Quote], count: int) -> List[Quote]:
        return [self._rng.choice(pool) for _ in range(count)]


class UniqueSelectionStrategy:
    """Selects distinct quotes, sampling without replacement where possible."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def select(self, pool: Sequence[Quote], count: int) -> List[Quote]:
        k = min(count, len(pool))
        return self._rng.sample(list(pool), k)


# --------------------------------------------------------------------------- #
# Formatter layer (factory + strategy)
# --------------------------------------------------------------------------- #
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


class PlainFormatter(QuoteFormatter, theme=OutputTheme.PLAIN):
    def render(self, quote: Quote) -> str:
        return f'"{quote.text}"\n    — {quote.author}'


class FancyFormatter(QuoteFormatter, theme=OutputTheme.FANCY):
    def render(self, quote: Quote) -> str:
        return f"❝ {quote.text} ❞\n        ✎ {quote.author}"


class BannerFormatter(QuoteFormatter, theme=OutputTheme.BANNER):
    def render(self, quote: Quote) -> str:
        wrapped = textwrap.wrap(quote.text, width=50) or [""]
        width = max(len(line) for line in wrapped + [quote.author]) + 4
        bar = "+" + "-" * (width - 2) + "+"
        body = "\n".join(f"| {line.ljust(width - 4)} |" for line in wrapped)
        author = f"| {('— ' + quote.author).rjust(width - 4)} |"
        return "\n".join((bar, body, author, bar))


class JsonFormatter(QuoteFormatter, theme=OutputTheme.JSON):
    def render(self, quote: Quote) -> str:
        import json

        return json.dumps(
            {"text": quote.text, "author": quote.author, "tags": list(quote.tags)},
            ensure_ascii=False,
        )


# --------------------------------------------------------------------------- #
# Event bus (observer pattern)
# --------------------------------------------------------------------------- #
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
            except Exception:  # pragma: no cover - observers must not break flow
                logger.exception("Observer %r raised; continuing", observer)


# --------------------------------------------------------------------------- #
# Service layer (dependency injection wires it all together)
# --------------------------------------------------------------------------- #
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


# --------------------------------------------------------------------------- #
# Command layer (command pattern over argparse)
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quote",
        description="Deliver curated programming quotations.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-n", "--count", type=int, default=None,
                        help="number of quotes to deliver")
    parser.add_argument("-t", "--theme", type=str, default=None,
                        choices=[t.value for t in OutputTheme],
                        help="rendering theme")
    parser.add_argument("--tag", type=str, default=None,
                        help="restrict selection to a tag")
    parser.add_argument("--seed", type=int, default=None,
                        help="seed the random generator for reproducibility")
    parser.add_argument("-u", "--unique", action="store_true", default=None,
                        help="avoid repeating quotes")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="enable debug logging")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    return parser


def _resolve_configuration(ns: argparse.Namespace) -> Configuration:
    base = Configuration.from_environment()
    overrides: Dict[str, object] = {
        "count": ns.count,
        "theme": OutputTheme(ns.theme) if ns.theme else None,
        "tag": ns.tag,
        "seed": ns.seed,
        "unique": ns.unique,
    }
    return base.merged_with(overrides)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    namespace = _build_parser().parse_args(args)

    logging.basicConfig(
        level=logging.DEBUG if namespace.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    config = _resolve_configuration(namespace)
    logger.debug("Resolved configuration: %r", config)

    try:
        service = ServiceFactory().create(config)
        for rendered in service.deliver(config.count, config.tag):
            print(rendered, end="\n\n")
    except (LookupError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
