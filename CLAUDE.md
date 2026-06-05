# CLAUDE.md — marketplace

Orientation for anyone (human or Claude) working in this repo.

## What this is

The **org plugin marketplace** for ember-research-lab: a catalog
(`.claude-plugin/marketplace.json`) plus in-repo plugin sources under
`plugins/`. Team machines register it once in `~/.claude/settings.json`
(`extraKnownMarketplaces` → `github: ember-research-lab/marketplace`); each
repo then opts into plugins via its checked-in `.claude/settings.json`
(`"<plugin>@ember-research-lab": true`). Every ember repo currently enables
`ember-conventions`.

## Catalog rules

- Two source shapes: a `./plugins/<name>` relative path (plugin lives
  here — e.g. `ember-conventions`) or a `{source: "url", url, ref}` git
  source (plugin lives in its own repo — e.g. `claude-cortex`, pinned to
  `main`). Use `url`, not `github`, as the source type — it's the
  universally supported schema (see git log for the schema fixes).
- Every plugin entry needs `name`, `source`, `description`; in-repo plugins
  need `skills/<name>/SKILL.md` (frontmatter `name` + `description`) and/or
  `agents/*.md`.
- CI (`.github/workflows/ci.yml`) runs `python3
  .github/validate_marketplace.py` (stdlib-only) which enforces all of the
  above. Run it locally before pushing.

## Editing the ember-conventions plugin

Skills: `ember-house-style` (CI bar + commit format), `add-threat-fixture`
(fixture discipline), `project-claude-md` (CLAUDE.md scaffolding). Agents:
`fixture-verifier`, `rigor-auditor`. Keep skill descriptions
trigger-focused (they're the retrieval surface), and keep house-style
claims consistent with what the repos' CI actually enforces — when they
drift, the repo CI is the truth, fix the skill.

Consumers pull from `main`; treat merges here as releases.
