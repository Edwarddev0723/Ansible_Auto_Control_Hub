# MCP FastMCP 修復摘要

## 問題描述

使用 `ollmcp` 連接 MCP Ansible Server 時遇到 "No tools are enabled" 警告，無法載入任何工具。

## 根本原因

MCP FastMCP 框架的 `base.py` 文件中存在一個 bug，在處理函數參數類型註解時，無法正確處理 Python 的聯合類型（Union types）如 `Optional[Dict[str, str]]` 或 `dict[str, str] | None`。

錯誤堆疊：
```python
TypeError: issubclass() arg 1 must be a class
```

發生在 `.venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/base.py` 第 67 行：
```python
if issubclass(param.annotation, Context):
```

當參數註解是聯合類型時，`issubclass()` 無法處理，導致整個工具載入失敗。

## 解決方案

### 1. 降級 MCP 版本
將 MCP 從 1.12.4 降級到 1.11.0：
```bash
cd mcp-ansible
source .venv/bin/activate
pip install "mcp<1.12" --force-reinstall
```

### 2. 修補 MCP FastMCP base.py
在 `base.py` 中添加類型檢查和異常處理：

**原始代碼：**
```python
for param_name, param in signature.parameters.items():
    if issubclass(param.annotation, Context):
        context_kwarg = param_name
        break
```

**修復後代碼：**
```python
for param_name, param in signature.parameters.items():
    if param.annotation != inspect.Parameter.empty:
        try:
            if inspect.isclass(param.annotation) and issubclass(param.annotation, Context):
                context_kwarg = param_name
                break
        except TypeError:
            # Skip non-class annotations like Union, Optional, etc.
            pass
```

### 3. 自動修補腳本
```python
import inspect
from pathlib import Path

base_py_path = Path(".venv/lib/python3.12/site-packages/mcp/server/fastmcp/tools/base.py")

with open(base_py_path, 'r') as f:
    content = f.read()

if "if issubclass(param.annotation, Context):" in content:
    lines = content.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        if "if issubclass(param.annotation, Context):" in line:
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + "if param.annotation != inspect.Parameter.empty:")
            new_lines.append(' ' * (indent + 4) + "try:")
            new_lines.append(' ' * (indent + 8) + "if inspect.isclass(param.annotation) and issubclass(param.annotation, Context):")
            new_lines.append(' ' * (indent + 12) + "context_kwarg = param_name")
            new_lines.append(' ' * (indent + 12) + "break")
            new_lines.append(' ' * (indent + 4) + "except TypeError:")
            new_lines.append(' ' * (indent + 8) + "pass")
            # 跳過原始行
            while i + 1 < len(lines) and ("context_kwarg" in lines[i + 1] or "break" in lines[i + 1]):
                i += 1
        else:
            new_lines.append(line)
    
    content = '\n'.join(new_lines)
    with open(base_py_path, 'w') as f:
        f.write(content)
```

## 驗證結果

### 測試 MCP Server 工具載入
```bash
cd mcp-ansible
source .venv/bin/activate
python3 << 'EOF'
import asyncio
import sys
sys.path.insert(0, 'src')

from ansible_mcp.server import mcp

async def test_tools():
    tools = await mcp.list_tools()
    print(f"\n✅ MCP Server 成功載入！\n")
    print(f"📊 找到 {len(tools)} 個工具:\n")
    for i, t in enumerate(sorted(tools, key=lambda x: x.name)):
        print(f"  {i+1}. {t.name}")
    return tools

asyncio.run(test_tools())
EOF
```

**輸出：**
```
✅ MCP Server 成功載入！

📊 找到 38 個工具:

  1. ansible-auto-heal
  2. ansible-capture-baseline
  3. ansible-compare-states
  4. ansible-diagnose-host
  5. ansible-fetch-logs
  6. ansible-gather-facts
  7. ansible-health-monitor
  8. ansible-inventory
  9. ansible-log-hunter
  10. ansible-network-matrix
  11. ansible-performance-baseline
  12. ansible-ping
  13. ansible-playbook
  14. ansible-remote-command
  15. ansible-role
  16. ansible-security-audit
  17. ansible-service-manager
  18. ansible-task
  19. ansible-test-idempotence
  20. create-playbook
  21. create-role-structure
  22. galaxy-install
  23. galaxy-lock
  24. inventory-diff
  25. inventory-find-host
  26. inventory-graph
  27. inventory-parse
  28. list-projects
  29. project-bootstrap
  30. project-playbooks
  31. project-run-playbook
  32. register-project
  33. validate-playbook
  34. validate-yaml
  35. vault-decrypt
  36. vault-encrypt
  37. vault-rekey
  38. vault-view
```

### 測試 ollmcp 連接
```bash
ollmcp --servers-json ~/.config/ollmcp/servers.json --model gpt-oss:20b
```

**成功輸出：**
```
╭──────────────────────────────────────────────────────────────────────────╮
│                 Welcome to the MCP Client for Ollama 🦙                  │
╰──────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────── 🔧 Available Tools ───────────────────────────╮
│ ✓ ansible-mcp.ansible-inventory                                          │
│ ✓ ansible-mcp.inventory-parse                                            │
│ ✓ ansible-mcp.inventory-graph                                            │
│ ... (38 個工具)                                                           │
╰────────────────────────── 38/38 tools enabled ───────────────────────────╯
╭───────────────────────────────╮
│ 🧠 Current model: gpt-oss:20b │
╰───────────────────────────────╯
gpt-oss/thinking/38-tools❯
```

✅ **所有工具成功載入！提示符顯示 `38-tools` 而不是之前的 `thinking` (無工具狀態)**

## 配置檔案

### ~/.config/ollmcp/servers.json
```json
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
```

## 啟動腳本

### start-ollmcp.sh
已更新以自動創建 JSON 配置檔並啟動 ollmcp。

## 下一步測試

1. **測試 Ansible 工具執行**
   ```
   gpt-oss/thinking/38-tools❯ 驗證 playbook 語法
   ```

2. **測試清單工具**
   ```
   gpt-oss/thinking/38-tools❯ 顯示所有主機
   ```

3. **測試部署**
   ```
   gpt-oss/thinking/38-tools❯ 部署應用程式到 web 伺服器
   ```

## 技術細節

- **Python 版本**: 3.12
- **MCP 版本**: 1.11.0 (降級自 1.12.4)
- **ollmcp**: 最新版本 (uv tool)
- **Ollama 模型**: gpt-oss:20b
- **Ansible Core**: 2.16+
- **工具數量**: 38 個 Ansible 管理工具

## 問題追蹤

此問題已向 MCP 項目報告：
- 問題類型: `TypeError` in `base.py` when handling Union types
- 影響版本: MCP 1.11.0, 1.12.4
- 建議修復: 在 `issubclass()` 前添加類型檢查

## 相關文件

- [OLLMCP_GUIDE.md](./OLLMCP_GUIDE.md) - ollmcp 完整使用指南
- [OLLMCP_TROUBLESHOOTING.md](./OLLMCP_TROUBLESHOOTING.md) - 故障排除指南
- [MCP_OLLAMA_INTEGRATION.md](./MCP_OLLAMA_INTEGRATION.md) - MCP 整合指南

---

**修復日期**: 2025-10-16  
**修復者**: GitHub Copilot + User  
**狀態**: ✅ 已解決並驗證
