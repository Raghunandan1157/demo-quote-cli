"""ASCII banner formatter."""
import textwrap

from ..config import OutputTheme
from ..domain import Quote
from .base import QuoteFormatter


class BannerFormatter(QuoteFormatter, theme=OutputTheme.BANNER):
    def render(self, quote: Quote) -> str:
        wrapped = textwrap.wrap(quote.text, width=50) or [""]
        width = max(len(line) for line in wrapped + [quote.author]) + 4
        bar = "+" + "-" * (width - 2) + "+"
        body = "\n".join(f"| {line.ljust(width - 4)} |" for line in wrapped)
        author = f"| {('— ' + quote.author).rjust(width - 4)} |"
        return "\n".join((bar, body, author, bar))
