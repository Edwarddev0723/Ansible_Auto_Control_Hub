# ollmcp 工具未啟用問題診斷

## 問題

當執行 `ollmcp` 時，出現：
```
Warning: No tools are enabled. Model will respond without tool access.
```

## 根本原因

`ollmcp` 無法正確連接到 MCP Ansible Server。可能的原因：

1. **MCP Server 路徑問題** - Server 腳本無法被 `ollmcp` 執行
2. **環境變數問題** - Python 環境或依賴未正確載入
3. **傳輸協定問題** - `ollmcp` 期待 STDIO transport，但Server可能配置不同

## 解決方案

### 方案 1: 使用 JSON 配置檔（推薦）

1. 創建 MCP Server 配置檔：

```bash
mkdir -p ~/.config/ollmcp
cat > ~/.config/ollmcp/servers.json << 'EOF'
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
        "MCP_ANSIBLE_PROJECT_NAME": "infra_owner_deploy",
        "PYTHONPATH": "/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/src"
      }
    }
  }
}
EOF
```

2. 使用配置檔啟動：

```bash
ollmcp --servers-json ~/.config/ollmcp/servers.json --model gpt-oss:20b
```

### 方案 2: 使用虛擬環境中的 Python

確保使用 MCP Server 虛擬環境中的 Python：

```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible
source .venv/bin/activate

# 使用虛擬環境中的 Python 路徑
ollmcp --mcp-server "$(pwd)/src/ansible_mcp/server.py" \
       --model gpt-oss:20b
```

### 方案 3: 創建包裝腳本

創建一個包裝腳本來正確設定環境：

```bash
cat > /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/run_server.sh << 'EOF'
#!/bin/bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible
source .venv/bin/activate
export MCP_ANSIBLE_PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy"
export MCP_ANSIBLE_INVENTORY="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"
exec python3 src/ansible_mcp/server.py
EOF

chmod +x /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/run_server.sh

# 使用包裝腳本
ollmcp --mcp-server /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible/run_server.sh \
       --model gpt-oss:20b
```

### 方案 4: 使用 Claude Desktop 配置（最可靠）

`ollmcp` 支援自動從 Claude Desktop 配置讀取 Server：

```bash
mkdir -p ~/Library/Application\ Support/Claude
cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
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

# 使用自動探索
ollmcp --auto-discovery --model gpt-oss:20b
```

## 驗證步驟

1. **測試 MCP Server 是否可執行**：
```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/mcp-ansible
source .venv/bin/activate
python3 -c "import sys; sys.path.insert(0, 'src'); from ansible_mcp.server import mcp; print('MCP Server 可導入')"
```

2. **檢查工具列表**：
啟動 `ollmcp` 後，按 `t` 查看工具選擇介面，確認是否有工具顯示

3. **查看日誌**：
```bash
# 啟動時添加詳細輸出
ollmcp --servers-json ~/.config/ollmcp/servers.json --model gpt-oss:20b -vvv
```

## 暫時解決方案

如果以上都無法解決，可以直接使用 Ansible CLI：

```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy

# 直接執行部署
ansible-playbook playbooks/deploy_compose.yml

# 或使用驗證腳本
../verify-deployment.sh
```

## 預期行為

成功連接後，`ollmcp` 應該顯示：

```
╭─────────────────────────────────────────────────────────────╮
│ MCP Client for Ollama                                       │
│ Connected to 1 server(s) with 8 tool(s)                    │
╰─────────────────────────────────────────────────────────────╯

gpt-oss/8-tools❯
```

而不是：

```
gpt-oss/thinking❯ 
Warning: No tools are enabled.
```
