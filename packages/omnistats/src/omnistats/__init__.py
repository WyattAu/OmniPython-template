"""Example domain package — the omnicore→omnistats internal-dependency
pattern from OmniR, in Python."""

from omnistats.stats import ParseError, mean, normalize_id, zscore

__all__ = ["ParseError", "mean", "normalize_id", "zscore"]
