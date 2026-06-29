#!/usr/bin/env python3
"""Tiny CLI that prints a random programming quote."""
import random
import sys

QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Programs must be written for people to read.", "Harold Abelson"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
]


def pick() -> str:
    text, author = random.choice(QUOTES)
    return f'"{text}"\n    — {author}'


def main(argv: list[str]) -> int:
    if "-n" in argv:
        count = int(argv[argv.index("-n") + 1])
        for _ in range(count):
            print(pick(), end="\n\n")
    else:
        print(pick())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
