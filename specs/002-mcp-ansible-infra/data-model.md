# Data Model: MCP-Controlled Docker Compose Deployment

**Created**: 2025-10-15  
**Feature**: [spec.md](./spec.md) | [plan.md](./plan.md) | [research.md](./research.md)

## Overview

This document defines the data structures, configuration schemas, and state models for the Docker Compose deployment automation system.

## Configuration Entities

### 1. Deployment Configuration

Defines all deployment parameters and paths.

**Fields**:
- `repo_root` (string): Local repository root path containing application source
  - Default: `"./Infra_owner_demo"`
  - Validation: Must be an existing directory path
  - Example: `"/Users/user/projects/Infra_owner_demo"`
  
- `remote_app_dir` (string): Remote deployment directory on target servers
  - Default: `"/opt/infra_owner_demo"`
  - Validation: Absolute path required
  - Example: `"/opt/myapp"`
  
- `inventory_group` (string): Ansible inventory group for target servers
  - Default: `"web"`
  - Validation: Must exist in inventory file
  - Example: `"production_web"`
  
- `http_port` (integer): External HTTP port for web application
  - Default: `80`
  - Validation: 1-65535, must not conflict with existing services
  - Example: `8080`

- `compose_file_local` (string): Local path to docker-compose source file
  - Default: `"{{ repo_root }}/infra/docker-compose.yaml"`
  - Validation: Must be valid YAML file
  - Example: `"./infra/docker-compose.yaml"`

- `dockerfile_local` (string): Local path to Dockerfile
  - Default: `"{{ repo_root }}/infra/Dockerfile"`
  - Validation: Must be valid Dockerfile syntax
  - Example: `"./infra/Dockerfile"`

- `nginx_conf_local` (string): Local path to Nginx configuration
  - Default: `"{{ repo_root }}/infra/nginx.conf"`
  - Validation: Must be valid Nginx configuration syntax
  - Example: `"./infra/nginx.conf"`

**Relationships**:
- References → Inventory Group (many-to-one)
- Produces → Deployment Execution (one-to-many)

**State Transitions**: None (static configuration)

---

### 2. Inventory Group

Represents a named group of target servers in Ansible inventory.

**Fields**:
- `name` (string): Group name identifier
  - Example: `"web"`, `"production_web"`
  
- `hosts` (list[string]): List of hostnames or IPs in the group
  - Validation: Each host must be reachable via SSH
  - Example: `["web1.example.com", "web2.example.com"]`
  
- `variables` (dict): Group-specific Ansible variables
  - Optional group_vars overrides
  - Example: `{"ansible_user": "deploy", "ansible_become": true}`

**Relationships**:
- Contains → Server Hosts (one-to-many)
- Referenced by → Deployment Configuration (many-to-one)

**State Transitions**: None (inventory configuration)

---

### 3. Deployment Execution

Represents a single playbook execution instance with complete audit trail.

**Fields**:
- `run_id` (string): Unique execution identifier
  - Format: `"deploy-YYYYMMDD-HHMMSS-<random>"`
  - Example: `"deploy-20251015-143022-a4f9"`
  
- `timestamp_start` (datetime): Execution start time
  - ISO 8601 format
  - Example: `"2025-10-15T14:30:22Z"`
  
- `timestamp_end` (datetime): Execution completion time
  - ISO 8601 format
  - Example: `"2025-10-15T14:35:18Z"`
  
- `status` (enum): Execution outcome
  - Values: `"pending"`, `"running"`, `"success"`, `"failed"`, `"rolled_back"`
  - Initial: `"pending"`
  
- `initiator` (string): User or system that triggered deployment
  - Example: `"user@example.com"`, `"ci-pipeline"`
  
- `target_hosts` (list[string]): Hosts included in this execution
  - Example: `["web1.example.com", "web2.example.com"]`
  
- `configuration_snapshot` (dict): Deployment configuration at execution time
  - Captures all variables for audit and replay
  
- `tasks_executed` (list[TaskResult]): Detailed task execution results
  - See TaskResult entity below
  
- `log_file_path` (string): Path to detailed execution log
  - Example: `"./logs/ansible-deployment-20251015-143022.log"`
  
- `error_message` (string|null): Error details if status is `"failed"`
  - Null for successful executions

**Relationships**:
- Executes on → Inventory Group (many-to-one)
- Contains → Task Results (one-to-many)
- May trigger → Rollback Execution (one-to-zero-or-one)

**State Transitions**:
```
pending → running → success
pending → running → failed → rolled_back
```

---

### 4. Task Result

Represents the outcome of a single Ansible task within a playbook execution.

**Fields**:
- `task_name` (string): Human-readable task description
  - Example: `"Install Docker on Debian/Ubuntu"`
  
- `task_action` (string): Ansible module used
  - Example: `"ansible.builtin.apt"`, `"community.docker.docker_compose_v2"`
  
- `host` (string): Target host for this task
  - Example: `"web1.example.com"`
  
- `status` (enum): Task execution result
  - Values: `"ok"`, `"changed"`, `"skipped"`, `"failed"`, `"unreachable"`
  
- `changed` (boolean): Whether task made changes to system state
  - Used for idempotency verification
  
- `duration_seconds` (float): Task execution time
  - Example: `3.47`
  
- `stdout` (string): Standard output from task
  - May be empty for some tasks
  
- `stderr` (string): Standard error from task
  - Empty for successful tasks
  
- `return_code` (integer|null): Exit code for command/shell tasks
  - Null for non-command tasks

**Relationships**:
- Part of → Deployment Execution (many-to-one)

**Validation Rules**:
- If `status` is `"failed"`, `stderr` should be non-empty
- If `changed` is `true`, `status` must be `"changed"`
- `duration_seconds` must be non-negative

---

### 5. Docker Compose Service Status

Represents the runtime state of services defined in docker-compose.yml.

**Fields**:
- `service_name` (string): Service name from compose file
  - Example: `"nginx"`, `"frontend"`
  
- `container_id` (string): Docker container ID
  - Example: `"a4f9c3b21e55"`
  
- `state` (enum): Container runtime state
  - Values: `"running"`, `"exited"`, `"restarting"`, `"paused"`, `"created"`
  
- `health_status` (enum|null): Health check result
  - Values: `"healthy"`, `"unhealthy"`, `"starting"`, `null` (no health check defined)
  
- `ports` (list[string]): Published port mappings
  - Example: `["0.0.0.0:80->80/tcp"]`
  
- `image` (string): Docker image name and tag
  - Example: `"nginx:latest"`
  
- `started_at` (datetime): Container start time
  - ISO 8601 format

**Relationships**:
- Part of → Deployment Execution (many-to-one)

**Validation Rules**:
- If `health_status` is `"healthy"` or `"unhealthy"`, health checks must be defined in compose file
- `state` must be `"running"` for health check to be evaluated

---

### 6. Health Check Result

Represents the outcome of deployment health verification.

**Fields**:
- `check_type` (enum): Type of health check performed
  - Values: `"container_status"`, `"http_endpoint"`, `"compose_ps"`
  
- `timestamp` (datetime): When check was performed
  - ISO 8601 format
  
- `passed` (boolean): Whether check succeeded
  
- `details` (string): Additional information about check result
  - Example: `"HTTP 200 OK"`, `"All services healthy"`
  
- `retry_attempt` (integer): Which retry attempt (1-based)
  - For checks with retry logic
  - Example: `3` (third attempt)

**Relationships**:
- Associated with → Deployment Execution (many-to-one)

**Validation Rules**:
- `retry_attempt` must be between 1 and maximum configured retries
- If `passed` is `false` and `retry_attempt` < max_retries, check should be retried

---

### 7. Rollback State

Captures system state before deployment for potential rollback.

**Fields**:
- `deployment_id` (string): Reference to deployment that created this snapshot
  - Example: `"deploy-20251015-143022-a4f9"`
  
- `timestamp` (datetime): When snapshot was created
  - ISO 8601 format
  
- `image_tags` (list[dict]): Docker image tags before deployment
  - Structure: `[{"repository": "nginx", "tag": "1.21", "id": "sha256:..."}]`
  
- `compose_file_backup` (string): Previous docker-compose.yml content
  - Base64 encoded or plain text
  
- `service_states` (list[dict]): Service states before deployment
  - For restoration if needed

**Relationships**:
- Created by → Deployment Execution (many-to-one)
- Used by → Rollback Execution (one-to-zero-or-one)

**State Transitions**: None (immutable snapshot)

---

## Configuration File Schemas

### ansible.cfg Schema

```ini
[defaults]
# Callback configuration
stdout_callback = yaml
callback_whitelist = profile_tasks, timer

# Logging configuration
log_path = ./logs/ansible-deployment.log
display_skipped_hosts = false
display_ok_hosts = true

# SSH configuration
host_key_checking = false
timeout = 30

# Privilege escalation
become = true
become_method = sudo
become_user = root
become_ask_pass = false

[ssh_connection]
pipelining = true
control_path = %(directory)s/%%C
```

### requirements.yml Schema

```yaml
---
collections:
  - name: community.docker
    version: ">=3.0.0"
    source: https://galaxy.ansible.com
```

### Deployment Variables Schema (group_vars/all.yml)

```yaml
---
# Deployment Configuration
repo_root: "./Infra_owner_demo"
remote_app_dir: "/opt/infra_owner_demo"
inventory_group: "web"
http_port: 80

# File Paths
compose_file_local: "{{ repo_root }}/infra/docker-compose.yaml"
dockerfile_local: "{{ repo_root }}/infra/Dockerfile"
nginx_conf_local: "{{ repo_root }}/infra/nginx.conf"

# Docker Compose Configuration
compose_build: "always"
compose_pull: "missing"
compose_recreate: "smart"
compose_remove_orphans: true

# Health Check Configuration
health_check_retries: 10
health_check_delay: 3
health_check_timeout: 30

# Rollback Configuration
rollback_enabled: true
keep_previous_images: true
```

## MCP Tool Interface Schema

### Input Schema (MCP Tool Parameters)

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["deploy", "rollback", "status", "validate"],
      "description": "Operation to perform"
    },
    "inventory_group": {
      "type": "string",
      "default": "web",
      "description": "Target inventory group"
    },
    "repo_root": {
      "type": "string",
      "default": "./Infra_owner_demo",
      "description": "Local repository path"
    },
    "remote_app_dir": {
      "type": "string",
      "default": "/opt/infra_owner_demo",
      "description": "Remote deployment directory"
    },
    "http_port": {
      "type": "integer",
      "default": 80,
      "minimum": 1,
      "maximum": 65535,
      "description": "HTTP port for web application"
    },
    "dry_run": {
      "type": "boolean",
      "default": false,
      "description": "Run in check mode without making changes"
    }
  },
  "required": ["action"]
}
```

### Output Schema (MCP Tool Response)

```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether operation succeeded"
    },
    "run_id": {
      "type": "string",
      "description": "Unique execution identifier"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "running", "success", "failed", "rolled_back"],
      "description": "Execution status"
    },
    "duration_seconds": {
      "type": "number",
      "description": "Total execution time"
    },
    "tasks_summary": {
      "type": "object",
      "properties": {
        "ok": {"type": "integer"},
        "changed": {"type": "integer"},
        "skipped": {"type": "integer"},
        "failed": {"type": "integer"},
        "unreachable": {"type": "integer"}
      }
    },
    "health_checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "check_type": {"type": "string"},
          "passed": {"type": "boolean"},
          "details": {"type": "string"}
        }
      }
    },
    "log_file": {
      "type": "string",
      "description": "Path to detailed execution log"
    },
    "error_message": {
      "type": "string",
      "description": "Error details if failed"
    }
  },
  "required": ["success", "run_id", "status"]
}
```

## Data Validation Rules

### Pre-Deployment Validation
1. `repo_root` directory must exist and contain required files
2. `inventory_group` must exist in inventory file with at least one host
3. All target hosts must be reachable via SSH
4. Docker Compose file must be valid YAML and conform to compose-spec
5. Dockerfile must pass `docker build --check` validation
6. `http_port` must not be in use on target servers

### Post-Deployment Validation
1. All services must reach "running" state
2. Services with health checks must reach "healthy" status
3. HTTP endpoint must return 200 status code
4. Idempotency check: Second run must report zero changes

### Rollback Validation
1. Rollback state snapshot must exist for deployment
2. Previous image tags must be available in Docker registry
3. Rollback operation must restore all services to previous state

## Summary

The data model provides comprehensive schema definitions for deployment configuration, execution tracking, health monitoring, and rollback state management. All entities include validation rules and relationships to ensure data integrity throughout the deployment lifecycle. The MCP tool interface schemas enable seamless integration with natural language and GUI interfaces.
