# Ember Research Lab — Claude Code Marketplace

Plugins published by [Ember Research Lab](https://github.com/ember-research-lab) for Claude Code.

## Installation

Add the marketplace, then install plugins by name:

```sh
/plugin marketplace add ember-research-lab/marketplace
/plugin install claude-cortex@ember-research-lab
```

## Plugins

### claude-cortex

Persistent memory that makes Claude Code smarter across sessions. Rust workspace
implementing a blockchain-style ledger with Ed25519 signatures, BLAKE3 content
hashing, and confidence reinforcement on a 180-day half-life. Auto-loads
orientation directives at session start; surfaces top-confidence learnings for
the orchestrator to apply; auto-classifies outcomes at session end.

- Source: [`ember-research-lab/claude-cortex`](https://github.com/ember-research-lab/claude-cortex)
- Version: `0.3.0`
- Category: `memory`

After install, fetch the per-platform binaries from the [release artifacts](https://github.com/ember-research-lab/claude-cortex/releases) and put them on PATH (or `cargo install --path` from the source repo). See the cortex README for details.

## License

Each plugin carries its own license. The marketplace catalog itself (this
repo's `marketplace.json`) is published under MIT — see [LICENSE](LICENSE).
