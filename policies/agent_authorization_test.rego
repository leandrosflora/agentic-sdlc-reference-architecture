package agentic_sdlc.authorization

import rego.v1

# ---- project.read ----

test_project_read_allowed_for_matching_role_and_project if {
	allow with input as {
		"action": "project.read",
		"identity": {"project_id": "proj-1", "agent_role": "architecture"},
		"resource": {"project_id": "proj-1"},
	}
}

test_project_read_denied_cross_project if {
	not allow with input as {
		"action": "project.read",
		"identity": {"project_id": "proj-1", "agent_role": "architecture"},
		"resource": {"project_id": "proj-2"},
	}
}

test_project_read_denied_for_unknown_role if {
	not allow with input as {
		"action": "project.read",
		"identity": {"project_id": "proj-1", "agent_role": "unknown"},
		"resource": {"project_id": "proj-1"},
	}
}

# ---- repository.write ----

repo_write_base := {
	"action": "repository.write",
	"identity": {"project_id": "proj-1", "agent_role": "developer"},
	"resource": {"project_id": "proj-1", "protected_branch": false},
	"change": {"risk": "R2", "scope_approved": true},
}

test_repository_write_allowed_for_developer_low_risk_unprotected if {
	allow with input as repo_write_base
}

test_repository_write_denied_on_protected_branch if {
	denied := object.union(repo_write_base, {"resource": {"project_id": "proj-1", "protected_branch": true}})
	not allow with input as denied
}

test_repository_write_denied_for_high_risk if {
	denied := object.union(repo_write_base, {"change": {"risk": "R3", "scope_approved": true}})
	not allow with input as denied
}

test_repository_write_denied_without_scope_approval if {
	denied := object.union(repo_write_base, {"change": {"risk": "R2", "scope_approved": false}})
	not allow with input as denied
}

test_repository_write_denied_for_non_developer_role if {
	denied := object.union(repo_write_base, {"identity": {"project_id": "proj-1", "agent_role": "reviewer"}})
	not allow with input as denied
}

# ---- production.deploy ----

deploy_base := {
	"action": "production.deploy",
	"identity": {"agent_role": "release"},
	"change": {
		"artifact_digest": "sha256:abc",
		"author_id": "dev-1",
		"rollback_verified": true,
		"security_gate_passed": true,
		"test_gate_passed": true,
		"risk": "R3",
	},
	"approval": {
		"artifact_digest": "sha256:abc",
		"valid": true,
		"human": true,
		"actor_id": "approver-1",
	},
}

test_production_deploy_allowed_with_valid_independent_human_approval if {
	allow with input as deploy_base
}

test_production_deploy_denied_when_approval_not_human if {
	denied := object.union(deploy_base, {"approval": object.union(deploy_base.approval, {"human": false})})
	not allow with input as denied
}

test_production_deploy_denied_when_approver_is_author if {
	denied := object.union(deploy_base, {"approval": object.union(deploy_base.approval, {"actor_id": "dev-1"})})
	not allow with input as denied
}

test_production_deploy_denied_on_digest_mismatch if {
	denied := object.union(deploy_base, {"approval": object.union(deploy_base.approval, {"artifact_digest": "sha256:other"})})
	not allow with input as denied
}

test_production_deploy_denied_for_r4_risk if {
	denied := object.union(deploy_base, {"change": object.union(deploy_base.change, {"risk": "R4"})})
	not allow with input as denied
}

test_production_deploy_denied_without_rollback_verified if {
	denied := object.union(deploy_base, {"change": object.union(deploy_base.change, {"rollback_verified": false})})
	not allow with input as denied
}

test_production_deploy_denied_without_security_gate if {
	denied := object.union(deploy_base, {"change": object.union(deploy_base.change, {"security_gate_passed": false})})
	not allow with input as denied
}

# ---- observability.read ----

test_observability_read_allowed_for_incident_matching_project if {
	allow with input as {
		"action": "observability.read",
		"identity": {"project_id": "proj-1", "agent_role": "incident"},
		"resource": {"project_id": "proj-1"},
	}
}

test_observability_read_denied_cross_project if {
	not allow with input as {
		"action": "observability.read",
		"identity": {"project_id": "proj-1", "agent_role": "incident"},
		"resource": {"project_id": "proj-2"},
	}
}

test_incident_cannot_write_repository if {
	not allow with input as {
		"action": "repository.write",
		"identity": {"project_id": "proj-1", "agent_role": "incident"},
		"resource": {"project_id": "proj-1", "protected_branch": false},
		"change": {"risk": "R1", "scope_approved": true},
	}
}

# ---- requirements.update ----

requirements_update_base := {
	"action": "requirements.update",
	"identity": {"project_id": "proj-1", "agent_role": "product"},
	"resource": {"project_id": "proj-1"},
	"change": {"risk": "R1"},
}

test_requirements_update_allowed_for_product_low_risk if {
	allow with input as requirements_update_base
}

test_requirements_update_denied_for_non_product_role if {
	denied := object.union(requirements_update_base, {"identity": {"project_id": "proj-1", "agent_role": "developer"}})
	not allow with input as denied
}

test_requirements_update_denied_cross_project if {
	denied := object.union(requirements_update_base, {"resource": {"project_id": "proj-2"}})
	not allow with input as denied
}

test_requirements_update_denied_above_r1_risk if {
	denied := object.union(requirements_update_base, {"change": {"risk": "R2"}})
	not allow with input as denied
}

# ---- requirements.comment ----

test_requirements_comment_allowed_for_reviewer if {
	allow with input as {
		"action": "requirements.comment",
		"identity": {"project_id": "proj-1", "agent_role": "reviewer"},
		"resource": {"project_id": "proj-1"},
	}
}

test_requirements_comment_allowed_for_incident if {
	allow with input as {
		"action": "requirements.comment",
		"identity": {"project_id": "proj-1", "agent_role": "incident"},
		"resource": {"project_id": "proj-1"},
	}
}

test_requirements_comment_denied_for_non_authorized_role if {
	not allow with input as {
		"action": "requirements.comment",
		"identity": {"project_id": "proj-1", "agent_role": "developer"},
		"resource": {"project_id": "proj-1"},
	}
}

test_requirements_comment_denied_cross_project if {
	not allow with input as {
		"action": "requirements.comment",
		"identity": {"project_id": "proj-1", "agent_role": "reviewer"},
		"resource": {"project_id": "proj-2"},
	}
}

# ---- architecture.update ----

architecture_update_base := {
	"action": "architecture.update",
	"identity": {"project_id": "proj-1", "agent_role": "architecture"},
	"resource": {"project_id": "proj-1"},
	"change": {"risk": "R0"},
}

test_architecture_update_allowed_for_architecture_low_risk if {
	allow with input as architecture_update_base
}

test_architecture_update_denied_for_developer if {
	denied := object.union(architecture_update_base, {"identity": {"project_id": "proj-1", "agent_role": "developer"}})
	not allow with input as denied
}

test_architecture_update_denied_cross_project if {
	denied := object.union(architecture_update_base, {"resource": {"project_id": "proj-2"}})
	not allow with input as denied
}

test_architecture_update_denied_above_r1_risk if {
	denied := object.union(architecture_update_base, {"change": {"risk": "R2"}})
	not allow with input as denied
}

# ---- architecture.propose ----

architecture_propose_base := {
	"action": "architecture.propose",
	"identity": {"project_id": "proj-1", "agent_role": "developer"},
	"resource": {"project_id": "proj-1"},
	"change": {"risk": "R1"},
}

test_architecture_propose_allowed_for_developer_low_risk if {
	allow with input as architecture_propose_base
}

test_architecture_propose_denied_for_non_developer_role if {
	denied := object.union(architecture_propose_base, {"identity": {"project_id": "proj-1", "agent_role": "product"}})
	not allow with input as denied
}

test_architecture_propose_denied_for_architecture_role if {
	denied := object.union(architecture_propose_base, {"identity": {"project_id": "proj-1", "agent_role": "architecture"}})
	not allow with input as denied
}

test_architecture_propose_denied_cross_project if {
	denied := object.union(architecture_propose_base, {"resource": {"project_id": "proj-2"}})
	not allow with input as denied
}

test_architecture_propose_denied_above_r1_risk if {
	denied := object.union(architecture_propose_base, {"change": {"risk": "R2"}})
	not allow with input as denied
}

# ---- architecture.comment ----

test_architecture_comment_allowed_for_reviewer if {
	allow with input as {
		"action": "architecture.comment",
		"identity": {"project_id": "proj-1", "agent_role": "reviewer"},
		"resource": {"project_id": "proj-1"},
	}
}

test_architecture_comment_allowed_for_security if {
	allow with input as {
		"action": "architecture.comment",
		"identity": {"project_id": "proj-1", "agent_role": "security"},
		"resource": {"project_id": "proj-1"},
	}
}

test_architecture_comment_denied_for_non_authorized_role if {
	not allow with input as {
		"action": "architecture.comment",
		"identity": {"project_id": "proj-1", "agent_role": "incident"},
		"resource": {"project_id": "proj-1"},
	}
}

test_architecture_comment_denied_cross_project if {
	not allow with input as {
		"action": "architecture.comment",
		"identity": {"project_id": "proj-1", "agent_role": "security"},
		"resource": {"project_id": "proj-2"},
	}
}
