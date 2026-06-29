"""Example: render quotes using every available theme."""
from quotelib.config import Configuration, OutputTheme
from quotelib.services import ServiceFactory

if __name__ == "__main__":
    for theme in OutputTheme:
        print(f"=== {theme.value} ===")
        service = ServiceFactory().create(Configuration(count=1, seed=3, theme=theme))
        for line in service.deliver(1):
            print(line)
        print()
