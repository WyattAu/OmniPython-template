# OmniPython-template

Maximalist Python monorepo: **uv workspaces**, ruff (lint+format+security
rules), **pyright strict**, pytest + hypothesis, mkdocs-material docs.

```bash
uv sync
make ci
```

## Packages

| Package | Role |
|---|---|
| `omni-core` | L0 leaf — total functions, REQ-tagged, property-tested |
| `omnistats` | domain package composing on omni-core |

## Gates

| Gate | Threshold |
|---|---|
| ruff | `check` (E/F/I/UP/B/SIM/S/RUF/PT), format |
| pyright | strict |
| pytest | `--cov-fail-under=90` |
| hypothesis | property class per behavior (estate parity) |
| release | uv build + attestation + PyPI trusted publishing |
