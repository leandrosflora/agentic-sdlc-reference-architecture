package agentic_sdlc.authorization

import rego.v1

default allow := false

# Read-only access still requires matching project scope.
allow if {
  input.action == "project.read"
  input.identity.project_id == input.resource.project_id
  input.identity.agent_role in {"product", "architecture", "developer", "test", "security", "reviewer", "release", "incident"}
}

# Only the developer can modify application code, and never on a protected branch.
allow if {
  input.action == "repository.write"
  input.identity.agent_role == "developer"
  input.identity.project_id == input.resource.project_id
  not input.resource.protected_branch
  input.change.risk in {"R1", "R2"}
  input.change.scope_approved
}

# Production deployment is digest-bound and requires independent human approval.
allow if {
  input.action == "production.deploy"
  input.identity.agent_role == "release"
  input.change.artifact_digest == input.approval.artifact_digest
  input.approval.valid
  input.approval.human
  input.approval.actor_id != input.change.author_id
  input.change.rollback_verified
  input.change.security_gate_passed
  input.change.test_gate_passed
  input.change.risk in {"R1", "R2", "R3"}
}

# Incident automation is read-only; production mutation follows a separate
# human break-glass process and is intentionally absent from this policy.
allow if {
  input.action == "observability.read"
  input.identity.agent_role == "incident"
  input.identity.project_id == input.resource.project_id
}

# Only product can update requirements and acceptance criteria (Definition gate).
allow if {
  input.action == "requirements.update"
  input.identity.agent_role == "product"
  input.identity.project_id == input.resource.project_id
  input.change.risk in {"R0", "R1"}
}

# Reviewer and incident may comment on requirements; comment capability is not
# risk-gated so it stays available even on higher-risk changes.
allow if {
  input.action == "requirements.comment"
  input.identity.agent_role in {"reviewer", "incident"}
  input.identity.project_id == input.resource.project_id
}

# Only architecture can directly update architecture and contracts (Design gate).
allow if {
  input.action == "architecture.update"
  input.identity.agent_role == "architecture"
  input.identity.project_id == input.resource.project_id
  input.change.risk in {"R0", "R1"}
}

# Developer may propose an architecture/contract change for review -- a lower
# privilege than architecture.update, kept as its own rule (developer only,
# never architecture) so the two capabilities never collapse into one.
allow if {
  input.action == "architecture.propose"
  input.identity.agent_role == "developer"
  input.identity.project_id == input.resource.project_id
  input.change.risk in {"R0", "R1"}
}

# Reviewer and security may comment on architecture/contract changes; not
# risk-gated for the same reason as requirements.comment.
allow if {
  input.action == "architecture.comment"
  input.identity.agent_role in {"reviewer", "security"}
  input.identity.project_id == input.resource.project_id
}
