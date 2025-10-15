#!/bin/bash
# Deployment Verification Script
# Verifies playbook structure and configuration without executing deployment

set -e

PROJECT_DIR="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"

echo "=== Ansible Deployment Verification ==="
echo ""

# Check project structure
echo "✓ Checking project structure..."
required_dirs=(
    "$PROJECT_DIR/playbooks"
    "$PROJECT_DIR/inventory"
    "$PROJECT_DIR/group_vars"
    "$PROJECT_DIR/logs"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir exists"
    else
        echo "  ✗ $dir missing"
        exit 1
    fi
done

# Check required files
echo ""
echo "✓ Checking required files..."
required_files=(
    "$PROJECT_DIR/ansible.cfg"
    "$PROJECT_DIR/requirements.yml"
    "$PROJECT_DIR/inventory/hosts.ini"
    "$PROJECT_DIR/group_vars/all.yml"
    "$PROJECT_DIR/group_vars/web.yml"
    "$PROJECT_DIR/playbooks/deploy_compose.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        exit 1
    fi
done

# Validate playbook syntax
echo ""
echo "✓ Validating playbook syntax..."
cd "$PROJECT_DIR"
if ansible-playbook --syntax-check playbooks/deploy_compose.yml &>/dev/null; then
    echo "  ✓ Playbook syntax is valid"
else
    echo "  ✗ Playbook syntax check failed"
    ansible-playbook --syntax-check playbooks/deploy_compose.yml
    exit 1
fi

# Check collections
echo ""
echo "✓ Checking Ansible collections..."
if ansible-galaxy collection list | grep -q "community.docker"; then
    version=$(ansible-galaxy collection list | grep community.docker | awk '{print $2}')
    echo "  ✓ community.docker collection installed (version: $version)"
else
    echo "  ⚠ community.docker collection not found"
    echo "    Run: ansible-galaxy collection install -r requirements.yml"
fi

# Display configuration
echo ""
echo "✓ Configuration summary:"
echo "  - Ansible config: $PROJECT_DIR/ansible.cfg"
echo "  - Inventory: $PROJECT_DIR/inventory/hosts.ini"
echo "  - Log file: $PROJECT_DIR/logs/ansible-deployment.log"

# Parse variables
echo ""
echo "✓ Deployment variables (from group_vars/all.yml):"
grep -E "^[a-z_]+:" "$PROJECT_DIR/group_vars/all.yml" | head -10

echo ""
echo "=== Verification Complete ==="
echo ""
echo "To deploy, run:"
echo "  cd $PROJECT_DIR"
echo "  ansible-playbook playbooks/deploy_compose.yml"
echo ""
echo "For localhost with sudo:"
echo "  ansible-playbook playbooks/deploy_compose.yml --ask-become-pass"
echo ""
