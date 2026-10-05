#!/usr/bin/env bash
# Non-nix fallback. Canonical env: flake.nix (python + uv).
set -euo pipefail
cat <<'MSG'
Manual toolchain (no nix):
  1. uv (https://docs.astral.sh/uv/) — installs Python + everything else
  2. uv sync && make ci
Prefer zero setup? Open the repo in a devcontainer, or `nix develop`.
MSG
