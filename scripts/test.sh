#!/usr/bin/env bash
# Run the test suite.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 -m pytest -q
