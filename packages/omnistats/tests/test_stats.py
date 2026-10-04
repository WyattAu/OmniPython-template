import pytest
from hypothesis import given
from hypothesis import strategies as st

from omnistats import ParseError, mean, normalize_id, zscore


def test_mean() -> None:
    assert mean([1.0, 2.0, 3.0]) == 2.0


def test_mean_empty_raises() -> None:
    with pytest.raises(ValueError, match="empty"):
        mean([])


def test_zscore_constant_raises() -> None:
    with pytest.raises(ValueError, match="constant"):
        zscore([5.0, 5.0, 5.0], 5.0)


@given(st.lists(st.floats(allow_nan=False, min_value=-1e6, max_value=1e6), min_size=1, max_size=50))
def test_zscore_finite(values: list[float]) -> None:
    result = zscore(values, values[0])
    assert result == result  # NaN self-check


def test_composes_on_omni_core() -> None:
    assert normalize_id("  omni ") == "omni"
    with pytest.raises(ParseError):
        normalize_id("bad\nid")
