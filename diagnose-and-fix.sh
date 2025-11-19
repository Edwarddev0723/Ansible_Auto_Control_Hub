#!/bin/bash
# 快速診斷和修復 ollmcp 連接問題

set -e

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
MCP_SERVER="$PROJECT_ROOT/mcp-ansible/src/ansible_mcp/server.py"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"
CONFIG_FILE="$HOME/.config/ollmcp/servers.json"

echo "=== ollmcp 診斷與修復 ==="
echo ""

# 1. 檢查 ollmcp 是否已安裝
echo "🔍 檢查 ollmcp..."
if command -v ollmcp &> /dev/null; then
    echo "✓ ollmcp 已安裝: $(which ollmcp)"
else
    echo "❌ ollmcp 未安裝"
    read -p "現在安裝? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        pip install --upgrade ollmcp
    else
        exit 1
    fi
fi

# 2. 檢查 Ollama
echo ""
echo "🔍 檢查 Ollama..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama 未運行，啟動中..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi
echo "✓ Ollama 運行中"

# 3. 檢查模型
echo ""
echo "🔍 檢查模型..."
if ollama list | grep -q "gpt-oss:20b"; then
    echo "✓ gpt-oss:20b 已下載"
elif ollama list | grep -q "qwen2.5"; then
    echo "✓ qwen2.5 已下載（使用此模型）"
    MODEL="qwen2.5:7b"
else
    echo "⚠️  建議模型未找到"
    MODEL="qwen2.5:7b"
fi

# 4. 檢查 MCP Server
echo ""
echo "🔍 檢查 MCP Server..."
if [ -f "$MCP_SERVER" ]; then
    echo "✓ MCP Server 存在: $MCP_SERVER"
else
    echo "❌ MCP Server 不存在"
    exit 1
fi

# 5. 測試 MCP Server 可執行性
echo ""
echo "🔍 測試 MCP Server..."
cd "$PROJECT_ROOT/mcp-ansible"
if [ -d ".venv" ]; then
    source .venv/bin/activate
    if python3 -c "from mcp.server.fastmcp import FastMCP; print('OK')" 2>&1 | grep -q "OK"; then
        echo "✓ MCP Server 依賴正常"
    else
        echo "❌ MCP Server 依賴有問題"
        echo "嘗試重新安裝..."
        pip install -q -r requirements.txt
    fi
else
    echo "⚠️  虛擬環境不存在，創建中..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -U pip
    pip install -q -r requirements.txt
    pip install -q -e .
fi

# 6. 創建配置檔
echo ""
echo "📝 創建 MCP Server 配置檔..."
mkdir -p "$(dirname "$CONFIG_FILE")"

cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "ansible-mcp": {
      "command": "python3",
      "args": [
        "$MCP_SERVER"
      ],
      "env": {
        "MCP_ANSIBLE_PROJECT_ROOT": "$ANSIBLE_PROJECT",
        "MCP_ANSIBLE_INVENTORY": "$ANSIBLE_PROJECT/inventory/hosts.ini",
        "MCP_ANSIBLE_PROJECT_NAME": "infra_owner_deploy",
        "PYTHONPATH": "$PROJECT_ROOT/mcp-ansible/src"
      }
    }
  }
}
EOF

echo "✓ 配置檔已創建: $CONFIG_FILE"

# 7. 顯示配置內容
echo ""
echo "📋 配置內容："
cat "$CONFIG_FILE"

# 8. 測試配置檔
echo ""
echo "🧪 測試 JSON 配置檔有效性..."
if python3 -m json.tool "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "✓ JSON 格式正確"
else
    echo "❌ JSON 格式錯誤"
    exit 1
fi

# 9. 提示啟動資訊
echo ""
echo "╭─────────────────────────────────────────────────────────────╮"
echo "│ ✅ 診斷完成，準備啟動 ollmcp                               │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ 配置檔: $CONFIG_FILE"
echo "│ 模型: ${MODEL:-gpt-oss:20b}"
echo "│ MCP Server: ansible-mcp"
echo "│ 預期工具數: 8"
echo "╰─────────────────────────────────────────────────────────────╯"
echo ""
echo "💡 啟動後應顯示: 'Connected to 1 server(s) with 8 tool(s)'"
echo ""
echo "🎯 測試指令："
echo "   1. 按 't' → 應顯示 8 個 Ansible 工具"
echo "   2. 輸入: 驗證 playbook 語法"
echo "   3. 輸入: 顯示所有主機清單"
echo ""

# 10. 詢問是否啟動
read -p "現在啟動 ollmcp? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "🚀 啟動 ollmcp..."
    echo ""
    ollmcp --servers-json "$CONFIG_FILE" --model "${MODEL:-gpt-oss:20b}"
else
    echo ""
    echo "手動啟動指令:"
    echo "  ollmcp --servers-json $CONFIG_FILE --model ${MODEL:-gpt-oss:20b}"
fi
