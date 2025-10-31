# API 設計（簡單版）— 最小可行：以 Ansible 部署程式碼到多台主機

目的：
在最短時間內完成「將 Git 程式碼部署到多台 Linux 主機」的單一功能。省略使用者/群組/WebSocket 等進階能力，採用最小端點集合與資料表。

關鍵選擇（簡化）：
- 不做 Playbook 管理：後端固定生成一個極簡 Playbook（使用 ansible.builtin.git 模組）來 clone/pull 指定 repo 至指定路徑。
- 允許在建立 Job 時「直接提供目標主機清單（含認證）」，不需先建 Inventory/群組。
- 不提供 WebSocket：日誌以輪詢 API 取得（text 或 json 行陣列）。
- 認證（可選）：MVP 可不啟用，或以單一固定 Token 簡化開發。

Base
- Base URL: /api/v1
- 授權：無（MVP）；如需簡單保護，可於 Header 附上 X-API-Key
- 時間格式：ISO 8601 (UTC)
- 回應統一格式：
  成功：
  ```json
  { "ok": true, "data": ... }
  ```
  失敗：
  ```json
  { "ok": false, "error": { "code": "ERR_CODE", "message": "描述", "details": {"field":"..."} } }
  ```

---

## 目錄（簡單版）
1. Jobs（唯一核心模組）
2. Logs（取回執行日誌）
3. Errors & Validation（簡述）

---

## 1. Jobs（/api/v1/jobs）

說明：建立與查詢部署工作。後端會：
1) 依請求動態生成暫存 inventory；
2) 生成最小 Playbook（git clone/pull 到 dest_path）；
3) 背景執行 ansible；
4) 寫入 logs 與每台主機結果。

共用參數（Body 內的 targets）
- host: string（必填）IP 或 DNS
- port: int（選填，預設 22）
- username: string（必填）
- auth: object（必填）
  - type: "private_key" | "password"
  - private_key: string（auth.type=private_key 時必填，OpenSSH 私鑰字串）
  - passphrase: string|null（選填）
  - password: string（auth.type=password 時必填）

1.1 POST /api/v1/jobs
- 說明：建立並觸發一個部署任務（背景執行）
- Request JSON body：
```json
{
  "git_repo": "git@github.com:org/repo.git",   
  "git_branch": "main",                        
  "dest_path": "/var/www/app",                 
  "targets": [
    {
      "host": "192.0.2.10",
      "port": 22,
      "username": "ubuntu",
      "auth": { "type": "private_key", "private_key": "-----BEGIN OPENSSH PRIVATE KEY-----\n...\n-----END OPENSSH PRIVATE KEY-----\n", "passphrase": null }
    },
    {
      "host": "192.0.2.11",
      "username": "ubuntu",
      "auth": { "type": "password", "password": "secret" }
    }
  ],
  "run_mode": "parallel"   
}
```
- Response 202 範例：
```json
{ "ok": true, "data": { "job_id": "job_123", "status": "PENDING" } }
```
- 驗證要點：git_repo 必填（支援 SSH/HTTPS）；dest_path 必填且為絕對路徑；targets 至少一台；auth 規則依 type 驗證。

1.2 GET /api/v1/jobs
- 說明：列出工作（分頁/簡單篩選）
- Query：page, page_size, status, from, to
- Response 200 範例：
```json
{
  "ok": true,
  "data": {
    "items": [
      { "job_id":"job_123","status":"RUNNING","git_repo":"git@github.com:org/repo.git","git_branch":"main","requested_at":"2025-10-31T01:00:00Z","targets_count":2 },
      { "job_id":"job_122","status":"SUCCESS","git_repo":"https://github.com/org/other.git","git_branch":"v1.2","requested_at":"2025-10-31T00:20:00Z","finished_at":"2025-10-31T00:22:10Z","targets_count":3 }
    ],
    "total": 2,
    "page": 1,
    "page_size": 20
  }
}
```

1.3 GET /api/v1/jobs/{job_id}
- 說明：取得單一工作之詳細與每台主機的結果
- Response 200 範例：
```json
{
  "ok": true,
  "data": {
    "job_id": "job_123",
    "status": "RUNNING",
    "git_repo": "git@github.com:org/repo.git",
    "git_branch": "main",
    "dest_path": "/var/www/app",
    "run_mode": "parallel",
    "requested_at": "2025-10-31T01:00:00Z",
    "started_at": "2025-10-31T01:00:05Z",
    "finished_at": null,
    "targets": [
      { "host":"192.0.2.10","status":"SUCCESS","changed": true,  "elapsed_ms": 8200 },
      { "host":"192.0.2.11","status":"RUNNING","changed": null,  "elapsed_ms": null }
    ]
  }
}
```

1.4 POST /api/v1/jobs/{job_id}/retry（可選）
- 說明：以相同參數重跑（重新建立一個 job）
- Response 202：
```json
{ "ok": true, "data": { "job_id": "job_124", "status": "PENDING" } }
```

---

## 2. Logs（/api/v1/jobs/{job_id}/logs）

2.1 GET /api/v1/jobs/{job_id}/logs
- 說明：取得完整日誌（純文字或 json 行陣列）。MVP 採輪詢，不做 WebSocket。
- Query：format=text|json（預設 text），from_id（選填，僅當 format=json 時用於增量拉取）
- Response 200（text 範例）：
```
PLAY [all] ********************************************************************
TASK [git] ********************************************************************
changed: [192.0.2.10]
ok: [192.0.2.11]

PLAY RECAP ********************************************************************
192.0.2.10 : ok=3 changed=1 failed=0 skipped=0
192.0.2.11 : ok=3 changed=0 failed=0 skipped=0
```

- Response 200（json 範例）：
```json
{ "ok": true, "data": { "lines": [{"id":1,"ts":"...","host":null,"line":"PLAY [all] ..."}] } }
```

---

## 3. Errors & Validation（簡述）

- 統一錯誤格式：
```json
{ "ok": false, "error": { "code": "VALIDATION_ERROR", "message": "Request validation failed", "details": {"git_repo":"required"} } }
```

- 常見錯誤碼：
  - VALIDATION_ERROR (422)
  - NOT_FOUND (404)
  - INTERNAL_ERROR (500)

驗證重點：
- git_repo 必填、URL 合法（SSH/HTTPS 任一種即可）；
- dest_path 必填且看起來為絕對路徑（例如以/開頭）；
- targets 至少 1 台，且 auth 必填、依 type 驗證必填欄位；
- run_mode 僅允許 parallel|serial（未填預設 parallel）。
