---
name: add-threat-fixture
description: >
  Scaffold a new threat-intel fixture in an Ember security-suite repo (vetpkg,
  ember-network, ember-persistent, ember-agent-monitor). Use when adopting a new
  attack pattern, CVE, or incident into the regression corpus, when the user says
  "add a fixture", "pin this attack", "add this CVE to the corpus", or when a
  detection gap should be recorded as an honest-negative fixture.
---

# Add a threat-intel fixture

Every adopted attack pattern lands as a **named fixture** with pinned expected
verdicts, run by CI on every commit. Documented misses are fixtures too
(honest negatives) — a gap we know about is recorded, never silent.

## Naming

```
threat-intel/fixtures/<codename>_<vector>_<date>/
```

`<codename>` is the attacker/incident codename, `<vector>` the attack vector,
`<date>` month+year of the source intel. Examples from the corpus:
`lamehug_apt28_jul2025`, `clawhavoc_c2_91_92_242_30`, `s1ngularity_nx_aug2025`,
`promptmink_famous_chollima_apr2026`.

## Per-repo fixture shape

Look at an existing fixture in the target repo first — shapes differ by tool:

| Repo | Inputs | Expected |
|---|---|---|
| vetpkg | `intel.json` (modeled package intel) | `expected.json` with `expected_findings: [{package, version, verdict, signals_contain}]` |
| ember-network | `connections.jsonl`, `tool_calls.jsonl` | `expected.json` (pinned findings) |
| ember-persistent / ember-agent-monitor | session/event JSONL per their spec | `expected.json` |

Every fixture directory also gets a `README.md`.

## Required content

1. **README.md** — what the attack is, primary sources (vendor write-up, CVE id,
   news link) with dates, and which corpus-extension section it maps to.
2. **Input files** — modeled minimally: only the fields the detection layer reads.
   Don't paste real malware payloads; model the *signals*.
3. **expected.json** — pinned verdicts. Include a `_note` field explaining *why*
   the verdict is what it is, citing sources and the relevant signal names.

## Honest-negative fixtures

If the tool **cannot** catch the pattern (wrong layer, missing feature), still add
the fixture with the passing verdict it currently produces (e.g. `Allow`) and a
`_note` documenting:
- why it lands on null at this layer,
- which suite tool owns the catch surface (e.g. "catch surface is ember-network"),
- what future signal would flip the verdict (the fixture then becomes the
  regression test for that defense).

This is the established pattern — see `hidden_prompt_npm_dec2025` in vetpkg.

## Wire-up & verification

1. Check how the repo's fixture runner discovers fixtures (usually
   `tests/threat_intel_fixtures.rs` globs the fixtures directory — if so, no
   registration needed).
2. Run the fixture suite: `cargo test --test threat_intel_fixtures`.
3. Run `cargo fmt --all` (fixture-runner edits have failed CI on fmt before).
4. Commit as `feat(threat-intel): <codename> fixture — <one-line pattern summary>`
   or `test(threat-intel): ...` for honest negatives.

After landing, consider running the cross-tool e2e:
`~/ember-research-lab/tests/e2e_full_chain.sh`.
