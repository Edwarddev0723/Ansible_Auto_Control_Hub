# Feature Specification: MCP-Controlled Docker Compose Deployment

**Feature Branch**: `002-mcp-ansible-infra`  
**Created**: 2025-10-15  
**Status**: Draft  
**Input**: User description: "以 MCP 控制 Ansible，把 Infra_owner_demo 資料夾內的網站部署到 inventory 的 web 群組"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Docker Compose Deployment (Priority: P1)

DevOps engineers can deploy containerized web applications from a local repository to remote web servers through MCP-controlled Ansible automation, with automatic Docker installation, file synchronization, and service orchestration.

**Why this priority**: This is the core deployment workflow that delivers immediate value by automating the entire deployment process from local development to remote production servers.

**Independent Test**: Can be fully tested by running the deployment playbook against the web inventory group and verifying that the Docker Compose services are running and the web application is accessible on port 80.

**Acceptance Scenarios**:

1. **Given** a fresh target server without Docker installed, **When** the deployment playbook executes, **Then** Docker and docker-compose-plugin are installed, application files are synchronized, containers are built and running, and the website responds on HTTP port 80
2. **Given** the application is already deployed, **When** the playbook executes a second time, **Then** the deployment is idempotent with zero changes reported
3. **Given** deployment configuration is syntactically valid, **When** running ansible-playbook with --syntax-check flag, **Then** validation passes without errors

---

### User Story 2 - Health Verification and Rollback (Priority: P2)

Operations teams can verify deployment health through automated checks and automatically rollback failed deployments to prevent service disruption.

**Why this priority**: Ensures deployment reliability and minimizes downtime by detecting failures and reverting to known-good states automatically.

**Independent Test**: Can be tested by simulating a failed deployment (e.g., invalid configuration) and verifying that the system detects the failure and performs rollback operations.

**Acceptance Scenarios**:

1. **Given** containers are deployed, **When** health check executes, **Then** docker compose ps shows all services with "up" and "healthy" status within 30 seconds
2. **Given** deployment health check succeeds, **When** curl request is made to localhost on configured HTTP port, **Then** HTTP 200 response is received within 30 seconds
3. **Given** deployment fails health checks, **When** rollback procedure executes, **Then** either compose down is executed or previous container image version is restored

---

### User Story 3 - Cross-Distribution Compatibility (Priority: P3)

Platform administrators can deploy to heterogeneous server environments with automatic detection and adaptation to different Linux distributions (Debian/Ubuntu vs RHEL-based systems).

**Why this priority**: Provides flexibility for mixed infrastructure environments, though most deployments target a single distribution type.

**Independent Test**: Can be tested by running the playbook against both Debian-based and RHEL-based servers and verifying Docker installation succeeds on both.

**Acceptance Scenarios**:

1. **Given** target servers are Debian/Ubuntu-based, **When** Docker installation task executes, **Then** apt package manager is used to install docker.io and docker-compose-plugin
2. **Given** target servers are RHEL/CentOS-based, **When** Docker installation task executes, **Then** yum/dnf package manager is used with appropriate Docker repositories
3. **Given** inventory contains mixed distribution types, **When** deployment executes across all hosts, **Then** each server receives distribution-appropriate installation commands

---

### Edge Cases

- What happens when Docker daemon is not running after installation?
- How does system handle partial file synchronization failures (e.g., network interruption)?
- What occurs when Docker Compose build fails due to invalid Dockerfile?
- How does system manage concurrent deployments to the same web group?
- What happens when target directory already exists with conflicting ownership/permissions?
- How does rollback behave when no previous version exists (first deployment)?
- What occurs when health check timeout (30 seconds) is exceeded?
- How does system handle inventory hosts that are unreachable during deployment?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST install Docker engine and docker-compose-plugin on target servers in the web inventory group
- **FR-002**: System MUST automatically detect server Linux distribution and use appropriate package manager (apt for Debian/Ubuntu, yum/dnf for RHEL-based)
- **FR-003**: System MUST synchronize application files from local REPO_ROOT directory to remote REMOTE_APP_DIR path
- **FR-004**: System MUST synchronize docker-compose.yaml, Dockerfile, nginx.conf, and frontend directory contents
- **FR-005**: System MUST rename synchronized docker-compose.yaml to docker-compose.yml on remote server
- **FR-006**: System MUST build Docker images using community.docker.docker_compose_v2 module in idempotent manner
- **FR-007**: System MUST start Docker Compose services and ensure they remain running
- **FR-008**: System MUST configure Nginx according to provided nginx.conf with correct volume mounts
- **FR-009**: System MUST expose web application on configurable HTTP_PORT (default 80)
- **FR-010**: System MUST verify deployment health by checking docker compose ps output shows "up" and "healthy" status
- **FR-011**: System MUST verify deployment health by confirming HTTP 200 response from localhost on HTTP_PORT within 30 seconds
- **FR-012**: System MUST implement idempotent deployment where second execution reports zero changes
- **FR-013**: System MUST pass ansible-playbook --syntax-check validation
- **FR-014**: System MUST implement rollback mechanism that executes compose down or restores previous image version on failure
- **FR-015**: System MUST generate structured logs using YAML callback plugin
- **FR-016**: System MUST enable Ansible log_path configuration for audit trail
- **FR-017**: System MUST include community.docker collection in requirements.yml
- **FR-018**: System MUST provide runbook documentation for manual execution procedures
- **FR-019**: System MUST provide pipeline documentation for automation integration
- **FR-020**: System MUST support configurable variables: REPO_ROOT, REMOTE_APP_DIR, INVENTORY_GROUP, HTTP_PORT, COMPOSE_FILE_LOCAL, DOCKERFILE_LOCAL, NGINX_CONF_LOCAL

### Configuration Variables

- **REPO_ROOT**: Local repository path containing application files (default: ./Infra_owner_demo)
- **REMOTE_APP_DIR**: Remote deployment directory path (default: /opt/infra_owner_demo)
- **INVENTORY_GROUP**: Target inventory group name (default: web)
- **COMPOSE_FILE_LOCAL**: Local path to docker-compose.yaml (default: {{ REPO_ROOT }}/infra/docker-compose.yaml)
- **DOCKERFILE_LOCAL**: Local path to Dockerfile (default: {{ REPO_ROOT }}/infra/Dockerfile)
- **NGINX_CONF_LOCAL**: Local path to nginx.conf (default: {{ REPO_ROOT }}/infra/nginx.conf)
- **HTTP_PORT**: External HTTP port for web application (default: 80)

### Key Entities

- **Deployment Configuration**: Collection of variables defining source paths, target locations, and deployment parameters
- **Inventory Group**: Named group of target servers (web) that receive the deployment
- **Docker Compose Service**: Orchestrated container application defined by docker-compose.yml with health status
- **Health Check Result**: Verification outcome including container status, HTTP response, and timing metrics
- **Rollback State**: Previous deployment state used for recovery including image versions and configuration
- **Audit Log**: Structured deployment execution record with timestamps, tasks, and outcomes

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Deployment playbook passes syntax validation (--syntax-check) with zero errors
- **SC-002**: Docker and docker-compose-plugin installation completes successfully on all web group servers
- **SC-003**: All application files synchronize from local repository to remote servers without data loss
- **SC-004**: Docker Compose services reach "up" and "healthy" status within 30 seconds of deployment
- **SC-005**: Web application responds with HTTP 200 status code on configured HTTP_PORT within 30 seconds
- **SC-006**: Second playbook execution reports zero changes, confirming idempotent deployment
- **SC-007**: Rollback mechanism successfully reverts failed deployments within 60 seconds
- **SC-008**: Deployment process generates complete audit logs with all task outcomes and timestamps
- **SC-009**: Deployment succeeds on both Debian-based and RHEL-based servers with appropriate package managers
- **SC-010**: Documentation (runbook.md and pipeline.md) enables users to execute deployment without external guidance
- **SC-011**: MCP interface successfully initiates and monitors deployment status through Ansible integration
- **SC-012**: 100% of required configuration files (ansible.cfg, requirements.yml, playbook) are generated and functional
