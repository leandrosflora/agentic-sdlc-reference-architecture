#!/usr/bin/env python3
"""Executable, dependency-free golden path for the reference architecture.

It exercises onboarding, canonical intake, a multi-repository Change Set,
agent stages, parallel verification, human approval, release and observation.
All adapters and side effects are deterministic local fakes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative_path: str):
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def evidence(step: str, payload: dict) -> dict:
    encoded = json.dumps(payload, sort_keys=True).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    return {"step": step, "uri": f"memory://golden-path/{step}.json", "sha256": digest}


def run() -> dict:
    project = load("examples/project-manifest.instance.json")
    intake = load("examples/canonical-integration.instance.json")
    change_set = load("examples/change-set.instance.json")

    assert project["metadata"]["name"] == intake["correlation"]["project_id"]
    assert intake["correlation"]["change_id"] == change_set["change_id"]

    repository_ids = [item["id"] for item in change_set["repositories"]]
    assert set(repository_ids) == set(change_set["deployment_order"])
    completed: set[str] = set()
    for repository in change_set["repositories"]:
        assert set(repository["depends_on"]).issubset(completed)
        completed.add(repository["id"])
    assert change_set["rollback"]["order"] == list(reversed(change_set["deployment_order"]))

    steps = [
        ("intake", "service", {"work_item": intake["subject"]["external_id"]}),
        ("refine", "product", {"criteria": ["change is traceable", "same digests are promoted"]}),
        ("design", "architecture", {"change_set_id": change_set["change_set_id"]}),
        ("implement", "developer", {"repositories": repository_ids}),
        ("test", "test", {"status": "passed", "commit_set": repository_ids}),
        ("secure", "security", {"status": "passed", "findings": 0}),
        ("review", "reviewer", {"status": "approved"}),
        ("approve", "human", {"status": "approved", "digest_bound": True}),
        ("release", "release", {"order": change_set["deployment_order"]}),
        ("observe", "release", {"slo": "healthy", "status": "completed"}),
    ]

    events = []
    evidence_bundle = []
    for index, (step, actor, payload) in enumerate(steps, start=1):
        item = evidence(step, payload)
        evidence_bundle.append(item)
        events.append({
            "sequence": index,
            "step": step,
            "actor": actor,
            "status": "completed",
            "evidence_sha256": item["sha256"],
        })

    return {
        "workflow": "golden-path-v1",
        "project_id": project["metadata"]["name"],
        "change_id": change_set["change_id"],
        "change_set_id": change_set["change_set_id"],
        "risk": change_set["risk"],
        "status": "completed",
        "repository_count": len(repository_ids),
        "events": events,
        "evidence_bundle": evidence_bundle,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))


if __name__ == "__main__":
    main()
