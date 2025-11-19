# Playbook 執行修復說明

## 問題

執行 Playbook 時出現錯誤：
\\\`nERROR! the playbook: C:/Users/user/AppData/Local/Temp/tmpc9aejg_j/playbook.yml could not be found
\\\`n
## 原因分析

1. **ansible-runner 在 Windows 上的路徑問題**：ansible-runner 無法正確處理 Windows 路徑格式
2. **路徑轉換不完整**：原始代碼僅使用 \.replace('\\\\', '/')\，沒有轉換為 WSL 路徑格式

## 修復方案

### 1. Windows 路徑轉換為 WSL 路徑

**轉換邏輯：**
\\\python
def win_to_wsl_path(win_path):
    # 將反斜線轉為正斜線
    wsl_path = win_path.replace('\\\\', '/')
    if ':' in wsl_path:
        # C:/Users/... -> /mnt/c/Users/...
        drive = wsl_path[0].lower()
        rest = wsl_path[2:]  # 跳過 'C:'
        wsl_path = f'/mnt/{drive}{rest}'
    return wsl_path
\\\`n
**轉換示例：**
- Windows: \C:/Users/user/AppData/Local/Temp/test/playbook.yml\`n- WSL: \/mnt/c/Users/user/AppData/Local/Temp/test/playbook.yml\`n
### 2. 強制 Windows 使用 subprocess + WSL

**修改前：**
\\\python
if HAS_ANSIBLE_RUNNER:
    result = _execute_with_ansible_runner(...)
else:
    result = _execute_with_subprocess(...)
\\\`n
**修改後：**
\\\python
is_windows = platform.system() == 'Windows'

if HAS_ANSIBLE_RUNNER and not is_windows:
    # 僅在 macOS/Linux 使用 ansible-runner
    result = _execute_with_ansible_runner(...)
else:
    # Windows 使用 WSL，macOS/Linux 直接執行
    result = _execute_with_subprocess(...)
\\\`n
## 修改文件

- **文件**: \ackend/app/routers/playbooks.py\`n- **函數**: \_execute_with_subprocess()\`n- **行數**: 約 490-550

## 驗證步驟

### 前置條件
1. Windows 系統已安裝 WSL
2. WSL 中已安裝 Ansible：\wsl ansible --version\`n3. 後端服務運行中：\uvicorn app.main:app --reload\`n
### 測試流程
1. 前端選擇一個 Playbook
2. 點擊「執行」按鈕
3. 觀察進度對話框
4. 查看執行結果

### 預期結果
\\\json
{
    'success': true,
    'data': {
        'job_id': 'job-xxxxxx',
        'results': [
            {
                'id': 9,
                'name': 'test',
                'status': 'success',  // 或 'failed' 但有詳細錯誤
                'message': 'Execution completed successfully',
                'output': '... Ansible 執行輸出 ...'
            }
        ]
    }
}
\\\`n
## 已知限制

1. **Windows 必須安裝 WSL**：沒有 WSL 則無法執行
2. **WSL 需要 Ansible**：需在 WSL 內安裝 ansible-core
3. **臨時文件路徑**：WSL 可以訪問 \/mnt/c/...\ 路徑
4. **執行超時**：設定為 5 分鐘，複雜 Playbook 可能超時

## 替代方案

如果 WSL 不可用，可以考慮：
1. 使用 Docker 容器執行 Ansible
2. 安裝 Ansible for Windows (Cygwin)
3. 使用遠程 Linux 機器執行

## 未來改進

1. **非同步執行**：使用 Celery 或背景任務隊列
2. **即時日誌串流**：WebSocket 推送執行日誌
3. **執行歷史**：保存執行記錄到資料庫
4. **重試機制**：自動或手動重試失敗任務

