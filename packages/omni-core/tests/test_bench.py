"""Perf gate input: `make bench` runs this through scripts/bench-budget.sh and
compares it to the committed baseline in bench/baseline.tsv."""

from __future__ import annotations

from pytest_benchmark.fixture import BenchmarkFixture

from omni_core.text import parse_pub_id

# Batched timing: a single ~1us call has more timer noise than signal, so the
# benchmark measures 1000 iterations and the gate compares like with like.
ITERATIONS = 1_000


def test_bench_parse_pub_id(benchmark: BenchmarkFixture) -> None:
    """The validation regex is the hot path for every caller."""

    def batch() -> None:
        for _ in range(ITERATIONS):
            parse_pub_id("omni-core")

    benchmark(batch)
