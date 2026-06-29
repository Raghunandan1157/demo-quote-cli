"""Output theme enumeration."""
import enum


class OutputTheme(enum.Enum):
    """Enumerates supported rendering themes."""

    PLAIN = "plain"
    FANCY = "fancy"
    BANNER = "banner"
    JSON = "json"
