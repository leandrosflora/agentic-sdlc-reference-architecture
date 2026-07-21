## Context

`policies/agent_authorization.rego` is the single source of truth for authorization; the 8 `sdlc-<role>-agent` repos call it via `opa eval` and never re-implement policy logic locally (see their `authorization.py`). Today it only has rules for `project.read`, `repository.write`, `production.deploy`, `observability.read`. The remaining actions declared in the agents' `ACTIONS` dicts fall through `default allow := false`. This change adds the 5 lowest-risk (R0/R1, per `docs/governance.md`'s risk table) actions still uncovered: `requirements.update`, `requirements.comment`, `architecture.update`, `architecture.propose`, `architecture.comment`.

## Goals / Non-Goals

**Goals:**
- Give product, architecture, reviewer, incident, and security agents a real (non-default-deny) authorization path for their Definition/Design-gate and comment capabilities.
- Keep every new rule symmetric in shape with the existing ones: scoped by `input.identity.project_id == input.resource.project_id`, guarded by `input.identity.agent_role`.
- Keep the rego file the only place these rules are defined; no duplication into the agent repos.

**Non-Goals:**
- Actions tied to Build/Security/Release/Verification gates (`tests.write`, `security.fix`, `review.report`, `artifact.publish`, `deployment.nonprod`, `hotfix.propose`) — these need evidence-bundle fields (test results, scan findings, digests) that don't exist in the input contract yet and are deferred to a follow-up change.
- Changing `contracts/change-envelope.schema.json` — none of the 5 new rules need a field that isn't already covered by `identity`/`resource`/`change.risk`.
- Fixing `sdlc-security-agent`'s missing `architecture.comment` entry in its `ACTIONS` dict — that's a one-line Python change in a sibling repo, outside this repo's `allowedEditRoots`, tracked as a follow-up in the proposal's Impact section.

## Decisions

1. **Comment actions get no `change.risk` guard.** `requirements.comment` and `architecture.comment` are read+annotate, not writes — same class as `project.read`, which also has no risk guard today. Only scope (`project_id` match) and role membership matter. Alternative considered: require `change.risk in {R0, R1}` for symmetry with write actions — rejected because a comment on a high-risk change is exactly when independent comment capability (security/reviewer/incident) matters most; gating it by risk would block the capability precisely when it's needed.

2. **`requirements.update` and `architecture.update` get a `change.risk in {"R0", "R1"}` guard**, mirroring the shape of `repository.write`'s risk guard (`{R1, R2}`) but one tier lower, matching governance.md's risk table (R0 = query/summary, R1 = doc or isolated test — both fit "editing a requirement" or "editing architecture docs/contracts" better than R2+, which is code-level). Alternative considered: no risk guard at all (like `project.read`) — rejected because these are writes to Definition/Design-gate artifacts, and the existing `repository.write` precedent is that writes always carry a risk guard.

3. **`architecture.propose` (developer) is a separate rule from `architecture.update` (architecture role), not a shared rule with an `in {"architecture","developer"}` role check.** Governance.md's capability matrix treats "proposta" (developer) as a strictly lower privilege than "✓" (architecture) for the same row ("Alterar arquitetura/contratos") — a shared rule would make the two roles indistinguishable in the policy and any future divergence (e.g. developer proposals requiring an extra approval field) would force a rule split anyway. Keeping them separate now costs a few duplicated lines but preserves the matrix's distinction directly in the rego, matching how `repository.write` (developer-only) and `production.deploy` (release-only) are already single-role rules rather than generic multi-role ones.

4. **No new fields invented.** All 5 rules reuse `identity.project_id`, `identity.agent_role`, `resource.project_id`, `change.risk` — already used by existing rules and already present in `contracts/change-envelope.schema.json`'s `risk` enum and the agents' example inputs. This avoids a contract change (which per `openspec/config.yaml`'s proposal rules would require an ADR) for a policy change that doesn't need one.

## Risks / Trade-offs

- [Comment actions unguarded by risk could be seen as inconsistent with write actions] → Mitigated by decision #1's rationale being explicit in this doc and in code comments on the rule itself, so a future reader doesn't "fix" it into a regression.
- [Five near-identical rule blocks read as repetitive] → Rego does not have a natural place for parameterized rule templates without hurting readability of `opa eval` output tracing; the existing file already accepts this repetition (`project.read`, `repository.write`, `production.deploy` are each independent blocks), so this change stays consistent with the file's existing style rather than introducing a new abstraction unilaterally.

## Migration Plan

Pure addition — no existing `allow` behavior changes, so no rollback beyond reverting the commit. Sequence: rego rules → `opa test policies/` passes → example inputs validated via `scripts/validate.py` → CI (`validate.yml`) green.
