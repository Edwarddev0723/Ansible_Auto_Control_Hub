
# 前端 UI 規格 — Inventory Groups（繁體中文）

說明
- 本檔為針對 Inventory Groups 的前端功能與介面規格。直接對應 `docs/API設計.md` 中的群組 API（CRUD 與成員管理）。內容涵蓋每個畫面要顯示的欄位、表單驗證、使用者流程、以及對應的 API 呼叫範例，供前端工程師直接實作或轉為 wireframe / component 規格。

目標讀者
- 前端工程師、UI/UX 設計師、後端工程師（做 API 對應）

對應 API（參考）
- GET /api/v1/inventory/groups
- POST /api/v1/inventory/groups
- GET /api/v1/inventory/groups/{group_id}
- PUT /api/v1/inventory/groups/{group_id}
- PATCH /api/v1/inventory/groups/{group_id}/members
- DELETE /api/v1/inventory/groups/{group_id}

畫面與元件總覽
- 群組列表（/inventory/groups）
- 建立群組（Modal 或 /inventory/groups/new）
- 群組詳細（/inventory/groups/:group_id）
- 共用元件：Host Picker（multi-select）、Key/Value Editor、Confirmation Modal、Typeahead 搜尋

1) 群組列表頁（/inventory/groups）

主要目的
- 快速瀏覽、搜尋與對群組做批次或單筆操作（編輯、刪除、選為部署目標）。

介面欄位（Table）
- Checkbox（批次選取）
- 名稱（clickable → 群組詳細）
- 描述（短文，hover 顯示完整）
- 成員數量（members_count）
- 操作：編輯、刪除、加入部署（快速動作）

控制項與互動
- 搜尋（依名稱）
- 篩選：有成員 / 空群組
- 分頁控制（page, page_size）
- 批次操作列：當有選取時顯示「加入部署」「刪除群組」按鈕

API 映射
- 頁面載入：GET /api/v1/inventory/groups?page=1&page_size=20
- 搜尋：GET /api/v1/inventory/groups?search=<q>
- 單一刪除：DELETE /api/v1/inventory/groups/{group_id}
- 批次刪除：前端可依序呼叫 DELETE 或後端若支援再改用批次 API

UX 建議
- 單筆刪除需二次確認（production 環境可要求輸入名稱確認）
- 若列表有大量群組，支援伺服器端分頁與快速搜尋

2) 建立群組（Modal / /inventory/groups/new）

表單欄位與驗證
- name（text, required, 3-100 chars, allowed [A-Za-z0-9_-]）
- description（textarea, optional）
- members（multi-select searchable dropdown）
  - 顯示 host name + hostname
  - typeahead 呼叫：GET /api/v1/inventory/hosts?search=<q>&page_size=20
- vars（key/value editor，key 不可重複，value 為字串）

按鈕
- 取消、建立（當 name 欄位為空或驗證失敗時停用）

API
- POST /api/v1/inventory/groups
  範例 body:
  {
    "name": "production",
    "description": "Prod web servers",
    "members": ["host_1","host_2"],
    "vars": {"ansible_user":"ubuntu"}
  }

成功處理
- 關閉 modal、刷新列表、顯示 toast "已建立群組"；可選導向群組詳細頁

3) 群組詳細頁（/inventory/groups/:group_id）

目的
- 檢視群組 metadata、變數與成員清單，並進行成員管理（增/刪）、編輯或刪除群組。

主要區塊
- 標頭：群組名稱、描述、成員數、建立者、建立時間
- 操作列：編輯（開啟 edit modal）、刪除、加入部署、匯出成員清單
- 變數區：key/value 顯示及編輯（Admin）
- 成員表：
  - 欄位：checkbox、主機名稱（link）、hostname/ip、port、username、主機狀態、操作（ping）
  - 支援分頁或 lazy-load（大於 page_size 時）

對應 API
- 載入：GET /api/v1/inventory/groups/{group_id}
- 新增成員：PATCH /api/v1/inventory/groups/{group_id}/members with { "add": [ids] }
- 移除成員：PATCH /api/v1/inventory/groups/{group_id}/members with { "remove": [ids] }
- 更新 metadata/vars：PUT /api/v1/inventory/groups/{group_id}
- 刪除群組：DELETE /api/v1/inventory/groups/{group_id}

UX 與行為細節
- 新增成員時使用主機挑選器（typeahead + 多選），提交後僅更新該群組的成員區塊（no full page reload）
- 成員移除支援批次選取再一次 PATCH remove
- 變數編輯禁止重複 key，必要時前端可將 key normalize（trim 及小寫）再送後端

4) 成員挑選器（Host Picker）

規格
- searchable, virtualized list（支援大量 host）
- 顯示每項：name / hostname / status
- 支援選擇整個 group（若在群組 context 顯示）
- API：GET /api/v1/inventory/hosts?search=<q>&page_size=20

5) Key/Value Editor

規格
- 每行為一對 key/value，key 不可空且不重複
- 支援 import/export JSON
- 前端驗證：key pattern（例如 /^[a-z0-9_]+$/i）與 trim

6) 錯誤與例外處理

- 422 驗證錯誤：將 API 的 error.details map 到對應欄位顯示
- 409 衝突：顯示資源已被修改（提供重新載入按鈕）
- 網路錯誤：顯示 toast 並提供重試

Edge cases
- 同步編輯衝突：若 PUT 回 409，顯示當前資源並提示是否覆蓋或合併
- 超大型群組：當成員數 > 1000，成員表改為 lazy-load 分頁並提供 "選取全部 X 位" 的確認

Accessibility & Performance
- 表單含 label 與 aria 屬性，支援鍵盤操作
- Typeahead 使用 300ms debounce
- 列表採伺服器端分頁，避免一次載入大量資料

示範流程（快速）
- 建立群組並加入主機：使用者在 modal 填 name -> typeahead 選 host -> submit -> POST /api/v1/inventory/groups -> refresh list
- 新增/移除成員：群組詳細頁使用主機挑選器新增（PATCH add），或選取成員批次 remove（PATCH remove）

後端注意事項（給後端團隊）
- PATCH /members 必須為冪等操作（已存在的 add 不應報錯）
- 刪除群組時若有依賴（job/policy），回 409 並附帶依賴列表
- list response 建議包含 members_count 以降低後續查詢

驗收標準
- 前端能透過文件中列出的 API 完成群組的建立、編輯、刪除與成員管理
- 新增/移除成員使用 PATCH 並在 UI 上無需整頁重載即可更新
- API 回傳的欄位應與前端所需欄位一致（尤其是 members_count 與 members 詳細）

交付物選項（我可以替您產出）
1) 把此文件存為 `docs/inventory-groups-ui-spec.md`（已完成）
2) 產生一個 minimal React 範例（群組列表 + 新增 modal + 成員挑選器 mock）
3) 產生 OpenAPI mock 或 FastAPI stub 供前端串接

如需我把此檔案 commit 至另一個路徑或做格式調整（例如加入 wireframe 圖片或 Figma 連結），請告訴我具體要求。


