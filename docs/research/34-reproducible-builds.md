# Research note 34 — reproducible builds & hermeticity

**Sources.** Lamb & Zacchiroli, *Reproducible Builds: Increasing the Integrity
of Software Supply Chains* (IEEE Software 39(2), 2022; arXiv:2104.06020) — the
definitional paper from the Debian reproducible-builds effort. Reproducible
Builds project monthly report 2026-03 (Python bytecode-cache poisoning at ~
12,500-package scale on PyPI). Google OSS Rebuild (automated rebuild +
attestation). SLSA build track.

## What the state of the art says

1. **Definition.** A build is reproducible when *all legitimate build inputs*
   are controlled and replicated identical in the second build — not merely
   "we ran the same command twice". Inputs include toolchain versions, locale,
   filesystem order, timestamps, and the CPU/parallelism environment.
2. **The diagnosis layer.** Debian's practice pairs the hash comparison with
   `.buildinfo` files (a record of every input) and diffoscope (which localises
   *why* two artifacts differ). A bare "MISMATCH" is a failure you cannot act
   on.
3. **The 2026 frontier is Python-specific.** Bytecode-cache poisoning: ship a
   `__pycache__/*.pyc` whose bytecode disagrees with the source — the
   interpreter happily executes it, and ~12,500 PyPI packages currently carry
   unreproducible cache files. A deterministic poisoned `.pyc` passes a hash
   comparison; presence itself must be a finding.

## Delta analysis — estate vs state of the art

| Practice | SOTA | Estate before | Estate after (loop 34) |
|---|---|---|---|
| hash double-build | baseline | yes (loop 3) | yes |
| input recording (`.buildinfo`) | Debian practice | missing | **yes** — git, epoch, uv, python, lock hash, runner recorded per run and compared |
| bytecode-cache guard | 2026-03 report | missing | **yes** — error on any `*.pyc`/`__pycache__` in artifacts |
| root-cause output | diffoscope | hash-only MISMATCH | **partial** — diverging artifacts listed; full diffoscope is future work (heavy dependency) |
| order-dependence test | disorderfs | missing | future work (needs container shims) |
| cross-infrastructure rebuild | OSS Rebuild | same-runner only | future work (needs a second runner class) |

## What we do that the references do not (checked claims)

- The gate is **per-toolchain-honest**: toolchains that embed timestamps by
  design run in report mode with the mismatch printed and explained (ADR-0006),
  instead of being silently marked irreproducible. nixpkgs tracks this as
  per-package notes; our gate encodes the distinction in the gate itself.
- The bytecode guard is a **hard error inside the repro gate**, not a separate
  advisory lint — the 2026 attack is deterministic, so a hash comparison alone
  is structurally blind to it.

## Follow-ups filed

- Generalise `.buildinfo` + the pyc guard to every template's repro gate
  (estate sweep) — Rust/Go/Haskell need their own "no nondeterministic
  byproducts" guard classes.
- diffoscope on mismatch, advisory.
- A second runner class for true cross-infrastructure rebuild (OSS Rebuild
  style) — needs infrastructure decisions (owner).
