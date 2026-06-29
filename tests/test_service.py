from quotelib.config import Configuration, OutputTheme
from quotelib.services import ServiceFactory


def test_service_delivers_requested_count():
    config = Configuration(count=3, seed=1)
    service = ServiceFactory().create(config)
    assert len(service.deliver(3)) == 3


def test_unique_delivery_has_no_repeats():
    config = Configuration(count=6, seed=1, unique=True)
    service = ServiceFactory().create(config)
    rendered = service.deliver(6)
    assert len(set(rendered)) == len(rendered)


def test_json_theme_is_valid_json():
    import json

    config = Configuration(count=1, seed=1, theme=OutputTheme.JSON)
    service = ServiceFactory().create(config)
    [out] = service.deliver(1)
    assert "author" in json.loads(out)
