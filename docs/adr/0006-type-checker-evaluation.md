# ADR-0006: pyright stays; `ty` evaluated and rejected for now

- **Status**: Accepted (loop 8)
- **Date**: 2026-10-08

## Context

Astral's `ty` (0.0.85) is the native, Rust-based type checker for Python: ~13x
faster than pyright on this tree (0.22s vs 2.9s). The estate's rule is to adopt
the best tool, and speed at the gate matters.

## Decision

**Keep pyright strict.** Measured on this template:

- pyright: 0 errors, 0 warnings on the full workspace.
- `ty check .`: **14 diagnostics, all false positives** — `unresolved-import`
  for every workspace-internal import (`omni_core`, `omnistats`), i.e. ty
  0.0.85 does not yet resolve uv-workspace `src/` layouts.

A checker that cannot see the workspace produces noise, and noise at a strict
gate trains people to ignore the gate.

## Consequences

- The `ty` re-evaluation stays on the loop backlog: adopt the first version
  that resolves this workspace layout cleanly (test: `uvx ty check .` must be
  clean on `main`).
- pyright strict remains the type gate; its cost (~3s) is acceptable.
- This is the template's recorded evaluation — derived repos inherit the
  reasoning, not just the config.
