#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Second, independent type checker. pyright (strict, mature) remains the primary
# gate; ty runs ~13x faster and fails on a different class of defect. Both must
# pass -- a single checker is a single point of failure for the type contract.
exec uv run ty check .
