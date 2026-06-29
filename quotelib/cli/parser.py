"""Argument parser construction."""
from __future__ import annotations

import argparse

from ..config import OutputTheme
from ..version import __version__


def build_parser() -> argparse.ArgumentParser:
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
