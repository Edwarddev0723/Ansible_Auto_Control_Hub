# Implementation Plan: MCP-Controlled Docker Compose Deployment

**Branch**: `002-mcp-ansible-infra` | **Date**: 2025-10-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-mcp-ansible-infra/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy containerized web applications from Infra_owner_demo repository to remote web servers using MCP-controlled Ansible automation. The system installs Docker infrastructure, synchronizes application files, builds and orchestrates containers using Docker Compose v2, implements health verification with automatic rollback, and maintains complete audit trails. Technical approach: Ansible playbooks with community.docker collection, OS-aware package management (apt/dnf), idempotent deployment strategy, and structured logging.

## Technical Context

**Language/Version**: Ansible Core 2.16+, Python 3.10+ (for Ansible execution environment)  
**Primary Dependencies**: ansible-core, community.docker collection (2.0+), docker-compose-plugin (v2), Docker Engine  
**Storage**: File-based deployment artifacts, Docker volumes for application data, Ansible log files  
**Testing**: ansible-playbook --syntax-check, molecule (optional), idempotency validation (check_mode + diff)  
**Target Platform**: Linux servers (Debian 11+/Ubuntu 20.04+, RHEL 8+/CentOS 8+/Rocky Linux 8+)  
**Project Type**: Infrastructure automation (Ansible playbooks)  
**Performance Goals**: Deployment completion <5 minutes for fresh install, <2 minutes for updates, health check response <30 seconds  
**Constraints**: Idempotent operations (zero changes on re-run), SSH connectivity required, sudo/become privileges needed, HTTP port 80 availability  
**Scale/Scope**: Single or multiple web servers in inventory group, concurrent deployment support, rollback capability within 60 seconds

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Security-First**: Deny-by-default security model with RBAC implementation planned
  - SSH key-based authentication required (no password auth)
  - Become/sudo privileges explicit and scoped per task
  - Secrets (SSH keys, tokens) managed via ansible-vault or environment variables
  - No privileged containers in docker-compose.yml specifications
- [x] **Plan-Apply Review**: Infrastructure changes follow plan → review → apply workflow
  - Ansible check mode (--check) for dry-run validation
  - Diff mode (--diff) shows exact changes before apply
  - Health checks mandatory before considering deployment successful
  - Rollback mechanism validates before execution
- [x] **Human-Machine Auditability**: Complete audit logging with correlation IDs specified
  - ANSIBLE_STDOUT_CALLBACK=yaml for structured output
  - ANSIBLE_LOG_PATH enabled for persistent audit trail
  - Task-level timestamps and execution duration recorded
  - Playbook run_id embedded in logs for correlation
- [x] **Test Coverage ≥70%**: Unit test strategy defined with coverage requirements
  - Syntax validation (--syntax-check) mandatory pre-deployment
  - Idempotency tests (second run = zero changes) automated
  - Health check verification (HTTP 200 + docker compose ps) required
  - Rollback mechanism tested in failure scenarios
- [x] **Schema-First Design**: OpenAPI/JSON Schema contracts planned before implementation
  - Ansible variable schema defined with defaults and validation
  - Docker Compose schema (compose-spec.io) compliance verified
  - MCP tool interface schema defined for ansible-playbook invocation
  - Health check response format standardized (JSON or structured text)
- [x] **Dual Interface Equivalence**: GUI and natural language interfaces provide equivalent functionality
  - MCP natural language interface can invoke all deployment operations
  - Future web GUI will provide equivalent playbook execution capabilities
  - Both interfaces use same underlying Ansible playbooks
  - Audit logs identical regardless of invocation method

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
ansible_projects/
├── infra_owner_deploy/
│   ├── ansible.cfg                    # Ansible configuration with yaml callback, log_path
│   ├── requirements.yml               # Galaxy requirements (community.docker)
│   ├── inventory/
│   │   └── hosts.ini                  # Inventory with [web] group
│   ├── playbooks/
│   │   └── deploy_compose.yml         # Main deployment playbook
│   ├── roles/                         # Optional: modularized tasks
│   │   ├── docker_setup/
│   │   │   └── tasks/main.yml        # Docker installation tasks
│   │   ├── app_sync/
│   │   │   └── tasks/main.yml        # File synchronization tasks
│   │   ├── compose_deploy/
│   │   │   └── tasks/main.yml        # Docker Compose deployment tasks
│   │   └── health_check/
│   │       └── tasks/main.yml        # Health verification tasks
│   ├── group_vars/
│   │   ├── all.yml                   # Global variables
│   │   └── web.yml                   # Web group specific variables
│   └── logs/                         # Ansible execution logs
│
├── Infra_owner_demo/                  # Source repository (input)
│   ├── frontend/                      # Frontend application files
│   └── infra/
│       ├── docker-compose.yaml        # Source compose file
│       ├── Dockerfile                 # Application Dockerfile
│       └── nginx.conf                 # Nginx configuration
│
└── docs/
    ├── runbook.md                     # Manual execution procedures
    └── pipeline.md                    # CI/CD integration guide
```

**Structure Decision**: Infrastructure automation project using Ansible best practices with role-based organization for modularity and reusability. The Infra_owner_demo directory contains source files to be deployed, while ansible_projects/infra_owner_deploy contains the automation logic.

## Complexity Tracking

*No constitution violations - all checks passed with implementations planned*
