# GUI × AI × MCP × Ansible — 團隊完整 README

> 以「圖形化介面 + 自然語言（MCP）」自動完成：建立 Kubernetes 叢集 → 建立測試 VM → 佈署示範服務 → 用 Ansible 驗證可用性 → 蒐證 → 產出 Audit Report（HTML/PDF）→ 可選清理。

---

## 目錄
- [亮點 / 成果](#亮點--成果)
- [系統架構](#系統架構)
- [技術棧與先決條件](#技術棧與先決條件)
- [安裝與初始化](#安裝與初始化)
- [.env.example](#envexample)
- [目錄結構](#目錄結構)
- [Makefile 範本](#makefile-範本)
- [快速開始](#快速開始)
- [前後端 API 契約](#前後端-api-契約)
- [事件格式](#事件格式)
- [MCP 工具定義（摘要）](#mcp-工具定義摘要)
- [基礎設施樣板](#基礎設施樣板)
- [Ansible 驗證樣板](#ansible-驗證樣板)
- [報告模板與輸出](#報告模板與輸出)
- [開發流程（兩天節奏）](#開發流程兩天節奏)
- [角色分工與 RACI](#角色分工與-raci)
- [故障排除 FAQ](#故障排除-faq)
- [延伸功能（可選）](#延伸功能可選)
- [授權 / 貢獻](#授權--貢獻)

---

## 亮點 / 成果
- **雙入口**：AI 模式（自然語言 → MCP）與 GUI 模式（表單 → 計畫預覽 → 執行）
- **可觀測**：流程事件（SSE/WS）+ 狀態機（state.json）
- **可稽核**：Ansible JSON 證據、K8s/VM 快照、HTML/PDF 報告
- **一鍵體驗**：`make up / demo / validate / report / down`

---

## 系統架構
```mermaid
flowchart LR
U[前端 UI
(AI 模式/GUI 模式)] -->|REST / SSE| B[Orchestrator API
(狀態機 + 事件流)]
B --> K[Tool: K8s
(k3d/kubectl/helm)]
B --> V[Tool: VM
(KubeVirt 或 EC2)]
B --> A[Tool: Ansible
(playbook + callback)]
B --> E[Tool: Evidence
(kubectl/terraform/ansible/git)]
B --> R[Tool: Report
(Jinja2 → HTML/PDF)]
U -.-> M[MCP Planner
自然語言 → 工具序列]
M --> B
```

---

## 技術棧與先決條件
**系統**：macOS / Linux  
**必備**：Docker、kubectl、k3d、Python 3.11+、pip、Ansible、git、wkhtmltopdf 或 weasyprint 其一、（KubeVirt 需 virtctl）

---

## 安裝與初始化
```bash
# 1) 取得專案並安裝依賴
make bootstrap      # 建虛擬環境、安裝後端/報告依賴、前端依賴

# 2) 準備環境變數
cp .env.example .env.local && $EDITOR .env.local

# 3) 啟動本機叢集與示範服務/VM（首次跑 demo 建議）
make up

# 4) 開發時啟動後端與前端
make dev-backend    # 啟動 Orchestrator API (http://localhost:8000)
make dev-frontend   # 啟動 UI (http://localhost:5173 或 3000)
```

---

## .env.example
```ini
# 後端 API
API_HOST=0.0.0.0
API_PORT=8000
API_BASE=http://localhost:8000

# 前端
VITE_API_BASE=http://localhost:8000

# K8s / k3d
K3D_CLUSTER_NAME=demo
K3D_CONFIG=infra/local/k3d.yaml
KUBECONFIG=.kube/demo-kubeconfig

# VM / KubeVirt
SSH_PUBLIC_KEY=~/.ssh/id_rsa.pub
VM_NAME=test-vm
VM_NAMESPACE=default

# 報告
REPORT_TEMPLATE=report/templates/report.md.j2
REPORT_OUT_DIR=report/out

# 其他
PYTHON_ENV=.venv
RUN_ARTIFACTS_DIR=artifacts
```

---

## 目錄結構
```text
.
├─ ui/                    # 前端：AI/GUI、事件流、報告下載
├─ orchestrator/          # 後端：狀態機、事件流、REST+SSE/WS
├─ tools/                 # 動作適配：k8s / vm / ansible / report / monitor
│  ├─ k8s/
│  ├─ vm/
│  ├─ ansible/
│  ├─ report/
│  └─ monitor/
├─ k8s/                   # 範例服務 manifests (nginx)
├─ infra/                 # IaC (local k3d / 可選 cloud eks)
│  ├─ local/k3d.yaml
│  └─ cloud/eks/*
├─ mcp/                   # tools.json + 規劃器
├─ report/                # 模板與轉檔腳本
├─ artifacts/             # 證據（依 run_id 分層）
├─ scripts/               # kubectl/ansible/terraform 封裝
├─ Makefile
└─ .env.example
```

**Artifacts 與命名**  
`run_id = YYYYMMDD-HHMMSS-rand3`
```text
artifacts/<run_id>/
  ├─ k8s_snapshot.json
  ├─ vm_status.json
  ├─ ansible_run.json
  ├─ events.jsonl
  └─ params.json
report/out/<run_id>.{html,pdf}
```

---

## Makefile 範本
```Makefile
.PHONY: bootstrap up down demo validate report dev-backend dev-frontend smoke

PY=python3
PIP=pip
BACKEND=orchestrator
UI=ui
RUN_ID?=$(shell date +%Y%m%d-%H%M%S)-$$(LC_ALL=C tr -dc a-z0-9 </dev/urandom | head -c3)

bootstrap:
	$(PIP) install -r $(BACKEND)/requirements.txt
	cd $(UI) && npm install

up: ## 建叢集+VM+服務
	scripts/k3d_up.sh $(K3D_CONFIG)
	scripts/kubevirt_up.sh $(VM_NAME)
	kubectl apply -f k8s/

validate: ## Ansible 驗證
	ANSIBLE_STDOUT_CALLBACK=json ansible-playbook tools/ansible/playbooks/site.yml \
	  -i tools/ansible/inventories/runs/$(RUN_ID)/hosts.ini \
	  -e run_id=$(RUN_ID)

report: ## 產生報告
	$(PY) report/build.py --run-id $(RUN_ID) --template $(REPORT_TEMPLATE) --out-dir $(REPORT_OUT_DIR)

demo: ## 以 MCP 進行端到端 (讀 REQ)
	$(PY) orchestrator/cli.py run --req "$(REQ)" --run-id $(RUN_ID)

down: ## 清場（保留 artifacts/report）
	scripts/k3d_down.sh $(K3D_CONFIG)
	scripts/kubevirt_down.sh $(VM_NAME)

smoke:
	scripts/smoke.sh $(RUN_ID)

dev-backend:
	$(PY) -m uvicorn orchestrator.app:app --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000} --reload

dev-frontend:
	cd $(UI) && npm run dev
```

---

## 快速開始
```bash
# 1) 一鍵建立環境與服務
make up

# 2) 以 AI 模式跑一次端到端（或直接用前端輸入）
make demo REQ="幫我新建一個 Kubernetes cluster 並建立 test VM，連動 Ansible 驗證服務可用性，最後產生完整 Audit Report"

# 3) 產出報告
make report RUN_ID=<同上一個 run_id>

# 4) 清理（保留 artifacts/ 與 report/out/）
make down
```

---

## 前後端 API 契約
**基底 URL**：`http://localhost:8000`

```yaml
# OpenAPI（摘要）
paths:
  /api/run:
    post:
      summary: AI 模式入口（自然語言）
      requestBody: { text/plain or app/json: {text: string} }
      responses: {200: {run_id: string}}
  /api/plan:
    post:
      summary: GUI 模式產生計畫（dry-run）
      requestBody: {app/json: {provider, vmType, replicas, ...}}
      responses: {200: {plan_id: string, steps: array}}
  /api/execute:
    post:
      summary: 執行前一步的計畫
      requestBody: {app/json: {plan_id: string}}
      responses: {200: {run_id: string}}
  /api/runs/{id}/events:
    get:
      summary: 事件串流（SSE/WS）
  /api/runs/{id}/report:
    get:
      summary: 取得 HTML/PDF 報告
  /api/runs/{id}/retry|skip|cleanup:
    post:
      summary: 對指定步驟重試/跳過/清理
```

---

## 事件格式
```json
{
  "run_id": "2025-10-07-001",
  "ts": "2025-10-07T04:12:33Z",
  "step": "deploy_service",
  "phase": "start|end|error",
  "level": "info|warn|error",
  "msg": "nginx rollout complete",
  "kv": {"replicas": 2, "duration_sec": 23.4}
}
```

---

## MCP 工具定義（摘要）
**六大工具**
1. `tool.create_cluster({provider:"k3d|eks", name, nodes, dry_run}) → {context, kubeconfig_path, evidence}`
2. `tool.create_vm({type:"kubevirt|ec2", image, size, ssh_pubkey, dry_run}) → {inventory_host, vm_ip|vmi_name}`
3. `tool.deploy_service({name,image,replicas,expose}) → {url|svc_dns}`
4. `tool.ansible_validate({inventory,playbook,extra_vars}) → {summary, ansible_json}`
5. `tool.collect_evidence({run_id}) → {artifacts_dir}`
6. `tool.build_audit_report({run_id,template}) → {report_html, report_pdf}`

**JSON Schema（樣例）**
```json
{
  "name": "tool.create_cluster",
  "description": "Create or reuse a K8s cluster",
  "input_schema": {
    "type": "object",
    "properties": {
      "provider": {"type": "string", "enum": ["k3d", "eks"]},
      "name": {"type": "string"},
      "nodes": {"type": "integer", "minimum": 1, "default": 3},
      "dry_run": {"type": "boolean", "default": false}
    },
    "required": ["provider", "name"]
  }
}
```

---

## 基礎設施樣板
**k3d 叢集（infra/local/k3d.yaml）**
```yaml
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata: { name: demo }
servers: 1
agents: 2
ports:
  - port: 8080:80
    nodeFilters: [loadbalancer]
```

**KubeVirt VM（tools/vm/kubevirt/vm.yaml）**
```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata: { name: test-vm, namespace: default }
spec:
  running: false
  template:
    metadata: { labels: { kubevirt.io/domain: test-vm } }
    spec:
      domain:
        devices: { disks: [{ name: containerdisk }, { name: cloudinitdisk }] }
        resources: { requests: { memory: 512Mi } }
      volumes:
        - name: containerdisk
          containerDisk: { image: quay.io/containerdisks/ubuntu:22.04 }
        - name: cloudinitdisk
          cloudInitNoCloud:
            userData: |
              #cloud-config
              ssh_authorized_keys:
                - ${SSH_PUBLIC_KEY_CONTENT}
              packages: [curl]
```

---

## Ansible 驗證樣板
**Playbook（tools/ansible/playbooks/site.yml）**
```yaml
- hosts: validator
  gather_facts: false
  vars:
    service_url: "http://nginx.default.svc.cluster.local"
  tasks:
    - name: Wait for nginx pods ready
      kubernetes.core.k8s_info:
        kind: Pod
        namespace: default
        label_selectors: ["app=nginx"]
      register: pods
      until: >-
        (pods.resources | length) > 0 and
        ((pods.resources | map(attribute='status.containerStatuses.0.ready') | list) | all)
      retries: 12
      delay: 5

    - name: HTTP 200 check
      uri:
        url: "{{ service_url }}"
        return_content: true
        status_code: 200
      register: httpcheck
      retries: 6
      delay: 5
      until: httpcheck.status == 200

    - name: Persist proof
      copy:
        dest: "artifacts/{{ run_id }}/nginx_probe.txt"
        content: "{{ httpcheck.content | default('') }}"
```

**Callback（可選，自訂輸出 JSON 到 artifacts）**
- 方式 A：環境變數 `ANSIBLE_STDOUT_CALLBACK=json` 後由後端收斂
- 方式 B：自製 `callback_plugins/json_dump.py` 直接寫 `artifacts/<run_id>/ansible_run.json`

---

## 報告模板與輸出
**模板（report/templates/report.md.j2）**
```markdown
# Audit Report — {{ run_id }}

## Summary
- Request: {{ req_text }}
- Git Commit: {{ git_commit }}
- Timestamp: {{ ts }}

## Infrastructure Evidence
- Cluster Nodes: {{ nodes_count }}
- VM Status: {{ vm_status }}

## Service Health
- Probes: {{ probes_summary }}

## Artifacts
- [k8s snapshot](../artifacts/{{ run_id }}/k8s_snapshot.json)
- [ansible run](../artifacts/{{ run_id }}/ansible_run.json)
- [events](../artifacts/{{ run_id }}/events.jsonl)
```

**轉檔腳本（report/build.py，摘要）**
```python
from jinja2 import Environment, FileSystemLoader
import json, argparse, pathlib, subprocess

def main(run_id, template, out_dir):
    env = Environment(loader=FileSystemLoader('report/templates'))
    t = env.get_template(pathlib.Path(template).name)
    ctx = load_context(run_id)
    html = t.render(**ctx)
    out = pathlib.Path(out_dir) / f"{run_id}.html"
    out.write_text(html, encoding='utf-8')
    # PDF：擇一使用 wkhtmltopdf 或 weasyprint
    subprocess.run(["wkhtmltopdf", str(out), str(out).replace('.html', '.pdf')], check=False)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-id', required=True)
    ap.add_argument('--template', required=True)
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args()
    main(a.run_id, a.template, a.out_dir)
```

---

## 開發流程（兩天節奏）
**Day 1 上午**：Infra 起叢集/VM；Ansible 本機驗證；Backend 架 API+Mock；Frontend 串 Mock；AI 撰 tools schema  
**Day 1 下午**：Backend 串真步驟；Frontend 換真 API；AI 完成 dry-run→execute；全線打通一次  
**Day 2 上午**：重試/跳過、Partial Report、事件視覺化、Artifacts 歸檔  
**Day 2 下午**：一鍵彩排（up → demo/report → down），產截圖

---

## 角色分工與 RACI
- **Frontend**：雙模式 UI、事件流、報告下載（R/A）
- **Backend**：狀態機、事件、REST+SSE/WS、重試/跳過/清理、Partial Report（R/A）
- **AI/MCP**：規劃器與 tools（R/A）
- **Infra**：k3d、KubeVirt/EC2、smoke（R/A）
- **Validation/Report**：Ansible/模板/轉檔/蒐證（R/A）

---

## 故障排除 FAQ
- **Pod 卡 ContainerCreating**：檢查映像拉取與節點事件；`kubectl describe pod` + `kubectl get events`
- **VMI NotReady**：核對 virtctl 與 CRDs；檢查 `virt-handler` 日誌
- **Ansible 解析不到 `*.svc.cluster.local`**：改以 `NodePort` 或 `port-forward` URL
- **PDF 轉檔出錯**：切換轉檔器（weasyprint ↔ wkhtmltopdf）

---

## 延伸功能（可選）
- **安全附錄**：Trivy 鏡像掃描、kube-bench（CIS）分數納入報告
- **策略管控**：OPA/Gatekeeper Policy，違規列附錄
- **CI/CD**：GitHub Actions 產 report 上傳為 Release assets

---

## 授權 / 貢獻
- 內部 Demo 用。若對外開源，請補上 LICENSE 與 CONTRIBUTING。

