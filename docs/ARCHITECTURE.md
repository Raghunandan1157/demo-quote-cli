# Architecture

This project delivers random programming quotes. It does so through an
elaborately layered architecture that is, by design, far more than the task
requires.

## Layers

```
quote.py  ──►  quotelib.cli  ──►  quotelib.services  ──►  quotelib.repositories
                    │                     │                       │
                    │                     ├──► quotelib.strategies
                    │                     ├──► quotelib.formatters
                    │                     └──► quotelib.events
                    └──► quotelib.config
```

| Package | Responsibility |
|---------|----------------|
| `quotelib.domain` | The immutable `Quote` value object |
| `quotelib.config` | Theme enum + layered `Configuration` cascade |
| `quotelib.repositories` | Data-access abstraction + in-memory corpus |
| `quotelib.strategies` | Pluggable selection policies |
| `quotelib.formatters` | Theme-driven rendering registry |
| `quotelib.events` | Synchronous publish/subscribe bus |
| `quotelib.services` | Orchestration + DI factory |
| `quotelib.cli` | Argument parsing + entry point |
| `quotelib.utils` | Assorted helpers of dubious necessity |

## Design patterns employed

- Repository
- Strategy
- Factory
- Registry (via `__init_subclass__`)
- Observer / Event bus
- Dependency injection
- Value object

All to print a sentence.
