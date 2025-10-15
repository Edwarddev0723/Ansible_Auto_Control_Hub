# 🚀 MCP + Ollama 快速參考卡

## 一鍵啟動

```bash
./start-mcp-ollama.sh
```

---

## 🎯 自然語言指令範例

### 部署操作

| 您說 | MCP 執行 |
|------|---------|
| "部署應用程式到 web 伺服器" | `ansible-playbook playbooks/deploy_compose.yml` |
| "部署到埠號 8080" | `ansible-playbook playbooks/deploy_compose.yml -e "http_port=8080"` |
| "驗證 playbook 語法" | `ansible-playbook --syntax-check playbooks/deploy_compose.yml` |
| "執行乾運行測試" | `ansible-playbook playbooks/deploy_compose.yml --check` |

### 狀態檢查

| 您說 | MCP 執行 |
|------|---------|
| "檢查服務狀態" | `docker compose ps` |
| "測試 HTTP 端點" | `curl http://localhost:80` |
| "顯示所有主機" | `ansible-inventory --list` |
| "ping web 伺服器" | `ansible web -m ping` |

### 管理操作

| 您說 | MCP 執行 |
|------|---------|
| "查看部署日誌" | `tail -f logs/ansible-deployment.log` |
| "顯示容器日誌" | `docker compose logs` |
| "停止服務" | `docker compose down` |
| "重啟服務" | `docker compose restart` |

---

## ⚙️ 配置位置

### Claude Desktop
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Cursor
```bash
~/.cursor/mcp.json
```

### 配置範本
```bash
docs/claude_desktop_config.example.json
```

---

## 🔧 常用命令

### 啟動 Ollama
```bash
ollama serve
```

### 下載模型
```bash
ollama pull llama3.1      # 推薦
ollama pull codellama     # 程式碼專用
ollama pull qwen2.5-coder # 技術任務
```

### 測試 MCP Server
```bash
cd mcp-ansible
source .venv/bin/activate
python src/ansible_mcp/server.py
```

### 使用 MCP Inspector
```bash
npx @modelcontextprotocol/inspector \
  python mcp-ansible/src/ansible_mcp/server.py
```

---

## 📋 MCP 工具列表

| 工具 | 功能 |
|------|------|
| `ansible-playbook` | 執行 Playbook |
| `validate-playbook` | 驗證語法 |
| `ansible-task` | 執行 ad-hoc 任務 |
| `ansible-inventory` | 列出清單 |
| `create-playbook` | 建立 Playbook |
| `ansible-role` | 執行 Role |

---

## 🛡️ 安全檢查清單

- ✅ SSH 金鑰配置完成
- ✅ Sudo 權限已設定
- ✅ 防火牆規則已開放 (80, 22)
- ✅ Secrets 不在對話中
- ✅ 審計日誌已啟用

---

## 🆘 快速除錯

### Ollama 無回應
```bash
# 重啟 Ollama
pkill ollama
ollama serve
```

### MCP Server 錯誤
```bash
# 檢查環境變數
echo $MCP_ANSIBLE_PROJECT_ROOT
echo $MCP_ANSIBLE_INVENTORY

# 重新安裝依賴
cd mcp-ansible
pip install -r requirements.txt
```

### Ansible 錯誤
```bash
# 檢查連線
ansible web -m ping

# 檢查 sudo
ansible web -m shell -a "sudo whoami" -b
```

---

## 📚 文件連結

- **完整指南**: `docs/MCP_OLLAMA_INTEGRATION.md`
- **API 規格**: `specs/002-mcp-ansible-infra/contracts/mcp-tool-api.json`
- **部署指南**: `ansible_projects/infra_owner_deploy/README.md`

---

## 🎓 學習路徑

1. ✅ 安裝 Ollama 和模型
2. ✅ 配置 MCP Server
3. ✅ 測試基本指令
4. ✅ 整合到 Claude/Cursor
5. ✅ 執行完整部署
6. ✅ 監控和除錯

---

**更新日期**: 2025-10-16  
**版本**: v1.0
