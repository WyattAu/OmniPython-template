# OmniPython-template

Maximalist Python **monorepo** template: **uv workspaces** + ruff (lint,
format, security rules) + **pyright strict** + pytest/hypothesis with a
**≥90% coverage gate** + mkdocs-material + PyPI trusted publishing — nix
flake, dual devcontainers, VS Code. Part of the
[WyattAu Omni template family](https://github.com/WyattAu?tab=repositories&q=omni-).

> v2 is a ground-up rewrite of the 2025 poetry-based template (ADR-0001,
> ADR-0002): one lockfile (`uv.lock`), one linter (ruff), strict types.

## Start here (after "Use this template")

1. Rename packages: `omni-core` / `omnistats` → yours (keep the
   internal-dependency pair — it's the monorepo pattern).
2. Pick a door — all resolve to identical toolchains:

   | Door | Command |
   |---|---|
   | nix + direnv (host) | `direnv allow` |
   | Devcontainer (image) | VS Code → *Reopen in Container* |
   | Devcontainer (nix)  | palette → *Rebuild in Container* → pick `.devcontainer/nix/` |

   No nix, no docker? `./scripts/bootstrap.sh` prints the manual path.
3. `uv sync --frozen && make ci` — must be green before your first push.

## Make targets

| Target | Gate |
|---|---|
| `make build` | `uv build` per package |
| `make test` | pytest + hypothesis, `--cov-fail-under=90` |
| `make lint` / `fmt` | ruff check / ruff format+fix |
| `make typecheck` | pyright **strict** |
| `make docs` | mkdocs build --strict |
| `make contract` | Omni Core Contract structural checks |
| `make ci` | contract + fmt-check + lint + typecheck + test |

## What is inside

```
pyproject.toml         virtual workspace root + ALL gate configs (ruff/pyright/pytest)
uv.lock                THE dependency pin (CI installs --frozen, never resolves)
packages/omni-core     L0 leaf: total functions, REQ-tagged, hypothesis properties
packages/omnistats     domain package composing on omni-core (workspace source)
docs/ + mkdocs.yml     material docs site
scripts/  + Makefile   the gates (make ci == CI)
docs/adr/              decision log (uv workspaces, ruff stack)
.github/workflows/     ci (3.12/3.13 + 3.14 tip + pyright + cov), release (trusted publishing), docs, devcontainers
.forgejo/              thin self-hosted mirror (scripts are canonical)
```

## Release flow

Tag `v*` → `uv build` → attestation → PyPI **trusted publishing** (OIDC —
no tokens). One-time setup: add a pending publisher for this repo on
pypi.org and create the `pypi` GitHub environment.

## Estate pointers

- Gates, policies: [engineering-standards](https://github.com/WyattAu/engineering-standards)
- Omni Core Contract: [OMNI-CORE.md](https://github.com/WyattAu/engineering-standards/blob/main/OMNI-CORE.md)

## License

Apache-2.0 — commercial use expressly permitted (v1's AGPLv3 retired with
the poetry stack).


## Performance budgets

Performance is a gate, not a hope. `make bench` measures, writes
`bench/current.tsv`, and compares it against the committed
`bench/baseline.tsv`; anything more than the threshold worse fails. The
comparator (`scripts/compare-bench.py`) is identical across the whole Omni
estate, so the policy is auditable in one place.

| Verb | What it does |
|---|---|
| `make bench` | measure + compare (advisory job in CI: `perf`) |
| `make bench-update` | deliberately re-baseline; the only way a baseline moves |

The first run on a fresh clone records the baseline instead of failing, so the
gate is meaningful from the second run onwards. Override the budget per run
with `OMNI_BENCH_THRESHOLD_PCT=15 make bench`. Rationale and per-template
metrics: `docs/adr/0005-performance-budget-gate.md`.


## Determinism

`make repro` builds twice from a clean state with a pinned `SOURCE_DATE_EPOCH`
and compares artifact hashes. Toolchains that are deterministic gate the build;
toolchains that embed timestamps or build ids by design report the difference
and explain why, rather than pretending to be reproducible. Rationale and the
per-toolchain split: `docs/adr/0006-determinism-verification.md`.

> Derived repos receive this line via the template update channel (ADR-0001).
