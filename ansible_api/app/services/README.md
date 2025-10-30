AI 服務說明
=================

此資料夾內的 `ai_service.py` 為一個 client stub，用來連接「外部的 AI 核心（另一個專案）」或在沒有外部服務時回退到本地的 mock 產生器。

設計要點
- 前端（或 UI）會在聊天室中逐步收集使用者輸入（prompt），並把最終/或中間的 prompt 傳到後端的這個 client。
- 實際的 AI 核心（例如訓練或運行大型 LLM 的服務）放在另一個專案，透過 HTTP API 提供 `POST /generate_playbook` 之類的介面。
- 這個 repo 不包含 AI 核心本身；只保留一個安全的 client stub 以便開發與測試。

如何設定
- 在本專案的環境變數或 `.env` 檔中設定：
  - `AI_CORE_URL`：外部 AI core 的 base URL，例如 `https://ai-core.example.com`。
  - `AI_CORE_API_KEY`：若外部服務需要 API key，請填入（可選）。

行為
- 若 `AI_CORE_URL` 未設定，`generate_playbook_from_prompt` 會使用內建 mock 回傳可用的 playbook 範例，方便離線開發。
- 若設定了 `AI_CORE_URL`，client 會嘗試呼叫 `POST {AI_CORE_URL}/generate_playbook`，並傳送 JSON {"prompt": "..."}。

下一步建議
- 在另一個專案實作 AI core，提供 `/generate_playbook` endpoint，回傳 JSON {"playbook": "...yaml..."}。
- 前端聊天室可以逐步發送 prompt（或把對話狀態存在後端），並在使用者要求時呼叫此 client 生成 playbook。

範例（快速測試）
1. 不設定 `AI_CORE_URL`，啟動服務並呼叫生成函式，可看到 mock 輸出。
2. 若要整合遠端服務，設定 `AI_CORE_URL` 並啟動遠端 API，再呼叫即可取得真實回應。
