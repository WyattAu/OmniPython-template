# ADR-0007: pyright stays; `ty` evaluated and rejected for now

- **Status**: **Superseded by loop 20** (decision below reversed; both checkers now gate)
- **Date**: 2026-10-08 (superseded 2026-10-08, loop 20)

## Superseded (loop 20) -- the rejection was a config error, not a tool limit

Re-tested at the **same version** (ty 0.0.85): the 14 `unresolved-import`
diagnostics reappear until `[tool.ty.environment]` names the workspace member
sources (`extra-paths` + `root`). With that config, `ty check .` is **clean**
on `main`, at 0.22s vs pyright's 2.9s. ty was never unable to resolve the
workspace layout -- it was never told where it was.

Decision: **keep pyright strict AND gate with ty** (`make typecheck` runs
`scripts/typecheck.sh` then `scripts/typecheck-ty.sh`). Two independent checkers
means one blind spot cannot silently pass; ~3s of extra CI time is cheap
against a type contract. `ty` is pinned `>=0.0.85,<0.1` in the dev group so the
gate is reproducible and Dependabot-driven bumps stay reviewable.

Lesson recorded: a rejection measured *without* the tool's configuration is not
an evaluation. The original reasoning is kept below unmodified.

## Original decision (loop 8)


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
