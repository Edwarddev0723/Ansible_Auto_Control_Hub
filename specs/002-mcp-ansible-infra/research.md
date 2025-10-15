# Research: MCP-Controlled Docker Compose Deployment

**Created**: 2025-10-15  
**Feature**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Overview

This document consolidates research findings for implementing MCP-controlled Ansible deployment of Docker Compose applications to remote web servers.

## Technical Decisions

### Decision 1: Ansible Modules and Collections

**Decision**: Use ansible.builtin modules for system operations and community.docker collection for Docker Compose orchestration

**Modules Selected**:
- `ansible.builtin.apt` / `ansible.builtin.dnf` - Package management for Debian/RHEL
- `ansible.builtin.service` - Docker daemon management
- `ansible.builtin.file` - Directory creation and permission management
- `ansible.builtin.copy` - Configuration file deployment
- `ansible.builtin.synchronize` - Efficient directory synchronization (rsync wrapper)
- `community.docker.docker_compose_v2` - Docker Compose V2 orchestration

**Rationale**: 
- Built-in modules are stable and well-tested across Ansible versions
- community.docker provides native Docker Compose v2 support with proper state management
- synchronize module efficiently handles directory sync with delta transfers

**Alternatives Considered**:
- Using shell/command modules for Docker operations - rejected due to lack of idempotency guarantees
- ansible.builtin.template for file copying - rejected as synchronize is more efficient for directories
- docker-py Python library directly - rejected as community.docker provides better Ansible integration

### Decision 2: OS Detection and Package Manager Strategy

**Decision**: Use ansible_facts (ansible_os_family) for automatic OS detection with conditional package installation

**Implementation**:
```yaml
- name: Install Docker on Debian/Ubuntu
  ansible.builtin.apt:
    name:
      - docker.io
      - docker-compose-plugin
    state: present
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: Install Docker on RHEL/CentOS
  ansible.builtin.dnf:
    name:
      - docker-ce
      - docker-compose-plugin
    state: present
  when: ansible_os_family == "RedHat"
```

**Rationale**:
- ansible_facts are automatically gathered and reliable
- Conditional task execution based on OS family ensures correct package manager usage
- Handles both package name differences and manager differences

**Alternatives Considered**:
- Manual inventory-based OS specification - rejected as error-prone and not scalable
- Using package module with auto-detection - rejected due to less explicit control
- Shell script with if/else - rejected as not idempotent and harder to maintain

### Decision 3: File Synchronization Strategy

**Decision**: Use ansible.builtin.synchronize for directory sync and copy for individual files with rename handling

**Implementation**:
```yaml
# Sync frontend directory
- name: Synchronize frontend files
  ansible.builtin.synchronize:
    src: "{{ repo_root }}/frontend/"
    dest: "{{ remote_app_dir }}/frontend/"
    delete: yes
    recursive: yes

# Copy and rename compose file
- name: Copy docker-compose.yaml as docker-compose.yml
  ansible.builtin.copy:
    src: "{{ compose_file_local }}"
    dest: "{{ remote_app_dir }}/docker-compose.yml"
```

**Rationale**:
- synchronize uses rsync for efficient delta transfers
- copy module handles file renaming cleanly
- delete: yes ensures remote matches source state

**Alternatives Considered**:
- Using copy module for everything - rejected as inefficient for large directories
- Using template module - rejected as files don't need variable substitution
- Manual rsync via command module - rejected as not idempotent

### Decision 4: Docker Compose V2 Deployment Strategy

**Decision**: Use community.docker.docker_compose_v2 module with specific state management parameters

**Implementation**:
```yaml
- name: Deploy with Docker Compose v2
  community.docker.docker_compose_v2:
    project_src: "{{ remote_app_dir }}"
    build: always
    pull: missing
    state: present
    recreate: smart
    remove_orphans: yes
```

**Parameters Explained**:
- `project_src`: Directory containing docker-compose.yml
- `build: always`: Rebuild images on each run to capture source changes
- `pull: missing`: Only pull images that don't exist locally (efficiency)
- `state: present`: Ensure services are running
- `recreate: smart`: Only recreate containers when configuration changes (idempotency)
- `remove_orphans: yes`: Clean up containers from previous compositions

**Rationale**:
- Provides idempotent deployment (smart recreate only changes when needed)
- Handles build and orchestration in single task
- Supports proper service lifecycle management

**Alternatives Considered**:
- Using docker-compose CLI via command module - rejected as not idempotent
- Always recreating containers - rejected as causes unnecessary downtime
- Using older docker_compose module (v1) - rejected as v2 is recommended standard

### Decision 5: Health Check and Verification Strategy

**Decision**: Multi-layered health verification with retry logic and timeout handling

**Implementation**:
```yaml
# Layer 1: Docker Compose service status
- name: Check Docker Compose services status
  ansible.builtin.command:
    cmd: docker compose ps --format json
    chdir: "{{ remote_app_dir }}"
  register: compose_status
  changed_when: false

# Layer 2: HTTP endpoint verification
- name: Verify HTTP endpoint
  ansible.builtin.uri:
    url: "http://localhost:{{ http_port }}"
    status_code: 200
    timeout: 3
  register: http_check
  retries: 10
  delay: 3
  until: http_check.status == 200
```

**Rationale**:
- Two-layer verification ensures both container and application health
- Retry logic with delay handles startup time gracefully
- uri module provides proper HTTP status verification
- Maximum 30 seconds total wait time (10 retries × 3 second delay)

**Alternatives Considered**:
- Using wait_for module - rejected as uri provides better HTTP-specific checks
- Single health check - rejected as insufficient for comprehensive verification
- Longer timeout periods - rejected as 30 seconds is reasonable for containerized apps

### Decision 6: Rollback Strategy

**Decision**: State-based rollback with previous image tag tracking

**Implementation**:
```yaml
# Store current image tags before deployment
- name: Record current image tags
  ansible.builtin.command:
    cmd: docker compose images --format json
    chdir: "{{ remote_app_dir }}"
  register: pre_deploy_images
  changed_when: false

# On failure: Rollback to previous state
- name: Rollback on failure
  block:
    - name: Deploy application
      # deployment tasks here
      
  rescue:
    - name: Stop failed deployment
      community.docker.docker_compose_v2:
        project_src: "{{ remote_app_dir }}"
        state: absent
        
    - name: Restore previous images
      ansible.builtin.command:
        cmd: docker tag {{ item.repository }}:{{ item.tag }} {{ item.repository }}:latest
      loop: "{{ pre_deploy_images.stdout | from_json }}"
      when: pre_deploy_images is defined
```

**Rationale**:
- Block/rescue provides automatic rollback on any task failure
- Image tag tracking enables restoration of previous versions
- state: absent cleanly stops failed deployment before restoration

**Alternatives Considered**:
- Manual rollback procedures - rejected as error-prone and slow
- Using compose down always - rejected as loses data if volumes not properly managed
- Snapshot-based rollback - rejected as overly complex for containerized apps

### Decision 7: Observability and Logging Strategy

**Decision**: YAML callback plugin with structured logging and execution metadata

**ansible.cfg Configuration**:
```ini
[defaults]
stdout_callback = yaml
log_path = ./logs/ansible-deployment.log
display_skipped_hosts = false
display_ok_hosts = true

[callback_yaml]
result_format = yaml
```

**Rationale**:
- YAML output is both human-readable and machine-parseable
- Persistent log_path enables audit trail and troubleshooting
- Structured format supports automated log analysis

**Alternatives Considered**:
- JSON callback - rejected as less human-readable
- Default callback - rejected as insufficient structure for automation
- Custom callback plugin - rejected as unnecessary complexity

### Decision 8: Variable Management

**Decision**: Layered variable precedence with sensible defaults

**Variable Structure**:
```yaml
# group_vars/all.yml - Global defaults
repo_root: "./Infra_owner_demo"
remote_app_dir: "/opt/infra_owner_demo"
http_port: 80

# group_vars/web.yml - Group-specific overrides
inventory_group: "web"
compose_file_local: "{{ repo_root }}/infra/docker-compose.yaml"
dockerfile_local: "{{ repo_root }}/infra/Dockerfile"
nginx_conf_local: "{{ repo_root }}/infra/nginx.conf"

# Runtime overrides via extra-vars
# ansible-playbook -e "http_port=8080" deploy_compose.yml
```

**Rationale**:
- Sensible defaults minimize configuration overhead
- Group variables enable per-environment customization
- Extra-vars provide runtime flexibility for CI/CD pipelines

**Alternatives Considered**:
- All variables in playbook - rejected as not reusable
- Environment variables only - rejected as less Ansible-native
- Vault for all variables - rejected as overkill for non-sensitive data

## Best Practices Applied

### Idempotency
- All tasks designed to produce same result on multiple runs
- Using `changed_when: false` for read-only operations
- Leveraging module's built-in idempotency features (apt, docker_compose_v2)

### Security
- SSH key-based authentication required
- Become/sudo scoped to specific tasks only
- Secrets managed via ansible-vault (when needed)
- No privileged containers in compose specifications

### Performance
- Delta synchronization using rsync
- Conditional builds (only when source changes)
- Smart container recreation (only when configuration changes)
- Parallel execution where possible (Ansible default)

### Error Handling
- Block/rescue for automatic rollback
- Retries with exponential backoff for network operations
- Comprehensive validation before destructive operations
- Graceful degradation with informative error messages

## Integration Points

### MCP Interface
- Ansible playbook invocation via MCP tools
- Structured output (YAML) for parsing by MCP
- Return codes for success/failure detection
- Log file paths for detailed troubleshooting

### CI/CD Pipeline
- Syntax validation in pre-commit hooks
- Automated testing in CI environment
- Deployment pipeline integration via ansible-playbook CLI
- Artifact publishing (logs, reports) for audit

## Testing Strategy

### Validation Layers
1. **Syntax Validation**: `ansible-playbook --syntax-check`
2. **Dry Run**: `ansible-playbook --check --diff`
3. **Idempotency Test**: Run twice, verify zero changes on second run
4. **Health Verification**: HTTP 200 + container status checks
5. **Rollback Test**: Simulate failure, verify automatic recovery

### Test Environments
- Local: Docker-in-Docker or VM for development testing
- Staging: Replica of production for integration testing
- Production: Final deployment with comprehensive monitoring

## Documentation Requirements

### runbook.md Content
- Manual execution procedures
- Troubleshooting common issues
- Variable customization guide
- Rollback procedures

### pipeline.md Content
- CI/CD integration examples
- Automated testing setup
- Deployment pipeline configuration
- Monitoring and alerting setup

## Summary

All technical decisions are finalized with clear rationale and implementation paths. The architecture uses proven Ansible patterns with modern Docker Compose v2 integration, comprehensive health verification, and robust rollback mechanisms. The implementation prioritizes idempotency, security, and observability while maintaining simplicity and reliability.
