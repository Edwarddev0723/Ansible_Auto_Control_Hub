#!/bin/bash
# 一鍵啟動 MCP + Ollama 環境
# 用途：啟動 Ollama 服務和 MCP Ansible Server 以支援自然語言部署

set -e

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
MCP_DIR="$PROJECT_ROOT/mcp-ansible"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"

echo "=== 啟動 MCP + Ollama 環境 ==="
echo ""

# 1. 檢查 Ollama 是否已安裝
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama 未安裝"
    echo "請執行: brew install ollama"
    echo "或訪問: https://ollama.ai/download"
    exit 1
fi

# 2. 啟動 Ollama 服務（如果未運行）
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 啟動 Ollama 服務..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "✓ Ollama 服務已啟動"
else
    echo "✓ Ollama 服務已在運行"
fi

# 3. 檢查是否有下載模型
if ! ollama list | grep -q "llama"; then
    echo "⚠️  未找到 LLM 模型"
    echo "建議執行: ollama pull llama3.1"
    read -p "現在下載 llama3.1 嗎？(y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ollama pull llama3.1
    fi
fi

# 4. 檢查 MCP Server 目錄
if [ ! -d "$MCP_DIR" ]; then
    echo "❌ MCP Ansible Server 目錄不存在: $MCP_DIR"
    exit 1
fi

# 5. 檢查虛擬環境
cd "$MCP_DIR"
if [ ! -d ".venv" ]; then
    echo "🔧 建立 Python 虛擬環境..."
    python3 -m venv .venv
fi

# 6. 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source .venv/bin/activate

# 7. 安裝/更新依賴
echo "📦 檢查依賴..."
if [ -f "requirements.txt" ]; then
    pip install -q -U pip
    pip install -q -r requirements.txt
fi

# 8. 設定環境變數
echo "⚙️  設定環境變數..."
export MCP_ANSIBLE_PROJECT_ROOT="$ANSIBLE_PROJECT"
export MCP_ANSIBLE_INVENTORY="$ANSIBLE_PROJECT/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"

# 9. 驗證配置
echo ""
echo "=== 配置摘要 ==="
echo "Ollama 狀態: ✓ 運行中"
echo "MCP Server: $MCP_DIR"
echo "Ansible 專案: $MCP_ANSIBLE_PROJECT_ROOT"
echo "清單檔案: $MCP_ANSIBLE_INVENTORY"
echo ""

# 10. 顯示下一步
echo "=== 下一步 ==="
echo ""
echo "1️⃣  配置 Claude Desktop (推薦):"
echo "   編輯: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo '   {
     "mcpServers": {
       "ansible-mcp": {
         "command": "python",
         "args": ["'$MCP_DIR'/src/ansible_mcp/server.py"],
         "env": {
           "MCP_ANSIBLE_PROJECT_ROOT": "'$ANSIBLE_PROJECT'",
           "MCP_ANSIBLE_INVENTORY": "'$ANSIBLE_PROJECT'/inventory/hosts.ini",
           "MCP_ANSIBLE_PROJECT_NAME": "infra_owner_deploy"
         }
       }
     }
   }'
echo ""
echo "2️⃣  或手動啟動 MCP Server:"
echo "   python src/ansible_mcp/server.py"
echo ""
echo "3️⃣  測試自然語言指令:"
echo '   "部署 Infra_owner_demo 到 web 伺服器"'
echo ""
echo "4️⃣  使用 MCP Inspector 測試:"
echo "   npx @modelcontextprotocol/inspector python src/ansible_mcp/server.py"
echo ""

# 11. 詢問是否啟動 MCP Server
read -p "現在啟動 MCP Server？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 啟動 MCP Ansible Server..."
    python src/ansible_mcp/server.py
else
    echo ""
    echo "✓ 環境已準備就緒"
    echo "執行以下命令啟動 MCP Server:"
    echo "  cd $MCP_DIR"
    echo "  source .venv/bin/activate"
    echo "  python src/ansible_mcp/server.py"
fi
