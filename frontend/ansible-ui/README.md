# ansible-ui (前端)

這是本專案的前端，使用 Vite + Vue 3 構建，提供 Playbook 編輯、主機/清單管理、部署操作與 AI 助手（聊天式介面）等功能。

## 快速開始（前端）
在啟動前請先安裝 node_modules（一次性操作）：

```powershell
cd C:\Users\user\Desktop\school_work\internet\frontend\ansible-ui
npm install
```

啟動開發伺服器：

```powershell
npm run dev
```

開啟瀏覽器並前往 dev server 上顯示的 URL（通常 http://localhost:5173/）。

> 注意：若 `npm run dev` 出現錯誤，請先確保 `node` 與 `npm` 版本相容，並且執行 `npm install` 後沒有安裝錯誤。

## 主要功能簡介
- Playbook 編輯器（`src/views/playbooks/PlaybookEditor.vue`）：
  - 提供可視化的任務建構器（snippet、模組下拉、參數欄），可快速新增任務到 playbook，並與 YAML 預覽同步。
  - YAML 欄仍允許手動編輯以做微調。
- AI 助手（聊天介面）：
  - 前端應以聊天室互動方式收集使用者 prompt/對話，再呼叫後端 API（後端會向外部 AI core 或 mock 生成 playbook）。

## 前端與後端的整合
- 預設情況下，前端會呼叫後端 `ansible_api` 提供的 REST API（請確保後端正在本機或指定 URL 運行）。
- Playbook 儲存與載入透過後端的 `/playbooks` endpoint
- 若你要串接真實 AI core：
  - 在後端設定 `AI_CORE_URL` 與 `AI_CORE_API_KEY`（見後端 README）
  - 前端觸發的生成流程會先呼叫後端的 AI assistant endpoint（後端再向 AI core 呼叫）

## 開發提示與建議改進
- 建議安裝 `js-yaml`（如果你要把 YAML 解析/驗證搬到前端）來更正確的操作 playbook 結構：
  ```powershell
  npm install js-yaml
  ```
- 可加入 `vuedraggable` 以支援在 UI 上拖放排序 tasks。
- 將常用 snippets 與模組欄位定義抽成一個可管理的 JSON/後端配置，前端依據定義自動生成表單欄位。

## 偵錯
- 如果出現 "Failed to write the global types file" 或 TypeScript/Vue 相關錯誤：
  - 確認 `node_modules` 存在且 `vue` 為 direct dependency。
  - 可嘗試刪除 `node_modules` 與鎖檔（`package-lock.json` 或 `yarn.lock`），重新 `npm install`。

## 範例流程（測試 playbook 編輯器）
1. 啟動後端 API（參考後端 README）。
2. 啟動前端開發伺服器（`npm run dev`）。
3. 在 UI 建立新 Playbook，使用任務建構器新增幾個任務，檢視 YAML 預覽，最後點選儲存。
4. 確認後端接收到 POST 並儲存（或回傳成功）。

---

若要我幫你，我可以：
- 把 Playbook editor 加上 `js-yaml` 解析/驗證與更健全的新增/移除任務邏輯（會更新 `package.json` 並加上前端測試範例）。
- 增加 draggable 支援（任務排序）。
- 寫一小段示範把前端的 AI prompt 傳到後端並把回傳的 playbook 放入編輯器的程式碼。