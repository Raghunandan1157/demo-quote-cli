"""JSON formatter."""
import json

from ..config import OutputTheme
from ..domain import Quote
from .base import QuoteFormatter


class JsonFormatter(QuoteFormatter, theme=OutputTheme.JSON):
    def render(self, quote: Quote) -> str:
        return json.dumps(
            {"text": quote.text, "author": quote.author, "tags": list(quote.tags)},
            ensure_ascii=False,
        )
