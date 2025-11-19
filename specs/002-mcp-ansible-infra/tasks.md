---
description: "Task list for MCP-Controlled Docker Compose Deployment implementation"
---

# Tasks: MCP-Controlled Docker Compose Deployment

**Input**: Design documents from `/specs/002-mcp-ansible-infra/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are included as this is infrastructure automation requiring validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- Infrastructure automation project: `ansible_projects/infra_owner_deploy/` at repository root
- Source files: `Infra_owner_demo/` directory
- Documentation: `docs/` directory
- Paths shown below use ansible_projects structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create ansible project directory structure: `ansible_projects/infra_owner_deploy/` with subdirectories: `playbooks/`, `roles/`, `inventory/`, `group_vars/`, `logs/`
- [ ] T002 [P] Create ansible.cfg with YAML callback, log_path enabled in `ansible_projects/infra_owner_deploy/ansible.cfg`
- [ ] T003 [P] Create requirements.yml with community.docker collection specification in `ansible_projects/infra_owner_deploy/requirements.yml`
- [ ] T004 Install Ansible collections via `ansible-galaxy collection install -r ansible_projects/infra_owner_deploy/requirements.yml`
- [ ] T005 [P] Create inventory file with [web] group in `ansible_projects/infra_owner_deploy/inventory/hosts.ini`
- [ ] T006 [P] Create global variables file in `ansible_projects/infra_owner_deploy/group_vars/all.yml` with defaults: repo_root, remote_app_dir, http_port, compose settings
- [ ] T007 [P] Create web group variables file in `ansible_projects/infra_owner_deploy/group_vars/web.yml` with inventory_group and file paths

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Verify SSH connectivity to web group hosts using `ansible web -i ansible_projects/infra_owner_deploy/inventory/hosts.ini -m ping`
- [ ] T009 Verify sudo/become privileges on target hosts using `ansible web -i ansible_projects/infra_owner_deploy/inventory/hosts.ini -m shell -a "sudo whoami" -b`
- [ ] T010 Create OS detection task to identify ansible_os_family (Debian vs RedHat) in playbook structure
- [ ] T011 [P] Create docker_setup role directory structure in `ansible_projects/infra_owner_deploy/roles/docker_setup/tasks/`
- [ ] T012 [P] Create app_sync role directory structure in `ansible_projects/infra_owner_deploy/roles/app_sync/tasks/`
- [ ] T013 [P] Create compose_deploy role directory structure in `ansible_projects/infra_owner_deploy/roles/compose_deploy/tasks/`
- [ ] T014 [P] Create health_check role directory structure in `ansible_projects/infra_owner_deploy/roles/health_check/tasks/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Automated Docker Compose Deployment (Priority: P1) 🎯 MVP

**Goal**: Core deployment workflow that installs Docker, synchronizes files, builds and runs containers

**Independent Test**: Run deployment playbook against web group, verify Docker installed, containers running, website accessible on port 80

### Tests for User Story 1 ⚠️

**NOTE: Write these validation tasks FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Create syntax validation test task in playbook for `ansible-playbook --syntax-check playbooks/deploy_compose.yml`
- [ ] T016 [P] [US1] Create idempotency test scaffold to verify zero changes on second playbook run

### Implementation for User Story 1

- [ ] T017 [US1] Implement Docker installation for Debian/Ubuntu in `ansible_projects/infra_owner_deploy/roles/docker_setup/tasks/main.yml` using ansible.builtin.apt module
- [ ] T018 [US1] Implement Docker installation for RHEL/CentOS in `ansible_projects/infra_owner_deploy/roles/docker_setup/tasks/main.yml` using ansible.builtin.dnf module with conditional when: ansible_os_family
- [ ] T019 [US1] Implement Docker service start and enable in `ansible_projects/infra_owner_deploy/roles/docker_setup/tasks/main.yml` using ansible.builtin.service module
- [ ] T020 [P] [US1] Implement frontend directory synchronization in `ansible_projects/infra_owner_deploy/roles/app_sync/tasks/main.yml` using ansible.builtin.synchronize module
- [ ] T021 [P] [US1] Implement docker-compose.yaml file copy with rename to docker-compose.yml in `ansible_projects/infra_owner_deploy/roles/app_sync/tasks/main.yml` using ansible.builtin.copy module
- [ ] T022 [P] [US1] Implement Dockerfile copy in `ansible_projects/infra_owner_deploy/roles/app_sync/tasks/main.yml` using ansible.builtin.copy module
- [ ] T023 [P] [US1] Implement nginx.conf copy in `ansible_projects/infra_owner_deploy/roles/app_sync/tasks/main.yml` using ansible.builtin.copy module
- [ ] T024 [US1] Implement Docker Compose v2 build and up in `ansible_projects/infra_owner_deploy/roles/compose_deploy/tasks/main.yml` using community.docker.docker_compose_v2 module with parameters: build=always, pull=missing, state=present, recreate=smart
- [ ] T025 [US1] Create main deployment playbook in `ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml` orchestrating all roles in correct order
- [ ] T026 [US1] Add structured logging configuration to playbook with run_id generation and task-level timestamps
- [ ] T027 [US1] Execute syntax validation: `ansible-playbook --syntax-check ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml`
- [ ] T028 [US1] Execute first deployment run: `ansible-playbook -i ansible_projects/infra_owner_deploy/inventory/hosts.ini ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml`
- [ ] T029 [US1] Execute second deployment run for idempotency verification: verify changed=0

**Checkpoint**: At this point, User Story 1 should be fully functional - Docker installed, app deployed, containers running on port 80

---

## Phase 4: User Story 2 - Health Verification and Rollback (Priority: P2)

**Goal**: Automated health checks with retry logic and automatic rollback on failures

**Independent Test**: Simulate deployment failure, verify health checks detect it and rollback executes successfully

### Tests for User Story 2 ⚠️

- [ ] T030 [P] [US2] Create health check validation test to verify docker compose ps output format
- [ ] T031 [P] [US2] Create HTTP endpoint test scaffold to verify curl returns 200 within timeout

### Implementation for User Story 2

- [ ] T032 [P] [US2] Implement Docker Compose service status check in `ansible_projects/infra_owner_deploy/roles/health_check/tasks/main.yml` using docker compose ps --format json
- [ ] T033 [P] [US2] Implement HTTP endpoint health check in `ansible_projects/infra_owner_deploy/roles/health_check/tasks/main.yml` using ansible.builtin.uri module with retries=10, delay=3, timeout=3
- [ ] T034 [US2] Implement pre-deployment image tag capture in `ansible_projects/infra_owner_deploy/roles/compose_deploy/tasks/main.yml` using docker compose images --format json
- [ ] T035 [US2] Add block/rescue structure to deployment playbook in `ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml` for automatic rollback
- [ ] T036 [US2] Implement rollback tasks in rescue block: docker_compose_v2 state=absent to stop failed containers
- [ ] T037 [US2] Implement previous image restoration in rescue block using saved image tags
- [ ] T038 [US2] Add health check role invocation to main playbook after compose deployment
- [ ] T039 [US2] Test rollback mechanism by intentionally failing deployment (invalid config) and verify automatic recovery
- [ ] T040 [US2] Verify health checks execute with correct retry logic and timeout handling

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - deployment succeeds with health verification, failures trigger rollback

---

## Phase 5: User Story 3 - Cross-Distribution Compatibility (Priority: P3)

**Goal**: Support for both Debian-based and RHEL-based systems with automatic package manager detection

**Independent Test**: Run playbook against both Debian and RHEL servers, verify Docker installation succeeds on both

### Tests for User Story 3 ⚠️

- [ ] T041 [P] [US3] Create OS family detection validation test to verify ansible_os_family is correctly identified
- [ ] T042 [P] [US3] Create package installation verification test for both apt and dnf scenarios

### Implementation for User Story 3

- [ ] T043 [US3] Enhance docker_setup role with fact gathering to ensure ansible_os_family is available
- [ ] T044 [US3] Add Docker repository configuration for RHEL-based systems in `ansible_projects/infra_owner_deploy/roles/docker_setup/tasks/main.yml`
- [ ] T045 [US3] Add conditional validation to ensure correct package manager is used based on OS family
- [ ] T046 [US3] Test deployment on Debian/Ubuntu server and verify apt is used
- [ ] T047 [US3] Test deployment on RHEL/CentOS server and verify dnf/yum is used
- [ ] T048 [US3] Verify both deployments result in same functional outcome (Docker installed, app running)

**Checkpoint**: All user stories should now be independently functional and cross-platform compatible

---

## Phase 6: Documentation & Observability

**Purpose**: Complete documentation and audit trail capabilities

- [ ] T049 [P] Create runbook.md in `docs/runbook.md` documenting manual execution procedures, troubleshooting, variable customization, rollback procedures
- [ ] T050 [P] Create pipeline.md in `docs/pipeline.md` documenting CI/CD integration examples, automated testing setup, deployment pipeline configuration
- [ ] T051 [P] Verify ansible.cfg log_path is correctly capturing execution logs to `ansible_projects/infra_owner_deploy/logs/ansible-deployment.log`
- [ ] T052 [P] Verify YAML callback is producing structured output with all required fields (tasks, timing, results)
- [ ] T053 Create log summary script to extract key metrics from ansible logs (execution time, changed tasks, failed tasks)
- [ ] T054 Document all configurable variables in runbook.md with defaults and examples
- [ ] T055 Add troubleshooting section to runbook.md covering common issues: SSH failures, Docker installation, port conflicts, idempotency violations, health check timeouts

---

## Phase 7: Integration & Final Validation

**Purpose**: End-to-end validation and MCP integration verification

- [ ] T056 Execute complete deployment workflow from fresh state: `ansible-playbook -i ansible_projects/infra_owner_deploy/inventory/hosts.ini ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml`
- [ ] T057 Verify all acceptance criteria from spec.md: syntax check passes, docker compose ps shows healthy, HTTP 200 within 30s, idempotency verified, rollback works
- [ ] T058 Test deployment with custom variables: `ansible-playbook -e "http_port=8080" ...` and verify port override works
- [ ] T059 Generate deployment summary report with all metrics: execution time, tasks summary, health check results, log file path
- [ ] T060 [P] Document MCP tool integration points in contracts/mcp-tool-api.json implementation notes
- [ ] T061 [P] Create example MCP natural language commands and expected playbook invocations
- [ ] T062 Validate that all deliverables are present: ansible.cfg, requirements.yml, playbooks/deploy_compose.yml, runbook.md, pipeline.md, logs

---

## Phase 8: Risk Mitigation & Future Considerations

**Purpose**: Address edge cases and operational considerations

- [ ] T063 [P] Document OS-specific considerations: package naming differences, repository setup, SELinux handling
- [ ] T064 [P] Document firewall considerations: required ports (80/HTTP, 22/SSH), firewall rules examples for iptables/firewalld
- [ ] T065 [P] Document SELinux considerations for RHEL-based systems: required contexts, booleans for container access
- [ ] T066 [P] Add disk space pre-check task to verify adequate space for Docker images and application data
- [ ] T067 [P] Document backup and restore procedures for application data and configuration
- [ ] T068 Create monitoring integration examples: Prometheus exporters, log shipping to centralized logging
- [ ] T069 Document scaling considerations: adding hosts to web group, load balancer configuration
- [ ] T070 Create troubleshooting decision tree for common deployment failures

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Documentation (Phase 6)**: Depends on all desired user stories being complete
- **Integration (Phase 7)**: Depends on all user stories + documentation
- **Risk Mitigation (Phase 8)**: Can proceed in parallel with implementation, finalize after integration

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 playbook but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 docker_setup role but independently testable

### Within Each User Story

- Tests (validation tasks) MUST be written and FAIL before implementation
- Role implementations can proceed in parallel where marked [P]
- Main playbook orchestration comes after role implementations
- Validation and execution come after playbook creation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T005, T006, T007)
- All Foundational role directory creation tasks can run in parallel (T011, T012, T013, T014)
- Within User Story 1: File copy tasks can run in parallel (T020, T021, T022, T023)
- Within User Story 2: Health check implementations can run in parallel (T032, T033)
- Documentation tasks can run in parallel (T049, T050, T051, T052)
- Risk mitigation documentation tasks can run in parallel (T063, T064, T065, T066, T067)

---

## Parallel Example: User Story 1

```bash
# Launch all file sync tasks together (T020-T023):
Task: "Implement frontend directory synchronization in roles/app_sync/tasks/main.yml"
Task: "Implement docker-compose.yaml copy with rename in roles/app_sync/tasks/main.yml"
Task: "Implement Dockerfile copy in roles/app_sync/tasks/main.yml"
Task: "Implement nginx.conf copy in roles/app_sync/tasks/main.yml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T014) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T015-T029)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! - Basic deployment works)
3. Add User Story 2 → Test independently → Deploy/Demo (Health checks + rollback added)
4. Add User Story 3 → Test independently → Deploy/Demo (Cross-platform support added)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T015-T029)
   - Developer B: User Story 2 (T030-T040) - can start writing health_check role
   - Developer C: User Story 3 (T041-T048) - can start OS detection enhancements
3. Stories complete and integrate independently

---

## Task Acceptance Criteria

### Phase 1: Setup
- **T001**: All directories exist with correct structure
- **T002**: ansible.cfg contains stdout_callback=yaml and log_path setting
- **T003**: requirements.yml contains community.docker with version >=3.0.0
- **T004**: `ansible-galaxy collection list` shows community.docker installed
- **T005**: inventory/hosts.ini contains [web] group with at least one host
- **T006**: group_vars/all.yml contains all required default variables
- **T007**: group_vars/web.yml contains web-specific variables

### Phase 2: Foundational
- **T008**: `ansible web -m ping` returns SUCCESS for all hosts
- **T009**: `ansible web -m shell -a "sudo whoami" -b` returns "root" for all hosts
- **T010**: Playbook includes task to gather ansible_facts for OS family detection
- **T011-T014**: Each role directory exists with tasks/main.yml file

### Phase 3: User Story 1
- **T015**: Syntax check command exits with code 0
- **T016**: Test scaffold exists that will verify changed=0 on second run
- **T017-T019**: Docker installation completes successfully on all web hosts
- **T020-T023**: All files synchronized to {{ remote_app_dir }} with correct names
- **T024**: Docker Compose builds images and starts containers successfully
- **T025**: Playbook file exists and includes all roles in correct order
- **T026**: Playbook output includes run_id and timestamps
- **T027**: `ansible-playbook --syntax-check` passes with exit code 0
- **T028**: First deployment completes successfully with containers running
- **T029**: Second run reports changed=0 (idempotent)

### Phase 4: User Story 2
- **T030**: Test can parse docker compose ps JSON output
- **T031**: Test scaffold can verify HTTP 200 response
- **T032**: `docker compose ps` shows all services with state=running
- **T033**: `curl http://localhost:{{ http_port }}` returns HTTP 200 within 30 seconds
- **T034**: Previous image tags are saved before deployment
- **T035**: Block/rescue structure exists in playbook
- **T036**: Rescue block includes docker_compose_v2 state=absent task
- **T037**: Rescue block restores previous images from saved tags
- **T038**: Health check role is invoked after deployment in playbook
- **T039**: Simulated failure triggers rollback successfully
- **T040**: Health checks retry 10 times with 3-second delays

### Phase 5: User Story 3
- **T041**: Test verifies ansible_os_family returns "Debian" or "RedHat"
- **T042**: Test verifies apt used on Debian, dnf/yum used on RHEL
- **T043**: Fact gathering is enabled in docker_setup role
- **T044**: Docker CE repository configuration added for RHEL-based systems
- **T045**: Conditional validation checks OS family before package installation
- **T046**: Deployment on Debian uses apt module successfully
- **T047**: Deployment on RHEL uses dnf/yum module successfully
- **T048**: Both deployments result in running containers on port 80

### Phase 6: Documentation
- **T049**: runbook.md contains all required sections with examples
- **T050**: pipeline.md contains CI/CD integration examples
- **T051**: Log file is created at logs/ansible-deployment.log with content
- **T052**: YAML output includes all tasks, timing, and results
- **T053**: Log summary script produces execution metrics
- **T054**: All variables documented with defaults and override examples
- **T055**: Troubleshooting section covers all common failure scenarios

### Phase 7: Integration
- **T056**: Full deployment completes from fresh state within 5 minutes
- **T057**: All spec.md acceptance criteria verified and passing
- **T058**: Custom variable override works correctly
- **T059**: Summary report generated with all required metrics
- **T060**: MCP integration points documented in contracts
- **T061**: Example MCP commands documented with expected outputs
- **T062**: All deliverable files exist and are complete

### Phase 8: Risk Mitigation
- **T063**: OS-specific documentation covers package naming, repos, SELinux
- **T064**: Firewall documentation includes port requirements and rule examples
- **T065**: SELinux documentation covers contexts and booleans
- **T066**: Disk space check task verifies minimum 5GB available
- **T067**: Backup/restore procedures documented with examples
- **T068**: Monitoring integration examples provided
- **T069**: Scaling documentation covers multi-host scenarios
- **T070**: Troubleshooting decision tree covers deployment failure paths

---

## Notes

- [P] tasks = different files or independent operations, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach for infrastructure validation)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

**Total Tasks**: 70 tasks
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 7 tasks  
- Phase 3 (User Story 1 - P1): 15 tasks
- Phase 4 (User Story 2 - P2): 11 tasks
- Phase 5 (User Story 3 - P3): 8 tasks
- Phase 6 (Documentation): 7 tasks
- Phase 7 (Integration): 7 tasks
- Phase 8 (Risk Mitigation): 8 tasks

**Parallel Opportunities**: 23 tasks marked [P] can run in parallel

**MVP Scope**: Phases 1-3 (T001-T029) = 29 tasks for core deployment functionality

**Independent Test Criteria**:
- US1: Deploy to web group, verify Docker + containers + HTTP 200
- US2: Simulate failure, verify rollback executes
- US3: Deploy to both Debian and RHEL, verify both succeed

Each task has clear completion criteria and deliverables enabling autonomous execution.
