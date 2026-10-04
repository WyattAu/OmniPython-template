"""Leaf primitives for the OmniPython workspace.

The L0 pattern made concrete: zero workspace dependencies, total
functions (errors, never crashes), and requirement-tagged tests.
"""

from omni_core.text import ParseError, MAX_LEN, parse_pub_id

__all__ = ["MAX_LEN", "ParseError", "parse_pub_id"]
