"""Pointless text transformations."""
from __future__ import annotations


def shout(text: str) -> str:
    """Return text in uppercase with emphasis."""
    return text.upper() + "!"


def whisper(text: str) -> str:
    """Return text in lowercase, parenthesized."""
    return f"({text.lower()})"
