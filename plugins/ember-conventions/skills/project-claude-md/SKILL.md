---
name: project-claude-md
description: >
  Scaffold a CLAUDE.md team-orientation file for an ember-research-lab repo that
  lacks one. Use when the user says "add a CLAUDE.md", "this repo needs orientation
  docs", "onboard this repo", or when starting substantial work in a repo with no
  CLAUDE.md.
---

# Scaffold a repo CLAUDE.md

The exemplar is `ember-smb-platform/CLAUDE.md`. A good repo CLAUDE.md is
**60–120 lines**, states only verified facts, and answers: what is this, what must
I read first, what must I never break, and how do I build/test it.

## Required sections (in order)

1. **What this is** — 1–2 sentences. Steal the Cargo.toml `description` if good.
2. **Read before substantial work** — the repo's key docs with one-line purposes
   (`design/*-spec.md`, `docs/internal-threat-model.md`, README). If the repo
   documents a read order (e.g. ember-agent-monitor), preserve it.
3. **Non-negotiable house rules** — numbered, each with its *rationale*. Pull from:
   - zero-dependency policy (if a security-suite repo — cite the CI guard step)
   - `#![forbid(unsafe_code)]` status and any documented exceptions
   - invariants from the spec ("capture is read-only", "TLS never terminated",
     "substrate format is inviolable", "never weaken the reveal/audit path", …)
   Violations of these are P0 bugs, not style nits.
4. **Architecture** — crate/module map, ASCII diagram if multi-crate. Brief.
5. **How to work here** — testing discipline (fixtures? conformance suite?),
   commit format (`type(scope): description — detail`), surgical-diff norm.
6. **Commands** — exact build/test/lint invocations from `.github/workflows/ci.yml`
   (the workflow file is ground truth, not memory).
7. **Honest scope** — what this tool does NOT do. Copy the spec's own scope
   statements; don't soften them.
8. **Automations** (if any) — hooks in `.claude/settings.json`, repo agents/skills.

## Rules

- **Verify everything.** Every claim must trace to a file in the repo. If you can't
  verify it, leave it out — a wrong CLAUDE.md is worse than none.
- Don't duplicate org-wide conventions (those live in the `ember-house-style`
  skill and the workspace-root CLAUDE.md) — link/mention, don't copy.
- Match the org voice: terse, em-dash one-liners, honest about gaps.
- Land it as a doc-only PR: branch `docs/claude-md`, commit
  `docs: add CLAUDE.md agent/team orientation`.
