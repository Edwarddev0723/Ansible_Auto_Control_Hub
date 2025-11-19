#!/bin/bash
# 測試 MCP 專案註冊功能

set -e

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"
MCP_DIR="$PROJECT_ROOT/mcp-ansible"
PROJECTS_DIR="$HOME/.ansible-mcp/projects"

echo "=== 測試 MCP 專案註冊 ==="
echo ""

# 1. 創建專案配置目錄
mkdir -p "$PROJECTS_DIR"
echo "✓ 專案目錄已創建: $PROJECTS_DIR"

# 2. 創建專案配置檔
PROJECT_CONFIG="$PROJECTS_DIR/infra_owner_deploy.json"
echo "📝 創建專案配置檔..."
cat > "$PROJECT_CONFIG" << EOF
{
  "name": "infra_owner_deploy",
  "root": "$ANSIBLE_PROJECT",
  "inventory": "$ANSIBLE_PROJECT/inventory/hosts.ini",
  "playbooks_path": "$ANSIBLE_PROJECT/playbooks",
  "roles_paths": ["$ANSIBLE_PROJECT/roles"],
  "default": true
}
EOF
echo "✓ 專案配置已創建: $PROJECT_CONFIG"
echo ""

# 3. 顯示配置內容
echo "📋 配置內容："
cat "$PROJECT_CONFIG"
echo ""

# 4. 使用 MCP 工具註冊專案
echo "🔧 使用 MCP register-project 工具註冊專案..."
cd "$MCP_DIR"
source .venv/bin/activate

export MCP_ANSIBLE_PROJECT_ROOT="$ANSIBLE_PROJECT"
export MCP_ANSIBLE_INVENTORY="$ANSIBLE_PROJECT/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"
export MCP_ANSIBLE_PROJECTS_DIR="$PROJECTS_DIR"

python3 << 'PYEOF'
import asyncio
import sys
import os
sys.path.insert(0, 'src')

from ansible_mcp.server import mcp

async def register_project():
    print("\n📊 可用的工具:")
    tools = await mcp.list_tools()
    register_tool = None
    for tool in tools:
        if tool.name == "register-project":
            register_tool = tool
            print(f"  ✓ 找到 register-project 工具")
            break
    
    if not register_tool:
        print("  ❌ 未找到 register-project 工具")
        return False
    
    print("\n🔧 註冊專案...")
    
    # 調用 register-project 工具
    try:
        from ansible_mcp.server import register_project
        result = register_project(
            name="infra_owner_deploy",
            root=os.environ['MCP_ANSIBLE_PROJECT_ROOT'],
            inventory=os.environ['MCP_ANSIBLE_INVENTORY'],
            make_default=True
        )
        
        print(f"\n✅ 註冊結果:")
        print(f"  - 成功: {result.get('ok', False)}")
        if result.get('ok'):
            print(f"  - 專案名稱: {result.get('name')}")
            print(f"  - 根目錄: {result.get('root')}")
            print(f"  - Inventory: {result.get('inventory')}")
            print(f"  - 預設專案: {result.get('default', False)}")
        else:
            print(f"  - 錯誤: {result.get('error', 'Unknown error')}")
        
        return result.get('ok', False)
    except Exception as e:
        print(f"❌ 註冊失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

success = asyncio.run(register_project())
sys.exit(0 if success else 1)
PYEOF

RESULT=$?

cd - > /dev/null

echo ""
if [ $RESULT -eq 0 ]; then
    echo "╭──────────────────────────────────────────────────────╮"
    echo "│ ✅ 專案註冊測試成功！                                │"
    echo "├──────────────────────────────────────────────────────┤"
    echo "│ 現在可以使用 ollmcp 執行：                           │"
    echo "│   • 執行專案 infra_owner_deploy 的 playbook         │"
    echo "│   • 顯示專案 infra_owner_deploy 的主機清單          │"
    echo "│   • 驗證專案 infra_owner_deploy 的 playbook 語法    │"
    echo "╰──────────────────────────────────────────────────────╯"
else
    echo "╭──────────────────────────────────────────────────────╮"
    echo "│ ❌ 專案註冊測試失敗                                  │"
    echo "├──────────────────────────────────────────────────────┤"
    echo "│ 請檢查：                                             │"
    echo "│   • MCP Server 虛擬環境是否正確設置                 │"
    echo "│   • 專案路徑是否正確                                 │"
    echo "│   • 環境變數是否正確設定                             │"
    echo "╰──────────────────────────────────────────────────────╯"
fi

exit $RESULT
