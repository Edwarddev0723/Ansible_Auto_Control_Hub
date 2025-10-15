# 使用 ollmcp 控制 Ansible 部署 - 完整指南

## 🎯 概述

`ollmcp` 是一個現代化的終端應用程式，讓您可以透過 **本地 Ollama LLM** 與 **MCP Server** 互動，實現自然語言控制 Ansible 部署。

相比傳統的 MCP 整合方式，`ollmcp` 提供：
- ✨ **即開即用**：無需複雜配置
- 🎨 **互動式 TUI**：美觀的終端使用者介面
- 🛠️ **工具管理**：動態啟用/停用工具
- 🔄 **熱重載**：開發時即時更新伺服器
- 🧑‍💻 **Human-in-the-Loop**：執行前審查確認

---

## 📋 前置需求

### 1. 安裝 Ollama

```bash
# macOS
brew install ollama

# 啟動 Ollama 服務
ollama serve
```

### 2. 下載 LLM 模型（支援工具呼叫）

```bash
# 推薦模型（選擇一個）
ollama pull qwen2.5:7b          # 預設，平衡效能
ollama pull llama3.2:3b         # 輕量級
ollama pull qwen3:1.7b          # 支援 Thinking Mode
ollama pull mistral:latest      # Mistral 系列

# 驗證模型已下載
ollama list
```

### 3. 安裝 ollmcp

```bash
# 方式 1: 使用 pip（推薦）
pip install --upgrade ollmcp

# 方式 2: 使用 uvx（免安裝執行）
uvx ollmcp

# 方式 3: 從源碼安裝
git clone https://github.com/jonigl/mcp-client-for-ollama.git
cd mcp-client-for-ollama
uv venv && source .venv/bin/activate
uv pip install .
```

### 4. 安裝 UV 套件管理器（可選）

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 🚀 快速開始

### 步驟 1: 確認 MCP Ansible Server 已配置

```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible

# 建立虛擬環境（如果尚未建立）
python3 -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
pip install -e .
```

### 步驟 2: 使用 ollmcp 連接 MCP Ansible Server

```bash
# 基本用法：直接連接 MCP Server 腳本
ollmcp --mcp-server /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src/ansible_mcp/server.py \
       --model qwen2.5:7b
```

### 步驟 3: 設定環境變數（重要！）

在執行 `ollmcp` 前，設定 Ansible 專案路徑：

```bash
# 方式 1: 臨時設定
export MCP_ANSIBLE_PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"
export MCP_ANSIBLE_INVENTORY="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"

# 方式 2: 寫入 shell 配置檔（永久生效）
echo 'export MCP_ANSIBLE_PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"' >> ~/.zshrc
echo 'export MCP_ANSIBLE_INVENTORY="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini"' >> ~/.zshrc
echo 'export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🎮 完整啟動腳本

創建自動化啟動腳本：

```bash
cat > /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/start-ollmcp.sh << 'EOF'
#!/bin/bash
# ollmcp 自動啟動腳本

set -e

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
MCP_SERVER="$PROJECT_ROOT/mcp-ansible/src/ansible_mcp/server.py"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"

echo "=== 啟動 ollmcp + Ansible MCP ==="

# 1. 檢查 Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama 未安裝，請執行: brew install ollama"
    exit 1
fi

# 2. 啟動 Ollama 服務
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 啟動 Ollama 服務..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi

# 3. 檢查模型
if ! ollama list | grep -q "qwen2.5"; then
    echo "📦 下載 qwen2.5 模型..."
    ollama pull qwen2.5:7b
fi

# 4. 設定環境變數
export MCP_ANSIBLE_PROJECT_ROOT="$ANSIBLE_PROJECT"
export MCP_ANSIBLE_INVENTORY="$ANSIBLE_PROJECT/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"

# 5. 顯示配置
echo ""
echo "=== 配置摘要 ==="
echo "MCP Server: $MCP_SERVER"
echo "Ansible 專案: $MCP_ANSIBLE_PROJECT_ROOT"
echo "清單檔案: $MCP_ANSIBLE_INVENTORY"
echo "模型: qwen2.5:7b"
echo ""

# 6. 啟動 ollmcp
echo "🚀 啟動 ollmcp..."
ollmcp --mcp-server "$MCP_SERVER" --model qwen2.5:7b

EOF

chmod +x /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/start-ollmcp.sh
```

### 使用啟動腳本

```bash
./start-ollmcp.sh
```

---

## 💬 自然語言互動範例

### 啟動後的互動介面

```
╭─────────────────────────────────────────────────────────────╮
│ MCP Client for Ollama                                       │
│ Connected to 1 server(s) with 8 tool(s)                    │
╰─────────────────────────────────────────────────────────────╯

qwen2.5/8-tools❯
```

### 基本部署指令

**您輸入：**
```
部署 Infra_owner_demo 應用程式到 web 伺服器
```

**ollmcp 會：**
1. 🤔 分析您的需求
2. 🛠️ 選擇適當的 MCP 工具（`ansible-playbook`）
3. 💡 顯示 Human-in-the-Loop 確認提示：
   ```
   ╭─────────────────────────────────────────────────────────╮
   │ Tool Call Request                                       │
   ├─────────────────────────────────────────────────────────┤
   │ Tool: ansible-playbook                                  │
   │ Arguments:                                              │
   │   playbook: playbooks/deploy_compose.yml                │
   │   inventory: inventory/hosts.ini                        │
   ├─────────────────────────────────────────────────────────┤
   │ [a] Approve  [s] Skip  [d] Disable HIL  [q] Quit       │
   ╰─────────────────────────────────────────────────────────╯
   ```
4. ⚡ 執行部署（您按 `a` 批准後）
5. 📊 顯示結果和效能指標

### 進階部署範例

#### 1. 自訂埠號部署

```
部署應用程式到 web 伺服器，使用埠號 8080
```

#### 2. 檢查部署狀態

```
檢查 web 伺服器上的 Docker 服務狀態
```

#### 3. 驗證 Playbook

```
驗證 deploy_compose.yml 的語法是否正確
```

#### 4. 查看主機清單

```
顯示所有 web 群組的伺服器
```

#### 5. 健康檢查

```
測試 web 伺服器的 HTTP 端點是否正常
```

---

## 🎛️ 互動式指令

在 `ollmcp` 聊天介面中，您可以使用以下指令：

### 基本指令

| 指令 | 快捷鍵 | 說明 |
|------|--------|------|
| `help` | `h` | 顯示所有可用指令 |
| `tools` | `t` | 開啟工具選擇介面 |
| `model` | `m` | 切換 Ollama 模型 |
| `quit` | `q` 或 `Ctrl+D` | 退出 ollmcp |
| `clear` | `cc` | 清除對話歷史 |
| `cls` | `clear-screen` | 清除終端螢幕 |

### 進階指令

| 指令 | 快捷鍵 | 說明 |
|------|--------|------|
| `model-config` | `mc` | 進階模型參數配置 |
| `thinking-mode` | `tm` | 切換 Thinking Mode |
| `show-thinking` | `st` | 顯示/隱藏思考過程 |
| `show-tool-execution` | `ste` | 顯示/隱藏工具執行細節 |
| `show-metrics` | `sm` | 顯示/隱藏效能指標 |
| `human-in-loop` | `hil` | 切換工具執行前確認 |

### 配置管理

| 指令 | 快捷鍵 | 說明 |
|------|--------|------|
| `save-config` | `sc` | 儲存當前配置 |
| `load-config` | `lc` | 載入配置 |
| `reset-config` | `rc` | 重設為預設配置 |
| `reload-servers` | `rs` | 熱重載 MCP Server |

---

## 🛠️ 工具選擇介面

按 `t` 或輸入 `tools` 開啟工具管理介面：

```
╭─────────────────────────────────────────────────────────────╮
│ Tool Selection - ansible-mcp                                │
├─────────────────────────────────────────────────────────────┤
│ [1] ✓ create-playbook       Create Ansible playbooks       │
│ [2] ✓ validate-playbook     Validate playbook syntax       │
│ [3] ✓ ansible-playbook      Execute playbooks              │
│ [4] ✓ ansible-task          Run ad-hoc tasks               │
│ [5] ✓ ansible-role          Execute roles                  │
│ [6] ✓ ansible-inventory     List inventory                 │
│ [7] ✓ register-project      Register Ansible project       │
│ [8] ✓ create-role-structure Scaffold role directory        │
├─────────────────────────────────────────────────────────────┤
│ Commands: 1,3,5 | 5-8 | S1 | a/n/d/j/s/q                   │
╰─────────────────────────────────────────────────────────────╯
```

### 工具選擇指令

- **數字**：`1,3,5` - 切換指定工具
- **範圍**：`5-8` - 切換連續工具
- **伺服器**：`S1` - 切換整個伺服器的所有工具
- **快捷鍵**：
  - `a` / `all` - 啟用所有工具
  - `n` / `none` - 停用所有工具
  - `d` / `desc` - 顯示/隱藏工具描述
  - `j` / `json` - 顯示工具 JSON schema
  - `s` / `save` - 儲存變更並返回
  - `q` / `quit` - 取消變更並返回

---

## ⚙️ 進階模型配置

輸入 `model-config` 或 `mc` 開啟進階設定：

```
╭─────────────────────────────────────────────────────────────╮
│ Advanced Model Configuration - qwen2.5:7b                   │
├─────────────────────────────────────────────────────────────┤
│ System Prompt                                               │
│ [sp] System Prompt: "You are an Ansible automation..."     │
│                                                             │
│ Key Parameters                                              │
│ [1]  Context Window (num_ctx): 2048 (unset = auto)        │
│ [2]  Keep Tokens: - (unset)                                │
│ [3]  Max Tokens: - (unset = auto)                          │
│ [4]  Seed: -1 (random)                                     │
│ [5]  Temperature: 0.7 (balance)                            │
│ [6]  Top K: - (unset)                                      │
│ [7]  Top P: 0.9                                            │
│ ...                                                         │
├─────────────────────────────────────────────────────────────┤
│ Commands: 1-15 | sp | u1-15/uall | h | undo | s/q         │
╰─────────────────────────────────────────────────────────────╯
```

### 推薦配置

#### 🎯 Ansible 部署專用配置

```
System Prompt: "你是一個 Ansible 自動化專家，專門協助使用者部署和管理 Docker Compose 應用程式。請使用繁體中文回答，並在執行操作前清楚說明將要執行的動作。"

Temperature: 0.3          # 降低隨機性，提高準確性
Top P: 0.5                # 更聚焦的選擇
Seed: 42                  # 可重現的結果
Context Window: 4096      # 足夠的上下文
```

#### 🎨 創意探索配置

```
Temperature: 1.0+
Top P: 0.95
Presence Penalty: 0.2
```

#### 📝 事實查詢配置

```
Temperature: 0.0-0.3
Top P: 0.1-0.5
Seed: 42
```

---

## 🔄 開發者功能：熱重載

當您修改 MCP Server 程式碼時，無需重啟 `ollmcp`：

```bash
# 在 ollmcp 介面中輸入
reload-servers

# 或使用快捷鍵
rs
```

**熱重載會：**
1. 🔌 斷開所有 MCP Server 連線
2. 🔄 使用相同參數重新連線
3. 💾 保留您的工具啟用/停用設定
4. ✅ 顯示更新後的伺服器和工具狀態

**適用場景：**
- 修改 `mcp-ansible/src/ansible_mcp/server.py` 後
- 更新 MCP Server 配置檔案後
- 除錯時確保使用最新版本

---

## 🧑‍💻 Human-in-the-Loop（HIL）

預設啟用，每次工具執行前都會詢問確認：

```
╭─────────────────────────────────────────────────────────────╮
│ Human-in-the-Loop Confirmation                              │
├─────────────────────────────────────────────────────────────┤
│ Tool: ansible-playbook                                      │
│                                                             │
│ Arguments:                                                  │
│ {                                                           │
│   "playbook": "playbooks/deploy_compose.yml",              │
│   "inventory": "inventory/hosts.ini",                       │
│   "extra_vars": {"http_port": 80}                          │
│ }                                                           │
├─────────────────────────────────────────────────────────────┤
│ This will execute the deployment playbook                   │
├─────────────────────────────────────────────────────────────┤
│ [a] Approve  [s] Skip  [d] Disable HIL  [q] Quit           │
╰─────────────────────────────────────────────────────────────╯
```

### HIL 選項

- **`a` (Approve)** - 批准並執行此工具
- **`s` (Skip)** - 跳過此工具，繼續對話
- **`d` (Disable)** - 停用 HIL，之後不再詢問
- **`q` (Quit)** - 取消操作

### 切換 HIL

```bash
# 在 ollmcp 介面中
human-in-loop    # 或 hil
```

---

## 📊 效能指標

輸入 `show-metrics` 或 `sm` 啟用效能指標顯示：

```
╭─────────────────────────────────────────────────────────────╮
│ Performance Metrics                                         │
├─────────────────────────────────────────────────────────────┤
│ Total Duration: 3.42s                                       │
│ Load Duration: 245ms                                        │
│ Prompt Eval Count: 128 tokens                               │
│ Prompt Eval Duration: 156ms                                 │
│ Eval Count: 256 tokens                                      │
│ Eval Duration: 2.87s                                        │
│ Prompt Eval Rate: 820 tokens/s                              │
│ Eval Rate: 89 tokens/s                                      │
╰─────────────────────────────────────────────────────────────╯
```

---

## 💾 配置管理

### 儲存配置

```bash
# 儲存為預設配置
save-config

# 儲存為命名配置
save-config ansible-deploy
```

### 載入配置

```bash
# 載入預設配置
load-config

# 載入命名配置
load-config ansible-deploy
```

### 配置儲存位置

- 預設配置：`~/.config/ollmcp/config.json`
- 命名配置：`~/.config/ollmcp/{name}.json`

### 配置內容

配置會儲存：
- ✅ 當前模型選擇
- ✅ 進階模型參數（system prompt, temperature 等）
- ✅ 工具啟用/停用狀態
- ✅ Context retention 設定
- ✅ Thinking mode 設定
- ✅ HIL 設定
- ✅ 顯示偏好（metrics, tool execution 等）

---

## 🎯 完整工作流程範例

### 場景：首次部署 Infra_owner_demo

```bash
# 1. 啟動 ollmcp
./start-ollmcp.sh

# 2. 在 ollmcp 介面中
qwen2.5/8-tools❯ 驗證 deploy_compose.yml 的語法

# ollmcp 回應：
# ✓ 語法檢查通過

qwen2.5/8-tools❯ 顯示 web 群組的所有主機

# ollmcp 回應：
# localhost (ansible_connection=local)

qwen2.5/8-tools❯ 部署應用程式到 web 伺服器

# HIL 確認提示出現
# 按 'a' 批准

# ollmcp 執行部署並顯示：
# ✓ Docker 已安裝
# ✓ 檔案已同步
# ✓ Docker Compose 已部署
# ✓ 健康檢查通過

qwen2.5/8-tools❯ 測試 HTTP 端點

# ollmcp 回應：
# ✓ HTTP 200 OK
# ✓ 應用程式運行正常

qwen2.5/8-tools❯ 儲存目前配置
save-config ansible-deploy

# 配置已儲存至 ~/.config/ollmcp/ansible-deploy.json
```

---

## 🔧 故障排除

### 問題 1: ollmcp 找不到 MCP Server

**症狀：**
```
Error: Could not connect to MCP server
```

**解決方案：**
```bash
# 檢查 MCP Server 路徑
ls -la /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src/ansible_mcp/server.py

# 檢查 Python 環境
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible
source .venv/bin/activate
python -c "import mcp; print('MCP installed')"
```

### 問題 2: 環境變數未設定

**症狀：**
```
Error: MCP_ANSIBLE_PROJECT_ROOT not set
```

**解決方案：**
```bash
# 設定環境變數
export MCP_ANSIBLE_PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"
export MCP_ANSIBLE_INVENTORY="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"

# 使用啟動腳本（已包含環境變數設定）
./start-ollmcp.sh
```

### 問題 3: Ollama 服務未啟動

**症狀：**
```
Error: Could not connect to Ollama
```

**解決方案：**
```bash
# 啟動 Ollama
ollama serve

# 檢查 Ollama 狀態
curl http://localhost:11434/api/tags
```

### 問題 4: 模型不支援工具呼叫

**症狀：**
```
Warning: Model may not support tool calling
```

**解決方案：**
```bash
# 切換到支援工具呼叫的模型
# 在 ollmcp 介面中輸入
model

# 選擇以下其中一個：
# - qwen2.5:7b (推薦)
# - llama3.2:3b
# - qwen3:1.7b
# - mistral:latest
```

---

## 📚 延伸學習

### 官方資源

- **ollmcp GitHub**: https://github.com/jonigl/mcp-client-for-ollama
- **MCP 規格**: https://modelcontextprotocol.io/
- **Ollama 文件**: https://ollama.ai/
- **MCP Servers 集合**: https://github.com/modelcontextprotocol/servers

### 本專案資源

- **Ansible 部署指南**: `ansible_projects/infra_owner_deploy/README.md`
- **MCP API 規格**: `specs/002-mcp-ansible-infra/contracts/mcp-tool-api.json`
- **實施摘要**: `ansible_projects/infra_owner_deploy/DEPLOYMENT_SUMMARY.md`

---

## 🎉 總結

使用 `ollmcp` 的優勢：

✅ **零配置啟動** - 一行指令即可開始  
✅ **互動式介面** - 美觀的 TUI，易於使用  
✅ **安全控制** - Human-in-the-Loop 確認機制  
✅ **開發友善** - 熱重載功能，快速迭代  
✅ **效能監控** - 即時查看模型效能指標  
✅ **配置管理** - 儲存和載入配置，重複使用  

### 立即開始

```bash
# 1. 執行啟動腳本
./start-ollmcp.sh

# 2. 開始對話
部署應用程式到 web 伺服器

# 3. 享受自動化！🚀
```

---

**最後更新**: 2025-10-16  
**版本**: v1.0  
**適用於**: ollmcp v1.x + Ansible MCP Server
