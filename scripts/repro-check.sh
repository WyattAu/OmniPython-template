#!/usr/bin/env bash
# Reproducible-build check (loop 3): build twice from a clean state with a pinned
# epoch and compare artifact hashes.
#
# MODE=gate - "gate" for toolchains that are deterministic (a mismatch is a
# real finding), "report" for toolchains that embed timestamps by design (a
# mismatch is printed and explained, never blocks). See the ADR.
set -euo pipefail
cd "$(dirname "$0")/.."
MODE=gate
EPOCH="${SOURCE_DATE_EPOCH:-$(git log -1 --pretty=%ct 2>/dev/null || echo 0)}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

compare() {
  if [ "$1" = "$2" ]; then
    echo "reproducible: OK ($1)"
    return 0
  fi
  echo "reproducible: MISMATCH" >&2
  echo "  run A: $1" >&2
  echo "  run B: $2" >&2
  echo "  diverging artifacts:" >&2
  diff <(printf '%s\n' "$1") <(printf '%s\n' "$2") | grep -E '^[<>]' | head -20 >&2 || true
  if [ "$MODE" = "gate" ]; then
    echo "  this toolchain is expected to be deterministic - fix the build" >&2
    exit 1
  fi
  echo "  reported only: " >&2
  exit 0
}

# Wheels/sdists honour SOURCE_DATE_EPOCH, so the artifact set must hash the
# same twice over. `--all-packages` because the workspace root is
# `package = false` - a bare `uv build` tries to build the root and fails.
# uv drops a .gitignore into the out-dir; it is tool noise, not an artifact.
buildinfo() {
  # Lamb & Zacchiroli (IEEE Software 2022): a reproducible build controls and
  # replicates *all legitimate build inputs*, not just the command. Record the
  # environment of every run so build 2 must reproduce build 1's inputs too.
  {
    echo "git: $(git rev-parse HEAD)"
    echo "epoch: $EPOCH"
    echo "uv: $(uv --version 2>/dev/null || echo unknown)"
    echo "python: $(python3 --version 2>/dev/null || echo unknown)"
    echo "lock: $(sha256sum uv.lock | awk '{print $1}')"
    echo "runner: $(uname -srmo)"
  } > "$WORK/$1/.buildinfo"
}

fingerprint() {
  mkdir -p "$WORK/$1"
  buildinfo "$1"
  SOURCE_DATE_EPOCH="$EPOCH" uv build --all-packages --out-dir "$WORK/$1" >/dev/null
  # Bytecode-cache poisoning guard (reproducible-builds.org report 2026-03:
  # ~12,500 PyPI packages ship unreproducible __pycache__ files that execute
  # without touching source). A poisoned-but-deterministic .pyc would pass the
  # hash comparison below -- it must not be in the artifact set at all.
  if find "$WORK/$1" -type f \( -name '*.pyc' -o -path '*__pycache__*' \) | grep -q .; then
    echo "repro guard: bytecode cache present in artifacts" >&2
    find "$WORK/$1" -name '*.pyc' -o -path '*__pycache__*' >&2
    exit 1
  fi
  find "$WORK/$1" -type f ! -name '.gitignore' ! -name '.buildinfo' -print0 | sort -z | xargs -0 sha256sum     | awk '{print $1, $2}' | sed "s|$WORK/$1/||"
}
a="$(fingerprint a)"
b="$(fingerprint b)"
compare "$a" "$b"
