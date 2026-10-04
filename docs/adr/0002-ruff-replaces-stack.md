# 0002 — ruff replaces black/isort/flake8/bandit

Date: 2026-10-04

## Status

Accepted

## Context

v1 ran four tools with overlapping configs (black+isort+flake8+bandit) —
four sources of truth for style and security.

## Decision

ruff does lint + format + import order + security rules (S = bandit ruleset).
pyright (strict) is the only type gate. Test files allow asserts (S101) via
one per-file-ignore.

## Consequences

- One config block in pyproject.toml; hook failures match CI failures.
- Removing bandit/safety is safe: S-rules + Dependabot/uv audit cover it.
