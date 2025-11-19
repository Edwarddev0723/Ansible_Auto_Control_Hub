# Deployment Guide

## Overview

This deployment playbook automates the deployment of the Infra_owner_demo application using Docker Compose with automatic health checks and rollback capabilities.

## Prerequisites

1. **Ansible** installed (version 2.9+)
2. **SSH access** to target servers (or local Docker for localhost testing)
3. **Sudo privileges** on target servers
4. **Python 3** installed on target servers

## Directory Structure

```
ansible_projects/infra_owner_deploy/
├── ansible.cfg              # Ansible configuration
├── requirements.yml         # Ansible Galaxy collections
├── inventory/
│   └── hosts.ini           # Target server inventory
├── group_vars/
│   ├── all.yml             # Global variables
│   └── web.yml             # Web group variables
├── playbooks/
│   └── deploy_compose.yml  # Main deployment playbook
└── logs/
    └── ansible-deployment.log  # Execution logs
```

## Configuration

### Default Variables (group_vars/all.yml)

- `repo_root`: `./Infra_owner_demo` - Source directory for application files
- `remote_app_dir`: `/opt/infra_owner_demo` - Deployment directory on target servers
- `http_port`: `80` - HTTP service port
- `health_check_retries`: `10` - Number of health check attempts
- `health_check_delay`: `3` - Delay between health checks (seconds)

### Inventory Configuration

Edit `inventory/hosts.ini` to add your target servers:

```ini
[web]
webserver1 ansible_host=192.168.1.10 ansible_user=ubuntu
webserver2 ansible_host=192.168.1.11 ansible_user=ubuntu

[web:vars]
ansible_python_interpreter=/usr/bin/python3
```

## Usage

### 1. Install Required Collections

```bash
cd ansible_projects/infra_owner_deploy
ansible-galaxy collection install -r requirements.yml
```

### 2. Validate Playbook Syntax

```bash
ansible-playbook --syntax-check playbooks/deploy_compose.yml
```

### 3. Run Deployment

**For remote servers (with SSH):**

```bash
ansible-playbook playbooks/deploy_compose.yml
```

**For localhost testing (requires sudo password):**

```bash
ansible-playbook playbooks/deploy_compose.yml --ask-become-pass
```

**With custom variables:**

```bash
ansible-playbook playbooks/deploy_compose.yml -e "http_port=8080"
```

**Dry run (check mode):**

```bash
ansible-playbook playbooks/deploy_compose.yml --check
```

## Deployment Process

The playbook performs the following steps:

### 1. Docker Installation
- Updates package cache (apt for Debian/Ubuntu, dnf for RHEL/CentOS)
- Adds Docker repository
- Installs Docker CE and Docker Compose plugin
- Starts and enables Docker service

### 2. Application Setup
- Creates remote application directory (`/opt/infra_owner_demo`)
- Captures current Docker Compose state for rollback

### 3. File Synchronization
- Synchronizes `frontend/` directory
- Copies `docker-compose.yaml` (renamed to `docker-compose.yml`)
- Copies `Dockerfile`
- Copies `nginx.conf`

### 4. Docker Compose Deployment
- Builds images with `build: always`
- Pulls base images with `pull: missing`
- Deploys containers with `recreate: smart` (idempotent)

### 5. Health Checks
- Verifies Docker Compose services are running
- Checks HTTP endpoint returns 200 status
- Retries up to 10 times with 3-second delays

### 6. Rollback (on failure)
- Stops failed containers
- Restores previous images if available
- Reports failure details

## Output and Verification

### Deployment Summary

After successful deployment, you'll see:

```yaml
=== Deployment Summary ===
Status: SUCCESS
Run ID: 20251015T120000
Started: 2025-10-15T12:00:00Z
Completed: 2025-10-15T12:05:00Z
Target: webserver1
Application Directory: /opt/infra_owner_demo
HTTP Endpoint: http://localhost:80
Log File: logs/ansible-deployment.log
==========================
```

### Docker Compose Status

```bash
docker compose ps
```

### HTTP Verification

The playbook automatically verifies the HTTP endpoint. You can also manually test:

```bash
curl http://localhost:80
```

### Log Files

- **Ansible execution log**: `logs/ansible-deployment.log`
- **Structured YAML output**: Console output with YAML callback

## Troubleshooting

### Issue: "sudo: a password is required"

**Solution**: Use `--ask-become-pass` flag:

```bash
ansible-playbook playbooks/deploy_compose.yml --ask-become-pass
```

### Issue: SSH connection failed

**Solution**: Verify SSH connectivity:

```bash
ansible web -m ping
```

### Issue: Docker installation failed

**Solution**: Check OS compatibility (Debian 11+/Ubuntu 20.04+ or RHEL 8+)

### Issue: Health check timeout

**Solution**: 
- Check if port is already in use: `netstat -tulpn | grep 80`
- Verify Docker containers are running: `docker compose ps`
- Check container logs: `docker compose logs`

### Issue: Deployment not idempotent (changes on second run)

**Solution**: This is expected if application code changes. For true idempotency:
- Ensure file content is identical
- Check `recreate: smart` is configured (default)

## Advanced Usage

### Override Variables

```bash
# Deploy to custom port
ansible-playbook playbooks/deploy_compose.yml -e "http_port=8080"

# Use custom application directory
ansible-playbook playbooks/deploy_compose.yml -e "remote_app_dir=/srv/myapp"

# Adjust health check settings
ansible-playbook playbooks/deploy_compose.yml \
  -e "health_check_retries=5" \
  -e "health_check_delay=5"
```

### Target Specific Hosts

```bash
# Deploy to single host
ansible-playbook playbooks/deploy_compose.yml --limit webserver1

# Deploy to subset
ansible-playbook playbooks/deploy_compose.yml --limit 'web[0:1]'
```

### Verbose Output

```bash
# Debug level
ansible-playbook playbooks/deploy_compose.yml -v

# More verbose
ansible-playbook playbooks/deploy_compose.yml -vvv
```

## Security Considerations

1. **SSH Keys**: Use SSH key authentication instead of passwords
2. **Sudo Access**: Ensure proper sudo configuration on target servers
3. **Firewall**: Open required ports (80/HTTP, 22/SSH)
4. **SELinux**: May require additional configuration on RHEL-based systems

## Integration with MCP

This playbook can be invoked via Model Context Protocol (MCP) for natural language control:

**Example MCP commands:**

- "Deploy the application to web servers"
- "Check deployment status"
- "Rollback to previous version"

See `specs/002-mcp-ansible-infra/contracts/mcp-tool-api.json` for API specification.

## Performance

- **Fresh installation**: ~5 minutes (includes Docker installation)
- **Update deployment**: ~30 seconds (idempotent, only changed files)
- **Health check timeout**: 30 seconds maximum (10 retries × 3 seconds)

## References

- Ansible Documentation: https://docs.ansible.com/
- Docker Compose: https://docs.docker.com/compose/
- Community Docker Collection: https://galaxy.ansible.com/community/docker
