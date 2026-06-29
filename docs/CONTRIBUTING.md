# Contributing

1. Create a virtual environment.
2. Install dev dependencies: `pip install -e .[dev]`.
3. Run the tests: `scripts/test.sh`.
4. Add a new formatter by subclassing `quotelib.formatters.base.QuoteFormatter`
   with a `theme=` keyword — it self-registers.
5. Add a new selection strategy by implementing the
   `quotelib.strategies.base.SelectionStrategy` protocol.

Keep the over-engineering tasteful.
