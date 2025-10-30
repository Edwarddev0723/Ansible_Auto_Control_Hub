# API 設計 — Ansible 自動化網站部署管理系統

目的：為前後端拆分開發提供清晰可執行的 REST API 規格。重點為「部署程式碼到多台 host」流程；本版本不含 Playbook YAML 上傳功能（前端不為檔案編輯器），Playbook 與即時/臨時部署皆以結構化 JSON (content_struct) 為主。

Base
- Base URL: /api/v1
- 授權：Authorization: Bearer <access_token>
- 時間格式：ISO 8601 (UTC)
- 回應統一格式：
  - 成功：{ "ok": true, "data": ... }
  - 失敗：{ "ok": false, "error": { "code": "ERR_CODE", "message": "描述", "details": {...} } }

備註：為了前端和後端可以獨立開發，所有 endpoint 都標示：方法、路徑、授權、接收的參數 (query/path/body/header)、以及範例回應。

---

## 目錄
- 1. Auth / Users
- 2. Inventory (hosts, groups)
- 3. Playbooks (structure-only, no YAML upload)
- 4. Deployment (deploy code to hosts)
- 5. WebSocket: realtime logs
- 6. Audit / History
- 7. SSH Keys
- 8. Errors & Validation

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
  {
    "ok": true,
    "data": {
      "access_token": "ey...",
      "token_type": "bearer",
      "expires_in": 3600,
      "user": { "id": "u1", "username": "alice", "role": "Admin" }
    }
  }
- Errors: 401 Unauthorized (invalid credentials)

Frontend note: store token securely; subsequent API calls must include Authorization header.

1.2 GET /api/v1/users/me
- 說明：取得目前使用者資訊
- 授權：Bearer token
- Request: Authorization header
- Success 200 example:
  { "ok": true, "data": { "id":"u1","username":"alice","role":"Admin","email":"alice@example.com" } }

1.3 GET /api/v1/users
- 說明：列出使用者（分頁、搜尋）
- 授權：Admin
- Query params: page (int), page_size (int), search (string)
- Response 200 example:
  { "ok": true, "data": { "items": [ {"id":"u1","username":"alice","role":"Admin"} ], "total": 50 } }

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
  {
    "ok": true,
    "data": {
      "items": [ { "id":"host_1","name":"web-01","hostname":"192.0.2.10","groups":["web"] } ],
      "total": 123
    }
  }

2.2 POST /api/v1/inventory/hosts
- 說明：新增一台主機
- 授權：Admin
- Request JSON body (validation):
  {
    "name": "web-01",           // string, required
    "hostname": "192.0.2.10",  // string (IP or DNS), required
    "port": 22,                  // int, optional (default 22)
    "username": "ubuntu",      // string, required
    "ssh_key_id": "key_123",   // string|null, optional
    "groups": ["production"],  // array[string], optional
    "vars": {"ansible_python_interpreter":"/usr/bin/python3"} // object, optional
  }
- Response 201 example:
  { "ok": true, "data": { "id": "host_123", "name": "web-01" } }
- Errors: 400/422 validation, 409 duplicate

2.3 GET /api/v1/inventory/hosts/{host_id}
- 說明：取得單台主機詳細資料
- 授權：Developer / Admin
- Path param: host_id
- Response 200 example: { "ok": true, "data": { "id":"host_123","name":"web-01","hostname":"192.0.2.10","vars":{...} } }

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
- Response 200 example:
  { "ok": true, "data": { "reachable": true, "elapsed_ms": 120, "detail": "pong" } }

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
  {
    "ok": true,
    "data": {
      "items": [ { "id":"g1", "name":"production", "members_count": 8, "description":"Prod web servers" } ],
      "total": 5
    }
  }

POST /api/v1/inventory/groups
- 說明：建立新群組
- 權限：Admin
- Request JSON body (validation):
  {
    "name": "production",            // string, required, unique
    "description": "Production web servers",
    "members": ["host_1","host_2"], // optional
    "vars": { "ansible_user": "ubuntu" } // optional
  }
- Response 201 example:
  { "ok": true, "data": { "id": "g1", "name": "production" } }
- Errors: 400/422 (validation), 409 (name already exists)

GET /api/v1/inventory/groups/{group_id}
- 說明：取得單一群組詳細（包含 members 列表與 group vars）
- 權限：Developer / Admin
- Path param: group_id
- Response 200 example:
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

PUT /api/v1/inventory/groups/{group_id}
- 說明：更新群組（全量更新）；可接受 members 清單覆蓋
- 權限：Admin
- Request JSON body:
  {
    "name": "production",
    "description": "...",
    "members": ["host_1","host_3"],
    "vars": { ... }
  }
- Response 200 example: updated group object

PATCH /api/v1/inventory/groups/{group_id}/members
- 說明：增/刪群組成員（推薦使用，避免整個覆蓋）
- 權限：Admin
- Request JSON body:
  {
    "add": ["host_4"],
    "remove": ["host_2"]
  }
- Response 200 example: { "ok": true, "data": { "id":"g1", "members_added": ["host_4"], "members_removed": ["host_2"] } }

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
```
{
  "vars": [ { "name": "git_branch", "type": "string", "default": "main", "required": true } ],
  "tasks": [ { "id": "t1", "name": "Checkout", "module": "git", "params": { "repo": "git@...", "dest": "/var/www" } } ]
}
```

3.1 POST /api/v1/playbooks
- 說明：建立 Playbook（由前端以表單產生 content_struct）
- 授權：Admin
- Request JSON body:
  {
    "name": "deploy-web",            // string, required
    "description": "Deploy web app",
    "content_struct": { ... }         // object, required (vars array, tasks array)
  }
- Response 201 example:
  { "ok": true, "data": { "id": "pb_1", "name": "deploy-web" } }
- Errors: 400/422 validation

3.2 GET /api/v1/playbooks
- 說明：列出 Playbook（分頁）
- 授權：Developer / Admin
- Query: page, page_size, search
- Response 200 example:
  { "ok": true, "data": { "items": [ {"id":"pb_1","name":"deploy-web"} ], "total": 10 } }

3.3 GET /api/v1/playbooks/{playbook_id}
- 說明：取得 Playbook 詳細（包含 content_struct 與 raw_yaml 可選）
- 授權：Developer / Admin
- Response 200 example:
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
- extra_vars: object (optional) — 例如 { "git_branch":"main","release_tag":"v1.2.3" }
- run_mode: string (optional) — e.g. "parallel" | "serial"

Validation rules (server side):
- 必須提供 playbook_id 或 inline_playbook_struct
- target_host_ids 至少一個
- extra_vars keys 應符合 playbook.vars 定義（若可驗證）

4.1 POST /api/v1/deployment/jobs
- 說明：建立並觸發一個部署任務（背景執行）；重點為部署程式碼到 target hosts
- 授權：Developer / Admin
- Request JSON example:
  {
    "playbook_id": "pb_123",
    "target_host_ids": ["host_1","host_2"],
    "extra_vars": { "git_branch": "main", "git_repo": "git@github.com:org/repo.git" },
    "run_mode": "parallel"
  }
- Response 202 example:
  { "ok": true, "data": { "job_id": "job_456", "status": "PENDING" } }

Notes on deployment behavior (for backend implementer):
- 建議：建立 job 回 202，實際執行由 background worker (Celery / RQ / or FastAPI BackgroundTasks for demo) 執行。Worker 應：
  1) 產生暫時 inventory（依 target_host_ids）
  2) 以 ansible-runner / subprocess 執行 playbook（或透過 ansible python API）並即時寫入 log
  3) 更新 job 狀態與結果

4.2 GET /api/v1/deployment/jobs
- 說明：列出 job（分頁與篩選）
- 授權：Developer / Admin
- Query: page, page_size, status, initiated_by, from, to
- Response 200 example:
  { "ok": true, "data": { "items": [ { "job_id":"job_456","status":"SUCCESS","started_at":"..." } ], "total": 50 } }

4.3 GET /api/v1/deployment/jobs/{job_id}
- 說明：取得 job 詳細（including per-host results & links to logs）
- 授權：Developer / Admin
- Response 200 example:
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

4.4 POST /api/v1/deployment/jobs/{job_id}/retry
- 說明：以相同參數建立新 job 並執行
- 授權：Developer / Admin
- Response 202: { "ok": true, "data": { "job_id":"job_789","status":"PENDING" } }

4.5 POST /api/v1/deployment/jobs/{job_id}/cancel
- 說明：嘗試取消正在執行的 job（視 backend runner 支援而定）
# API 設計 — 簡易 Ansible 網站部署

說明：本檔為極簡化版本，僅保留對「把網站程式碼部署到多台主機」必要的 API。目標是讓前後端能快速分工並整合 Ansible 執行流程。

通用規範
- Base URL: /api/v1
- 授權：Authorization: Bearer <access_token>（簡單驗證流程即可）
- 時間格式：ISO 8601 (UTC)
- 回應結構：
  - 成功：{ "ok": true, "data": ... }
  - 失敗：{ "ok": false, "error": { "code": "ERR_CODE", "message": "描述", "details": {...} } }

只保留的模組：
- 認證（Auth）
- Inventory（主機）
- 部署（Deployment）
- 即時日誌（WebSocket）
- 稽核（簡單的 Job 列表與 raw log 下載）

---

## 1. 認證

POST /api/v1/auth/token
- 說明：使用者登入取得 token
- 權限：public
- Form: username, password
- 回傳 200 範例：
  { "ok": true, "data": { "access_token":"ey...", "expires_in":3600, "user": {"id":"u1","username":"alice"} } }

（前端：登入表單，取得 token 後帶入 Authorization header）

---

## 2. Inventory（主機管理，簡化）

說明：只需要能管理要佈署的主機清單。

GET /api/v1/inventory/hosts
- Query: page, page_size, search
- Response 200 範例：
  { "ok": true, "data": { "items": [ {"id":"host_1","name":"web-01","hostname":"192.0.2.10"} ], "total": 1 } }

POST /api/v1/inventory/hosts
- Body:
  {
    "name": "web-01", "hostname": "192.0.2.10", "port":22, "username":"ubuntu", "ssh_key_id": null
  }
- Response 201 範例: { "ok": true, "data": { "id":"host_1" } }

GET /api/v1/inventory/hosts/{host_id}
- Response 200 範例: { "ok": true, "data": { "id":"host_1","name":"web-01","hostname":"192.0.2.10","port":22 } }

PUT /api/v1/inventory/hosts/{host_id}
- Body: same as POST (更新主機資訊)

DELETE /api/v1/inventory/hosts/{host_id}
- Response: 204

POST /api/v1/inventory/hosts/{host_id}/ping
- 回傳 200 範例: { "ok": true, "data": { "reachable": true } }

前端：主機頁面以表單新增/編輯主機；部署畫面可多選主機作為 target。

---

## 3. 部署（Deployment）— 核心功能

目的：由前端以簡單表單提供要部署的資訊（git repo 與分支），後端負責用 Ansible 把程式碼佈署到指定主機。

POST /api/v1/deployment/jobs
- 說明：建立並觸發部署任務（背景執行）
- 權限：Authenticated (Developer / Admin)
- Request JSON (必填欄位註記):
  {
    "target_host_ids": ["host_1","host_2"],   // required
    "git_repo": "git@github.com:org/repo.git", // required (或 artifact_url)
    "git_ref": "main",                          // branch 或 tag，required
    "deploy_path": "/var/www/myapp",            // required
    "extra_vars": { "ENV":"staging" }        // optional
  }
- Response 202 範例:
  { "ok": true, "data": { "job_id": "job_1", "status": "PENDING" } }

實作提示（後端）：
- 建議工作流程：
  1) 建立 Job 紀錄（status=PENDING）
  2) 建暫時 inventory，產生 ansible play（或使用固定模板）
  3) 以 ansible-runner 或 subprocess 執行，stream log 到儲存與 WebSocket
  4) 更新 Job 狀態（RUNNING → SUCCESS/FAILED）並存 raw log

注意：不需要讓前端上傳 playbook YAML；後端可使用一個固定 playbook 模板，並以 extra_vars 傳入 git_repo/git_ref/deploy_path。

GET /api/v1/deployment/jobs
- Query: page, page_size, status, initiated_by
- Response 200 範例：
  { "ok": true, "data": { "items": [ { "job_id":"job_1","status":"SUCCESS","started_at":"..." } ], "total": 10 } }

GET /api/v1/deployment/jobs/{job_id}
- Response 200 範例：
  { "ok": true, "data": { "job_id":"job_1","status":"SUCCESS","targets": [ {"host_id":"host_1","status":"SUCCESS"} ], "logs_url": "/api/v1/audit/deployments/job_1/logs" } }

POST /api/v1/deployment/jobs/{job_id}/cancel
- 嘗試取消 job（若 runner 支援）
- Response: 200 範例 { "ok": true, "data": { "job_id":"job_1","status":"CANCELLING" } }

前端表單設計（部署）:
- 欄位：target hosts (multi-select), git repo (text), git ref (text), deploy path (text), extra vars (簡單 key/value 列表)
- 驗證：target_host_ids 與 git_repo 與 git_ref 與 deploy_path 為必填
- 流程：填表 → 確認摘要頁（顯示選取主機與變數）→ 送出 → 顯示 job_id 與連 WebSocket 取得即時 log

---

## 4. 即時日誌（WebSocket）

URI: ws://<host>/api/v1/ws/jobs/{job_id}/log
- 驗證：可用 Authorization header 或 query token
- 訊息範例：{ "ts":"...","host":"web-01","level":"INFO","line":"TASK ..." }

前端需要：自動滾動、暫停/播放、過濾錯誤等簡單功能。

---

## 5. 稽核（簡單）

GET /api/v1/audit/deployments
- 列出 job 歷史（分頁、filter）

GET /api/v1/audit/deployments/{job_id}/logs
- 下載 raw log（text/plain）

---

## 6. 錯誤處理

- 驗證失敗回 422 並在 error.details 提供欄位錯誤
- 常用狀態碼：200,201,202,204,400,401,403,404,409,422,500

---

如果您同意這個極簡版本，我可以接著為您：
1) 產生 FastAPI minimal stub（包含 auth stub、inventory endpoints、deployment job create + background demo、WebSocket stub）方便前端先做串接；或
2) 產出 OpenAPI 規格檔（YAML）

請選 1 或 2，或告訴我要微調的欄位名稱/必填條件。
