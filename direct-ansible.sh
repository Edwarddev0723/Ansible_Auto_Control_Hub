#!/bin/bash
# 繞過 ollmcp，直接使用 MCP Server 執行 Ansible 任務

set -e

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
MCP_DIR="$PROJECT_ROOT/mcp-ansible"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"

echo "╭──────────────────────────────────────────────────────────╮"
echo "│ 直接執行 Ansible Playbook (繞過 ollmcp)                 │"
echo "╰──────────────────────────────────────────────────────────╯"
echo ""

cd "$MCP_DIR"
source .venv/bin/activate

export MCP_ANSIBLE_PROJECT_ROOT="$ANSIBLE_PROJECT"
export MCP_ANSIBLE_INVENTORY="$ANSIBLE_PROJECT/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"

# 選擇操作
echo "請選擇操作："
echo "  1) 驗證 playbook 語法"
echo "  2) 執行 playbook"
echo "  3) 查看主機清單"
echo "  4) 測試主機連通性"
echo "  5) 註冊專案"
echo ""
read -p "請輸入選項 (1-5): " choice

case $choice in
  1)
    echo ""
    echo "🔍 驗證 playbook 語法..."
    python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from ansible_mcp.server import validate_playbook
import os

result = validate_playbook(
    playbook_path=os.path.join(
        os.environ['MCP_ANSIBLE_PROJECT_ROOT'],
        'playbooks/deploy_compose.yml'
    )
)

if result['ok'] and result.get('valid'):
    print("\n✅ Playbook 語法正確！")
else:
    print(f"\n❌ 語法錯誤：{result.get('error', 'Unknown error')}")
    if result.get('stderr'):
        print(f"錯誤訊息：\n{result['stderr']}")
EOF
    ;;

  2)
    echo ""
    echo "🚀 執行 playbook..."
    read -p "是否需要 sudo 密碼？(y/N) " need_sudo
    
    python3 << EOF
import sys
sys.path.insert(0, 'src')
from ansible_mcp.server import ansible_playbook
import os

playbook_path = os.path.join(
    os.environ['MCP_ANSIBLE_PROJECT_ROOT'],
    'playbooks/deploy_compose.yml'
)
inventory = os.environ['MCP_ANSIBLE_INVENTORY']

print(f"\n執行: {playbook_path}")
print(f"Inventory: {inventory}\n")

result = ansible_playbook(
    playbook_path=playbook_path,
    inventory=inventory,
    verbose=1
)

print(f"\n{'='*60}")
if result['ok']:
    print("✅ Playbook 執行成功！")
    print(f"RC: {result['rc']}")
    if result.get('stdout'):
        print(f"\n輸出：\n{result['stdout']}")
else:
    print("❌ Playbook 執行失敗！")
    print(f"錯誤：{result.get('error', 'Unknown error')}")
    if result.get('stderr'):
        print(f"\n錯誤訊息：\n{result['stderr']}")
print(f"{'='*60}\n")
EOF
    ;;

  3)
    echo ""
    echo "📋 查看主機清單..."
    python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from ansible_mcp.server import ansible_inventory
import os
import json

result = ansible_inventory(
    inventory=os.environ['MCP_ANSIBLE_INVENTORY'],
    include_hostvars=True
)

if result['ok']:
    print("\n✅ 主機清單：")
    print(f"\n主機：")
    for host in result.get('hosts', []):
        print(f"  • {host}")
    print(f"\n群組：")
    for group, hosts in result.get('groups', {}).items():
        print(f"  • {group}: {', '.join(hosts)}")
else:
    print(f"\n❌ 錯誤：{result.get('error', 'Unknown error')}")
EOF
    ;;

  4)
    echo ""
    echo "🏓 測試主機連通性..."
    python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from ansible_mcp.server import ansible_ping
import os

result = ansible_ping(
    host_pattern='all',
    inventory=os.environ['MCP_ANSIBLE_INVENTORY']
)

if result['ok']:
    print("\n✅ Ping 結果：")
    if result.get('stdout'):
        print(result['stdout'])
else:
    print(f"\n❌ Ping 失敗：{result.get('error', 'Unknown error')}")
    if result.get('stderr'):
        print(f"\n錯誤訊息：\n{result['stderr']}")
EOF
    ;;

  5)
    echo ""
    echo "📝 註冊專案..."
    python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from ansible_mcp.server import register_project
import os

result = register_project(
    name='infra_owner_deploy',
    root=os.environ['MCP_ANSIBLE_PROJECT_ROOT'],
    inventory=os.environ['MCP_ANSIBLE_INVENTORY'],
    make_default=True
)

if result['ok']:
    print("\n✅ 專案註冊成功！")
    print(f"名稱：{result.get('name')}")
    print(f"根目錄：{result.get('root')}")
    print(f"Inventory：{result.get('inventory')}")
    print(f"預設專案：{result.get('default', False)}")
else:
    print(f"\n❌ 註冊失敗：{result.get('error', 'Unknown error')}")
EOF
    ;;

  *)
    echo "❌ 無效的選項"
    exit 1
    ;;
esac

echo ""
cd - > /dev/null
