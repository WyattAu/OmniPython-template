# 0001 — uv workspaces (poetry/pdm retired)

Date: 2026-10-04

## Status

Accepted

## Context

The v1 template shipped pdm.lock AND poetry.lock — two contradictory pins —
and a poetry-only CI. uv won the toolchain race: faster, lockfile-native,
workspace-aware, one binary.

## Decision

- uv is the only supported runner; `uv.lock` is the authoritative pin.
- Workspace root is virtual (`tool.uv.package = false`); packages build via
  hatchling.
- `uv sync --frozen` is the CI install (never resolve in CI).

## Consequences

- One lockfile, fastest installs, no plugin matrix.
- CI resolves nothing: lockfile drift fails loudly.
