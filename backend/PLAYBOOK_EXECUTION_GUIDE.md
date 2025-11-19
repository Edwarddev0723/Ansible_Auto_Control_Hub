# Playbook 執行功能實作說明

## ✅ 已實作功能

### 1. 完整的 Ansible Playbook 執行流程
- **動態 Inventory 生成**: 支援從資料庫中的 Inventory 或 Playbook 定義生成 inventory 檔案
- **YAML Playbook 構建**: 將資料庫中的 Tasks 轉換為標準 Ansible Playbook YAML 格式
- **臨時檔案管理**: 使用 Python tempfile 安全處理臨時檔案，執行後自動清理
- **命令執行**: 使用 subprocess 執行 'ansible-playbook' 命令
- **狀態更新**: 根據執行結果自動更新 Playbook 狀態 (Success/Fail) 和最後執行時間

### 2. 錯誤處理機制
- **超時控制**: 5 分鐘執行超時保護
- **命令未找到檢測**: 檢查系統是否安裝 Ansible
- **驗證檢查**: 確保 Inventory、Tasks 存在且有效
- **異常捕獲**: 完整的 try-catch 錯誤處理

### 3. 執行結果回傳
- **Job ID**: 每次執行生成唯一的 job-{uuid} 識別碼
- **詳細結果**: 包含每個 Playbook 的執行狀態、訊息、輸出和錯誤
- **時間戳記**: 記錄執行時間

## ⚠️ 遇到的問題與限制

### 問題 1: Ansible 環境依賴
**問題描述**: 此功能依賴系統已安裝 Ansible

**影響範圍**:
- Windows 系統需要透過 WSL 或其他方式安裝 Ansible
- Linux/macOS 需要透過套件管理器安裝

**解決方案**:
\\\ash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ansible

# macOS
brew install ansible

# Windows (需要 WSL2)
wsl --install
# 進入 WSL 後
sudo apt-get update && sudo apt-get install ansible
\\\

**檢查方式**:
\\\ash
ansible-playbook --version
\\\

### 問題 2: Task Content 格式解析
**問題描述**: 資料庫中的 Task content 可能不是有效的 YAML 格式

**當前處理方式**:
- 嘗試用 yaml.safe_load() 解析
- 解析失敗則包裝成 debug task

**範例**:
\\\python
# 有效的 Task content (YAML 格式)
name: Install nginx
apt:
  name: nginx
  state: present

# 無效格式會被轉換為:
name: Task 0
debug:
  msg: "原始內容"
\\\

**建議改進**:
- 在前端 PlaybookCreateView 和 PlaybookEditView 中加入 YAML 格式驗證
- 提供 Task 模板或範例
- 新增 Task content 預覽功能

### 問題 3: Inventory Config 格式限制
**問題描述**: Inventory.config 欄位格式需要符合 Ansible inventory 規範

**支援格式**:
1. **簡單主機列表**:
\\\
192.168.1.10
192.168.1.11
\\\

2. **INI 格式**:
\\\
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
\\\

3. **主機變數格式** (已在 InventoryDetailView 使用):
\\\
server1 ansible_ssh_host=192.168.1.100 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=password
\\\

**潛在問題**:
- 不支援 YAML 格式的 Inventory (可以擴充)
- 密碼明文儲存在 config 欄位 (安全性問題)

### 問題 4: 執行權限與安全性
**問題描述**: subprocess 執行外部命令存在安全風險

**安全隱患**:
1. **命令注入**: 雖然使用陣列方式傳參,但仍需注意
2. **密碼暴露**: Inventory config 中的密碼可能在 ps 命令中可見
3. **檔案權限**: 臨時檔案可能被其他使用者讀取

**建議改進**:
- 使用 Ansible Vault 加密敏感資訊
- 設定臨時檔案嚴格權限 (600)
- 考慮使用 Ansible Python API 而非 subprocess

### 問題 5: 並發執行限制
**問題描述**: 當前實作為同步執行,多個 Playbook 會依序執行

**影響**:
- 執行時間長 (每個 Playbook 最多 5 分鐘)
- API 請求會阻塞直到所有執行完成
- 前端可能出現請求超時

**建議改進**:
- 實作非同步任務佇列 (Celery + Redis)
- 回傳 job_id 供前端輪詢狀態
- 新增執行狀態查詢 API

### 問題 6: 缺乏執行歷史記錄
**問題描述**: 只記錄最後執行時間和狀態,沒有完整執行歷史

**缺失功能**:
- 執行日誌保存
- 歷史執行記錄查詢
- 輸出結果儲存
- 執行時間統計

**建議新增資料表**:
\\\sql
CREATE TABLE playbook_executions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    playbook_id INT,
    job_id VARCHAR(255),
    status ENUM('success', 'failed', 'timeout', 'error'),
    stdout TEXT,
    stderr TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    duration_seconds INT
);
\\\

### 問題 7: 缺乏進度回饋
**問題描述**: 執行期間無法得知當前進度

**使用者體驗問題**:
- 不知道執行到哪個 Task
- 無法即時看到輸出
- 不確定是否卡住

**建議改進**:
- 使用 WebSocket 即時推送執行狀態
- 實作 Server-Sent Events (SSE) 串流輸出
- 加入執行進度百分比

## 📋 API 變更

### 執行 Playbook API
\\\
POST /api/playbooks/execute
\\\

**請求範例**:
\\\json
{
  "playbook_ids": [1, 2, 3],
  "inventory_id": 1,
  "extra_vars": {
    "env": "production",
    "version": "1.0.0"
  }
}
\\\

**回應範例 (成功)**:
\\\json
{
  "success": true,
  "data": {
    "job_id": "job-a1b2c3d4",
    "results": [
      {
        "id": 1,
        "name": "Ansible GUI",
        "status": "success",
        "message": "Execution completed successfully",
        "output": "PLAY [Ansible GUI] ***\\n\\nTASK [Gathering Facts] ***..."
      },
      {
        "id": 2,
        "name": "Ansible introduction",
        "status": "failed",
        "message": "Execution failed",
        "error": "ERROR! ...",
        "output": "..."
      }
    ],
    "created_at": "2025-11-12T01:20:00"
  },
  "message": "Playbook execution completed"
}
\\\

## 🔧 前端整合建議

### 1. 執行按鈕處理
在 \PlaybookView.vue\ 中:
\\\	ypescript
const executePlaybooks = async () => {
  const selectedIds = selectedItems.value.map(item => item.id)
  
  try {
    loading.value = true
    const response = await executePlaybook({
      playbook_ids: selectedIds,
      inventory_id: selectedInventoryId.value // 可選
    })
    
    // 顯示結果
    response.data.results.forEach(result => {
      if (result.status === 'success') {
        console.log(\✅ \: 成功\)
      } else {
        console.error(\❌ \: \\)
      }
    })
    
    // 重新載入列表
    await loadPlaybooks()
  } catch (error) {
    alert('執行失敗')
  } finally {
    loading.value = false
  }
}
\\\

### 2. 執行結果顯示
建議新增:
- 執行結果對話框顯示每個 Playbook 狀態
- 點擊查看詳細輸出
- 錯誤訊息高亮顯示

### 3. Inventory 選擇器
- 執行前彈出 Inventory 選擇對話框
- 顯示可用的 Inventory 列表
- 提供「使用 Playbook 預設目標」選項

## 🚀 部署注意事項

### 1. 環境準備
\\\ash
# 1. 安裝 Ansible
apt-get install ansible

# 2. 安裝 Python 依賴
pip install -r requirements.txt

# 3. 驗證安裝
ansible-playbook --version
\\\

### 2. 權限設定
\\\ash
# 確保 backend 使用者有執行 ansible-playbook 權限
which ansible-playbook
ls -la /usr/bin/ansible-playbook
\\\

### 3. 測試執行
建議先建立一個簡單的測試 Playbook:
\\\yaml
- name: Test playbook
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Print message
      debug:
        msg: "Hello from Ansible!"
\\\

## 📊 監控建議

### 1. 日誌記錄
- 記錄每次執行的完整命令
- 保存 stdout 和 stderr 到檔案
- 記錄執行時間和資源使用

### 2. 告警機制
- 執行失敗超過 N 次觸發告警
- 執行時間超過閾值告警
- Ansible 命令不存在時告警

## 🔒 安全加固建議

1. **密碼加密**: 使用 Ansible Vault 或加密欄位儲存密碼
2. **存取控制**: 加入 JWT 認證,限制誰可以執行 Playbook
3. **審計日誌**: 記錄誰在何時執行了哪些 Playbook
4. **資源限制**: 限制並發執行數量,防止資源耗盡
5. **輸入驗證**: 嚴格驗證所有輸入參數,防止注入攻擊

## 📚 相關文件

- Ansible 官方文件: https://docs.ansible.com/
- Python subprocess: https://docs.python.org/3/library/subprocess.html
- FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/

---

**版本**: 1.0  
**最後更新**: 2025-11-12  
**作者**: Dev Agent
