
# Ansible 自動化網站部署管理系統 --- 專案說明書（含 AI 操作模組）

## 一、系統概述

本專案旨在開發一個**基於 Ansible
的自動化網站部署平台**，並提供「圖形化操作」與「智慧 AI
展開
message.txt
10 KB
圖片
amazingrobot_ — 下午 08:14
這是一個非常好的想法。將專案模組化是讓專案變得可維護、可擴展的關鍵步驟。

我將為您做兩件事：

1.  **提供一個清晰的 FastAPI 專案目錄結構**，將您單一檔案中的所有功能拆分到對應的模組中。
2.  **產生一份獨立的 API 文件（Markdown 格式）**，彙整所有 API 的說明，方便前後端協作。
展開
message.txt
9 KB
﻿
這是一個非常好的想法。將專案模組化是讓專案變得可維護、可擴展的關鍵步驟。

我將為您做兩件事：

1.  **提供一個清晰的 FastAPI 專案目錄結構**，將您單一檔案中的所有功能拆分到對應的模組中。
2.  **產生一份獨立的 API 文件（Markdown 格式）**，彙整所有 API 的說明，方便前後端協作。

-----

## 🚀 專案結構 (Project Structure)

這是一個專業且可擴展的 FastAPI 專案結構，它遵循「關注點分離」(Separation of Concerns) 原則：

```
ansible_deployer/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py         # 主路由器，匯入所有子路由
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── auth.py         # 模組 1: 認證
│   │       ├── inventory.py    # 模組 2: 伺服器管理
│   │       ├── playbooks.py    # 模組 3: Playbook 管理
│   │       ├── deployment.py   # 模組 4/5: 部署與紀錄 (含 WebSocket)
│   │       └── ai_assistant.py # 模組 7: AI 助理
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # 應用程式設定 (例如: 資料庫 URL, SECRET_KEY)
│   │   └── security.py       # 存放 get_current_user, oauth2_scheme 等
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py       # 模擬資料庫 (FAKE_DB)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── ai.py             # AIPrompt, AIPlan...
│   │   ├── deployment.py     # DeploymentCreate, DeploymentJob...
│   │   ├── host.py           # Host, HostCreate...
│   │   ├── playbook.py       # Playbook
│   │   ├── token.py          # Token
│   │   └── user.py           # User
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py     # 模擬 simulation_call_ai_service
│   │   └── ansible_runner.py # 模擬 simulation_run_ansible_playbook
│   │
│   └── main.py               # FastAPI 應用程式主進入點
│
├── requirements.txt          # 專案依賴
└── README.md                 # 專案說明 (您可以貼上 API 文件)
```

### 

結構說明

  * `app/main.py`: 應用程式的**進入點**。它非常精簡，只負責建立 `FastAPI` 實例、掛載主路由器 (`api.router.py`) 和 WebSocket。
  * `app/api/`: 存放所有 API **路由 (Endpoints)**。
      * `app/api/endpoints/`: 每個 `.py` 檔案對應您專案說明書中的一個功能模組（例如 `inventory.py` 對應伺服器管理）。
      * `app/api/router.py`: 像是一個「路由器總站」，它會 `include` 所有在 `endpoints/`
        中的子路由，`main.py` 只需要 `include` 這一個檔案即可。
  * `app/schemas/`: 存放所有的 Pydantic **資料模型 (Models)**。將 `Host`, `User`, `Playbook`
    等分開存放，讓路由檔案更乾淨。
  * `app/services/`: 存放**核心商業邏輯**。例如，實際執行 Ansible
    的邏輯 (`ansible_runner.py`) 或呼叫 AI 模型的邏輯 (`ai_service.py`)。路由檔案（如
    `deployment.py`）會呼叫這些 service 來完成工作。
  * `app/core/`: 存放應用的**核心配置與安全**。例如 `security.py`
    專門處理使用者認證、權限依賴（`Depends`）。
  * `app/db/`: 存放**資料庫**相關邏輯。在我們的範例中，就是那個模擬的 `DB` 字典。

-----

## 📋 API 說明文件 (Markdown)

這份文件是從您先前範例程式碼中的 `summary` 和 `description` 彙整而來。

# Ansible 自動化網站部署管理系統 API 文件

## 1\. 使用者登入與權限管理 (User Auth & Permissions)

### `POST /token`

  * **功能**: 使用者登入
  * **說明**: 使用表單（`application/x-www-form-urlencoded`）提交 `username` 和 `password` 進行登入，以換取 Access Token。

### `GET /users/me`

  * **功能**: 獲取當前使用者資訊
  * **說明**: 使用有效的 Access Token（HTTP Header
    `Authorization: Bearer <token>`），獲取當前登入者的使用者資料（角色、名稱等）。

### `GET /users`

  * **權限**: `[Admin]`
  * **功能**: 獲取所有使用者列表
  * **說明**: 僅限管理員(Admin)調用，獲取系統中所有使用者的列表。

-----

## 2\. 伺服器 (Inventory) 管理 (Inventory Management)

### `GET /inventory/hosts`

  * **權限**: `[Developer / Admin]`
  * **功能**: 獲取所有伺服器列表
  * **說明**: 列出資料庫中所有已註冊的伺服器。

### `POST /inventory/hosts`

  * **權限**: `[Admin]`
  * **功能**: 新增伺服器
  * **說明**: 僅限管理員(Admin)調用，在 Request Body 中傳入伺服器資料（hostname, ip, group...）以新增一台伺服器到 Inventory。

### `GET /inventory/hosts/{host_id}`

  * **權限**: `[Developer / Admin]`
  * **功能**: 獲取單一伺服器詳情
  * **說明**: 根據 ID 獲取特定伺服器的詳細資訊。

### `POST /inventory/hosts/{host_id}/ping`

  * **權限**: `[Developer / Admin]`
  * **功能**: 測試伺服器連線 (Ping)
  * **說明**: 執行 `ansible -m ping` 測試與目標伺服器的 SSH 連線狀態。

### `DELETE /inventory/hosts/{host_id}`

  * **權限**: `[Admin]`
  * **功能**: 刪除伺服器
  * **說明**: 僅限管理員(Admin)調用，根據 ID 刪除一台伺服器。

-----

## 3\. 任務與 Playbook 管理 (Playbook Management)

### `GET /playbooks/`

  * **權限**: `[Developer / Admin]`
  * **功能**: 獲取 Playbook 列表
  * **說明**: 列出所有已註冊、可執行的 Playbook 及其描述。

### `POST /playbooks/`

  * **權限**: `[Admin]`
  * **功能**: 新增 Playbook
  * **說明**: 僅限管理員(Admin)調用，註冊一個新的 Playbook。

### `GET /playbooks/{playbook_id}`

  * **權限**: `[Developer / Admin]`
  * **功能**: 獲取 Playbook 詳情
  * **說明**: 根據 ID 獲取單一 Playbook 的詳細資訊。

-----

## 4 & 5. 部署執行 與 紀錄審計 (Deployment & History)

### `POST /deployment/jobs`

  * **權限**: `[Developer / Admin]`
  * **功能**: 執行部署任務 (Job)
  * **說明**: 觸發一個新的 Ansible
    部署任務。系統會立即回傳 Job ID（狀態碼 `202 Accepted`），並在背景開始執行。
  * **Request Body**:
      * `playbook_id` (str): 要執行的 Playbook。
      * `target_host_ids` (List[str]): 目標主機的 ID 列表。
      * `extra_vars` (Dict): 額外傳遞的變數 (例如: git\_branch)。

### `GET /deployment/jobs`

  * **權限**: `[Developer / Admin]`
  * **功能**: 獲取所有部署紀錄
  * **說明**: 列出所有歷史部署任務的摘要（狀態、執行者、時間等）。

### `GET /deployment/jobs/{job_id}`

  * **權限**: `[Developer / Admin]`
  * **功能**: 獲取單一部署紀錄詳情
  * **說明**: 根據 Job ID 獲取特定任務的詳細狀態與**完整執行日誌**。

### `POST /deployment/jobs/{job_id}/retry`

  * **權限**: `[Developer / Admin]`
  * **功能**: 重新執行部署任務
  * **說明**: 使用與舊 Job 相同的參數，重新觸發一次部署，系統會建立一個新的 Job ID。

### `WS /ws/jobs/{job_id}/log` (WebSocket)

  * **功能**: 獲取即時部署日誌
  * **說明**: 這是一個 WebSocket 端點。當前端觸發部署後，應立即連線此
    WS。伺服器會將 Ansible
    執行的日誌即時（逐行）推送到此連線，直到任務完成。

-----

## 7\. AI 智能助理操作模組 (AI Assistant)

### `POST /ai/assist`

  * **權限**: `[Developer / Admin]`
  * **功能**: AI 助理 - 分析指令
  * **說明**: 傳送自然語言指令給 AI（例如:
    `"幫我更新 staging 網站"`）。AI
    會分析意圖並回傳一個「部署計畫」（`AIPlan`），包含建議的
    Playbook YAML 內容、目標主機等，供使用者確認。

### `POST /ai/execute`

  * **權限**: `[Developer / Admin]`
  * **功能**: AI 助理 - 執行計畫
  * **說明**: 使用者在前端確認（或修改）AI 產生的計畫後，呼叫此 API
    來實際執行。系統會將 AI 產生的 Playbook
    儲存為臨時任務並執行。
  * **Request Body**:
      * `plan_id` (str): 從 `/ai/assist` 取得的計畫 ID。
      * `playbook_yaml` (str): 使用者最終確認的 Playbook 內容。
      * `target_hostnames` (List[str]): 使用者最終確認的目標主機列表。
  * **回應**: 返回一個新的部署任務（`DeploymentJob`），狀態為 `202 Accepted`。
