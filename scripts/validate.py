#!/usr/bin/env python3
"""Dependency-free structural checks for the reference architecture."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AGENTS = {
    "product", "architecture", "developer", "test", "security", "reviewer", "release", "incident"
}


def load_json(relative_path: str):
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(relative_path: str) -> None:
    schema = load_json(relative_path)
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]).issubset(schema["properties"])


def validate_instance(instance, schema: dict, path: str = "$") -> None:
    """Minimal, dependency-free JSON Schema check covering the subset this
    repo's contracts actually use: object/array/string/integer/number,
    required, additionalProperties, enum, const, pattern, minLength, minItems.
    """
    schema_type = schema.get("type")

    if "const" in schema:
        assert instance == schema["const"], f"{path}: expected const {schema['const']!r}, got {instance!r}"

    if "enum" in schema:
        assert instance in schema["enum"], f"{path}: {instance!r} not in {schema['enum']}"

    if schema_type == "object":
        assert isinstance(instance, dict), f"{path}: expected object, got {type(instance).__name__}"
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            assert key in instance, f"{path}: missing required property {key!r}"
        if schema.get("additionalProperties") is False:
            unknown = set(instance) - set(properties)
            assert not unknown, f"{path}: unexpected properties {unknown}"
        for key, value in instance.items():
            if key in properties:
                validate_instance(value, properties[key], f"{path}.{key}")

    elif schema_type == "array":
        assert isinstance(instance, list), f"{path}: expected array, got {type(instance).__name__}"
        if "minItems" in schema:
            assert len(instance) >= schema["minItems"], f"{path}: expected at least {schema['minItems']} items"
        if "items" in schema:
            for index, item in enumerate(instance):
                validate_instance(item, schema["items"], f"{path}[{index}]")

    elif schema_type == "string":
        assert isinstance(instance, str), f"{path}: expected string, got {type(instance).__name__}"
        if "minLength" in schema:
            assert len(instance) >= schema["minLength"], f"{path}: shorter than minLength"
        if "pattern" in schema:
            assert re.match(schema["pattern"], instance), f"{path}: {instance!r} does not match {schema['pattern']}"

    elif schema_type == "integer":
        assert isinstance(instance, int) and not isinstance(instance, bool), f"{path}: expected integer"
        if "minimum" in schema:
            assert instance >= schema["minimum"], f"{path}: below minimum"

    elif schema_type == "number":
        assert isinstance(instance, (int, float)) and not isinstance(instance, bool), f"{path}: expected number"
        if "minimum" in schema:
            assert instance >= schema["minimum"], f"{path}: below minimum"


def validate_examples_against_contracts() -> None:
    change_envelope_schema = load_json("contracts/change-envelope.schema.json")
    agent_event_schema = load_json("contracts/agent-event.schema.json")

    validate_instance(load_json("examples/change-envelope.instance.json"), change_envelope_schema)

    for relative_path in (
        "examples/agent-events.rejected-rework.json",
        "examples/agent-events.incident-rollback.json",
    ):
        events = load_json(relative_path)
        assert isinstance(events, list) and events, f"{relative_path}: expected a non-empty array of events"
        for index, event in enumerate(events):
            validate_instance(event, agent_event_schema, f"{relative_path}[{index}]")


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
    assert (ROOT / "policies/agent_authorization_test.rego").is_file()


if __name__ == "__main__":
    for path in ("contracts/change-envelope.schema.json", "contracts/agent-event.schema.json"):
        validate_schema(path)
    validate_workflow()
    validate_docs()
    validate_examples_against_contracts()
    print("OK: schemas, workflow, segregation of duties, controls, examples, and documentation")
