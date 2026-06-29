#!/usr/bin/env bash
# Convenience wrapper around the CLI.
set -euo pipefail
exec python3 "$(dirname "$0")/../quote.py" "$@"
