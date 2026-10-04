"""REQ-001: property tests — parsing never crashes on arbitrary input
(hypothesis = proptest parity with the Rust kits)."""

import contextlib

import pytest
from hypothesis import given
from hypothesis import strategies as st

from omni_core import MAX_LEN, ParseError, parse_pub_id


@given(st.text(max_size=600))
def test_parse_never_crashes(raw: str) -> None:
    with contextlib.suppress(ParseError):
        parse_pub_id(raw)


def test_valid_round_trip() -> None:
    assert parse_pub_id("  hello-world  ") == "hello-world"


def test_rejects_empty() -> None:
    with pytest.raises(ParseError, match="empty"):
        parse_pub_id("   ")


def test_rejects_too_long() -> None:
    with pytest.raises(ParseError, match="exceeds"):
        parse_pub_id("x" * (MAX_LEN + 1))


def test_rejects_control_bytes() -> None:
    with pytest.raises(ParseError, match="non-printable"):
        parse_pub_id("a\nb")
