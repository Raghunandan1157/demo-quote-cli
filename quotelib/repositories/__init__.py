"""Repository layer."""
from .base import QuoteRepository
from .in_memory import InMemoryQuoteRepository

__all__ = ["QuoteRepository", "InMemoryQuoteRepository"]
