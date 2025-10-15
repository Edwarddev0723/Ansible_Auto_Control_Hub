╭──────────────────────────────────────────────────────────────────╮
│                   ollmcp 快速參考卡 v1.0                         │
╰──────────────────────────────────────────────────────────────────╯

🚀 啟動
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ./start-ollmcp.sh         # 啟動 ollmcp + MCP Ansible
  按 Ctrl+D 或輸入 quit     # 退出

📦 必需工具
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ Ollama (運行中)         # ollama serve
  ✓ ollmcp                  # pip install ollmcp
  ✓ MCP Server (已配置)     # mcp-ansible/.venv
  ✓ Python 3.12+
  ✓ Ansible 2.16+

🔧 快捷鍵
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  h         顯示幫助
  t         工具選擇器 (查看 38 個工具)
  m         切換模型
  hil       切換 Human-in-the-Loop
  tm        切換思考模式
  sm        切換性能指標
  c         切換上下文保留
  cc        清除對話上下文
  cls       清除螢幕

🎯 常用指令（推薦方式）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 執行 Playbook (完整路徑 - 最可靠)
執行 playbook /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml

# 驗證語法
驗證 playbook /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/playbooks/deploy_compose.yml 的語法

# 查看主機清單
顯示 inventory /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy/inventory/hosts.ini 的所有主機

# 測試連通性
使用 ansible-ping 工具測試 web 群組的連通性

# 執行單個任務
在 localhost 上執行 shell 命令 "docker --version"

📝 專案方式（需要先註冊）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1. 註冊專案（僅需一次）
註冊 Ansible 專案，名稱是 infra_owner_deploy，根目錄在 /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub/ansible_projects/infra_owner_deploy，inventory 在 inventory/hosts.ini，設為預設專案

# 2. 使用專案名稱執行
執行專案 infra_owner_deploy 的 playbook deploy_compose.yml

🔍 驗證與檢查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
驗證 playbook <PATH> 的語法
檢查 playbook <PATH> 的 YAML 格式
顯示 inventory <PATH> 的主機結構圖
查找 inventory <PATH> 中的主機 web-01

🎮 進階工具
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
診斷主機 localhost 的狀態
收集 web 群組的所有 facts
監控 web 群組的健康狀態
執行安全審計在 web 群組
自動修復 web-01 的常見問題

💡 提示與技巧
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 使用完整路徑避免歧義
  2. 明確指定目標主機/群組
  3. 關閉 HIL 加快連續操作: 輸入 "hil"
  4. 查看工具執行過程: 按 "ste"
  5. 需要詳細輸出: 加上 "verbose 模式"

⚠️ 常見錯誤
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

錯誤: "No project specified and no default set"
解決: 使用完整路徑執行 playbook，或先註冊專案

錯誤: "No tools are enabled"
解決: 重啟 ollmcp (Ctrl+D 然後 ./start-ollmcp.sh)

錯誤: Playbook 執行失敗
解決: 檢查 sudo 密碼、SSH 金鑰、主機連通性

📂 重要檔案位置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ollmcp 配置:    ~/.config/ollmcp/servers.json
  專案配置:       ~/.ansible-mcp/projects/infra_owner_deploy.json
  MCP Server:     mcp-ansible/src/ansible_mcp/server.py
  Ansible 專案:   ansible_projects/infra_owner_deploy/
  文件目錄:       docs/

📚 文件快速鏈接
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OLLMCP_USAGE.md            實用指南 (推薦)
  COMPLETION_SUMMARY.md      完成總結
  MCP_FIX_SUMMARY.md         問題修復說明
  OLLMCP_TROUBLESHOOTING.md  故障排除

🎓 範例會話
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
gpt-oss/thinking/38-tools❯ 驗證 playbook deploy_compose.yml 的語法

╭─ 🔧 Executing Tool ansible-mcp.validate-playbook ─╮
│  Arguments: { "playbook_path": "..." }            │
╰────────────────────────────────────────────────────╯

🧑‍💻 Human-in-the-Loop Confirmation
[y] → ✓ 語法正確！

gpt-oss/thinking/38-tools❯ ping 所有主機

╭─ 🔧 Executing Tool ansible-mcp.ansible-ping ─╮
│  Arguments: { "host_pattern": "all" }        │
╰───────────────────────────────────────────────╯

[y] → ✓ localhost | SUCCESS

╭──────────────────────────────────────────────────────────────────╮
│                      快速開始三步驟                              │
├──────────────────────────────────────────────────────────────────┤
│  1. ./start-ollmcp.sh        # 啟動                              │
│  2. 按 't' 查看工具          # 確認 38 個工具可用               │
│  3. 輸入自然語言指令         # 開始使用！                        │
╰──────────────────────────────────────────────────────────────────╯

需要幫助？輸入 'h' 或查看 docs/OLLMCP_USAGE.md

版本: 1.0 | 日期: 2025-10-16 | 狀態: ✅ 生產就緒
