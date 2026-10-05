"""Small, total statistics helpers. Errors, never crashes (REQ-001)."""

from __future__ import annotations

from collections.abc import Sequence

from omni_core import ParseError, parse_pub_id


def mean(values: Sequence[float]) -> float:
    """Arithmetic mean. Empty input raises ValueError (documented, total)."""
    if not values:
        raise ValueError("mean of empty sequence")
    return sum(values) / len(values)


def zscore(values: Sequence[float], x: float) -> float:
    """(x - mean) / stdev (population). Constant sequence raises."""
    if not values:
        raise ValueError("zscore of empty sequence")
    m = mean(values)
    variance = sum((v - m) ** 2 for v in values) / len(values)
    if variance == 0.0:
        raise ValueError("zscore undefined for constant sequence")
    return (x - m) / (variance**0.5)


def normalize_id(raw: str) -> str:
    """Compose on omni-core: binaries compose on packages, not copies."""
    result: str = parse_pub_id(raw)
    return result


__all__ = ["ParseError", "mean", "normalize_id", "zscore"]
