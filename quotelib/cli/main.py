"""CLI entry point."""
from __future__ import annotations

import argparse
import logging
import sys
from typing import Dict, Optional, Sequence

from ..config import Configuration, OutputTheme
from ..services import ServiceFactory
from .parser import build_parser

logger = logging.getLogger("quote")


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
    namespace = build_parser().parse_args(args)

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
