# Ansible Auto Control Hub - Backend API 規格文件

> 本文件根據前端代碼推論後端 API 需求規格  
> 文件版本: 1.0  
> 最後更新: 2025-11-10

## 目錄

- [概述](#概述)
- [前端功能清單](#前端功能清單)
- [通用規範](#通用規範)
- [Inventory 管理 API](#inventory-管理-api)
- [Playbook 管理 API](#playbook-管理-api)
- [AI 對話 API](#ai-對話-api)
- [SSH 連線測試 API](#ssh-連線測試-api)
- [資料模型](#資料模型)
- [錯誤代碼](#錯誤代碼)
- [API 使用對照表](#api-使用對照表)

---

## 前端功能清單

### 實際已實作的頁面與功能

#### 1. **Inventories 列表頁** (`/` - `InventoriesView.vue`)
- ✅ 顯示 Inventory 列表 (表格形式)
- ✅ 搜尋功能 (依名稱)
- ✅ 分頁功能
- ✅ 勾選多個項目
- ✅ SSH 連線測試按鈕
- ✅ 新增按鈕 → 跳轉到新增頁
- ✅ 編輯按鈕 → 跳轉到編輯頁
- ✅ 刪除按鈕 (含確認對話框)

#### 2. **Inventory 新增/編輯頁** (`/inventory/new`, `/inventory/edit/:id` - `InventoryDetailView.vue`)
- ✅ Textarea 編輯 Ansible Inventory 配置
- ✅ 標題顯示 (目前寫死，應改為動態)
- ✅ 儲存按鈕
- ✅ 取消按鈕 → 返回列表頁
- ⚠️ 目前無 API 串接，使用本地資料

#### 3. **Playbook 列表頁** (`/playbook` - `PlaybookView.vue`)
- ✅ 顯示 Playbook 列表
- ✅ 搜尋功能 (依名稱)
- ✅ 分頁功能
- ✅ 勾選多個項目
- ✅ 執行按鈕 (執行勾選的 Playbooks)
- ✅ 新增按鈕 → 跳轉到新增頁
- ✅ 編輯按鈕 → 跳轉到編輯頁
- ✅ 刪除按鈕 (含確認對話框)

#### 4. **Playbook 新增頁** (`/playbook/new` - `PlaybookCreateView.vue`)
- ✅ Main 頁籤
  - Name 輸入
  - Hosts 輸入
  - Gather_facts 選擇
  - 新增 Main 欄位按鈕
- ✅ Tasks 頁籤
  - 顯示多個 Task
  - 每個 Task 有啟用/停用開關
  - Textarea 編輯 YAML
  - 新增 Task 按鈕
- ✅ 下一步/上一步按鈕
- ✅ 儲存並返回按鈕

#### 5. **Playbook 編輯頁** (`/playbook/edit/:id` - `PlaybookEditView.vue`)
- ✅ 基礎資訊頁籤
  - Playbook 名稱
  - 型態選擇 (Machine/Other)
- ✅ Main 頁籤 (同新增頁)
- ✅ Task 頁籤 (同新增頁)
- ✅ 上一步/下一步按鈕
- ✅ 儲存並返回按鈕

#### 6. **AI 對話頁** (`/ai-deploy` - `AITalkView.vue`)
- ✅ 顯示對話記錄
- ✅ 訊息輸入框
- ✅ 發送按鈕
- ✅ 快速回覆按鈕 (Yes/No)
- ✅ 語音輸入按鈕
- ✅ 附件按鈕 (連結、圖片)
- ✅ 訊息自動滾動到底部
- ✅ 模擬 AI 自動回覆

### 目前狀態
- ❌ **未實作 API 串接**: 所有資料為前端本地模擬資料
- ❌ **無 API 服務層**: 沒有 `src/api/` 或 `src/services/` 目錄
- ❌ **無狀態管理**: 沒有使用 Pinia 或 Vuex
- ✅ **路由正常**: Vue Router 配置完整
- ✅ **UI 完整**: 所有頁面已完成視覺設計

---

## 概述

Ansible Auto Control Hub 是一個 Ansible 自動化管理平台,提供 Inventory 管理、Playbook 管理、AI 輔助部署等功能。

### 技術棧
- 前端: Vue 3 + TypeScript + Vite + Tailwind CSS + Vue Router 4
- 後端: Fest API (待實作)
- 狀態: 前端目前使用本地模擬資料，未串接實際 API

### Base URL
```
開發環境: http://localhost:8000/api
生產環境: https://api.ansible-hub.example.com/api
```

### 前端路由結構
```
/ (Inventories 列表)
/inventory/new (新增 Inventory)
/inventory/edit/:id (編輯 Inventory)
/playbook (Playbook 列表)
/playbook/new (新增 Playbook)
/playbook/edit/:id (編輯 Playbook)
/ai-deploy (AI 對話)
```

---

## 通用規範

### 請求格式
- Content-Type: `application/json`
- 編碼: UTF-8
- 認證方式: Bearer Token (推論)

### 響應格式

**成功響應**
```json
{
  "success": true,
  "data": {},
  "message": "操作成功"
}
```

**失敗響應**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "錯誤訊息"
  }
}
```

### 分頁參數
- `page`: 頁碼 (從 1 開始)
- `per_page`: 每頁數量 (默認 10)

### 分頁響應
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 100,
      "total_pages": 10
    }
  }
}
```

---

## Inventory 管理 API

### 1. 獲取 Inventory 列表

**端點**: `GET /inventories`

**查詢參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| search | string | 否 | 搜尋關鍵字 (搜尋名稱) |
| page | integer | 否 | 頁碼 (默認 1) |
| per_page | integer | 否 | 每頁數量 (默認 10) |

**請求範例**:
```bash
GET /api/inventories?search=Ansible&page=1&per_page=10
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Ansible GUI Inventory",
        "status": "On",
        "ssh_status": "Connected",
        "group": "Default",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-10T00:00:00Z"
      },
      {
        "id": 2,
        "name": "Ansible introduction Inventory",
        "status": "Off",
        "ssh_status": "Unconnected",
        "group": "Default",
        "created_at": "2025-01-02T00:00:00Z",
        "updated_at": "2025-01-09T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 2,
      "total_pages": 1
    }
  }
}
```

---

### 2. 獲取單一 Inventory (編輯頁使用)

**端點**: `GET /inventories/{id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Inventory ID |

**前端使用場景**: `InventoryDetailView.vue` 編輯模式時載入資料

**請求範例**:
```bash
GET /api/inventories/1
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Ansible GUI Inventory",
    "status": "On",
    "sshStatus": "Connected",
    "group": "Default",
    "config": "server1 ansible_ssh_host=127.0.0.1 ansible_ssh_port=55000 ansible_ssh_pass=docker",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-10T00:00:00Z"
  }
}
```

**注意**: 欄位命名使用 camelCase 以符合前端 TypeScript 規範

---

### 3. 創建 Inventory

**端點**: `POST /inventories`

**前端使用場景**: `InventoryDetailView.vue` 新增模式儲存時

**請求體**:
```json
{
  "name": "New Inventory",
  "group": "Default",
  "config": "server1 ansible_ssh_host=192.168.1.100 ansible_ssh_port=22"
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| name | string | 是 | Inventory 名稱 |
| group | string | 否 | 伺服器群組 (默認 "Default") |
| config | string | 是 | Ansible Inventory 配置內容 (YAML/INI 格式) |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "New Inventory",
    "status": "Off",
    "sshStatus": "Unconnected",
    "group": "Default",
    "config": "server1 ansible_ssh_host=192.168.1.100 ansible_ssh_port=22",
    "createdAt": "2025-01-10T10:00:00Z",
    "updatedAt": "2025-01-10T10:00:00Z"
  },
  "message": "Inventory 創建成功"
}
```

---

### 4. 更新 Inventory

**端點**: `PUT /inventories/{id}`

**前端使用場景**: `InventoryDetailView.vue` 編輯模式儲存時

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Inventory ID |

**請求體**:
```json
{
  "name": "Updated Inventory Name",
  "group": "Production",
  "config": "server1 ansible_ssh_host=192.168.1.101 ansible_ssh_port=22"
}
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Updated Inventory Name",
    "status": "On",
    "sshStatus": "Connected",
    "group": "Production",
    "config": "server1 ansible_ssh_host=192.168.1.101 ansible_ssh_port=22",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-10T10:30:00Z"
  },
  "message": "Inventory 更新成功"
}
```

---

### 5. 刪除 Inventory

**端點**: `DELETE /inventories/{id}`

**前端使用場景**: `InventoriesView.vue` 列表刪除按鈕

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Inventory ID |

**請求範例**:
```bash
DELETE /api/inventories/1
```

**響應範例**:
```json
{
  "success": true,
  "message": "Inventory 刪除成功"
}
```

**前端行為**: 刪除前會顯示確認對話框 `confirm('確定要刪除 ${inventory.name}?')`

---

## Playbook 管理 API

### 1. 獲取 Playbook 列表

**端點**: `GET /playbooks`

**查詢參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| search | string | 否 | 搜尋關鍵字 (搜尋名稱) |
| type | string | 否 | Playbook 類型 (Machine, Other) |
| status | string | 否 | 結果狀態 (Success, Fail, Not start) |
| page | integer | 否 | 頁碼 (默認 1) |
| per_page | integer | 否 | 每頁數量 (默認 10) |

**請求範例**:
```bash
GET /api/playbooks?search=Ansible&type=Machine&page=1
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Ansible GUI",
        "type": "Machine",
        "status": "Success",
        "last_run_at": "2025-01-09T10:00:00Z",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-09T10:00:00Z"
      },
      {
        "id": 2,
        "name": "Ansible introduction",
        "type": "Machine",
        "status": "Fail",
        "last_run_at": "2025-01-08T15:30:00Z",
        "created_at": "2025-01-02T00:00:00Z",
        "updated_at": "2025-01-08T15:30:00Z"
      },
      {
        "id": 3,
        "name": "Ansible introduction",
        "type": "Machine",
        "status": "Not start",
        "last_run_at": null,
        "created_at": "2025-01-03T00:00:00Z",
        "updated_at": "2025-01-03T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 3,
      "total_pages": 1
    }
  }
}
```

---

### 2. 獲取單一 Playbook

**端點**: `GET /playbooks/{id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Playbook ID |

**請求範例**:
```bash
GET /api/playbooks/1
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Ansible GUI",
    "type": "Machine",
    "status": "Success",
    "main": {
      "hosts": "all",
      "gather_facts": false
    },
    "tasks": [
      {
        "id": 1,
        "enabled": true,
        "content": "name: test1\ncommunity:\n  name: demo\nstate: absent"
      },
      {
        "id": 2,
        "enabled": true,
        "content": "name: test2\nCommunity2:\n  name: demo\nstate: absent"
      },
      {
        "id": 3,
        "enabled": false,
        "content": "name: test3\ndebug:\n  msg: \"XXX\""
      }
    ],
    "last_run_at": "2025-01-09T10:00:00Z",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-09T10:00:00Z"
  }
}
```

---

### 3. 創建 Playbook

**端點**: `POST /playbooks`

**請求體**:
```json
{
  "name": "New Playbook",
  "type": "Machine",
  "main": {
    "hosts": "all",
    "gather_facts": false
  },
  "tasks": [
    {
      "enabled": true,
      "content": "name: Install package\napt:\n  name: nginx\n  state: present"
    }
  ]
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| name | string | 是 | Playbook 名稱 |
| type | string | 是 | Playbook 類型 (Machine, Other) |
| main | object | 是 | Playbook 主配置 |
| main.hosts | string | 是 | 目標主機 |
| main.gather_facts | boolean | 否 | 是否收集系統資訊 (默認 false) |
| tasks | array | 是 | 任務列表 |
| tasks[].enabled | boolean | 是 | 任務是否啟用 |
| tasks[].content | string | 是 | 任務 YAML 內容 |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 4,
    "name": "New Playbook",
    "type": "Machine",
    "status": "Not start",
    "main": {
      "hosts": "all",
      "gather_facts": false
    },
    "tasks": [
      {
        "id": 1,
        "enabled": true,
        "content": "name: Install package\napt:\n  name: nginx\n  state: present"
      }
    ],
    "last_run_at": null,
    "created_at": "2025-01-10T11:00:00Z",
    "updated_at": "2025-01-10T11:00:00Z"
  },
  "message": "Playbook 創建成功"
}
```

---

### 4. 更新 Playbook

**端點**: `PUT /playbooks/{id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Playbook ID |

**請求體**:
```json
{
  "name": "Updated Playbook",
  "type": "Machine",
  "main": {
    "hosts": "webservers",
    "gather_facts": true
  },
  "tasks": [
    {
      "id": 1,
      "enabled": true,
      "content": "name: test1\ncommunity:\n  name: demo\nstate: present"
    },
    {
      "enabled": true,
      "content": "name: new task\ndebug:\n  msg: \"Hello\""
    }
  ]
}
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Updated Playbook",
    "type": "Machine",
    "status": "Success",
    "main": {
      "hosts": "webservers",
      "gather_facts": true
    },
    "tasks": [
      {
        "id": 1,
        "enabled": true,
        "content": "name: test1\ncommunity:\n  name: demo\nstate: present"
      },
      {
        "id": 5,
        "enabled": true,
        "content": "name: new task\ndebug:\n  msg: \"Hello\""
      }
    ],
    "last_run_at": "2025-01-09T10:00:00Z",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-10T11:30:00Z"
  },
  "message": "Playbook 更新成功"
}
```

---

### 5. 刪除 Playbook

**端點**: `DELETE /playbooks/{id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Playbook ID |

**請求範例**:
```bash
DELETE /api/playbooks/1
```

**響應範例**:
```json
{
  "success": true,
  "message": "Playbook 刪除成功"
}
```

---

### 6. 執行 Playbook

**端點**: `POST /playbooks/execute`

**前端使用場景**: `PlaybookView.vue` 的「執行」按鈕 (執行勾選的 Playbooks)

**請求體**:
```json
{
  "playbookIds": [1, 2, 3],
  "inventoryId": 1,
  "extraVars": {
    "env": "production"
  }
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| playbookIds | array | 是 | 要執行的 Playbook ID 列表 (前端從勾選項目取得) |
| inventoryId | integer | 否 | 使用的 Inventory ID (可能需要彈出選擇框) |
| extraVars | object | 否 | 額外變數 |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "jobId": "job-123456",
    "status": "queued",
    "playbooks": [
      {
        "id": 1,
        "name": "Ansible GUI",
        "status": "queued"
      },
      {
        "id": 2,
        "name": "Ansible introduction",
        "status": "queued"
      }
    ],
    "createdAt": "2025-01-10T12:00:00Z"
  },
  "message": "Playbook 執行已排程"
}
```

**前端行為**: 
- 點擊執行按鈕時收集所有 `selected: true` 的項目
- 顯示提示: `alert('執行 ${selected.length} 個 Playbook')`
- 建議改為顯示執行中狀態並輪詢結果

---

### 7. 獲取 Playbook 執行狀態

**端點**: `GET /playbooks/jobs/{job_id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| job_id | string | 是 | Job ID |

**請求範例**:
```bash
GET /api/playbooks/jobs/job-123456
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "job_id": "job-123456",
    "status": "completed",
    "playbooks": [
      {
        "id": 1,
        "name": "Ansible GUI",
        "status": "success",
        "output": "PLAY [all] *************\n\nTASK [test1] *************\nok: [server1]\n\nPLAY RECAP *************\nserver1: ok=1 changed=0 unreachable=0 failed=0",
        "started_at": "2025-01-10T12:00:05Z",
        "completed_at": "2025-01-10T12:00:10Z"
      },
      {
        "id": 2,
        "name": "Ansible introduction",
        "status": "failed",
        "output": "PLAY [all] *************\n\nTASK [test2] *************\nfatal: [server1]: FAILED!",
        "started_at": "2025-01-10T12:00:11Z",
        "completed_at": "2025-01-10T12:00:15Z"
      }
    ],
    "created_at": "2025-01-10T12:00:00Z",
    "started_at": "2025-01-10T12:00:05Z",
    "completed_at": "2025-01-10T12:00:15Z"
  }
}
```

---

## SSH 連線測試 API

### 測試 SSH 連線

**端點**: `POST /ssh/test`

**前端使用場景**: `InventoriesView.vue` 的「SSH連線測試」按鈕

**請求體**:
```json
{
  "inventoryIds": [1, 2]
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| inventoryIds | array | 否 | 要測試的 Inventory ID 列表。若為空或省略,則測試所有 Inventory |

**請求範例 1 (測試選中的):**
```json
{
  "inventoryIds": [1, 2]
}
```

**請求範例 2 (測試全部):**
```json
{}
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "inventoryId": 1,
        "inventoryName": "Ansible GUI Inventory",
        "status": "Connected",
        "message": "SSH 連線成功",
        "testedAt": "2025-01-10T12:30:00Z"
      },
      {
        "inventoryId": 2,
        "inventoryName": "Ansible introduction Inventory",
        "status": "Unconnected",
        "message": "連線逾時: Connection timed out",
        "testedAt": "2025-01-10T12:30:05Z"
      }
    ]
  },
  "message": "SSH 連線測試完成"
}
```

**前端處理建議**:
- 測試時顯示 Loading 狀態
- 測試完成後更新列表中的 `sshStatus` 欄位
- 顯示測試結果通知 (成功/失敗數量)

---

## AI 對話 API

### 1. 發送訊息

**端點**: `POST /ai/messages`

**請求體**:
```json
{
  "message": "如何部署 Nginx?",
  "context": {
    "conversation_id": "conv-123456",
    "inventory_id": 1
  }
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| message | string | 是 | 用戶訊息 |
| context | object | 否 | 對話上下文 |
| context.conversation_id | string | 否 | 對話 ID (用於保持上下文) |
| context.inventory_id | integer | 否 | 相關的 Inventory ID |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "conversation_id": "conv-123456",
    "user_message": {
      "id": "msg-1",
      "text": "如何部署 Nginx?",
      "time": "6:30 pm",
      "is_user": true,
      "created_at": "2025-01-10T18:30:00Z"
    },
    "ai_response": {
      "id": "msg-2",
      "text": "要部署 Nginx,您可以使用 Ansible playbook。我建議建立一個包含以下步驟的 playbook: 1) 更新套件列表 2) 安裝 nginx 3) 啟動並啟用 nginx 服務。需要我幫您生成 playbook 嗎?",
      "time": "6:30 pm",
      "is_user": false,
      "created_at": "2025-01-10T18:30:02Z"
    },
    "quick_replies": ["Yes", "No"],
    "suggested_actions": [
      {
        "type": "create_playbook",
        "label": "建立 Nginx 部署 Playbook",
        "data": {
          "name": "Deploy Nginx",
          "tasks": [...]
        }
      }
    ]
  }
}
```

---

### 2. 獲取對話歷史

**端點**: `GET /ai/conversations/{conversation_id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| conversation_id | string | 是 | 對話 ID |

**請求範例**:
```bash
GET /api/ai/conversations/conv-123456
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "conversation_id": "conv-123456",
    "messages": [
      {
        "id": "msg-1",
        "text": "如何部署 Nginx?",
        "time": "6:30 pm",
        "is_user": true,
        "created_at": "2025-01-10T18:30:00Z"
      },
      {
        "id": "msg-2",
        "text": "要部署 Nginx,您可以使用 Ansible playbook...",
        "time": "6:30 pm",
        "is_user": false,
        "created_at": "2025-01-10T18:30:02Z"
      }
    ],
    "created_at": "2025-01-10T18:30:00Z",
    "updated_at": "2025-01-10T18:30:02Z"
  }
}
```

---

### 3. 開始新對話

**端點**: `POST /ai/conversations`

**請求體**:
```json
{
  "title": "部署 Nginx 諮詢",
  "context": {
    "inventory_id": 1
  }
}
```

**響應範例**:
```json
{
  "success": true,
  "data": {
    "conversation_id": "conv-789012",
    "title": "部署 Nginx 諮詢",
    "messages": [],
    "created_at": "2025-01-10T19:00:00Z"
  },
  "message": "新對話已創建"
}
```

---

## 資料模型

### Inventory 模型

```typescript
// 前端實際使用的模型 (InventoriesView.vue)
interface Inventory {
  id: number
  name: string
  status: 'On' | 'Off'
  sshStatus: 'Connected' | 'Unconnected'  // camelCase
  group: string
  selected: boolean  // 前端用於勾選，不需傳給後端
}

// API 完整模型 (包含編輯頁需要的欄位)
interface InventoryDetail extends Inventory {
  config: string        // Ansible inventory 配置內容
  createdAt: string     // ISO 8601 格式
  updatedAt: string     // ISO 8601 格式
}
```

### Playbook 模型

```typescript
// 前端列表使用的模型 (PlaybookView.vue)
interface PlaybookItem {
  id: number
  name: string
  type: 'Machine' | 'Other'
  status: 'Success' | 'Fail' | 'Not start'
  selected: boolean  // 前端用於勾選
}

// API 完整模型 (包含編輯頁需要的欄位)
interface PlaybookDetail extends Omit<PlaybookItem, 'selected'> {
  main: PlaybookMain
  tasks: PlaybookTask[]
  lastRunAt: string | null  // 最後執行時間
  createdAt: string
  updatedAt: string
}

interface PlaybookMain {
  hosts: string              // 目標主機
  gatherFacts: boolean       // 是否收集系統資訊
  [key: string]: any         // 其他自訂欄位
}

interface PlaybookTask {
  id: number                 // Task ID
  enabled: boolean           // 是否啟用
  content: string            // YAML 格式的任務內容
}
```

### AI 訊息模型

```typescript
// 前端使用的模型 (AITalkView.vue)
interface Message {
  id: number
  text: string
  time: string           // 格式: "6:30 pm"
  isUser: boolean        // camelCase
}

// API 完整模型
interface AIMessage extends Message {
  createdAt: string      // ISO 8601 格式
}

interface Conversation {
  conversationId: string
  title?: string
  messages: AIMessage[]
  createdAt: string
  updatedAt: string
}
```

### 說明
- 所有 API 響應統一使用 **camelCase** 命名
- 前端模型中的 `selected` 欄位僅供前端使用，不包含在 API 響應中
- 時間格式統一使用 **ISO 8601** (如: `2025-01-10T12:30:00Z`)

---

## 錯誤代碼

### HTTP 狀態碼

| 狀態碼 | 說明 |
|--------|------|
| 200 | 請求成功 |
| 201 | 創建成功 |
| 400 | 請求參數錯誤 |
| 401 | 未授權 |
| 403 | 無權限 |
| 404 | 資源不存在 |
| 409 | 資源衝突 |
| 422 | 驗證失敗 |
| 500 | 伺服器內部錯誤 |
| 503 | 服務暫時不可用 |

### 錯誤代碼列表

| 錯誤代碼 | 說明 |
|----------|------|
| `INVENTORY_NOT_FOUND` | Inventory 不存在 |
| `INVENTORY_NAME_DUPLICATE` | Inventory 名稱重複 |
| `INVENTORY_IN_USE` | Inventory 正在使用中,無法刪除 |
| `INVALID_INVENTORY_CONFIG` | Inventory 配置格式錯誤 |
| `PLAYBOOK_NOT_FOUND` | Playbook 不存在 |
| `PLAYBOOK_NAME_DUPLICATE` | Playbook 名稱重複 |
| `PLAYBOOK_VALIDATION_ERROR` | Playbook 驗證失敗 |
| `INVALID_YAML_FORMAT` | YAML 格式錯誤 |
| `SSH_CONNECTION_FAILED` | SSH 連線失敗 |
| `SSH_AUTHENTICATION_FAILED` | SSH 認證失敗 |
| `SSH_TIMEOUT` | SSH 連線逾時 |
| `PLAYBOOK_EXECUTION_FAILED` | Playbook 執行失敗 |
| `JOB_NOT_FOUND` | Job 不存在 |
| `CONVERSATION_NOT_FOUND` | 對話不存在 |
| `AI_SERVICE_UNAVAILABLE` | AI 服務暫時不可用 |
| `INVALID_MESSAGE_FORMAT` | 訊息格式錯誤 |

---

## API 使用對照表

### 前端操作與 API 端點對應

| 前端頁面 | 操作 | 需要的 API | HTTP 方法 | 說明 |
|---------|------|-----------|----------|------|
| **InventoriesView** | 載入列表 | `/api/inventories` | GET | 支援搜尋、分頁 |
| | SSH 測試 | `/api/ssh/test` | POST | 測試選中或全部 |
| | 刪除 | `/api/inventories/:id` | DELETE | 含確認對話框 |
| **InventoryDetailView** | 載入 (編輯) | `/api/inventories/:id` | GET | 取得配置內容 |
| | 儲存 (新增) | `/api/inventories` | POST | 含 name, group, config |
| | 儲存 (編輯) | `/api/inventories/:id` | PUT | 更新配置 |
| **PlaybookView** | 載入列表 | `/api/playbooks` | GET | 支援搜尋、分頁 |
| | 執行 | `/api/playbooks/execute` | POST | 執行勾選的項目 |
| | 刪除 | `/api/playbooks/:id` | DELETE | 含確認對話框 |
| **PlaybookCreateView** | 儲存 | `/api/playbooks` | POST | 含 main 和 tasks |
| **PlaybookEditView** | 載入 | `/api/playbooks/:id` | GET | 取得完整資料 |
| | 儲存 | `/api/playbooks/:id` | PUT | 更新 playbook |
| **AITalkView** | 發送訊息 | `/api/ai/messages` | POST | AI 對話 |
| | 載入歷史 | `/api/ai/conversations/:id` | GET | (選用) |

### API 實作優先順序建議

#### 第一階段 - 核心功能 (優先實作)
1. ✅ `GET /api/inventories` - Inventory 列表
2. ✅ `POST /api/inventories` - 新增 Inventory
3. ✅ `GET /api/inventories/:id` - 取得單一 Inventory
4. ✅ `PUT /api/inventories/:id` - 更新 Inventory
5. ✅ `DELETE /api/inventories/:id` - 刪除 Inventory

#### 第二階段 - Playbook 管理
6. ✅ `GET /api/playbooks` - Playbook 列表
7. ✅ `POST /api/playbooks` - 新增 Playbook
8. ✅ `GET /api/playbooks/:id` - 取得單一 Playbook
9. ✅ `PUT /api/playbooks/:id` - 更新 Playbook
10. ✅ `DELETE /api/playbooks/:id` - 刪除 Playbook

#### 第三階段 - 執行功能
11. ✅ `POST /api/playbooks/execute` - 執行 Playbook
12. ✅ `GET /api/playbooks/jobs/:jobId` - 查詢執行狀態
13. ✅ `POST /api/ssh/test` - SSH 連線測試

#### 第四階段 - AI 功能
14. ✅ `POST /api/ai/messages` - AI 對話
15. ⭕ `GET /api/ai/conversations/:id` - 對話歷史 (選用)
16. ⭕ `POST /api/ai/conversations` - 新對話 (選用)

---

## 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.0 | 2025-01-10 | 初始版本,根據前端代碼推論 API 規格 |
| 1.1 | 2025-01-11 | 修正為 camelCase 命名，補充前端功能清單與使用對照表 |

---

## 注意事項

### 重要說明
1. ✅ 本文件已根據前端實際代碼分析完成
2. ✅ 所有欄位名稱統一使用 **camelCase** (如 `sshStatus`, `createdAt`)
3. ✅ 所有時間格式使用 **ISO 8601** 標準 (UTC 時區)
4. ⚠️ 前端目前**未串接任何 API**，使用本地模擬資料
5. ⚠️ 前端無 API 服務層 (`src/api/` 或 `src/services/`)

### 後端實作建議
- 使用 FastAPI / Flask / Express.js 等框架
- 實作 CORS 設定 (允許 `http://localhost:5173`)
- 回應格式統一使用文件中的規範
- 錯誤處理使用統一的錯誤代碼
- 考慮加入 JWT 認證機制

### 前端串接建議
1. 建立 `src/api/client.ts` - Axios 客戶端配置
2. 建立 `src/api/inventory.ts` - Inventory API 函式
3. 建立 `src/api/playbook.ts` - Playbook API 函式
4. 建立 `src/api/ai.ts` - AI API 函式
5. 考慮使用 Pinia 進行狀態管理

---

**文件結束**
