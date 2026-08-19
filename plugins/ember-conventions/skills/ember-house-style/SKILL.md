---
name: ember-house-style
description: >
  Ember Research Lab house style and engineering conventions. Use when writing or
  reviewing code in any ember-research-lab repo, when unsure about commit format,
  module documentation, error handling, dependency policy, or the CI bar, or when
  the user asks "what are the house rules", "ember style", or "team conventions".
---

# Ember house style

The conventions below are applied across all ember-research-lab repos. They are
enforced by CI where possible; the rest is reviewer discipline. When editing an
existing repo, the repo's own CLAUDE.md wins on any conflict.

## The CI bar (Rust)

Every Rust repo must pass all of these before merge — run them locally first:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings   # warnings ARE errors
cargo test --workspace
cargo deny check advisories bans sources               # supply-chain policy
```

Some repos add: a zero-dependency guard, pattern lints (`scripts/lint-patterns.sh`),
trufflehog secret scan, wasm/UniFFI/maturin builds. Read the repo's
`.github/workflows/ci.yml` — whatever is there is the bar, not a suggestion.

## Zero-dependency policy (security suite)

vetpkg, ember-network, ember-persistent, ember-agent-monitor, ember-vault keep
`[dependencies]` empty (or workspace-internal path deps only). This is the security
premise of the suite — the trust anchors are rustc + cargo + stdlib (+ the curl
binary where documented). CI fails the build on violation. Never add an external
crate to one of these repos; implement the minimal needed subset instead.

## Commit messages

```
type(scope): description — optional longer detail
```

- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Em-dash (`—`) separates the one-liner from elaboration
- Examples from the org's history:
  - `feat(threat-intel): tarball-driven runner + promptmink fixture`
  - `fix(episodic): tighten manifest watermark validation + correct comments (review round 2)`
- Feature branches + PRs; CI green before merge. Atomic commits.

## Rust code conventions

- **Module docs are mandatory.** Every crate and module opens with
  `//! name — purpose in one or two sentences` (em-dash, same voice as the rest
  of the org). Fuller description below if needed.
- **Errors are enums, not strings.** Named variants with context. No
  `Result<_, String>` in library code.
- **`#![forbid(unsafe_code)]`** at crate root. The only sanctioned exception is
  platform FFI behind a feature flag, with a comment explaining *why* unsafe is
  required (e.g. kernel interop).
- Tests: focused unit tests in `#[cfg(test)] mod tests`; integration and fixture
  tests in `tests/`.
- Workspace-internal crates that aren't published set `publish = false`
  (this also keeps cargo-deny's wildcard ban happy with versionless path deps).

## Honest scope

READMEs and specs name what a tool does **NOT** do, in its own section. Misses and
limitations are documented, not hidden — see the honest-negative fixture pattern in
`/add-threat-fixture`. When you discover a gap, the deliverable is a documented gap
(fixture, ledger entry, or spec note), never silence.

## Change discipline

- Surgical diffs: touch only what the task requires; match surrounding style even
  if you'd do it differently. No drive-by refactors — the team optimizes for
  reviewability and onboarding, not cleverness.
- If a change is hard to keep small, split the PR.
- Update the repo's CHANGELOG.md if the repo keeps one.

## Where deeper rules live

- Repo `CLAUDE.md` files **link** org conventions (this skill + the workspace
  `CLAUDE.md`); they do not recopy zero-dep / fmt / clippy / commit-format
  paragraphs. But a repo rule that is *stricter* than the org bar is a delta,
  not a duplicate — keep it. (`project-claude-md` already says the first half.)
- Repo-specific invariants: that repo's `CLAUDE.md` + `design/*-spec.md` +
  `docs/internal-threat-model.md`
- Research/formal work (Lean, manuscripts): `RIGOROUS_WORKFLOW.md` at the
  workspace root — tier system T0–T3, vacuity tests, falsifier/verifier
  separation. Use the `rigor-auditor` agent before claiming a tier.
