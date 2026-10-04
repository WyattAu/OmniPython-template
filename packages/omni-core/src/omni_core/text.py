"""Checked text primitives. REQ-001: parsing rejects invalid input with
ParseError (a ValueError), never crashes. REQ-100: no secrets or I/O here —
pure functions only."""

from __future__ import annotations

import re

MAX_LEN: int = 256

_PRINTABLE: re.Pattern[str] = re.compile(r"[!-~]+")


class ParseError(ValueError):
    """Raised when input is not a valid public identifier."""


def parse_pub_id(raw: str) -> str:
    """Validate a public identifier: 1..=MAX_LEN printable ASCII, trimmed.

    Raises:
        ParseError: on empty input, over-long input, or non-printable bytes.
    """
    if not isinstance(raw, str):  # pragma: no cover - type system enforces
        raise ParseError("input must be str")
    trimmed = raw.strip()
    if not trimmed:
        raise ParseError("input is empty")
    if len(trimmed) > MAX_LEN:
        raise ParseError(f"input exceeds {MAX_LEN} bytes")
    if _PRINTABLE.fullmatch(trimmed) is None:
        raise ParseError("input contains non-printable bytes")
    return trimmed
