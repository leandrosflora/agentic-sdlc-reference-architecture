#!/usr/bin/env python3
"""Keeps the scaffolding shared by the 8 agent repos in sync with one canonical copy.

Each sdlc-<role>-agent repo intentionally stays self-contained (no shared
package at runtime), so the common modules are vendored copies. This script
makes that duplication safe: templates/agent/ holds the single canonical
source, and sibling checkouts are compared against it (--check, the default)
or rewritten from it (--apply). The __ROLE__ placeholder is replaced with the
agent role in file contents.

Agents that are not checked out as siblings are skipped, so the check can run
anywhere without requiring the full workspace.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates" / "agent"
ROLES = ("product", "architecture", "developer", "test", "security", "reviewer", "release", "incident")
# template path (under templates/agent/) -> destination inside the agent repo,
# where {package} is sdlc_<role>_agent
TEMPLATES = {
    "authorization.py": "{package}/authorization.py",
    "tests/test_authorization.py": "tests/test_authorization.py",
    "tests/test_integration_opa.py": "tests/test_integration_opa.py",
}


def render(template: Path, role: str) -> str:
    return template.read_text(encoding="utf-8").replace("__ROLE__", role)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", action="store_true",
                        help="rewrite drifted files from the templates instead of only reporting")
    args = parser.parse_args()

    drifted: list[str] = []
    skipped: list[str] = []
    checked = 0
    for role in ROLES:
        repo = ROOT.parent / f"sdlc-{role}-agent"
        if not repo.is_dir():
            skipped.append(repo.name)
            continue
        package = f"sdlc_{role}_agent"
        for template_name, destination_pattern in TEMPLATES.items():
            expected = render(TEMPLATE_DIR / template_name, role)
            destination = repo / destination_pattern.format(package=package)
            actual = destination.read_text(encoding="utf-8") if destination.is_file() else None
            checked += 1
            if actual == expected:
                continue
            drifted.append(str(destination.relative_to(ROOT.parent)))
            if args.apply:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(expected, encoding="utf-8")

    if skipped:
        print(f"skipped (not checked out): {', '.join(skipped)}")
    if drifted:
        verb = "rewritten from template" if args.apply else "drifted from template"
        print(f"{verb}:")
        for path in drifted:
            print(f"  {path}")
        return 0 if args.apply else 1
    print(f"OK: {checked} files match the canonical agent scaffolding")
    return 0


if __name__ == "__main__":
    sys.exit(main())
