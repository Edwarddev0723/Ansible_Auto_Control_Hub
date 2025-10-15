# Quickstart Guide: MCP-Controlled Docker Compose Deployment

**Feature**: MCP-Controlled Docker Compose Deployment  
**Created**: 2025-10-15  
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md) | [research.md](./research.md) | [data-model.md](./data-model.md)

## Prerequisites

### Required Software
- Ansible Core 2.16+ installed locally
- Python 3.10+ (for Ansible execution)
- SSH client configured
- Target servers running:
  - Debian 11+/Ubuntu 20.04+ OR RHEL 8+/CentOS 8+/Rocky Linux 8+
  - SSH server with key-based authentication
  - Sudo/become privileges configured

### Required Files
- `Infra_owner_demo/` repository with:
  - `frontend/` directory (application files)
  - `infra/docker-compose.yaml`
  - `infra/Dockerfile`
  - `infra/nginx.conf`

## Quick Start (5 Minutes)

### Step 1: Install Ansible Dependencies

```bash
# Install Ansible if not already installed
pip install ansible-core>=2.16

# Install community.docker collection
ansible-galaxy collection install -r requirements.yml
```

### Step 2: Configure Inventory

Create `inventory/hosts.ini`:

```ini
[web]
web1.example.com ansible_user=deploy
web2.example.com ansible_user=deploy

[web:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Step 3: Verify SSH Connectivity

```bash
# Test SSH connectivity to all web hosts
ansible web -i inventory/hosts.ini -m ping
```

Expected output:
```
web1.example.com | SUCCESS => {
    "ping": "pong"
}
web2.example.com | SUCCESS => {
    "ping": "pong"
}
```

### Step 4: Run Deployment (Dry Run First)

```bash
# Validate syntax
ansible-playbook playbooks/deploy_compose.yml --syntax-check

# Dry run (check mode)
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml --check --diff

# Actual deployment
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml
```

### Step 5: Verify Deployment

```bash
# Check service status
ansible web -i inventory/hosts.ini -m shell -a "cd /opt/infra_owner_demo && docker compose ps"

# Test HTTP endpoint
curl http://web1.example.com:80
```

## Configuration

### Default Variables (group_vars/all.yml)

```yaml
---
# Source and destination paths
repo_root: "./Infra_owner_demo"
remote_app_dir: "/opt/infra_owner_demo"
inventory_group: "web"

# Application configuration
http_port: 80

# File paths
compose_file_local: "{{ repo_root }}/infra/docker-compose.yaml"
dockerfile_local: "{{ repo_root }}/infra/Dockerfile"
nginx_conf_local: "{{ repo_root }}/infra/nginx.conf"

# Docker Compose options
compose_build: "always"
compose_pull: "missing"
compose_recreate: "smart"
compose_remove_orphans: true

# Health check settings
health_check_retries: 10
health_check_delay: 3
health_check_timeout: 30

# Rollback settings
rollback_enabled: true
keep_previous_images: true
```

### Customizing Deployment

Override variables via command line:

```bash
# Deploy to different port
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  -e "http_port=8080"

# Deploy from different source directory
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  -e "repo_root=/path/to/custom/repo"

# Deploy to different remote directory
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  -e "remote_app_dir=/opt/myapp"
```

## Common Operations

### Check Deployment Status

```bash
# View running containers
ansible web -i inventory/hosts.ini -m shell \
  -a "docker compose -f /opt/infra_owner_demo/docker-compose.yml ps"

# Check service health
ansible web -i inventory/hosts.ini -m uri \
  -a "url=http://localhost:80 status_code=200"
```

### Update Deployment

```bash
# Pull latest code changes
cd Infra_owner_demo
git pull

# Re-run playbook (idempotent)
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml
```

Expected result: Only changed files trigger updates, zero changes if nothing modified.

### Rollback Deployment

```bash
# Automatic rollback on failure
# (built into playbook via block/rescue)

# Manual rollback
ansible web -i inventory/hosts.ini -m shell \
  -a "cd /opt/infra_owner_demo && docker compose down"
```

### View Logs

```bash
# Ansible execution logs
cat logs/ansible-deployment.log

# Application logs
ansible web -i inventory/hosts.ini -m shell \
  -a "docker compose -f /opt/infra_owner_demo/docker-compose.yml logs --tail=100"
```

## MCP Integration

### Natural Language Commands

Example MCP interactions:

```
User: "Deploy the Infra_owner_demo website to the web servers"
→ Executes: ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml

User: "Check if the deployment is healthy"
→ Executes: ansible web -m uri -a "url=http://localhost:80"

User: "Show me the deployment logs"
→ Returns: Contents of logs/ansible-deployment.log

User: "Rollback the last deployment"
→ Executes: Rollback playbook with previous state restoration
```

### MCP Tool Parameters

```json
{
  "action": "deploy",
  "inventory_group": "web",
  "repo_root": "./Infra_owner_demo",
  "remote_app_dir": "/opt/infra_owner_demo",
  "http_port": 80,
  "dry_run": false
}
```

## Troubleshooting

### Problem: SSH Connection Failure

```bash
# Verify SSH key is loaded
ssh-add -l

# Test manual SSH connection
ssh deploy@web1.example.com

# Check Ansible connectivity with verbose output
ansible web -i inventory/hosts.ini -m ping -vvv
```

### Problem: Docker Not Installed

```bash
# Check if Docker installation task ran
grep "Install Docker" logs/ansible-deployment.log

# Manually verify Docker on target
ansible web -i inventory/hosts.ini -m shell -a "docker --version"
```

### Problem: Port Already in Use

```bash
# Check if port 80 is available
ansible web -i inventory/hosts.ini -m shell \
  -a "netstat -tuln | grep :80"

# Deploy to different port
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  -e "http_port=8080"
```

### Problem: Idempotency Violation (Changes on Second Run)

```bash
# Run playbook twice and compare
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml --diff

# Expected: Second run shows "changed=0"
# If not, check for:
# - File timestamps being modified
# - Random values in templates
# - Improper use of command/shell modules
```

### Problem: Health Check Timeout

```bash
# Increase timeout and retries
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  -e "health_check_retries=20" \
  -e "health_check_delay=5"

# Manually check service startup time
time docker compose up -d
docker compose ps
```

## Performance Tips

### Speed Up File Synchronization

```yaml
# In group_vars/all.yml or as extra-vars
synchronize_compress: yes
synchronize_rsync_opts:
  - "--compress"
  - "--itemize-changes"
```

### Parallel Execution

```bash
# Deploy to multiple servers simultaneously
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  --forks=10
```

### Skip Tags (Advanced)

```bash
# Skip Docker installation if already installed
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  --skip-tags=docker_install

# Only run health checks
ansible-playbook -i inventory/hosts.ini playbooks/deploy_compose.yml \
  --tags=health_check
```

## Security Best Practices

### SSH Key Management

```bash
# Use SSH agent for key management
eval $(ssh-agent)
ssh-add ~/.ssh/deploy_key

# Or use ansible-vault for encrypted keys
ansible-vault encrypt_string 'my_ssh_password' --name 'ansible_ssh_pass'
```

### Secrets Management

```yaml
# Store sensitive variables in encrypted vault
# group_vars/web/vault.yml (encrypted)
---
vault_docker_registry_password: "secretpassword"
vault_api_key: "api_key_value"

# Reference in playbook
docker_registry_password: "{{ vault_docker_registry_password }}"
```

### Sudo Without Password Prompt

```bash
# On target servers, configure sudoers
echo "deploy ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/deploy
sudo chmod 0440 /etc/sudoers.d/deploy
```

## Next Steps

1. **Customize Configuration**: Edit `group_vars/all.yml` with your specific paths and ports
2. **Add Monitoring**: Integrate with monitoring systems (Prometheus, Grafana)
3. **CI/CD Integration**: See [pipeline.md](../../docs/pipeline.md) for automation setup
4. **Production Hardening**: Review security checklist and implement additional controls
5. **Backup Strategy**: Implement regular backups of application data and configuration

## Related Documentation

- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Implementation plan
- [research.md](./research.md) - Technical decisions and research
- [data-model.md](./data-model.md) - Data structures and schemas
- [contracts/mcp-tool-api.json](./contracts/mcp-tool-api.json) - API specification

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Ansible logs in `logs/ansible-deployment.log`
3. Run playbook with `-vvv` flag for verbose output
4. Consult the [research.md](./research.md) document for design decisions
