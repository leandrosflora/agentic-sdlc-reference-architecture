#!/usr/bin/env python3
"""Dependency-free structural checks for the reference architecture."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AGENTS = {
    "product", "architecture", "developer", "test", "security", "reviewer", "release", "incident"
}


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(relative_path: str) -> None:
    schema = load_json(relative_path)
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]).issubset(schema["properties"])


def validate_workflow() -> None:
    workflow = load_json("examples/workflow.json")
    assert set(workflow["agents"]) == EXPECTED_AGENTS
    steps = workflow["steps"]
    step_ids = [step["id"] for step in steps]
    assert len(step_ids) == len(set(step_ids)), "step ids must be unique"

    seen: set[str] = set()
    for step in steps:
        assert step["agent"] in EXPECTED_AGENTS | {"human"}
        assert set(step["requires"]).issubset(seen), f"invalid dependency for {step['id']}"
        assert step["produces"], f"{step['id']} must produce evidence"
        seen.add(step["id"])

    by_id = {step["id"]: step for step in steps}
    assert by_id["implement"]["agent"] != by_id["review"]["agent"]
    assert by_id["approve"]["agent"] == "human"
    assert "approve" in by_id["release"]["requires"]
    assert workflow["controls"]["default_deny"] is True
    assert workflow["controls"]["human_approval_for_production"] is True


def validate_docs() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for agent in EXPECTED_AGENTS:
        assert agent.title() in readme or agent.capitalize() in readme
    assert "enterprise-ai-platform-reference-architecture" in readme
    assert (ROOT / "policies/agent_authorization.rego").is_file()


if __name__ == "__main__":
    for path in ("contracts/change-envelope.schema.json", "contracts/agent-event.schema.json"):
        validate_schema(path)
    validate_workflow()
    validate_docs()
    print("OK: schemas, workflow, segregation of duties, controls, and documentation")
