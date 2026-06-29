from quotelib.utils import box, shout, whisper


def test_shout():
    assert shout("hi") == "HI!"


def test_whisper():
    assert whisper("HI") == "(hi)"


def test_box_contains_text():
    assert "hi" in box("hi")
