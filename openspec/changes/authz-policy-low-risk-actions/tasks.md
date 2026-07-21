## 1. Policy rules

- [x] 1.1 Add `requirements.update` rule (role `product`, project scope, `change.risk in {"R0","R1"}`)
- [x] 1.2 Add `requirements.comment` rule (roles `reviewer`/`incident`, project scope, no risk guard)
- [x] 1.3 Add `architecture.update` rule (role `architecture`, project scope, `change.risk in {"R0","R1"}`)
- [x] 1.4 Add `architecture.propose` rule (role `developer`, project scope, `change.risk in {"R0","R1"}`)
- [x] 1.5 Add `architecture.comment` rule (roles `reviewer`/`security`, project scope, no risk guard)

## 2. Policy tests

- [x] 2.1 Add allow + deny (wrong role, cross-project, risk-out-of-range) test cases for `requirements.update`
- [x] 2.2 Add allow + deny (wrong role, cross-project) test cases for `requirements.comment`
- [x] 2.3 Add allow + deny (wrong role, cross-project, risk-out-of-range) test cases for `architecture.update`
- [x] 2.4 Add allow + deny (wrong role, cross-project, risk-out-of-range) test cases for `architecture.propose`, including a case proving `architecture` role does NOT get this action
- [x] 2.5 Add allow + deny (wrong role, cross-project) test cases for `architecture.comment`
- [x] 2.6 Run `opa test policies/ -v` and confirm all tests pass

## 3. Regression check for this repo's own examples

- [x] 3.1 Run `python3 scripts/validate.py` and confirm the existing `examples/` (workflow, change-envelope, agent-events, docs) still validate unaffected by the policy change

Note: corrected during apply — `agentic-sdlc-reference-architecture/examples/` does not hold per-action OPA input fixtures (`scripts/validate.py` only checks `workflow.json`, `change-envelope.instance.json`, `agent-events.*.json`). Per-action `input.<action>.json` fixtures live in each sibling `sdlc-<role>-agent/examples/` repo, same as the security-agent fix below. Moved to section 4.

## 4. Follow-up in sibling agent repos (outside this repo's edit root)

- [x] 4.1 Add `architecture.comment` to `sdlc-security-agent`'s `ACTIONS` dict (governance.md grants Security this capability; Reviewer already has it)
- [x] 4.2 Add `input.requirements_update.allow.json` / `.deny_cross_project.json` to `sdlc-product-agent/examples/`
- [x] 4.3 Add `input.requirements_comment.allow.json` / `.deny_cross_project.json` to `sdlc-reviewer-agent/examples/`
- [x] 4.4 Add `input.architecture_update.allow.json` / `.deny_cross_project.json` to `sdlc-architecture-agent/examples/`
- [x] 4.5 Add `input.architecture_propose.allow.json` / `.deny_cross_project.json` to `sdlc-developer-agent/examples/`
- [x] 4.6 Add `input.architecture_comment.allow.json` / `.deny_cross_project.json` to `sdlc-security-agent/examples/`

Also done during apply (not originally a numbered task, but required for accuracy once the rules landed): updated the "Autorização (OPA)" section of the README.md in sdlc-product-agent, sdlc-architecture-agent, sdlc-developer-agent, sdlc-reviewer-agent, sdlc-incident-agent, and sdlc-security-agent — each previously stated its new action(s) were "ainda não codificadas como regra própria," which became false once this change's rules landed.
