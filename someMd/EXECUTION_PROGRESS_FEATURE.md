# Playbook 執行進度條與強制停止功能

## 功能概述

此功能為 Playbook 執行過程添加了視覺化進度追蹤和強制停止能力。

## 新增功能

### 1. 執行進度視覺化
- **進度條**: 顯示整體執行進度 (0-100%)
- **狀態訊息**: 即時顯示當前執行狀態
- **Job ID 顯示**: 追蹤每次執行的唯一標識符
- **個別 Playbook 狀態**: 列表顯示每個 Playbook 的執行結果
  - ✅ 成功 (綠色)
  - ❌ 失敗 (紅色)
  - ⚠️ 已中止 (橙色)
  - 🔄 執行中 (藍色旋轉動畫)

### 2. 強制停止功能
- **停止按鈕**: 執行過程中可隨時點擊停止
- **確認對話框**: 避免誤觸
- **後端 API**: 實際中止正在執行的任務
- **狀態更新**: 自動標記未完成的 Playbook 為 'aborted'

## 前端改動

### PlaybookView.vue

**新增響應式變數:**
\\\	ypescript
const showExecutionProgress = ref(false)  // 顯示進度框
const executionProgress = ref(0)          // 進度百分比
const executionStatus = ref('')           // 狀態文字
const executingPlaybooks = ref([])        // 執行中的 playbook 列表
const currentJobId = ref(null)            // 當前 Job ID
const executionAborted = ref(false)       // 是否已中止
\\\`n
**新增函數:**
- \stopExecution()\: 調用 API 中止執行
- \closeExecutionProgress()\: 關閉進度框並刷新列表

**UI 組件:**
- 全螢幕模態對話框
- 進度條 (0-100%)
- Job ID 顯示區域
- Playbook 執行狀態卡片列表
- 強制停止按鈕 (紅色)
- 關閉按鈕 (完成後顯示)

### playbook.ts API

**新增 API 函數:**
\\\	ypescript
// 中止執行
export const abortJob = async (jobId: string)

// 獲取 Job 狀態 (未來可用於輪詢)
export const getJobStatus = async (jobId: string)
\\\`n
## 後端改動

### playbooks.py

**新增端點:**

1. **POST /api/playbooks/jobs/{job_id}/abort**
   - 功能: 中止正在執行的 Job
   - 參數: job_id (路徑參數)
   - 返回: 中止狀態

2. **GET /api/playbooks/jobs/{job_id}/status**
   - 功能: 獲取 Job 執行狀態
   - 參數: job_id (路徑參數)
   - 返回: Job 詳細資訊 (狀態、進度、結果)

**全局變數:**
\\\python
active_jobs = {}  # 儲存正在執行的 job 資訊
\\\`n
## 使用流程

1. 使用者勾選要執行的 Playbook
2. 點擊「執行」按鈕
3. 彈出進度對話框，顯示執行狀態
4. 進度條從 0% 開始增加
5. 每個 Playbook 顯示各自的執行狀態
6. (可選) 點擊「強制停止」按鈕中止執行
7. 執行完成或中止後，點擊「關閉」返回列表

## 進度計算邏輯

- **10%**: 開始執行 (API 請求發送)
- **10-90%**: 根據完成的 Playbook 數量遞增
- **100%**: 所有 Playbook 執行完畢

公式: \progress = 10 + (completedCount / totalCount) * 80\`n
## 未來改進建議

1. **即時進度更新**: 使用 WebSocket 或輪詢機制即時更新進度
2. **執行日誌顯示**: 展開每個 Playbook 可查看詳細執行日誌
3. **執行歷史**: 將執行記錄儲存到資料庫
4. **重試機制**: 失敗的 Playbook 可單獨重試
5. **並行執行控制**: 設定最大並行執行數
6. **執行時間估算**: 根據歷史數據預估剩餘時間

## 測試要點

- ✅ 進度框正確顯示
- ✅ 進度條動畫流暢
- ✅ 各種狀態圖示正確顯示
- ✅ 強制停止功能正常工作
- ✅ 執行完成後自動關閉 (3 秒)
- ✅ 錯誤處理正確
- ✅ API 調用成功

## 相關文件

- 前端: \rontend/src/views/PlaybookView.vue\`n- 前端 API: \rontend/src/api/playbook.ts\`n- 後端: \ackend/app/routers/playbooks.py\`n
