"""Example: deliver a single quote programmatically."""
from quotelib.config import Configuration
from quotelib.services import ServiceFactory

if __name__ == "__main__":
    service = ServiceFactory().create(Configuration(count=1, seed=7))
    for line in service.deliver(1):
        print(line)
