# API 更新說明

## 更新日期: 2025-11-12

### ✅ 完成的三個任務

#### 1. 修復 Playbook Host 選項來源

**修改的檔案:**
- `frontend/src/views/PlaybookCreateView.vue`
- `frontend/src/views/PlaybookEditView.vue`

**變更內容:**
- 將 Host 下拉選單的資料來源從 `getHosts()` API 改為從 `getInventories()` API 獲取
- Host 選項現在顯示 Inventory 的名稱 (name 欄位)
- 移除對 `@/api/host` 的依賴，改用 `@/api/inventory`

**使用方式:**
```typescript
// 在 PlaybookCreateView 和 PlaybookEditView 中
const loadHosts = async () => {
  const response = await getInventories({ per_page: 1000 })
  if (response.success) {
    availableHosts.value = response.data.items.map(inv => inv.name)
  }
}
```

---

#### 2. 實作 SSH 連線測試 API

**後端新增:**

**檔案:** `backend/app/routers/inventories.py`

**新端點:**
```
POST /api/inventories/test-ssh
```

**請求格式:**
```json
{
  "inventory_ids": [1, 2, 3]
}
```

**回應格式:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Server-1",
      "status": "success",
      "message": "Connection successful: SSH Test Successful"
    },
    {
      "id": 2,
      "name": "Server-2",
      "status": "error",
      "message": "Connection timeout"
    }
  ],
  "message": "Tested 2 inventory connections"
}
```

**功能說明:**
- 使用 `paramiko` 套件進行 SSH 連線測試
- 從 Inventory 的 `config` 欄位解析 SSH 資訊 (host, port, password)
- 執行簡單的測試命令驗證連線
- 自動更新 Inventory 的 `ssh_status` 欄位
- 支援多個 Inventory 同時測試

**前端整合:**

**檔案:** 
- `frontend/src/api/inventory.ts` - 新增 `testSSHConnection()` 函數
- `frontend/src/views/InventoriesView.vue` - 整合 SSH 測試按鈕

**使用方式:**
1. 在 Inventories 列表中勾選要測試的伺服器
2. 點擊「SSH連線測試」按鈕
3. 系統會顯示每個伺服器的測試結果

**新增的 Python 依賴:**
- `paramiko==3.4.0` - SSH 連線庫

---

#### 3. 實作 AI 對話 API

**後端新增:**

**檔案:** `backend/app/routers/ai_chat.py` (新建)

**新端點:**

1. **聊天對話**
```
POST /api/ai/chat
```

**請求格式:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I configure Ansible inventory?"
    }
  ],
  "model": "gpt-4",
  "temperature": 0.7
}
```

**回應格式:**
```json
{
  "success": true,
  "data": {
    "role": "assistant",
    "content": "To configure Ansible inventory..."
  },
  "message": "AI response received successfully"
}
```

2. **健康檢查**
```
GET /api/ai/health
```

**回應格式:**
```json
{
  "success": true,
  "data": {
    "status": "connected",
    "server": "http://localhost:3001/api/chat"
  },
  "message": "MCP server is healthy"
}
```

**功能說明:**
- 支援串接外部 MCP server (透過環境變數 `MCP_SERVER_URL` 配置)
- 內建備援機制：MCP server 無法連線時提供模擬回應
- 支援完整的對話歷史記錄
- 可配置 AI model 和 temperature 參數

**前端整合:**

**檔案:**
- `frontend/src/api/ai.ts` (新建) - AI API 客戶端
- `frontend/src/views/AITalkView.vue` - AI 對話介面

**功能特點:**
- 完整的聊天介面 (訊息歷史、時間戳記)
- 自動滾動到最新訊息
- 顯示 AI 服務連線狀態
- 支援 Enter 鍵快速發送
- Loading 狀態顯示
- 錯誤處理與友善提示

**新增的 Python 依賴:**
- `httpx==0.25.2` - 非同步 HTTP 客戶端

**環境變數配置:**
```bash
# 在 backend/.env 中設定 (可選)
MCP_SERVER_URL=http://localhost:3001/api/chat
```

---

### 📦 新增的依賴套件

**Backend (requirements.txt):**
```
paramiko==3.4.0   # SSH 連線測試
httpx==0.25.2     # AI API 請求
```

**安裝指令:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install paramiko==3.4.0 httpx==0.25.2
```

---

### 🔧 設定說明

#### SSH 測試功能
- 預設使用 `root` 使用者連線
- 連線逾時設定為 5 秒
- SSH 資訊從 Inventory 的 `config` 欄位解析
- 測試結果會自動更新到資料庫的 `ssh_status` 欄位

#### AI 對話功能
- 預設連接 `http://localhost:3001/api/chat`
- 可透過環境變數 `MCP_SERVER_URL` 自訂 MCP server 位址
- 請求逾時設定為 30 秒
- 無法連線時會回傳友善的備援訊息

---

### 🚀 測試方式

#### 1. 測試 SSH 連線
```bash
# 1. 確保後端運行
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. 開啟前端
cd frontend
npm run dev

# 3. 操作步驟
# - 前往 Inventories 頁面
# - 勾選要測試的伺服器
# - 點擊「SSH連線測試」按鈕
# - 查看測試結果彈窗
```

#### 2. 測試 AI 對話
```bash
# 1. 開啟 AI Talk 頁面
# 2. 在輸入框輸入訊息
# 3. 按 Enter 或點擊 Send 按鈕
# 4. 查看 AI 回覆 (目前使用備援回應)

# 如要連接真實 MCP server:
# 在 backend/.env 設定 MCP_SERVER_URL
```

#### 3. API 直接測試
```bash
# SSH 測試
curl -X POST http://localhost:8000/api/inventories/test-ssh \
  -H "Content-Type: application/json" \
  -d '{"inventory_ids": [1, 2]}'

# AI 對話
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}],
    "model": "gpt-4"
  }'

# AI 健康檢查
curl http://localhost:8000/api/ai/health
```

---

### 📝 注意事項

1. **SSH 測試**
   - 需要確保目標伺服器的 SSH 服務正常運行
   - 確認防火牆允許 SSH 連線 (port 22)
   - Inventory 的 config 必須包含正確的 SSH 資訊

2. **AI 對話**
   - 目前使用備援回應機制
   - 實際部署時需要配置真實的 MCP server URL
   - 確認 MCP server 支援相同的 API 格式

3. **依賴安裝**
   - 安裝新套件後需要重新啟動後端服務
   - paramiko 需要 cryptography 套件 (已包含在 requirements.txt)

---

### 🎯 下一步建議

1. **PlaybookEditView API 整合**
   - 載入現有 Playbook 資料
   - 連接更新 API
   - 實作完整的編輯流程

2. **SSH 測試增強**
   - 支援自訂測試指令
   - 顯示更詳細的連線資訊 (延遲、SSH 版本等)
   - 記錄測試歷史

3. **AI 對話增強**
   - 整合真實的 LLM API (OpenAI/Claude/local models)
   - 支援 Ansible 專用指令建議
   - 聊天記錄持久化

4. **錯誤處理優化**
   - 統一的錯誤提示元件 (Toast/Notification)
   - 更詳細的錯誤訊息
   - 錯誤追蹤與日誌記錄
