#!/bin/bash
# 測試 ollmcp 與 MCP Ansible Server 連接

echo "=== ollmcp 連接測試 ==="
echo ""

# 方案 1: 使用 JSON 配置檔
echo "方案 1: JSON 配置檔"
echo "創建配置檔..."
CONFIG_FILE="$HOME/.config/ollmcp/test-servers.json"
mkdir -p "$(dirname "$CONFIG_FILE")"

cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "ansible-mcp": {
      "command": "python3",
      "args": [
        "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src/ansible_mcp/server.py"
      ],
      "env": {
        "MCP_ANSIBLE_PROJECT_ROOT": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy",
        "MCP_ANSIBLE_INVENTORY": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini",
        "MCP_ANSIBLE_PROJECT_NAME": "infra_owner_deploy"
      }
    }
  }
}
EOF

echo "✓ 配置檔已創建: $CONFIG_FILE"
echo ""
echo "執行指令:"
echo "  ollmcp --servers-json $CONFIG_FILE --model gpt-oss:20b"
echo ""

# 方案 2: 使用包裝腳本
echo "方案 2: 包裝腳本"
echo "執行指令:"
echo "  ollmcp --mcp-server /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/run_server.sh --model gpt-oss:20b"
echo ""

# 方案 3: Claude Desktop 配置（自動探索）
echo "方案 3: Claude Desktop 自動探索"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CLAUDE_CONFIG" ]; then
    echo "✓ Claude 配置存在: $CLAUDE_CONFIG"
    echo "執行指令:"
    echo "  ollmcp --auto-discovery --model gpt-oss:20b"
else
    echo "⚠️  Claude 配置不存在，創建中..."
    mkdir -p "$(dirname "$CLAUDE_CONFIG")"
    cat > "$CLAUDE_CONFIG" << 'EOFCLAUDE'
{
  "mcpServers": {
    "ansible-mcp": {
      "command": "python3",
      "args": [
        "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src/ansible_mcp/server.py"
      ],
      "env": {
        "MCP_ANSIBLE_PROJECT_ROOT": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy",
        "MCP_ANSIBLE_INVENTORY": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini",
        "MCP_ANSIBLE_PROJECT_NAME": "infra_owner_deploy"
      }
    }
  }
}
EOFCLAUDE
    echo "✓ Claude 配置已創建: $CLAUDE_CONFIG"
    echo "執行指令:"
    echo "  ollmcp --auto-discovery --model gpt-oss:20b"
fi

echo ""
echo "=== 推薦使用方案 1 (JSON 配置檔) ==="
echo ""
echo "現在執行方案 1..."
read -p "按 Enter 繼續，或 Ctrl+C 取消..."

ollmcp --servers-json "$CONFIG_FILE" --model gpt-oss:20b
