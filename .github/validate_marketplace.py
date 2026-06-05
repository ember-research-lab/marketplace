#!/usr/bin/env python3
"""Validate .claude-plugin/marketplace.json and in-repo plugin layout.

Stdlib only. Checks:
  1. marketplace.json parses and has name/owner/plugins.
  2. Every plugin entry has name, source, description.
  3. Relative-path sources exist in-repo and contain at least one of
     skills/ (each skill dir holding a SKILL.md with name+description
     frontmatter) or agents/ (each agent a .md file).
  4. URL sources are https git URLs.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / ".claude-plugin" / "marketplace.json"

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def check_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        err(f"{skill_dir}: missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        err(f"{skill_md}: missing YAML frontmatter block")
        return
    front = m.group(1)
    for field in ("name:", "description:"):
        if field not in front:
            err(f"{skill_md}: frontmatter missing `{field[:-1]}`")


def check_local_plugin(name: str, rel: str) -> None:
    pdir = ROOT / rel
    if not pdir.is_dir():
        err(f"plugin {name!r}: source path {rel} does not exist")
        return
    skills = pdir / "skills"
    agents = pdir / "agents"
    if not skills.is_dir() and not agents.is_dir():
        err(f"plugin {name!r}: {rel} has neither skills/ nor agents/")
    if skills.is_dir():
        for sd in sorted(p for p in skills.iterdir() if p.is_dir()):
            check_skill(sd)
    if agents.is_dir():
        mds = list(agents.glob("*.md"))
        if not mds:
            err(f"plugin {name!r}: agents/ contains no .md files")


def main() -> int:
    try:
        cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL: cannot load {CATALOG}: {e}")
        return 1

    for field in ("name", "owner", "plugins"):
        if field not in cat:
            err(f"marketplace.json: missing top-level `{field}`")

    for i, plugin in enumerate(cat.get("plugins", [])):
        label = plugin.get("name", f"<index {i}>")
        for field in ("name", "source", "description"):
            if field not in plugin:
                err(f"plugin {label!r}: missing `{field}`")
        src = plugin.get("source")
        if isinstance(src, str):
            if not src.startswith("./"):
                err(f"plugin {label!r}: string source must be a ./relative path")
            else:
                check_local_plugin(label, src)
        elif isinstance(src, dict):
            url = src.get("url", "")
            if src.get("source") == "url" and not url.startswith("https://"):
                err(f"plugin {label!r}: url source must be https ({url!r})")
        else:
            err(f"plugin {label!r}: source must be a string path or object")

    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
        return 1
    n = len(cat.get("plugins", []))
    print(f"OK: marketplace.json valid, {n} plugin(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
