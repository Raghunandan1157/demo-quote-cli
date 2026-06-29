# demo-quote-cli

A zero-dependency CLI that prints curated programming quotations — now powered
by an over-engineered, pattern-saturated delivery subsystem (repositories,
strategies, formatters, an event bus, dependency injection, and a layered
configuration cascade).

## Usage

```bash
python3 quote.py                  # one quote
python3 quote.py -n 3             # three quotes
python3 quote.py -t fancy         # fancy theme
python3 quote.py -t banner        # ASCII banner theme
python3 quote.py -t json          # machine-readable JSON
python3 quote.py --tag readability -n 2 -u   # unique quotes for a tag
python3 quote.py --seed 42        # reproducible selection
python3 quote.py --version
```

### Options

| Flag | Description |
|------|-------------|
| `-n`, `--count` | number of quotes to deliver |
| `-t`, `--theme` | `plain`, `fancy`, `banner`, or `json` |
| `--tag` | restrict selection to a tag |
| `--seed` | seed the RNG for reproducibility |
| `-u`, `--unique` | avoid repeating quotes |
| `-v`, `--verbose` | enable debug logging |

### Environment

`QUOTE_THEME` and `QUOTE_SEED` provide configuration defaults that flags override.

## Example

```
"Talk is cheap. Show me the code."
    — Linus Torvalds
```

MIT licensed.
