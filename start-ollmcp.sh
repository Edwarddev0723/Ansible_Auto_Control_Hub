#!/bin/bash
# ollmcp 自動啟動腳本 - 使用 ollmcp 連接 Ansible MCP Server
# 用途：透過互動式 TUI 用自然語言控制 Ansible 部署

set -e

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
MCP_SERVER="$PROJECT_ROOT/mcp-ansible/src/ansible_mcp/server.py"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"

echo "=== 啟動 ollmcp + Ansible MCP ==="
echo ""

# 1. 檢查 Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama 未安裝"
    echo "請執行: brew install ollama"
    echo "或訪問: https://ollama.ai/download"
    exit 1
fi

# 2. 啟動 Ollama 服務
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 啟動 Ollama 服務..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "✓ Ollama 服務已啟動"
else
    echo "✓ Ollama 服務已在運行"
fi

# 3. 檢查是否有下載模型
RECOMMENDED_MODEL="gpt-oss:20b"
if ! ollama list | grep -q "gpt-oss:20b"; then
    echo "⚠️  未找到推薦模型: $RECOMMENDED_MODEL"
    read -p "現在下載 $RECOMMENDED_MODEL 嗎？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "📦 下載模型（這可能需要幾分鐘）..."
        ollama pull $RECOMMENDED_MODEL
    else
        echo "提示：您可以稍後手動下載: ollama pull $RECOMMENDED_MODEL"
    fi
fi

# 4. 檢查 ollmcp 是否已安裝
if ! command -v ollmcp &> /dev/null; then
    echo "⚠️  ollmcp 未安裝"
    read -p "使用 pip 安裝 ollmcp？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "📦 安裝 ollmcp..."
        pip install --upgrade ollmcp
    else
        echo "❌ 無法繼續，請先安裝 ollmcp: pip install ollmcp"
        exit 1
    fi
fi

# 5. 檢查 MCP Server 路徑
if [ ! -f "$MCP_SERVER" ]; then
    echo "❌ MCP Ansible Server 不存在: $MCP_SERVER"
    echo "請確認 mcp-ansible 專案已正確安裝"
    exit 1
fi

# 6. 檢查 MCP Server 依賴
MCP_DIR="$PROJECT_ROOT/mcp-ansible"
if [ ! -d "$MCP_DIR/.venv" ]; then
    echo "🔧 建立 MCP Server 虛擬環境..."
    cd "$MCP_DIR"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -U pip
    pip install -q -r requirements.txt
    pip install -q -e .
    cd - > /dev/null
fi

# 7. 創建專案配置目錄並註冊專案
PROJECTS_DIR="$HOME/.ansible-mcp/projects"
mkdir -p "$PROJECTS_DIR"

PROJECT_CONFIG="$PROJECTS_DIR/infra_owner_deploy.json"
echo "📝 註冊 Ansible 專案到 MCP..."
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
echo "✓ 專案已註冊: $PROJECT_CONFIG"

# 8. 設定環境變數
echo "⚙️  設定環境變數..."
export MCP_ANSIBLE_PROJECT_ROOT="$ANSIBLE_PROJECT"
export MCP_ANSIBLE_INVENTORY="$ANSIBLE_PROJECT/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"
export MCP_ANSIBLE_PROJECTS_DIR="$PROJECTS_DIR"

# 9. 顯示配置摘要
echo ""
echo "╭─────────────────────────────────────────────────────────────╮"
echo "│ 配置摘要                                                    │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ Ollama 狀態: ✓ 運行中                                      │"
printf "│ MCP Server: %-47s │\n" "$(basename $MCP_SERVER)"
printf "│ 專案名稱: %-49s │\n" "infra_owner_deploy"
printf "│ 專案路徑: %-47s │\n" "$(basename $ANSIBLE_PROJECT)"
printf "│ 清單檔案: %-47s │\n" "inventory/hosts.ini"
printf "│ 預設 Playbook: %-42s │\n" "deploy_compose.yml"
printf "│ 模型: %-51s │\n" "$RECOMMENDED_MODEL"
echo "╰─────────────────────────────────────────────────────────────╯"
echo ""

# 10. 提示使用資訊
echo "💡 使用提示："
echo "   - 輸入 'help' 查看所有指令"
echo "   - 輸入 'tools' 管理可用工具"
echo "   - 輸入 'model' 切換 LLM 模型"
echo "   - 按 Ctrl+D 或輸入 'quit' 退出"
echo ""
echo "🎯 範例指令（專案已註冊，直接使用）："
echo "   - 執行專案 infra_owner_deploy 的 deploy_compose.yml"
echo "   - 驗證專案 infra_owner_deploy 的 playbook 語法"
echo "   - 顯示專案 infra_owner_deploy 的主機清單"
echo "   - 檢查 web 群組的 Docker 服務狀態"
echo ""

# 11. 創建 MCP Server 配置檔
CONFIG_FILE="$HOME/.config/ollmcp/servers.json"
mkdir -p "$(dirname "$CONFIG_FILE")"

echo "📝 創建 MCP Server 配置檔..."
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "ansible-mcp": {
      "command": "python3",
      "args": [
        "$MCP_SERVER"
      ],
      "env": {
        "MCP_ANSIBLE_PROJECT_ROOT": "$MCP_ANSIBLE_PROJECT_ROOT",
        "MCP_ANSIBLE_INVENTORY": "$MCP_ANSIBLE_INVENTORY",
        "MCP_ANSIBLE_PROJECT_NAME": "$MCP_ANSIBLE_PROJECT_NAME",
        "MCP_ANSIBLE_PROJECTS_DIR": "$PROJECTS_DIR",
        "PYTHONPATH": "$MCP_DIR/src"
      }
    }
  }
}
EOF

echo "✓ 配置檔已創建: $CONFIG_FILE"
echo ""

# 12. 驗證專案配置
echo "� 驗證專案配置..."
if [ -f "$PROJECT_CONFIG" ]; then
    echo "✓ 專案配置檔存在"
    echo "  位置: $PROJECT_CONFIG"
else
    echo "❌ 專案配置檔不存在"
    exit 1
fi
echo ""

# 13. 啟動 ollmcp
echo "🚀 啟動 ollmcp..."
echo "   按 't' 查看 38 個可用工具"
echo "   按 'h' 查看所有指令"
echo "   輸入 'hil' 可關閉確認提示"
echo ""
ollmcp --servers-json "$CONFIG_FILE" --model $RECOMMENDED_MODEL
