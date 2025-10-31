# ansible_api

這個專案是後端 API，提供 Ansible playbook 管理、部署與 AI 助手的 server-side client stub。AI 核心（實際生成 playbook 的 model）設計為放在另一個專案並以 HTTP API 提供服務，本 repo 提供接入點與本地 mock 回退以便開發。

## 目錄結構（重點）
- `app/`：FastAPI 應用程式來源
  - `app/core/config.py`：環境變數與設定
  - `app/services/ai_service.py`：AI client stub（會嘗試呼叫外部 AI core，失敗則回退 mock）
  - `app/api/v1/endpoints/`：REST API endpoints（playbooks、deployments、ai assistant 等）
- `create_user.py`：命令列建立管理員帳號的腳本
- `requirements.txt`：Python 相依套件

## 快速開始（後端）
建議使用虛擬環境來隔離相依套件 (Windows PowerShell 範例)：

```powershell
cd C:\Users\user\Desktop\school_work\internet\ansible_api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker pull mysql:8.0
docker run --name ansible_mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=ansible_api_db -p 3308:3306 -v c:\Users\user\Desktop\school_work\internet\ansible_api\mysql_data:/var/lib/mysql -d mysql:8.0 --default-authentication-plugin=mysql_native_password
docker ps --filter name=ansible_mysql --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

python create_user.py --email admin@example.com --password NewPass123 --role admin --force

```

啟動開發伺服器：

```powershell
uvicorn app.main:app --reload --port 8000
```

API 會在 http://127.0.0.1:8000 上運行（預設）。

## 重要環境變數
可把下列值放在 `.env` 檔或直接在環境變數中設定：

- `SECRET_KEY`：JWT/安全用密鑰（預設：`changeme`，生產請設定強隨機字串）
- `DATABASE_URL`：資料庫連線字串，預設 `sqlite:///./test.db`
- `OPENAI_API_KEY`：若直接使用 OpenAI 等 LLM，可放入金鑰（本專案使用外部 AI core 時未必需要）
- `AI_CORE_URL`：外部 AI core 的 base URL（例如 `https://ai-core.example.com`）。若設定此值，`ai_service` 會嘗試呼叫 `{AI_CORE_URL}/generate_playbook`。
- `AI_CORE_API_KEY`：若外部 AI core 要求 API key，設定此值

範例 `.env`：

```
SECRET_KEY=your-secret
DATABASE_URL=sqlite:///./dev.db
AI_CORE_URL=https://ai-core.example.com
AI_CORE_API_KEY=xxxx
```

## AI 整合行為說明
- `app/services/ai_service.py` 的 `generate_playbook_from_prompt(prompt: str)` 預期行為：
  - 若 `AI_CORE_URL` 有設定，會對 `{AI_CORE_URL}/generate_playbook` 做 POST，送出 JSON `{ "prompt": "..." }`。
  - 期望遠端回傳 JSON `{ "playbook": "...yaml..." }`。
  - 若未設定或 HTTP 呼叫失敗，會回退回本地的 mock generator（方便離線開發與測試）。

## 常用指令
- 建立管理者帳號：

```powershell
python create_user.py --email admin@example.com --password NewPass123 --role admin --force
```

- 查看被 git 忽略（驗證 `.gitignore`）：

```powershell
git status --ignored
```

## 測試與開發建議
- 單元測試（如加入 pytest）可以模擬 `httpx` 的回應來測試成功/失敗情境（可使用 `respx` 或 `httpx.MockTransport`）。
- 若要在本地模擬完整的 AI core，可以另起一個小型 FastAPI 專案，實作 `/generate_playbook` endpoint 回傳固定的 YAML，並在 `.env` 設定 `AI_CORE_URL` 指向它。

## 進階建議
- 將 AI core 與此後端分離部署：AI core 負責模型、prompt engineering、安全與費用管理；後端只負責驗證、排隊、儲存與回傳生成結果。
- 在生產環境把 `AI_CORE_API_KEY` 與 `SECRET_KEY` 管理在安全的 secret manager（例如 Azure Key Vault、AWS Secrets Manager）。

---

如果你想，我也可以幫你：
- 加入後端的單元測試範例（pytest + respx 模擬 AI core）。
- 寫一個簡易的 local AI core 範例 server，方便整合測試。