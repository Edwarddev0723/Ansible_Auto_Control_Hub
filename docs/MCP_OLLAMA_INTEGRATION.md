# MCP + Ollama 整合指南：控制 Ansible 部署

## 📋 概述

本指南說明如何使用 **Ollama** 透過 **MCP (Model Context Protocol)** 來自然語言控制 Ansible Docker Compose 部署。

---

## 🏗️ 架構說明

```
┌─────────────┐        ┌──────────────┐        ┌─────────────────┐
│   Ollama    │◄──────►│  MCP Server  │◄──────►│ Ansible Playbook│
│  (LLM 模型) │  MCP   │ (ansible-mcp)│ 執行   │  (deploy_compose)│
└─────────────┘  協定  └──────────────┘        └─────────────────┘
      ▲                                                 │
      │                                                 │
      │ 自然語言                                        ▼
      │ "部署應用程式到 web 伺服器"               ┌──────────────┐
      │                                           │ Docker Compose│
  ┌───┴────┐                                     │  容器部署      │
  │  使用者 │                                     └──────────────┘
  └────────┘
```

---

## 🚀 設定步驟

### 步驟 1: 安裝 Ollama

```bash
# macOS (使用 Homebrew)
brew install ollama

# 或下載安裝程式
# https://ollama.ai/download

# 啟動 Ollama 服務
ollama serve
```

### 步驟 2: 下載 LLM 模型

```bash
# 推薦模型（選擇一個）
ollama pull llama3.1          # Meta Llama 3.1 (8B)
ollama pull codellama         # Code Llama (7B) - 適合程式碼
ollama pull qwen2.5-coder     # Qwen 2.5 Coder - 適合技術任務

# 驗證模型已下載
ollama list
```

### 步驟 3: 設定 MCP Ansible Server

```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible

# 建立 Python 虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install -U pip
pip install -r requirements.txt

# 本地安裝 MCP server
pip install -e .
```

### 步驟 4: 配置環境變數

創建 `.env` 檔案：

```bash
cat > /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/.env << 'EOF'
# MCP Ansible Server 環境變數
export MCP_ANSIBLE_PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"
export MCP_ANSIBLE_INVENTORY="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"
EOF
```

載入環境變數：

```bash
source /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/.env
```

---

## 🔧 整合方式

### 方式 1: Claude Desktop 整合（推薦）

編輯 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "ansible-mcp": {
      "command": "python",
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
```

**重啟 Claude Desktop** 後即可使用！

### 方式 2: VS Code + Cursor 整合

編輯 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "ansible-mcp": {
      "command": "python",
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
```

### 方式 3: 命令列直接測試

使用 MCP Inspector 測試：

```bash
# 安裝 MCP Inspector
npm install -g @modelcontextprotocol/inspector

# 啟動 Inspector
npx @modelcontextprotocol/inspector \
  python \
  /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src/ansible_mcp/server.py
```

---

## 💬 自然語言互動範例

### 基本部署指令

**使用者輸入（自然語言）：**

```
部署 Infra_owner_demo 應用程式到 web 伺服器群組
```

**MCP 會自動執行：**

```bash
ansible-playbook \
  -i /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini \
  /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml
```

### 進階部署指令

**1. 自訂埠號部署**

```
部署應用程式到 web 伺服器，使用埠號 8080
```

MCP 執行：
```bash
ansible-playbook playbooks/deploy_compose.yml -e "http_port=8080"
```

**2. 檢查部署狀態**

```
檢查 web 伺服器上的 Docker Compose 服務狀態
```

MCP 執行：
```bash
ansible web -m shell -a "docker compose -f /opt/infra_owner_demo/docker-compose.yml ps"
```

**3. 驗證健康狀態**

```
驗證 web 伺服器的 HTTP 端點是否正常
```

MCP 執行：
```bash
ansible web -m uri -a "url=http://localhost:80 method=GET status_code=200"
```

**4. 回滾部署**

```
回滾上一次的部署
```

MCP 執行：
```bash
ansible-playbook playbooks/deploy_compose.yml --tags rollback
```

### 管理指令

**5. 查看清單**

```
顯示所有 web 群組的伺服器
```

MCP 執行：
```bash
ansible-inventory --list -i inventory/hosts.ini
```

**6. 驗證 Playbook**

```
驗證部署 Playbook 的語法
```

MCP 執行：
```bash
ansible-playbook --syntax-check playbooks/deploy_compose.yml
```

**7. 乾運行**

```
執行部署的乾運行測試
```

MCP 執行：
```bash
ansible-playbook playbooks/deploy_compose.yml --check
```

---

## 🛠️ MCP Server 可用工具

MCP Ansible Server 提供以下工具（自動透過自然語言映射）：

| 工具名稱 | 功能 | 自然語言範例 |
|---------|------|-------------|
| `ansible-playbook` | 執行 Playbook | "執行部署 playbook" |
| `validate-playbook` | 驗證語法 | "檢查 playbook 語法" |
| `ansible-task` | 執行 ad-hoc 任務 | "在 web 伺服器執行 ping" |
| `ansible-inventory` | 列出清單 | "顯示所有主機" |
| `create-playbook` | 建立 Playbook | "建立一個安裝 nginx 的 playbook" |
| `ansible-role` | 執行 Role | "執行 docker_setup role" |
| `register-project` | 註冊專案 | "註冊這個 Ansible 專案" |

---

## 📝 實際使用流程

### 完整部署對話範例

```
👤 使用者: 我想部署 Infra_owner_demo 到 web 伺服器

🤖 Ollama (透過 MCP):
好的，我會幫您部署。首先讓我驗證 playbook 語法...

[執行] validate-playbook playbooks/deploy_compose.yml
✓ 語法檢查通過

現在開始部署...

[執行] ansible-playbook playbooks/deploy_compose.yml

部署步驟：
1. ✓ 更新套件快取
2. ✓ 安裝 Docker 和 Docker Compose
3. ✓ 建立應用目錄 /opt/infra_owner_demo
4. ✓ 同步 frontend 檔案
5. ✓ 複製 docker-compose.yml, Dockerfile, nginx.conf
6. ✓ 建置並啟動 Docker Compose 服務
7. ✓ 健康檢查通過 (HTTP 200)

部署完成！
- 服務狀態: 運行中
- HTTP 端點: http://localhost:80
- 日誌: logs/ansible-deployment.log

👤 使用者: 檢查部署狀態

🤖 Ollama:
[執行] ansible web -m shell -a "docker compose ps"

服務狀態:
- nginx-frontend: Up (healthy) - 0.0.0.0:80->80/tcp

👤 使用者: 測試 HTTP 端點

🤖 Ollama:
[執行] ansible web -m uri -a "url=http://localhost:80"

HTTP 檢查結果:
- 狀態碼: 200 OK
- 回應時間: 0.05 秒
- 內容長度: 1234 bytes

✓ 應用程式運行正常！
```

---

## 🔍 除錯與監控

### 查看 MCP Server 日誌

```bash
# 啟動 MCP Server 時顯示詳細日誌
python src/ansible_mcp/server.py --verbose
```

### 測試 MCP 連線

```bash
# 使用 MCP CLI 測試工具
mcp dev /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src/ansible_mcp/server.py
```

### 查看 Ansible 執行日誌

```bash
# 即時監控部署日誌
tail -f /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/logs/ansible-deployment.log
```

---

## 🎯 快速開始腳本

創建一鍵啟動腳本：

```bash
cat > /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/start-mcp-ollama.sh << 'EOF'
#!/bin/bash
# 一鍵啟動 MCP + Ollama 環境

set -e

echo "=== 啟動 MCP + Ollama 環境 ==="

# 1. 啟動 Ollama 服務（如果未運行）
if ! pgrep -x "ollama" > /dev/null; then
    echo "啟動 Ollama 服務..."
    ollama serve &
    sleep 3
fi

# 2. 進入 MCP 專案目錄
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible

# 3. 啟動虛擬環境
source .venv/bin/activate

# 4. 載入環境變數
export MCP_ANSIBLE_PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"
export MCP_ANSIBLE_INVENTORY="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"

# 5. 啟動 MCP Server
echo "啟動 MCP Ansible Server..."
python src/ansible_mcp/server.py

EOF

chmod +x /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/start-mcp-ollama.sh
```

使用方式：

```bash
./start-mcp-ollama.sh
```

---

## 📚 進階整合：建立自訂 MCP 工具

您可以擴展 MCP Server 來新增自訂工具：

```python
# 在 mcp-ansible/src/ansible_mcp/server.py 中新增

@mcp.tool()
def deploy_infra_owner(http_port: int = 80) -> dict:
    """
    部署 Infra_owner_demo 應用程式到 web 伺服器
    
    Args:
        http_port: HTTP 服務埠號（預設: 80）
    
    Returns:
        部署結果摘要
    """
    playbook_path = Path(os.environ['MCP_ANSIBLE_PROJECT_ROOT']) / 'playbooks/deploy_compose.yml'
    inventory_path = Path(os.environ['MCP_ANSIBLE_INVENTORY'])
    
    cmd = [
        'ansible-playbook',
        '-i', str(inventory_path),
        str(playbook_path),
        '-e', f'http_port={http_port}'
    ]
    
    returncode, stdout, stderr = _run_command(cmd)
    
    return {
        'success': returncode == 0,
        'output': stdout,
        'errors': stderr if returncode != 0 else None
    }
```

---

## ✅ 驗證整合

### 測試 MCP 整合

```bash
# 1. 啟動 MCP Server
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible
source .venv/bin/activate
python src/ansible_mcp/server.py &

# 2. 在另一個終端測試 Ollama
ollama run llama3.1 "列出所有可用的 MCP 工具"

# 3. 測試自然語言部署
ollama run llama3.1 "使用 Ansible 部署 Docker Compose 應用程式到 web 伺服器"
```

---

## 🎓 學習資源

- **MCP 文件**: https://modelcontextprotocol.io/
- **Ollama 文件**: https://ollama.ai/
- **Ansible MCP Server**: https://github.com/bsahane/mcp-ansible
- **本專案 API 規格**: `specs/002-mcp-ansible-infra/contracts/mcp-tool-api.json`

---

## 🆘 常見問題

### Q1: Ollama 找不到 MCP Server？

**A**: 確認環境變數已設定：

```bash
echo $MCP_ANSIBLE_PROJECT_ROOT
echo $MCP_ANSIBLE_INVENTORY
```

### Q2: MCP Server 無法執行 Ansible？

**A**: 檢查 Ansible 是否在 PATH 中：

```bash
which ansible-playbook
ansible --version
```

### Q3: 如何調整 Ollama 模型參數？

**A**: 使用 Modelfile 自訂：

```bash
cat > Modelfile << 'EOF'
FROM llama3.1
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "你是一個 Ansible 部署專家，專門協助使用者透過自然語言控制 Docker Compose 部署。"
EOF

ollama create ansible-expert -f Modelfile
ollama run ansible-expert
```

---

## 🎉 總結

使用 **Ollama + MCP** 整合後，您可以：

✅ 用**自然語言**控制 Ansible 部署  
✅ 自動執行**複雜的 DevOps 任務**  
✅ 即時**查詢部署狀態**  
✅ 快速**回滾與修復**  
✅ 完整**審計追蹤**（符合 Constitution 要求）

開始使用：

```bash
# 1. 啟動環境
./start-mcp-ollama.sh

# 2. 在 Claude Desktop 或 Cursor 中輸入
"部署應用程式到 web 伺服器"

# 3. 享受自動化！🚀
```
