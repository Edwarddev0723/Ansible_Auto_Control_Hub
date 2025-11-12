# Ansible Galaxy Collections 管理功能

## 🎯 功能概述

新增了完整的 Ansible Galaxy Collections 管理介面,提供視覺化的方式管理專案所需的 Ansible Collections,取代手動編輯 requirements.yml 和執行 CLI 命令。

---

## 📦 已建立的檔案

### 後端 (Backend)
- ✅ `app/routers/galaxy.py` - Galaxy API 路由
- ✅ `ansible/requirements.yml` - Collections 配置檔案
- ✅ `app/main.py` - 註冊 Galaxy 路由

### 前端 (Frontend)
- ✅ `src/api/galaxy.ts` - Galaxy API Client
- ✅ `src/views/GalaxyView.vue` - Galaxy 管理頁面
- ✅ `src/router/index.ts` - 註冊 /galaxy 路由
- ✅ `src/components/AppLayout.vue` - 側邊欄新增導航

---

## 🚀 啟動方式

### 1. 後端啟動
```bash
cd backend
# 如果 uvicorn 還在運行,會自動重載
# 如果沒有運行:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 前端啟動
```bash
cd frontend
npm run dev
# 訪問: http://localhost:5173/galaxy
```

---

## 🎨 功能說明

### Tab 1: Requirements.yml 管理

#### 功能列表:
- ✅ **視覺化編輯器**: 卡片式顯示所有 Collections
- ✅ **新增 Collection**: 點擊 ➕ 按鈕新增
- ✅ **編輯 Collection**: 修改名稱和版本
- ✅ **移除 Collection**: 從 requirements.yml 移除
- ✅ **單個安裝**: 安裝指定的 Collection
- ✅ **批次安裝**: 一鍵安裝所有 Collections
- ✅ **YAML 預覽**: 即時顯示 requirements.yml 內容

#### 操作流程:
1. 點擊「新增 Collection」
2. 輸入 Collection 名稱 (例: `community.docker`)
3. 輸入版本 (選填,留空使用 latest)
4. 點擊「新增」
5. 點擊「全部安裝」執行安裝

### Tab 2: 已安裝 Collections

#### 功能列表:
- ✅ **列出已安裝**: 執行 `ansible-galaxy collection list`
- ✅ **顯示詳細資訊**: Collection 名稱、版本、安裝路徑
- ✅ **卸載提示**: 顯示卸載指引 (Ansible 無內建卸載命令)

---

## 📡 API 端點

### GET `/api/galaxy/collections`
列出已安裝的 Collections

**回應範例:**
```json
{
  "success": true,
  "data": [
    {
      "name": "community.docker",
      "version": "4.8.1",
      "path": "/usr/share/ansible/collections/ansible_collections"
    }
  ]
}
```

### POST `/api/galaxy/collections/install`
安裝單一 Collection

**請求:**
```json
{
  "name": "community.docker",
  "version": "4.8.1"
}
```

**回應:**
```json
{
  "success": true,
  "message": "Installation completed",
  "output": "Installing 'community.docker:4.8.1'..."
}
```

### GET `/api/galaxy/requirements`
讀取 requirements.yml

**回應:**
```json
{
  "success": true,
  "data": {
    "collections": [
      {
        "name": "community.docker",
        "version": "4.8.1"
      }
    ],
    "yaml": "collections:\n  - name: community.docker\n    version: '4.8.1'\n"
  }
}
```

### POST `/api/galaxy/requirements`
更新 requirements.yml

**請求:**
```json
{
  "collections": [
    {
      "name": "community.docker",
      "version": "4.8.1"
    },
    {
      "name": "ansible.posix",
      "version": "1.5.0"
    }
  ]
}
```

### POST `/api/galaxy/requirements/install`
安裝 requirements.yml 中的所有 Collections

**回應:**
```json
{
  "success": true,
  "message": "Installation completed",
  "output": "Process install dependency map\n..."
}
```

### DELETE `/api/galaxy/collections/{collection_name}`
卸載 Collection (提供手動刪除指引)

**回應:**
```json
{
  "success": true,
  "message": "Collection found at: /path/to/collections/community/docker",
  "path": "/path/to/collections/community/docker",
  "note": "Please manually delete this directory to uninstall"
}
```

### GET `/api/galaxy/playbooks/{playbook_id}/dependencies`
檢查 Playbook 依賴 (未來功能)

**回應:**
```json
{
  "success": true,
  "data": {
    "playbook_id": 1,
    "playbook_name": "Deploy App",
    "dependencies": [
      {
        "collection": "community.docker",
        "satisfied": true,
        "required": true
      }
    ],
    "all_satisfied": true
  }
}
```

---

## 🔧 跨平台支援

### Windows (使用 WSL)
```python
# 自動轉換路徑
C:/Users/.../requirements.yml -> /mnt/c/Users/.../requirements.yml

# 執行命令
wsl ansible-galaxy collection install -r /mnt/c/.../requirements.yml
```

### macOS / Linux
```python
# 直接執行
ansible-galaxy collection install -r /path/to/requirements.yml
```

---

## 🎯 使用場景

### 場景 1: 新增專案依賴
1. 訪問 `/galaxy` 頁面
2. 切換到「Requirements.yml」Tab
3. 點擊「新增 Collection」
4. 輸入 `community.docker` 和版本 `4.8.1`
5. 點擊「全部安裝」

### 場景 2: 檢查已安裝 Collections
1. 訪問 `/galaxy` 頁面
2. 切換到「已安裝 Collections」Tab
3. 查看所有已安裝的 Collections 及其版本

### 場景 3: 更新 Collection 版本
1. 在「Requirements.yml」Tab 找到要更新的 Collection
2. 點擊「編輯」
3. 修改版本號
4. 點擊「更新」
5. 點擊該 Collection 的「安裝」按鈕 (使用 --force 覆蓋)

---

## 📊 UI 截圖指引

### Requirements.yml 管理頁面
- 頂部: 標題和全部安裝按鈕
- 中間: Collection 卡片網格 (3 列)
- 每張卡片顯示:
  - Collection 名稱
  - 版本號
  - 安裝/編輯按鈕
  - 移除按鈕 (❌)
- 右下角: 新增 Collection 卡片 (虛線框 + ➕)
- 底部: YAML 預覽區塊

### 已安裝 Collections 頁面
- 頂部: 標題和重新載入按鈕
- 中間: 表格顯示
  - Collection 名稱
  - 版本
  - 安裝路徑
  - 卸載按鈕

### Toast 提示
- 固定在右下角
- 顯示操作結果 (成功/失敗)
- 包含詳細輸出 (可展開)
- 5 秒後自動消失

---

## 🐛 已知限制

1. **卸載功能**: Ansible Galaxy CLI 沒有內建卸載命令,目前只提供路徑資訊供手動刪除
2. **依賴檢查**: Playbook 依賴檢查功能為簡單的模式匹配,可能無法偵測所有 Collections
3. **版本衝突**: 不檢查 Collection 之間的版本衝突

---

## 🚀 未來增強功能

### 第二階段
- [ ] 從 Ansible Galaxy 官方倉庫搜尋 Collections
- [ ] 顯示 Collection 詳細資訊 (README, 模組列表)
- [ ] 自動檢測 Playbook 中使用的 Collections
- [ ] 批次更新所有 Collections

### 第三階段
- [ ] Collection 依賴關係視覺化
- [ ] 支援私有 Galaxy 伺服器
- [ ] Collection 變更歷史記錄
- [ ] 匯出/匯入 requirements.yml

---

## 📝 測試步驟

### 1. 測試 Requirements.yml 管理
```bash
# 訪問頁面
http://localhost:5173/galaxy

# 新增 Collection
1. 點擊「新增 Collection」
2. 輸入 name: community.general
3. 輸入 version: 8.0.0
4. 點擊「新增」
5. 確認卡片出現

# 編輯 Collection
1. 點擊卡片上的「編輯」
2. 修改版本為 8.1.0
3. 點擊「更新」
4. 確認版本已更新

# 安裝 Collections
1. 點擊「全部安裝」
2. 等待安裝完成
3. 確認 Toast 顯示成功訊息
```

### 2. 測試已安裝列表
```bash
# 切換 Tab
1. 點擊「已安裝 Collections」Tab
2. 確認顯示已安裝的 Collections
3. 確認顯示版本和路徑資訊

# 重新載入
1. 點擊「重新載入」
2. 確認列表更新
```

### 3. 測試 API (使用 curl)
```bash
# 列出已安裝
curl http://localhost:8000/api/galaxy/collections

# 讀取 requirements
curl http://localhost:8000/api/galaxy/requirements

# 安裝 Collection
curl -X POST http://localhost:8000/api/galaxy/collections/install \
  -H "Content-Type: application/json" \
  -d '{"name": "community.docker", "version": "4.8.1"}'

# 安裝 requirements
curl -X POST http://localhost:8000/api/galaxy/requirements/install
```

---

## 🎉 完成!

Galaxy Collections 管理功能已完整建立,提供直觀的 GUI 介面來管理 Ansible Collections,大幅提升開發效率!

**訪問網址**: http://localhost:5173/galaxy
