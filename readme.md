# README — 角色分工細節與開發流程（Demo 專用）測試

> 本文件僅包含兩部分：**A) 角色分工細節**、**B) 開發流程**。其餘安裝、API、樣板請見專案其他文件。

---

## A) 角色分工細節（五角協作）

> 共同規範：
> - `run_id = YYYYMMDD-HHMMSS-rand3`
> - 證據路徑：`artifacts/<run_id>/`
> - 報告路徑：`report/out/<run_id>.{html,pdf}`
> - 服務 URL Key：`service_url`
> - Inventory：`ansible/inventories/runs/<run_id>/hosts.ini`

### 1) 前端（Frontend Owner）
**目標**：提供「AI 模式 + GUI 模式」操作入口，顯示事件流，支援重試/跳過/清理，下載報告。

**你要產出**
- 單頁 UI（兩分頁）：
  - **AI 模式**：文字輸入 → `POST /api/run` → 事件流/SSE → 報告下載
  - **GUI 模式**：表單 → `POST /api/plan`（預覽 steps）→ Confirm → `POST /api/execute`
- 事件流視圖（SSE/WS）：`step/phase(level)/耗時/重試次數`，錯誤列上提供 **Retry / Skip / Cleanup** 按鈕
- 報告面板：`GET /api/runs/{id}/report` 下載 HTML/PDF

**你要完成的工項**
- 頁面骨架、狀態管理（run_id 對應事件串流）
- SSE/WS 客戶端，第一條事件 ≤ 1s 顯示
- 動作按鈕串 API：`/retry|/skip|/cleanup`
- 空狀態、失敗重試、Loading/Disable 邏輯

**介面（消費/輸出）**
- 消費：`POST /api/run`、`POST /api/plan`、`POST /api/execute`、`GET /api/runs/{id}/events`、`GET /api/runs/{id}/report`、`POST /api/runs/{id}/retry|skip|cleanup`
- 輸出：無（前端僅呼叫後端）

**驗收（DoD）**
- 兩模式皆可跑通；送出後 ≤1s 出現第一條事件
- 錯誤事件可一鍵補救；可下載報告並開啟

---

### 2) 後端 Orchestrator / API（Backend Owner）
**目標**：把端到端流程做成可觀測的狀態機，提供 REST + SSE/WS。

**你要產出**
- Pipeline：`create_cluster → create_vm → deploy_service → ansible_validate → collect_evidence → build_audit_report`
- 事件與狀態：
  - `artifacts/<run_id>/events.jsonl`（SSE/WS 推流）
  - `artifacts/<run_id>/state.json`（各步 `pending|running|success|failed`）
- 控制 API：`/api/run /api/plan /api/execute /api/runs/{id}/events /api/runs/{id}/report /retry|skip|cleanup`
- 失敗策略：可重試/跳過、Best‑effort 產 **Partial Report**

**你要完成的工項**
- 統一步驟介面：`step(params) -> {result_path, metrics} | {error_code,hint}`
- Backoff 重試（上限/可配置）、可回放（依 state.json 續跑）
- 檔案歸檔：每步 `params.json / result.json`、stderr/stdout 摘要

**介面（消費/輸出）**
- 消費：工具層（k8s/vm/ansible/report）的本地腳本或 SDK
- 輸出：上述 API 與 artifacts 檔案

**驗收（DoD）**
- 任一步可重試/跳過；事件可回放；部分失敗亦能產報

---

### 3) AI / MCP Tools（AI Owner）
**目標**：把自然語言轉成穩定的工具呼叫序列（先 dry‑run 再 execute），並給出自動補救計畫。

**你要產出**
- `mcp/tools.json`（六工具 Schema + 描述）
- Planner：語句 → `steps[]`（`dry_run:true`）；收到前端確認旗標後執行
- 錯誤對應表：`timeout / rollout_failed / vm_unreachable` → (重試/重建/回滾) 計畫

**你要完成的工項**
- NL → 結構化參數對齊：provider、vmType、replicas、service_url、run_id
- 多措辭同語意對映測試（中/英/口語）
- 補救計畫產生與與後端 API 協作

**介面（消費/輸出）**
- 消費：後端 `/api/plan`、`/api/execute` 與分步 API
- 輸出：`plan.steps[]`、`execute` 指令序列（由後端執行）

**驗收（DoD）**
- 三種不同措辭產生**等價計畫**；≥3 類錯誤能給補救並成功恢復一次

---

### 4) 基礎設施 / K8s & VM & IaC（Infra Owner）
**目標**：一鍵建立/銷毀 Demo 環境（本機優先）。

**你要產出**
- `make cluster-up|down`（k3d 叢集，映射 8080→80）
- KubeVirt + CDI 安裝、`vm.yaml`（cloud‑init：curl/ab + SSH 公鑰）
- `scripts/smoke.sh`：nodes/pods/svc 快照 → `k8s_snapshot.json`

**你要完成的工項**
- kubeconfig/context 路徑交付給 Backend 與 Ansible
- 若 KubeVirt 風險高，提供 EC2 Terraform 備援，輸出相同欄位

**介面（消費/輸出）**
- 消費：kubectl/virtctl/terraform
- 輸出：kubeconfig、VM `hosts.ini`、`k8s_snapshot.json`

**驗收（DoD）**
- 60s 內叢集 Ready；VM 可 `ping/curl`；失敗提供 `describe/events` 診斷

---

### 5) 驗證與報告（Validation & Report Owner）
**目標**：以 Ansible 驗證可用性並產出可稽核報告。

**你要產出**
- Playbook：Pod Ready + HTTP 200（含 retries/until）
- JSON 證據：`artifacts/<run_id>/ansible_run.json`、`nginx_probe.txt`
- 報告：Jinja2 → HTML/PDF（附 artifacts 連結）

**你要完成的工項**
- `roles/healthcheck` 與 callback（`ANSIBLE_STDOUT_CALLBACK=json` 或自製 plugin）
- `report/templates/report.md.j2`、轉檔腳本（wkhtmltopdf 或 weasyprint）
- 聚合 `k8s_snapshot.json / ansible_run.json / events.jsonl / git/tf 摘要`

**介面（消費/輸出）**
- 消費：`hosts.ini`、服務 URL、kubeconfig 摘要
- 輸出：HTML/PDF 報告 + 證據檔

**驗收（DoD）**
- `make validate` 成功且輸出完整 JSON；`report/out/<run_id>.pdf` 可開並含鏈結

---

## B) 開發流程（兩天節奏）

> 每一階段列出：輸入 → 動作 → 輸出 → 驗收（DoD）→ Owner

### Phase 0｜Bootstrap（全員，~1hr）
- **輸入**：Repo、`.env.example`、Docker/kubectl/k3d/Ansible/Python 3.11+
- **動作**：`make bootstrap`、建立分支 `feature/<role>-init`、對齊事件格式
- **輸出**：可啟動的本地環境
- **DoD**：lint 通過；後端空殼 API 可起
- **Owner**：全員

### Phase 1｜K8s 叢集（Infra，~2–3hr）
- **輸入**：`infra/local/k3d.yaml`
- **動作**：`make cluster-up`；`scripts/smoke.sh` 產 `k8s_snapshot.json`
- **輸出**：Ready 的叢集與快照
- **DoD**：60s 內 `kubectl get nodes` Ready
- **Owner**：Infra

### Phase 2｜測試 VM（Infra，~2–3hr）
- **輸入**：KubeVirt/CDI manifests、`vm.yaml`
- **動作**：安裝 KubeVirt、`virtctl start test-vm`；生成 `hosts.ini`
- **輸出**：可連線 VM + inventory
- **DoD**：`ansible -m ping` 成功；VM 可 `curl`
- **Owner**：Infra（與 Validation 對接）

### Phase 3｜示範服務（Infra，~1hr）
- **輸入**：`k8s/deploy.yaml`、`svc.yaml`
- **動作**：套用 manifests，回報 service DNS 或對外 URL
- **輸出**：可用的 nginx 服務
- **DoD**：`rollout status` OK；`curl` 200
- **Owner**：Infra

### Phase 4｜Ansible 驗證（Validation，~2–3hr）
- **輸入**：`hosts.ini`、service_url
- **動作**：執行 playbook（Pod Ready + HTTP 200），輸出 JSON 證據
- **輸出**：`ansible_run.json`、`nginx_probe.txt`
- **DoD**：`make validate` 返回 0；JSON 含 `ok/changed/failed/timestamps`
- **Owner**：Validation & Report

### Phase 5｜Orchestrator / API（Backend，~3–4hr）
- **輸入**：Infra/Ansible 的腳本入口
- **動作**：
  - 流程：`create_cluster → create_vm → deploy_service → ansible_validate → collect_evidence → build_audit_report`
  - 推送事件（SSE/WS）、維護 `state.json`
  - 提供 API：`/api/run /api/plan /api/execute /events /report /retry|/skip|/cleanup`
- **輸出**：可驅動的端到端管線
- **DoD**：任一步可重試/跳過；Partial Report 可產
- **Owner**：Backend

### Phase 6｜前端 UI（Frontend，~3–4hr）
- **輸入**：Backend API、事件格式
- **動作**：完成 AI/GUI 雙模式與事件流、操作按鈕
- **輸出**：可互動的單頁 UI
- **DoD**：首條事件 ≤1s；錯誤可補救；可下載報告
- **Owner**：Frontend

### Phase 7｜AI / MCP（AI，~3–4hr）
- **輸入**：`mcp/tools.json` 範圍
- **動作**：語句 → `plan.steps[]`（dry‑run）；確認後執行；錯誤給補救計畫
- **輸出**：可重現的工具序列
- **DoD**：三種措辭 → 等價計畫；≥3 類錯誤能恢復一次
- **Owner**：AI

### Phase 8｜蒐證與報告（Validation，~2–3hr）
- **輸入**：`k8s_snapshot.json / ansible_run.json / events.jsonl / git/tf 摘要`
- **動作**：Jinja2 → HTML；轉 PDF；附可點 artifacts 連結
- **輸出**：`report/out/<run_id>.{html,pdf}`
- **DoD**：PDF 可開；Partial 也能產
- **Owner**：Validation & Report

### Phase 9｜整合彩排（全員，~2–3hr）
- **動作**：
  - `make up` → `make demo REQ="…"` → `make report` → `make down`
  - 注入一次故障（例如 rollout 失敗）→ 驗證重試與 Partial Report
- **DoD**：一口氣跑通；清場後可重跑不殘留
- **Owner**：全員

---

## 依賴順序與關鍵路徑
1) Infra（叢集/VM）→ 2) Validation（Ansible JSON 穩定）→ 3) Backend（流程與事件）→ 4) Frontend（串接）＋ AI（dry‑run → execute）→ 5) Report（PDF）

## 驗收總表（一次核對）
- **Frontend**：AI/GUI 跑通；事件首條 ≤1s；錯誤可補救；可下載報告
- **Backend**：重試/跳過/Partial；事件可回放
- **AI**：同語意不同措辭 → 等價計畫；錯誤有補救
- **Infra**：叢集 60s Ready；VM 可 `ping/curl`
- **Report**：PDF/HTML 含完整證據與可點連結
