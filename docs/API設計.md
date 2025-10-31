# API 設計 — Ansible 自動化網站部署管理系統

目的：
為前後端拆分開發提供清晰可執行的 REST API 規格。重點為「部署程式碼到多台 host」流程。

Base
- Base URL: /api/v1
- 授權：Authorization: Bearer <access_token>
- 時間格式：ISO 8601 (UTC)
- 回應統一格式：
  
  成功範例：
  ```json
  { 
    "ok": true, 
    "data": ... 
  }
  ```

  失敗範例：
  ```json
  { 
    "ok": false, 
    "error": { 
      "code": "ERR_CODE", 
      "message": "描述", 
      "details": {...} 
    } 
  }
  ```

備註：為了前端和後端可以獨立開發，所有 endpoint 都標示：方法、路徑、授權、接收的參數 (query/path/body/header)、以及範例回應。

---

## 目錄
1. Auth / Users
2. Inventory (hosts, groups)
3. Playbooks (structure-only, no YAML upload)
4. Deployment (deploy code to hosts)
5. WebSocket: realtime logs
6. Audit / History
7. SSH Keys
8. Errors & Validation

---

## 1. Auth / Users

1.1 POST /api/v1/auth/token
- 說明：使用者登入，取得 access token
- 授權：public
- Content-Type: application/x-www-form-urlencoded
- Request form fields:
  - username: string (required)
  - password: string (required)
- Success 200 example:
  ```json
  {
    "ok": true,
    "data": {
      "access_token": "ey...",
      "token_type": "bearer",
      "expires_in": 3600,
      "user": { "id": "u1", "username": "alice", "role": "Admin" }
    }
  }
  ```
- Errors: 401 Unauthorized (invalid credentials)

Frontend note: store token securely; subsequent API calls must include Authorization header.

1.2 GET /api/v1/users/me
- 說明：取得目前使用者資訊
- 授權：Bearer token
- Request: Authorization header
  ```json
  { "ok": true, "data": { "id":"u1","username":"alice","role":"Admin","email":"alice@example.com" } }
  ```

1.3 GET /api/v1/users
- 說明：列出使用者（分頁、搜尋）
- 授權：Admin
- Query params: page (int), page_size (int), search (string)
  ```json
  { "ok": true, "data": { "items": [ {"id":"u1","username":"alice","role":"Admin"} ], "total": 50 } }
  ```

---

## 2. Inventory（/api/v1/inventory）

用途：集中管理可被部署的主機列表與群組。

2.1 GET /api/v1/inventory/hosts
- 說明：列出主機
- 授權：Developer / Admin
- Query params:
  - page (int, optional)
  - page_size (int, optional)
  - group (string, optional)
  - search (string, optional, 名稱/hostname)
- Response 200 example:
  ```json
  {
    "ok": true,
    "data": {
      "items": [ { "id":"host_1","name":"web-01","hostname":"192.0.2.10","groups":["web"] } ],
      "total": 123
    }
  }
  ```

2.2 POST /api/v1/inventory/hosts
- 說明：新增一台主機
- 授權：Admin
- Request JSON body (validation):
  ```json
  {
    "name": "web-01",           // string, required
    "hostname": "192.0.2.10",  // string (IP or DNS), required
    "port": 22,                  // int, optional (default 22)
    "username": "ubuntu",      // string, required
    "ssh_key_id": "key_123",   // string|null, optional
    "groups": ["production"],  // array[string], optional
    "vars": {"ansible_python_interpreter":"/usr/bin/python3"} // object, optional
  }
  ```
- Response 201 example:
  ```json
  { "ok": true, "data": { "id": "host_123", "name": "web-01" } }
  ```
- Errors: 400/422 validation, 409 duplicate

2.3 GET /api/v1/inventory/hosts/{host_id}
- 說明：取得單台主機詳細資料
- 授權：Developer / Admin
- Path param: host_id
- Response 200 example: { "ok": true, "data": { "id":"host_123","name":"web-01","hostname":"192.0.2.10","vars":{...} } }
  Response 200 example:
  ```json
  { "ok": true, "data": { "id":"host_123","name":"web-01","hostname":"192.0.2.10","vars":{...} } }
  ```

2.4 PUT /api/v1/inventory/hosts/{host_id}
- 說明：更新主機資料（全量或部分，亦可改用 PATCH）
- 授權：Admin
- Body: same as POST (fields optional for partial update)
- Response 200: updated host

2.5 DELETE /api/v1/inventory/hosts/{host_id}
- 說明：刪除主機（可實作 soft-delete）
- 授權：Admin
- Response: 204 No Content (or 200 with message if soft-delete)

2.6 POST /api/v1/inventory/hosts/{host_id}/ping
- 說明：執行 Ansible ping 檢查 SSH 連線
- 授權：Developer / Admin
  Response 200 example:
  ```json
  { "ok": true, "data": { "reachable": true, "elapsed_ms": 120, "detail": "pong" } }
  ```

2.7 Groups (inventory groups)

用途：以群組管理主機集合（例如 staging、production、web、db），方便以群組為單位執行部署或檢視狀態。

通用欄位（Group 物件）
- id: string
- name: string (required, unique)
- description: string (optional)
- members: array[string] (host_id list)
- vars: object (group 層級變數，會套用到該群組所有主機)
- created_by: string
- created_at: ISO 8601

Endpoints:

GET /api/v1/inventory/groups
- 說明：列出所有群組（支援分頁、搜尋）
- 權限：Developer / Admin
- Query params: page, page_size, search (name)
- Response 200 example:
  ```json
  {
    "ok": true,
    "data": {
      "items": [ { "id":"g1", "name":"production", "members_count": 8, "description":"Prod web servers" } ],
      "total": 5
    }
  }
  ```

POST /api/v1/inventory/groups
- 說明：建立新群組
- 權限：Admin
  Request JSON body (validation):
  ```json
  {
    "name": "production",            // string, required, unique
    "description": "Production web servers",
    "members": ["host_1","host_2"], // optional
    "vars": { "ansible_user": "ubuntu" } // optional
  }
  ```
  - Response 201 example:
  ```json
  { "ok": true, "data": { "id": "g1", "name": "production" } }
  ```
- Errors: 400/422 (validation), 409 (name already exists)

GET /api/v1/inventory/groups/{group_id}
- 說明：取得單一群組詳細（包含 members 列表與 group vars）
- 權限：Developer / Admin
- Path param: group_id
  Response 200 example:
  ```json
  {
    "ok": true,
    "data": {
      "id": "g1",
      "name": "production",
      "description": "Prod web servers",
      "members": [ {"id":"host_1","name":"web-01","hostname":"192.0.2.10"} ],
      "vars": {"ansible_user":"ubuntu"},
      "created_by": "u1",
      "created_at": "2025-10-30T12:00:00Z"
    }
  }
  ```

PUT /api/v1/inventory/groups/{group_id}
- 說明：更新群組（全量更新）；可接受 members 清單覆蓋
- 權限：Admin
  Request JSON body:
  ```json
  {
    "name": "production",
    "description": "...",
    "members": ["host_1","host_3"],
    "vars": { ... }
  }
  ```
  - Response 200 example: updated group object

PATCH /api/v1/inventory/groups/{group_id}/members
- 說明：增/刪群組成員（推薦使用，避免整個覆蓋）
- 權限：Admin
  Request JSON body:
  ```json
  {
    "add": ["host_4"],
    "remove": ["host_2"]
  }
  ```
  - Response 200 example:
  ```json
  { "ok": true, "data": { "id":"g1", "members_added": ["host_4"], "members_removed": ["host_2"] } }
  ```

DELETE /api/v1/inventory/groups/{group_id}
- 說明：刪除群組（不刪除主機）
- 權限：Admin
- Response: 204 No Content (若群組有被某些部署政策或 job 鎖定則回 409 並列出依賴)

前端建議與 UI 行為（summary）
- 群組列表視圖：名稱、描述、members count、快速操作（編輯、刪除、選擇成員執行部署）
- 建立/編輯群組表單欄位：name (required), description, members (multi-select searchable dropdown), vars (key-value editor)
- 成員選擇器應支援 typeahead search 並顯示 host 狀態 (online/last_seen) 以協助選擇
- 編輯群組時顯示成員表格，支援批次移除與新增

前端 payload/UX 要點：
- 使用 PATCH /members 做增刪，避免 PUT 導致 race condition
- 建立/更新操作完成後前端應自動刷新相關 host 列表與 playbook 執行可選目標


前端注意：主機新增/編輯採表單化驗證（必填欄位明確）；主機列表支援批次選取以便觸發部署。

---

## 3. Playbooks（/api/v1/playbooks） — structure-only, no YAML upload

說明：Playbook 以結構化 JSON 儲存（content_struct），供前端以表單編輯與產生部署變數表單。**不提供檔案上傳 / 內嵌 YAML 編輯器**。如需顯示原始 YAML，後端可提供 raw_yaml 字段作為只讀下載。

content_struct 範例：
```json
{
  "vars": [ { "name": "git_branch", "type": "string", "default": "main", "required": true } ],
  "tasks": [ { "id": "t1", "name": "Checkout", "module": "git", "params": { "repo": "git@...", "dest": "/var/www" } } ]
}
```

3.1 POST /api/v1/playbooks
- 說明：建立 Playbook（由前端以表單產生 content_struct）
- 授權：Admin
  Request JSON body:
  ```json
  {
    "name": "deploy-web",            // string, required
    "description": "Deploy web app",
    "content_struct": { ... }         // object, required (vars array, tasks array)
  }
  ```
  - Response 201 example:
  ```json
  { "ok": true, "data": { "id": "pb_1", "name": "deploy-web" } }
  ```
- Errors: 400/422 validation

3.2 GET /api/v1/playbooks
- 說明：列出 Playbook（分頁）
- 授權：Developer / Admin
- Query: page, page_size, search
  Response 200 example:
  ```json
  { "ok": true, "data": { "items": [ {"id":"pb_1","name":"deploy-web"} ], "total": 10 } }
  ```

3.3 GET /api/v1/playbooks/{playbook_id}
- 說明：取得 Playbook 詳細（包含 content_struct 與 raw_yaml 可選）
- 授權：Developer / Admin
  Response 200 example:
  ```json
  {
    "ok": true,
    "data": {
      "id": "pb_1",
      "name": "deploy-web",
      "description": "...",
      "content_struct": { ... },
      "raw_yaml": "---"   // optional, read-only
    }
  }
  ```

3.4 PUT /api/v1/playbooks/{playbook_id}
- 說明：更新 Playbook（接受 content_struct）
- 授權：Admin
- Request JSON: same as POST (name required)
- Response 200: updated playbook

3.5 DELETE /api/v1/playbooks/{playbook_id}
- 說明：刪除 Playbook
- 授權：Admin
- Response: 204 No Content

前端: 以 content_struct 生成變數表單（playbook.vars -> 表單欄位），以 task 列表做為可編輯模組化卡片（每個 task 的 module 與參數為欄位）。

---

## 4. Deployment（/api/v1/deployment） — 部署程式碼為主

目標：把程式碼部署到選定的 host(s)。部署可以使用已註冊的 Playbook (content_struct) 或以 inline content_struct 在建立 job 時直接傳入（皆為 JSON）。**不使用檔案上傳**。

DeploymentJob body fields (create)：
- playbook_id: string (選用，若使用已儲存 Playbook)
- inline_playbook_struct: object (選用，若希望本次使用臨時結構化 playbook)
- target_host_ids: array[string] (required)
- extra_vars: object (optional) — 例如:
  ```json
  { "git_branch":"main","release_tag":"v1.2.3" }
  ```
- run_mode: string (optional) — e.g. "parallel" | "serial"

Validation rules (server side):
- 必須提供 playbook_id 或 inline_playbook_struct
- target_host_ids 至少一個
- extra_vars keys 應符合 playbook.vars 定義（若可驗證）

4.1 POST /api/v1/deployment/jobs
- 說明：建立並觸發一個部署任務（背景執行）；重點為部署程式碼到 target hosts
- 授權：Developer / Admin
- Request JSON example:
  ```json
  {
    "playbook_id": "pb_123",
    "target_host_ids": ["host_1","host_2"],
    "extra_vars": { "git_branch": "main", "git_repo": "git@github.com:org/repo.git" },
    "run_mode": "parallel"
  }
  ```

  - Response 202 example:
  ```json
  { "ok": true, "data": { "job_id": "job_456", "status": "PENDING" } }
  ```

Notes on deployment behavior (for backend implementer):
- 建議：建立 job 回 202，實際執行由 background worker (Celery / RQ / or FastAPI BackgroundTasks for demo) 執行。Worker 應：
  1) 產生暫時 inventory（依 target_host_ids）
  2) 以 ansible-runner / subprocess 執行 playbook（或透過 ansible python API）並即時寫入 log
  3) 更新 job 狀態與結果

4.2 GET /api/v1/deployment/jobs
- 說明：列出 job（分頁與篩選）
- 授權：Developer / Admin
- Query: page, page_size, status, initiated_by, from, to
  Response 200 example:
  ```json
  { "ok": true, "data": { "items": [ { "job_id":"job_456","status":"SUCCESS","started_at":"..." } ], "total": 50 } }
  ```

4.3 GET /api/v1/deployment/jobs/{job_id}
- 說明：取得 job 詳細（including per-host results & links to logs）
- 授權：Developer / Admin
  Response 200 example:
  ```json
  {
    "ok": true,
    "data": {
      "job_id": "job_456",
      "status": "SUCCESS",
      "started_at": "...",
      "finished_at": "...",
      "targets": [ { "host_id":"host_1","status":"SUCCESS","changed": true } ],
      "logs_url": "/api/v1/audit/deployments/job_456/logs"
    }
  }
  ```

4.4 POST /api/v1/deployment/jobs/{job_id}/retry
- 說明：以相同參數建立新 job 並執行
- 授權：Developer / Admin
  - Response 202:
  ```json
  { "ok": true, "data": { "job_id":"job_789","status":"PENDING" } }
  ```

4.5 POST /api/v1/deployment/jobs/{job_id}/cancel
- 說明：嘗試取消正在執行的 job（視 backend runner 支援而定）
