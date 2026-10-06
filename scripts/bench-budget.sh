#!/usr/bin/env bash
# Perf budget gate: measure, emit bench/current.tsv, compare to the committed
# baseline with the shared comparator. `make bench-update` re-baselines
# deliberately - it is the only way a baseline moves.
set -euo pipefail
cd "$(dirname "$0")/.."
BASELINE=bench/baseline.tsv
CURRENT=bench/current.tsv
THRESHOLD_PCT="${OMNI_BENCH_THRESHOLD_PCT:-10}"
UPDATE=()
[ "${1:-}" = "--update" ] && UPDATE=(--update)
mkdir -p bench

uv sync --frozen
# `python -m pytest` (not bare `pytest`) so the interpreter's own plugins are
# used; --no-cov because a benchmark-only run would never meet the coverage gate.
uv run python -m pytest --benchmark-only --benchmark-json=bench/pytest-bench.json --no-cov -q

python3 - <<'PY' >"$CURRENT"
import json

report = json.loads(open("bench/pytest-bench.json").read())
rows = []
for entry in report["benchmarks"]:
    stats = entry["stats"]
    name = entry["fullname"].split("::")[-1]
    # stats are seconds; the gate works in nanoseconds.
    rows.append((name, float(stats["mean"]) * 1e9, "ns", "gate",
                 float(stats.get("stddev", 0.0)) * 1e9))
if not rows:
    raise SystemExit("bench: no measurements in bench/pytest-bench.json")
for name, value, unit, mode, noise in sorted(rows):
    print(f"{name}\t{value:.3f}\t{unit}\t{mode}\t{noise:.3f}")
PY

python3 scripts/compare-bench.py "$BASELINE" "$CURRENT" \
  --threshold-pct "$THRESHOLD_PCT" "${UPDATE[@]+"${UPDATE[@]}"}"
