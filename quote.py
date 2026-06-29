#!/usr/bin/env python3
"""Thin entry point delegating to the absurdly modular :mod:`quotelib`.

Backwards compatible with the original CLI:

    python3 quote.py            # one quote
    python3 quote.py -n 3       # three quotes
"""
import sys

from quotelib.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
