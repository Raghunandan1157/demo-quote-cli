import pytest

from quotelib.domain import Quote


def test_quote_requires_text():
    with pytest.raises(ValueError):
        Quote("", "Someone")


def test_quote_defaults_author():
    q = Quote("hello", "")
    assert q.author == "Anonymous"


def test_fingerprint_is_stable():
    a = Quote("hi", "X")
    b = Quote("hi", "X")
    assert a.fingerprint == b.fingerprint
