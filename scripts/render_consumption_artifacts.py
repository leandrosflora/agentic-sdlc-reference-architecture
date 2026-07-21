#!/usr/bin/env python3
"""Render dashboard JSON and PR summary from the executable golden path."""

from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COSTS = {
    "intake": 0.001, "refine": 0.012, "design": 0.018,
    "implement": 0.025, "test": 0.008, "secure": 0.007,
    "review": 0.009, "approve": 0.0, "release": 0.004, "observe": 0.002,
}


def golden_path() -> dict:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_golden_path.py"), "--compact"],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def dashboard(source: dict) -> dict:
    change_set = json.loads((ROOT / "examples/change-set.instance.json").read_text(encoding="utf-8"))
    events = []
    for event in source["events"]:
        events.append({**event, "cost_usd": COSTS[event["step"]]})
    return {
        **{key: source[key] for key in ("workflow", "project_id", "change_id", "change_set_id", "risk", "status")},
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "cost": {"total_usd": round(sum(COSTS.values()), 6)},
        "repositories": [
            {"component": item["component"], "repository": item["repository"], "status": "healthy"}
            for item in change_set["repositories"]
        ],
        "events": events,
        "evidence_bundle": source["evidence_bundle"],
    }


def markdown(data: dict) -> str:
    completed = sum(item["status"] == "completed" for item in data["events"])
    lines = [
        "<!-- agentic-sdlc-summary -->",
        "## Agentic SDLC · Change summary",
        "",
        f"| Change | Risk | Status | Progress | Cost | Evidence |",
        "|---|---|---|---:|---:|---:|",
        f"| {data['change_id']} | {data['risk']} | **{data['status']}** | {completed}/{len(data['events'])} | US$ {data['cost']['total_usd']:.3f} | {len(data['evidence_bundle'])} |",
        "",
        "| Step | Actor | Result | Cost |",
        "|---|---|---|---:|",
    ]
    lines.extend(
        f"| {item['step']} | {item['actor']} | {item['status']} | US$ {item['cost_usd']:.3f} |"
        for item in data["events"]
    )
    lines += ["", f"Change Set: **{data['change_set_id']}** · Repositories: **{len(data['repositories'])}**"]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dashboard")
    parser.add_argument("--summary")
    args = parser.parse_args()
    data = dashboard(golden_path())
    if args.dashboard:
        Path(args.dashboard).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if args.summary:
        Path(args.summary).write_text(markdown(data), encoding="utf-8")
    if not args.dashboard and not args.summary:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
