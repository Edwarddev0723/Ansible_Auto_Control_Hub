# Ansible Auto Control Hub

> 基礎設施自動化控制中心，整合 Ansible + MCP + ollmcp 實現自然語言控制

## 🚀 快速開始

### 傳統 Ansible 方式
```bash
cd ansible_projects/infra_owner_deploy
ansible-playbook playbooks/deploy_compose.yml --ask-become-pass
```

### ollmcp 自然語言方式 ⭐ 新功能
```bash
./start-ollmcp.sh

# 在 ollmcp 提示符下：
執行 playbook deploy_compose.yml
```

## 📁 專案結構

```
Ansible_Auto_Control_Hub/
├── ansible_projects/           # Ansible 專案目錄
│   └── infra_owner_deploy/    # 基礎設施部署專案
│       ├── playbooks/         # Playbook 檔案
│       │   └── deploy_compose.yml  # Docker Compose 部署
│       ├── inventory/         # 主機清單
│       │   └── hosts.ini
│       ├── group_vars/        # 群組變數
│       └── roles/            # Ansible Roles
│
├── mcp-ansible/               # MCP Ansible Server
│   ├── src/
│   │   └── ansible_mcp/
│   │       └── server.py     # MCP 工具伺服器（38 個工具）
│   ├── .venv/                # Python 虛擬環境
│   └── requirements.txt
│
├── docs/                      # 📚 完整文件
│   ├── QUICK_REFERENCE.md    # ⭐ 快速參考卡
│   ├── OLLMCP_USAGE.md       # ⭐ 實用指南
│   ├── COMPLETION_SUMMARY.md # 整合完成總結
│   ├── MCP_FIX_SUMMARY.md    # 問題修復說明
│   ├── OLLMCP_GUIDE.md       # 完整整合指南
│   └── OLLMCP_TROUBLESHOOTING.md  # 故障排除
│
├── start-ollmcp.sh           # ollmcp 啟動腳本
└── readme.md                 # 本文件
```

## 🎯 核心功能

### 1. Ansible 自動化部署
- ✅ Docker 安裝與配置
- ✅ Docker Compose 應用部署
- ✅ 健康檢查與自動回滾
- ✅ 主機清單管理
- ✅ Playbook 語法驗證

### 2. ollmcp + MCP 自然語言控制 🆕
- ✅ 38 個 Ansible 工具集成
- ✅ 自然語言執行 Ansible 任務
- ✅ Human-in-the-Loop 安全確認
- ✅ 即時執行反饋與結果
- ✅ 互動式 TUI 介面

## 🔧 系統需求

### 必需工具
- Python 3.10+
- Ansible Core 2.16+
- Docker Engine
- docker-compose-plugin v2

### ollmcp 模式額外需求
- Ollama（本地 LLM 運行環境）
- ollmcp（MCP 客戶端）
- MCP Ansible Server（已包含）

## 📖 使用方式

### 方式 1: 傳統 Ansible CLI

```bash
# 1. 安裝依賴
cd ansible_projects/infra_owner_deploy
ansible-galaxy collection install -r requirements.yml

# 2. 驗證語法
ansible-playbook playbooks/deploy_compose.yml --syntax-check

# 3. 執行部署
ansible-playbook playbooks/deploy_compose.yml --ask-become-pass

# 4. 驗證部署
./verify-deployment.sh
```

### 方式 2: ollmcp 自然語言控制 ⭐

```bash
# 1. 啟動 ollmcp
./start-ollmcp.sh

# 2. 在 ollmcp 提示符下使用自然語言
gpt-oss/thinking/38-tools❯ 驗證 playbook deploy_compose.yml 的語法
gpt-oss/thinking/38-tools❯ 顯示所有主機清單
gpt-oss/thinking/38-tools❯ 執行 playbook deploy_compose.yml
gpt-oss/thinking/38-tools❯ 檢查 web 群組的 Docker 服務狀態
```

**常用自然語言指令**：
- `執行 playbook <PATH>`
- `驗證 playbook <PATH> 的語法`
- `顯示所有主機清單`
- `ping web 群組的所有主機`
- `診斷主機 localhost 的狀態`
- `在 localhost 上執行命令查看 Docker 版本`

**提示**：
- 按 `t` 查看 38 個可用工具
- 按 `h` 查看所有快捷鍵
- 輸入 `hil` 關閉確認提示
- 按 `Ctrl+D` 或輸入 `quit` 退出

## 🛠️ 可用的 38 個 Ansible 工具

### 核心執行工具
- `ansible-playbook` - 執行 playbook
- `ansible-task` - 執行單個任務
- `ansible-role` - 執行 role
- `ansible-inventory` - 管理主機清單
- `ansible-ping` - 測試連通性

### Playbook 管理
- `create-playbook` - 創建新 playbook
- `validate-playbook` - 驗證語法
- `ansible-test-idempotence` - 測試冪等性

### 專案管理
- `register-project` - 註冊專案
- `list-projects` - 列出所有專案
- `project-playbooks` - 查看專案 playbooks
- `project-run-playbook` - 執行專案 playbook

### 進階診斷與監控
- `ansible-gather-facts` - 收集主機資訊
- `ansible-diagnose-host` - 診斷主機狀態
- `ansible-health-monitor` - 健康監控
- `ansible-auto-heal` - 自動修復
- `ansible-security-audit` - 安全審計
- `ansible-performance-baseline` - 效能基準測試

### 其他工具
- Inventory 工具（解析、圖形化、差異比對）
- Vault 工具（加密、解密、查看）
- Galaxy 工具（安裝、鎖定依賴）
- Role 工具（創建結構、管理）
- 以及更多...

完整工具列表請按 `t` 鍵在 ollmcp 中查看。

## 📚 文件導航

### 新手入門
1. **[快速參考卡](docs/QUICK_REFERENCE.md)** ⭐ 必讀
   - 常用指令速查
   - 快捷鍵說明
   - 範例會話

2. **[實用指南](docs/OLLMCP_USAGE.md)** ⭐ 推薦
   - 三種執行方式
   - 實用範例
   - 最佳實踐

### 進階文件
3. **[完成總結](docs/COMPLETION_SUMMARY.md)**
   - 整合狀態概覽
   - 系統架構說明
   - 配置檔案位置

4. **[問題修復說明](docs/MCP_FIX_SUMMARY.md)**
   - 技術實現細節
   - 問題診斷與修復
   - 驗證測試方法

5. **[完整整合指南](docs/OLLMCP_GUIDE.md)**
   - 詳細安裝步驟
   - 深入配置說明
   - 架構設計文件

6. **[故障排除](docs/OLLMCP_TROUBLESHOOTING.md)**
   - 常見問題解決
   - 錯誤訊息說明
   - 除錯技巧

### Ansible 專案文件
7. **[部署指南](ansible_projects/infra_owner_deploy/README.md)**
   - Ansible 項目說明
   - 傳統部署方式
   - 配置變數說明

8. **[部署摘要](ansible_projects/infra_owner_deploy/DEPLOYMENT_SUMMARY.md)**
   - 實作任務列表
   - 技術決策說明
   - 目錄結構

## 🎓 使用範例

### 範例 1: 驗證並執行 Playbook

**ollmcp 方式**:
```
gpt-oss/thinking/38-tools❯ 驗證 playbook deploy_compose.yml 的語法

╭─ 🔧 Executing Tool ansible-mcp.validate-playbook ─╮
│  Arguments: { "playbook_path": "..." }            │
╰────────────────────────────────────────────────────╯

[y] → ✓ 語法正確！

gpt-oss/thinking/38-tools❯ 執行 playbook deploy_compose.yml

╭─ 🔧 Executing Tool ansible-mcp.ansible-playbook ─╮
│  Arguments: { "playbook_path": "..." }           │
╰───────────────────────────────────────────────────╯

[y] → ✓ 部署完成！
```

**傳統 CLI 方式**:
```bash
ansible-playbook playbooks/deploy_compose.yml --syntax-check
ansible-playbook playbooks/deploy_compose.yml --ask-become-pass
```

### 範例 2: 主機狀態檢查

**ollmcp 方式**:
```
gpt-oss/thinking/38-tools❯ 診斷主機 localhost 的狀態

# 自動執行多個檢查並生成報告
```

**傳統 CLI 方式**:
```bash
ansible localhost -m ping
ansible localhost -m setup
ansible localhost -m shell -a "docker ps"
```

### 範例 3: 批次操作

**ollmcp 方式**:
```
gpt-oss/thinking/38-tools❯ 在 web 群組的所有主機上檢查 Docker 版本、記憶體使用率和磁碟空間

# 一次指令自動執行多個檢查
```

**傳統 CLI 方式**:
```bash
ansible web -m shell -a "docker --version"
ansible web -m shell -a "free -h"
ansible web -m shell -a "df -h"
```

## ⚙️ 配置檔案

### ollmcp 配置
```
位置: ~/.config/ollmcp/servers.json

用途: 定義 MCP Server 連接資訊
```

### 專案配置
```
位置: ~/.ansible-mcp/projects/infra_owner_deploy.json

用途: 專案路徑、inventory、playbooks 設定
```

### Ansible 配置
```
位置: ansible_projects/infra_owner_deploy/ansible.cfg

用途: Ansible 執行設定（日誌、callback、超時）
```

### 環境變數
```bash
MCP_ANSIBLE_PROJECT_ROOT     # 專案根目錄
MCP_ANSIBLE_INVENTORY        # 預設 inventory 路徑
MCP_ANSIBLE_PROJECT_NAME     # 專案名稱
MCP_ANSIBLE_PROJECTS_DIR     # 專案配置目錄
```

## 🔐 安全注意事項

### Human-in-the-Loop (HIL)
- ✅ 預設啟用，每次執行前需要確認
- ✅ 防止意外執行破壞性操作
- ✅ 提供透明度和控制權
- ⚠️ 生產環境建議保持啟用

### 存取控制
- 📝 確保 Ansible inventory 中的主機認證正確配置
- 📝 使用 SSH 金鑰而非密碼認證（遠端主機）
- 📝 定期檢查 sudo 權限設置
- 📝 敏感資料使用 Ansible Vault 加密

## 🐛 常見問題

### Q: ollmcp 顯示 "No tools are enabled"
**A**: 重新啟動 ollmcp：
```bash
# 按 Ctrl+D 退出，然後
./start-ollmcp.sh
```

### Q: "No project specified and no default set"
**A**: 使用完整路徑執行 playbook，或先註冊專案：
```
註冊 Ansible 專案，名稱是 infra_owner_deploy，根目錄在 <PATH>，設為預設專案
```

### Q: Ansible playbook 執行失敗
**A**: 常見原因與解決方案：
- Sudo 密碼問題 → 使用 `--ask-become-pass`
- SSH 連接問題 → 檢查 SSH 金鑰配置
- Docker 權限問題 → 確保用戶在 docker 群組中

詳細故障排除請參考 [OLLMCP_TROUBLESHOOTING.md](docs/OLLMCP_TROUBLESHOOTING.md)

## 🚧 開發狀態

### 已完成 ✅
- [x] Ansible 專案結構
- [x] Docker Compose 部署 playbook
- [x] 健康檢查與回滾機制
- [x] MCP Ansible Server 整合
- [x] ollmcp 自然語言介面
- [x] 38 個 Ansible 工具集成
- [x] Human-in-the-Loop 安全機制
- [x] 完整文件與範例

### 計畫中 🚀
- [ ] 專案註冊自動化
- [ ] 更多 playbook 範例
- [ ] 批次部署支援
- [ ] 部署歷史記錄
- [ ] Web UI 介面

## 📄 授權

本專案為內部使用專案，未指定公開授權。

## 🤝 貢獻

本專案目前為內部開發專案。如有問題或建議，請聯繫專案維護者。

## 📞 支援

- 查看文件：[docs/](docs/)
- 快速參考：[docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)
- 故障排除：[docs/OLLMCP_TROUBLESHOOTING.md](docs/OLLMCP_TROUBLESHOOTING.md)

---

**最後更新**: 2025-10-16  
**版本**: 2.0 - ollmcp 整合版本  
**狀態**: ✅ 生產就緒
