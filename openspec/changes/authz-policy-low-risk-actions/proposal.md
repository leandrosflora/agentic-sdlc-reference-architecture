## Why

Eight `sdlc-<role>-agent` repos already declare action surfaces (e.g. `requirements.update`, `architecture.propose`, `architecture.comment`) derived from the capability matrix in `docs/governance.md`, but `policies/agent_authorization.rego` only has rules for 4 of the ~19 declared actions. Every other action falls through `default allow := false`, which is indistinguishable from a deliberate business-rule denial. This blocks the lowest-risk (R0/R1) agents — product and architecture — from ever getting a real `allow` from the canonical policy, and leaves reviewer/security/incident unable to exercise their "comentário" capability at all.

## What Changes

- Add OPA rules for the five lowest-risk actions still on default-deny:
  - `requirements.update` — role `product`, own project only (Definition gate).
  - `requirements.comment` — roles `reviewer` and `incident`, own project only.
  - `architecture.update` — role `architecture`, own project only (Design gate).
  - `architecture.propose` — role `developer`, own project only (lower privilege than `architecture.update`: proposal, not direct write).
  - `architecture.comment` — roles `reviewer` and `security`, own project only.
- Add corresponding allow/deny cases to `policies/agent_authorization_test.rego` for each new rule (per this repo's own proposal rule: new rego rules require test cases).
- Add validated example input JSON documents under `examples/` for at least one allow and one deny case per new action, consistent with the existing `examples/agent-events.*.json` pattern and validated via `scripts/validate.py`.

Higher-risk actions already flagged in the prior review (`tests.write`, `security.fix`, `review.report`, `artifact.publish`, `deployment.nonprod`, `hotfix.propose`) remain out of scope — deliberately deferred to a later change once Build/Security/Release gate evidence fields are designed.

## Capabilities

### New Capabilities

- `agent-authorization-policy`: the OPA/Rego rules that decide, per `(action, agent_role, project scope, change risk)`, whether an agent's request is allowed. This is the first formal spec for `policies/agent_authorization.rego`; the spec captures both the 4 rules that exist today and the 5 being added by this change, so future changes to this file have a spec to diff against.

### Modified Capabilities

(none — no existing spec file for this policy yet)

## Impact

- `policies/agent_authorization.rego` — 5 new `allow if { ... }` blocks.
- `policies/agent_authorization_test.rego` — new test cases (allow + deny per rule, including cross-role and cross-project denial).
- `examples/` — new validated input documents for the 5 actions.
- Out of this repo's scope but tracked as a follow-up: `sdlc-security-agent`'s `ACTIONS` dict is missing `architecture.comment` even though `docs/governance.md` grants Security that capability (Reviewer already has it correctly). That's a one-line fix in a sibling repo, done separately from this proposal since it's outside `agentic-sdlc-reference-architecture`.
