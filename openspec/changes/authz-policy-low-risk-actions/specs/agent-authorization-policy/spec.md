## ADDED Requirements

### Requirement: Product agent may update requirements within its own project
The policy SHALL allow `requirements.update` when `input.identity.agent_role` is `product`, `input.identity.project_id` equals `input.resource.project_id`, and `input.change.risk` is `R0` or `R1`. It SHALL deny the action for any other role, any cross-project request, or any `change.risk` outside `{R0, R1}`.

#### Scenario: Product agent updates a low-risk requirement in its own project
- **WHEN** a `product` agent submits `requirements.update` with matching `project_id` and `change.risk` = `R1`
- **THEN** the policy allows the action

#### Scenario: Non-product role is denied
- **WHEN** a `developer` agent submits `requirements.update` with matching `project_id` and `change.risk` = `R1`
- **THEN** the policy denies the action

#### Scenario: Cross-project request is denied
- **WHEN** a `product` agent submits `requirements.update` where `identity.project_id` differs from `resource.project_id`
- **THEN** the policy denies the action

#### Scenario: Risk above R1 is denied
- **WHEN** a `product` agent submits `requirements.update` with matching `project_id` and `change.risk` = `R2`
- **THEN** the policy denies the action

### Requirement: Reviewer and incident agents may comment on requirements within their own project
The policy SHALL allow `requirements.comment` when `input.identity.agent_role` is `reviewer` or `incident`, and `input.identity.project_id` equals `input.resource.project_id`. No `change.risk` guard applies — comment capability must remain available regardless of the change's risk level. It SHALL deny the action for any other role or any cross-project request.

#### Scenario: Reviewer comments on a requirement in its own project
- **WHEN** a `reviewer` agent submits `requirements.comment` with matching `project_id`
- **THEN** the policy allows the action

#### Scenario: Incident agent comments on a requirement in its own project
- **WHEN** an `incident` agent submits `requirements.comment` with matching `project_id`
- **THEN** the policy allows the action

#### Scenario: Non-authorized role is denied
- **WHEN** a `developer` agent submits `requirements.comment` with matching `project_id`
- **THEN** the policy denies the action

#### Scenario: Cross-project request is denied
- **WHEN** a `reviewer` agent submits `requirements.comment` where `identity.project_id` differs from `resource.project_id`
- **THEN** the policy denies the action

### Requirement: Architecture agent may update architecture and contracts within its own project
The policy SHALL allow `architecture.update` when `input.identity.agent_role` is `architecture`, `input.identity.project_id` equals `input.resource.project_id`, and `input.change.risk` is `R0` or `R1`. It SHALL deny the action for any other role, any cross-project request, or any `change.risk` outside `{R0, R1}`.

#### Scenario: Architecture agent updates architecture in its own project
- **WHEN** an `architecture` agent submits `architecture.update` with matching `project_id` and `change.risk` = `R0`
- **THEN** the policy allows the action

#### Scenario: Developer cannot directly update architecture
- **WHEN** a `developer` agent submits `architecture.update` with matching `project_id` and `change.risk` = `R0`
- **THEN** the policy denies the action

#### Scenario: Cross-project request is denied
- **WHEN** an `architecture` agent submits `architecture.update` where `identity.project_id` differs from `resource.project_id`
- **THEN** the policy denies the action

#### Scenario: Risk above R1 is denied
- **WHEN** an `architecture` agent submits `architecture.update` with matching `project_id` and `change.risk` = `R2`
- **THEN** the policy denies the action

### Requirement: Developer agent may propose architecture/contract changes within its own project
The policy SHALL allow `architecture.propose` when `input.identity.agent_role` is `developer`, `input.identity.project_id` equals `input.resource.project_id`, and `input.change.risk` is `R0` or `R1`. This is a distinct, lower-privilege rule from `architecture.update`: it authorizes only the `developer` role, never `architecture`, since proposing and directly updating are different capabilities in the governance capability matrix even though both apply to the same architecture/contracts row.

#### Scenario: Developer proposes an architecture change in its own project
- **WHEN** a `developer` agent submits `architecture.propose` with matching `project_id` and `change.risk` = `R1`
- **THEN** the policy allows the action

#### Scenario: Non-developer role is denied
- **WHEN** a `product` agent submits `architecture.propose` with matching `project_id` and `change.risk` = `R1`
- **THEN** the policy denies the action

#### Scenario: Cross-project request is denied
- **WHEN** a `developer` agent submits `architecture.propose` where `identity.project_id` differs from `resource.project_id`
- **THEN** the policy denies the action

#### Scenario: Risk above R1 is denied
- **WHEN** a `developer` agent submits `architecture.propose` with matching `project_id` and `change.risk` = `R2`
- **THEN** the policy denies the action

### Requirement: Reviewer and security agents may comment on architecture/contracts within their own project
The policy SHALL allow `architecture.comment` when `input.identity.agent_role` is `reviewer` or `security`, and `input.identity.project_id` equals `input.resource.project_id`. No `change.risk` guard applies, for the same reason as `requirements.comment`. It SHALL deny the action for any other role or any cross-project request.

#### Scenario: Reviewer comments on an architecture change in its own project
- **WHEN** a `reviewer` agent submits `architecture.comment` with matching `project_id`
- **THEN** the policy allows the action

#### Scenario: Security agent comments on an architecture change in its own project
- **WHEN** a `security` agent submits `architecture.comment` with matching `project_id`
- **THEN** the policy allows the action

#### Scenario: Non-authorized role is denied
- **WHEN** an `incident` agent submits `architecture.comment` with matching `project_id`
- **THEN** the policy denies the action

#### Scenario: Cross-project request is denied
- **WHEN** a `security` agent submits `architecture.comment` where `identity.project_id` differs from `resource.project_id`
- **THEN** the policy denies the action
