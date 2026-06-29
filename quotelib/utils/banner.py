"""A box-drawing helper nobody asked for."""
from __future__ import annotations


def box(text: str) -> str:
    """Wrap a single line of text in an ASCII box."""
    width = len(text) + 2
    bar = "+" + "-" * width + "+"
    return f"{bar}\n| {text} |\n{bar}"
