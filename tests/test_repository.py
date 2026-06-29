from quotelib.repositories import InMemoryQuoteRepository


def test_repository_non_empty():
    repo = InMemoryQuoteRepository()
    assert len(repo) > 0


def test_by_tag_filters():
    repo = InMemoryQuoteRepository()
    readability = repo.by_tag("readability")
    assert all("readability" in q.tags for q in readability)
    assert len(readability) >= 1
