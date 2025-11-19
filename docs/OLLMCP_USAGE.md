# 如何使用 ollmcp 執行 Ansible 專案

## 🚀 快速啟動

```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub
./start-ollmcp.sh
```

啟動後，ollmcp 會自動：
1. ✓ 檢查並啟動 Ollama 服務
2. ✓ 驗證 MCP Server 環境
3. ✓ 創建專案配置檔（`~/.ansible-mcp/projects/infra_owner_deploy.json`）
4. ✓ 設置環境變數
5. ✓ 連接 MCP Ansible Server（38 個工具）

## 📝 專案配置

專案已自動註冊，配置位於：
```
~/.ansible-mcp/projects/infra_owner_deploy.json
```

配置內容：
```json
{
  "name": "infra_owner_deploy",
  "root": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy",
  "inventory": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini",
  "playbooks_path": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks",
  "roles_paths": ["/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/roles"],
  "default": true
}
```

## 🎯 使用方式

### 方式 1: 直接指定 Playbook 路徑（推薦）⭐

在 ollmcp 提示符下輸入：

```
執行 playbook /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml
```

或使用相對路徑：

```
執行 playbook ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml
```

### 方式 2: 使用專案名稱（需要先註冊）

首先註冊專案：

```
註冊 Ansible 專案，名稱是 infra_owner_deploy，根目錄在 /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy，inventory 在 inventory/hosts.ini，設為預設專案
```

然後執行：

```
執行專案 infra_owner_deploy 的 playbook deploy_compose.yml
```

### 方式 3: 使用 ansible-playbook 工具直接調用

```
使用 ansible-playbook 工具執行 /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml，清單檔案是 /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini
```

## 🔧 其他有用的指令

### 驗證 Playbook 語法

```
驗證 playbook /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml 的語法
```

### 查看主機清單

```
顯示 inventory /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini 的所有主機
```

### 檢查主機連通性

```
ping web 群組的所有主機
```

### 執行單個任務

```
在 localhost 上執行 docker_version 命令查看 Docker 版本
```

### 查看專案列表

```
顯示所有已註冊的 Ansible 專案
```

## 💡 提示

1. **Human-in-the-Loop (HIL)**：
   - 預設啟用，每次執行工具前會要求確認
   - 輸入 `hil` 或 `human-in-the-loop` 可關閉確認提示
   - 按 `y` 執行，`n` 跳過，`disable` 永久關閉

2. **查看工具**：
   - 按 `t` 鍵打開工具選擇器
   - 查看所有 38 個可用的 Ansible 工具
   - 可以啟用/禁用特定工具

3. **切換模型**：
   - 按 `m` 鍵選擇不同的 Ollama 模型
   - 推薦模型：`gpt-oss:20b`、`qwen2.5:7b`

4. **調試模式**：
   - 按 `tm` 切換 thinking mode（思考模式）
   - 按 `st` 切換顯示思考過程
   - 按 `sm` 切換顯示性能指標

5. **更具體的指令**：
   - 提供完整的檔案路徑避免歧義
   - 明確指定目標主機或群組
   - 指定需要的選項（verbose、check、diff 等）

## 🐛 故障排除

### 錯誤："No project specified and no default set"

**原因**：MCP Server 無法找到專案配置

**解決方案**：
1. 使用完整路徑執行 playbook（方式 1）
2. 或先註冊專案（方式 2 的第一步）
3. 檢查環境變數 `MCP_ANSIBLE_PROJECTS_DIR` 是否正確設置

### 錯誤："No tools are enabled"

**原因**：ollmcp 無法連接到 MCP Server

**解決方案**：
1. 停止 ollmcp：按 `Ctrl+D` 或輸入 `quit`
2. 檢查 MCP Server 虛擬環境：`cd mcp-ansible && source .venv/bin/activate && python3 -c "from mcp.server.fastmcp import FastMCP"`
3. 重新啟動：`./start-ollmcp.sh`

### 工具執行失敗

**檢查項目**：
1. Ansible 是否已安裝：`ansible --version`
2. Inventory 檔案是否存在
3. Playbook 檔案是否存在
4. 目標主機是否可連接

## 📚 相關文件

- [MCP_FIX_SUMMARY.md](./MCP_FIX_SUMMARY.md) - MCP 修復摘要
- [OLLMCP_GUIDE.md](./OLLMCP_GUIDE.md) - ollmcp 完整指南
- [OLLMCP_TROUBLESHOOTING.md](./OLLMCP_TROUBLESHOOTING.md) - 故障排除指南
- [MCP_OLLAMA_INTEGRATION.md](./MCP_OLLAMA_INTEGRATION.md) - MCP 整合指南

## 🎓 範例會話

```
gpt-oss/thinking/38-tools❯ 驗證 playbook deploy_compose.yml 的語法

╭─ 🔧 Executing Tool ansible-mcp.validate-playbook ─╮
│  Arguments:                                        │
│  {                                                 │
│    "playbook_path": "deploy_compose.yml"           │
│  }                                                 │
╰────────────────────────────────────────────────────╯

🧑‍💻 Human-in-the-Loop Confirmation
[y] → 執行

╭── ✅ Tool Response ───╮
│  {                    │
│    "ok": true,        │
│    "valid": true      │
│  }                    │
╰───────────────────────╯

✓ Playbook 語法正確！
```

---

**更新日期**: 2025-10-16  
**版本**: 1.0  
**狀態**: ✅ 已驗證
