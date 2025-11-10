# Ansible Auto Control Hub - Backend API 規格文件

> 本文件根據前端代碼推論後端 API 需求規格  
> 文件版本: 1.0  
> 最後更新: 2025-11-10

## 目錄

- [概述](#概述)
- [通用規範](#通用規範)
- [Inventory 管理 API](#inventory-管理-api)
- [Playbook 管理 API](#playbook-管理-api)
- [AI 對話 API](#ai-對話-api)
- [SSH 連線測試 API](#ssh-連線測試-api)
- [資料模型](#資料模型)
- [錯誤代碼](#錯誤代碼)

---

## 概述

Ansible Auto Control Hub 是一個 Ansible 自動化管理平台,提供 Inventory 管理、Playbook 管理、AI 輔助部署等功能。

### 技術棧
- 前端: Vue 3 + TypeScript + Vite + Tailwind CSS
- 路由: Vue Router 4
- 後端 API: RESTful API (推論)

### Base URL
```
開發環境: http://localhost:8000/api
生產環境: https://api.ansible-hub.example.com/api
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

### 2. 獲取單一 Inventory

**端點**: `GET /inventories/{id}`

**路徑參數**:
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | integer | 是 | Inventory ID |

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
    "ssh_status": "Connected",
    "group": "Default",
    "config": "server1 ansible_ssh_host=127.0.0.1 ansible_ssh_port=55000 ansible_ssh_pass=docker",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-10T00:00:00Z"
  }
}
```

---

### 3. 創建 Inventory

**端點**: `POST /inventories`

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
| config | string | 是 | Ansible Inventory 配置內容 |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "New Inventory",
    "status": "Off",
    "ssh_status": "Unconnected",
    "group": "Default",
    "config": "server1 ansible_ssh_host=192.168.1.100 ansible_ssh_port=22",
    "created_at": "2025-01-10T10:00:00Z",
    "updated_at": "2025-01-10T10:00:00Z"
  },
  "message": "Inventory 創建成功"
}
```

---

### 4. 更新 Inventory

**端點**: `PUT /inventories/{id}`

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
    "ssh_status": "Connected",
    "group": "Production",
    "config": "server1 ansible_ssh_host=192.168.1.101 ansible_ssh_port=22",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-10T10:30:00Z"
  },
  "message": "Inventory 更新成功"
}
```

---

### 5. 刪除 Inventory

**端點**: `DELETE /inventories/{id}`

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

**請求體**:
```json
{
  "playbook_ids": [1, 2, 3],
  "inventory_id": 1,
  "extra_vars": {
    "env": "production"
  }
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| playbook_ids | array | 是 | 要執行的 Playbook ID 列表 |
| inventory_id | integer | 否 | 使用的 Inventory ID |
| extra_vars | object | 否 | 額外變數 |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "job_id": "job-123456",
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
    "created_at": "2025-01-10T12:00:00Z"
  },
  "message": "Playbook 執行已排程"
}
```

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

**請求體**:
```json
{
  "inventory_ids": [1, 2]
}
```

**欄位說明**:
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| inventory_ids | array | 否 | 要測試的 Inventory ID 列表。若為空,則測試所有 Inventory |

**響應範例**:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "inventory_id": 1,
        "inventory_name": "Ansible GUI Inventory",
        "status": "Connected",
        "message": "SSH 連線成功",
        "tested_at": "2025-01-10T12:30:00Z"
      },
      {
        "inventory_id": 2,
        "inventory_name": "Ansible introduction Inventory",
        "status": "Unconnected",
        "message": "連線逾時",
        "tested_at": "2025-01-10T12:30:05Z"
      }
    ]
  },
  "message": "SSH 連線測試完成"
}
```

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
interface Inventory {
  id: number;
  name: string;
  status: 'On' | 'Off';
  ssh_status: 'Connected' | 'Unconnected';
  group: string;
  config: string;
  created_at: string;
  updated_at: string;
}
```

### Playbook 模型

```typescript
interface Playbook {
  id: number;
  name: string;
  type: 'Machine' | 'Other';
  status: 'Success' | 'Fail' | 'Not start';
  main: PlaybookMain;
  tasks: PlaybookTask[];
  last_run_at: string | null;
  created_at: string;
  updated_at: string;
}

interface PlaybookMain {
  hosts: string;
  gather_facts: boolean;
  [key: string]: any;  // 額外的 main 欄位
}

interface PlaybookTask {
  id: number;
  enabled: boolean;
  content: string;  // YAML 格式
}
```

### AI 訊息模型

```typescript
interface Message {
  id: string;
  text: string;
  time: string;
  is_user: boolean;
  created_at: string;
}

interface Conversation {
  conversation_id: string;
  title?: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
}
```

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

## 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.0 | 2025-11-10 | 初始版本,根據前端代碼推論 API 規格 |

---

## 注意事項

1. 本文件基於前端代碼推論,實際後端 API 規格可能有所差異
2. 所有時間格式使用 ISO 8601 標準 (UTC 時區)
3. 所有 ID 均為正整數
4. 文件內容可能需要根據實際後端實作進行調整

---

**文件結束**
