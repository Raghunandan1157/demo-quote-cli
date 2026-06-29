"""Plain text formatter."""
from ..config import OutputTheme
from ..domain import Quote
from .base import QuoteFormatter


class PlainFormatter(QuoteFormatter, theme=OutputTheme.PLAIN):
    def render(self, quote: Quote) -> str:
        return f'"{quote.text}"\n    — {quote.author}'
