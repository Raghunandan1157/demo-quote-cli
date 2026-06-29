"""Fancy unicode formatter."""
from ..config import OutputTheme
from ..domain import Quote
from .base import QuoteFormatter


class FancyFormatter(QuoteFormatter, theme=OutputTheme.FANCY):
    def render(self, quote: Quote) -> str:
        return f"❝ {quote.text} ❞\n        ✎ {quote.author}"
