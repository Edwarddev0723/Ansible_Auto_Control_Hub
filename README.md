# Ansible Auto Control Hub

> Ansible 自動化管理平台 - 提供視覺化介面管理 Inventory、Playbook、Galaxy Collections，並支援 AI 輔助部署

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3.4+-blue.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)

---

## 📋 目錄

- [專案簡介](#專案簡介)
- [核心功能](#核心功能)
- [技術架構](#技術架構)
- [系統需求](#系統需求)
- [快速開始](#快速開始)
- [系統操作說明](#系統操作說明)
- [資料庫管理](#資料庫管理)
- [API 文件](#api-文件)
- [開發指南](#開發指南)
- [專案結構](#專案結構)

---

## 📖 專案簡介

Ansible Auto Control Hub 是一個全端 Web 應用程式，旨在簡化 Ansible 自動化管理工作流程。透過直覺的視覺化介面，使用者可以輕鬆管理伺服器清單 (Inventory)、執行腳本 (Playbook)、安裝依賴套件 (Galaxy Collections)，並透過 AI 助手獲得部署建議。

### ✨ 主要特色

- 🎯 **視覺化管理** - 取代手動編輯 YAML/INI 設定檔
- 🔄 **即時執行** - 直接從瀏覽器執行 Playbook 並查看結果
- 📦 **依賴管理** - 自動檢查並安裝 Ansible Galaxy Collections
- 🤖 **AI 輔助** - 智能對話助手協助設定與除錯
- 🗂️ **群組管理** - 靈活的伺服器分組與批次操作
- 🔐 **SSH 測試** - 快速驗證伺服器連線狀態

---

## 🚀 核心功能

### 1. Inventory 管理
- ✅ CRUD 操作 (新增/讀取/更新/刪除)
- ✅ 伺服器群組分類
- ✅ SSH 連線測試
- ✅ 批次選取與操作
- ✅ 搜尋與分頁

### 2. Playbook 管理
- ✅ 視覺化編輯介面
- ✅ 支援 Group/Host 目標選擇
- ✅ Task 啟用/停用控制
- ✅ 多行 YAML 編輯器
- ✅ 即時執行與結果回饋
- ✅ Working Directory 設定

### 3. Galaxy Collections
- ✅ Requirements.yml 視覺化編輯
- ✅ 查看已安裝的 Collections
- ✅ 一鍵安裝/卸載
- ✅ 檢查 Playbook 依賴

### 4. AI 對話助手
- ✅ 自然語言互動
- ✅ 部署建議與除錯
- ✅ Playbook 生成協助
- ✅ 快速回覆按鈕

### 5. 群組管理
- ✅ 建立自訂伺服器群組
- ✅ 批次管理多台伺服器
- ✅ 群組層級 Playbook 執行

---

## 🏗️ 技術架構

### 後端技術棧
```
FastAPI 0.104+          # Web 框架
SQLAlchemy 2.0+         # ORM
Alembic                 # 資料庫遷移
MySQL 8.0+              # 資料庫
PyYAML                  # YAML 解析
Pydantic                # 資料驗證
Uvicorn                 # ASGI 伺服器
```

### 前端技術棧
```
Vue 3.4+                # 前端框架
TypeScript 5.0+         # 型別檢查
Vite 5.0+               # 建置工具
Axios                   # HTTP 客戶端
Vue Router 4            # 路由管理
Tailwind CSS            # CSS 框架
```

### 部署架構
```
Docker Desktop          # 容器化 (Windows)
WSL 2 (Ubuntu)          # Linux 子系統 (執行 Ansible)
Ansible                 # 自動化引擎
```

---

## 💻 系統需求

### Windows 環境
- **作業系統**: Windows 10/11 (64-bit)
- **Docker Desktop**: 最新穩定版
- **WSL 2**: Ubuntu 20.04 或更新版本
- **Python**: 3.9+
- **Node.js**: 18+
- **記憶體**: 至少 8GB RAM

### macOS/Linux 環境
- **Python**: 3.9+
- **Node.js**: 18+
- **MySQL**: 8.0+
- **Ansible**: 2.9+

---

## 🎯 快速開始

### 步驟 1: 環境準備 (Windows 使用者)

#### 1.1 安裝 Docker Desktop
```bash
# 下載並安裝 Docker Desktop
# https://www.docker.com/products/docker-desktop/

# 啟動 Docker Desktop 並確認 WSL 2 integration 已啟用
```

#### 1.2 安裝 WSL 2 Ubuntu
```powershell
# 以管理員身份執行 PowerShell
wsl --install -d Ubuntu-20.04

# 設定 Ubuntu 使用者名稱和密碼
# 更新套件並安裝 Ansible
wsl
sudo apt update
sudo apt install -y ansible python3-pip
exit
```

### 步驟 2: Clone 專案
```bash
git clone https://github.com/Edwarddev0723/Ansible_Auto_Control_Hub.git
cd Ansible_Auto_Control_Hub
```

### 步驟 3: 啟動資料庫
```bash
cd backend
docker-compose up -d

# 確認 MySQL 容器運行中
docker ps
```

### 步驟 4: 設定後端

#### 4.1 建立虛擬環境
```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

#### 4.2 安裝依賴
```bash
pip install -r requirements.txt
```

#### 4.3 設定環境變數
```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案 (預設值通常可直接使用)
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=ansible_user
# DB_PASSWORD=ansible_pass
# DB_NAME=ansible_hub
```

#### 4.4 執行資料庫遷移
```bash
# 套用所有遷移檔案到資料庫
alembic upgrade head

# 確認遷移版本
alembic current
```

#### 4.5 初始化測試資料
```bash
python seed_data.py
```

#### 4.6 啟動後端服務
```bash
uvicorn app.main:app --reload

# 後端 API: http://localhost:8000
# API 文件: http://localhost:8000/docs
```

### 步驟 5: 設定前端

#### 5.1 安裝依賴
```bash
cd ../frontend
npm install
```

#### 5.2 設定環境變數 (選用)
```bash
# 複製環境變數範本
cp .env.example .env

# 預設 API URL: http://localhost:8000
# 如需修改可編輯 .env 檔案
```

#### 5.3 啟動開發伺服器
```bash
npm run dev

# 前端應用: http://localhost:5173
```

### 步驟 6: 驗證安裝

1. 開啟瀏覽器訪問 `http://localhost:5173`
2. 應該能看到 Inventories 列表頁面
3. 測試功能:
   - 查看範例 Inventory
   - 執行 SSH 連線測試
   - 查看範例 Playbook
   - 訪問 Galaxy Collections 頁面

---

## 📚 系統操作說明

### Inventory 管理

#### 新增 Inventory
1. 點擊 Inventories 頁面的「新增 Inventory」按鈕
2. 輸入 Inventory 配置 (INI 格式):
   ```ini
   [webservers]
   server1 ansible_ssh_host=192.168.1.100 ansible_ssh_port=22 ansible_ssh_user=admin ansible_ssh_pass=password
   ```
3. 選擇伺服器群組
4. 點擊「儲存」

#### 測試 SSH 連線
1. 勾選要測試的 Inventory
2. 點擊「SSH連線測試」按鈕
3. 等待測試結果 (狀態會更新為 Connected/Unconnected)

### Playbook 管理

#### 建立 Playbook
1. 點擊 Playbooks 頁面的「新增 Playbook」按鈕
2. **基礎資訊頁籤**:
   - 輸入 Playbook 名稱
   - 選擇類型 (Machine/Other)
3. **Main 頁籤**:
   - 選擇目標類型 (Group/Host)
   - 從下拉選單選擇目標
   - 設定 Gather Facts
   - (選用) 設定 Working Directory
4. **Tasks 頁籤**:
   - 點擊「新增 Task」
   - 編輯 Task 內容 (YAML 格式)
   - 使用開關控制 Task 啟用/停用
5. 點擊「儲存並返回」

#### 執行 Playbook
1. 在 Playbooks 列表勾選要執行的項目
2. 點擊「執行」按鈕
3. 在彈出的對話框選擇 Inventory
4. 確認執行
5. 查看執行結果與日誌

### Galaxy Collections 管理

#### 安裝 Collection
1. 訪問 Galaxy Collections 頁面
2. **方法一 - 新增到 Requirements**:
   - 點擊「新增 Collection」卡片
   - 輸入 Collection 名稱 (例如: `community.docker`)
   - 輸入版本號 (選填，留空安裝最新版)
   - 點擊「新增」
   - 點擊 Collection 卡片上的「安裝」按鈕
3. **方法二 - 批次安裝**:
   - 在 Requirements.yml 頁籤管理多個 Collections
   - 點擊「全部安裝」一次安裝所有依賴

#### 檢查已安裝的 Collections
1. 切換到「已安裝 Collections」頁籤
2. 查看所有已安裝的 Collections、版本和路徑
3. 可點擊「卸載」移除不需要的 Collection

### 群組管理

#### 建立伺服器群組
1. 訪問 Inventory 群組管理頁面
2. 點擊「新增群組」按鈕
3. 輸入群組名稱 (例如: `production`, `testing`)
4. 點擊「新增」

#### 指派 Inventory 到群組
1. 編輯 Inventory
2. 從「群組」下拉選單選擇目標群組
3. 儲存變更

### AI 對話助手

#### 使用 AI 協助
1. 訪問 AI 對話頁面
2. 在輸入框輸入問題或需求
3. 範例問題:
   - "如何部署 Nginx？"
   - "幫我檢查 Playbook 的錯誤"
   - "如何安裝 Docker？"
4. 使用快速回覆按鈕 (Yes/No) 快速回應
5. AI 會提供建議和可執行的 Playbook 範例

---

## 🗄️ 資料庫管理

### Alembic 資料庫遷移

#### 查看目前版本
```bash
cd backend
.\venv\Scripts\Activate.ps1
alembic current
```

#### 查看遷移歷史
```bash
alembic history --verbose
```

#### 建立新的遷移檔案
```bash
# 修改 models 後自動生成遷移
alembic revision --autogenerate -m "Add new column to playbook"

# 檢查生成的遷移檔案
# backend/alembic/versions/xxxxx_add_new_column_to_playbook.py
```

#### 套用遷移
```bash
# 套用所有未執行的遷移
alembic upgrade head

# 套用到特定版本
alembic upgrade <revision_id>
```

#### 回滾遷移
```bash
# 回滾到上一版
alembic downgrade -1

# 回滾到特定版本
alembic downgrade <revision_id>

# 回滾到初始狀態
alembic downgrade base
```

### 重置資料庫
```bash
# 方法 1: 使用 Docker (推薦)
cd backend
docker-compose down -v
docker-compose up -d
alembic upgrade head
python seed_data.py

# 方法 2: 手動重置
# 登入 MySQL
docker exec -it ansible_hub_db mysql -u ansible_user -p

# 刪除並重建資料庫
DROP DATABASE ansible_hub;
CREATE DATABASE ansible_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 重新執行遷移
alembic upgrade head
python seed_data.py
```

---

## 📖 API 文件

### Swagger UI (推薦)
訪問 `http://localhost:8000/docs` 查看互動式 API 文件

### 主要端點

#### Inventories
- `GET /api/inventories` - 取得 Inventory 列表
- `POST /api/inventories` - 建立 Inventory
- `GET /api/inventories/{id}` - 取得單一 Inventory
- `PUT /api/inventories/{id}` - 更新 Inventory
- `DELETE /api/inventories/{id}` - 刪除 Inventory
- `POST /api/inventories/ssh-test` - SSH 連線測試

#### Playbooks
- `GET /api/playbooks` - 取得 Playbook 列表
- `POST /api/playbooks` - 建立 Playbook
- `GET /api/playbooks/{id}` - 取得單一 Playbook
- `PUT /api/playbooks/{id}` - 更新 Playbook
- `DELETE /api/playbooks/{id}` - 刪除 Playbook
- `POST /api/playbooks/execute` - 執行 Playbook

#### Groups
- `GET /api/groups` - 取得群組列表
- `POST /api/groups` - 建立群組
- `DELETE /api/groups/{id}` - 刪除群組

#### Galaxy Collections
- `GET /api/galaxy/collections` - 列出已安裝的 Collections
- `POST /api/galaxy/collections/install` - 安裝單一 Collection
- `DELETE /api/galaxy/collections/{name}` - 卸載 Collection
- `GET /api/galaxy/requirements` - 取得 requirements.yml
- `POST /api/galaxy/requirements` - 更新 requirements.yml
- `POST /api/galaxy/requirements/install` - 安裝 requirements.yml

#### AI Chat
- `POST /api/ai/messages` - 發送訊息給 AI
- `GET /api/ai/conversations/{id}` - 取得對話歷史

詳細 API 規格請參考 `frontend/docs/api.md`

---

## 🛠️ 開發指南

### 後端開發

#### 新增 API 端點
1. 在 `backend/app/routers/` 建立或編輯路由檔案
2. 定義 Pydantic Schema 於 `backend/app/schemas/`
3. 更新資料庫模型於 `backend/app/models/__init__.py`
4. 建立 Alembic 遷移: `alembic revision --autogenerate -m "描述"`
5. 套用遷移: `alembic upgrade head`

#### 程式碼風格
```bash
# 使用 Black 格式化
pip install black
black backend/app

# 使用 isort 排序 imports
pip install isort
isort backend/app
```

### 前端開發

#### 新增頁面
1. 在 `frontend/src/views/` 建立 Vue 元件
2. 在 `frontend/src/router/index.ts` 註冊路由
3. 在 `frontend/src/api/` 建立對應的 API 函式

#### 程式碼風格
```bash
# ESLint 檢查
npm run lint

# Prettier 格式化
npm run format
```

#### 建置生產版本
```bash
npm run build

# 預覽建置結果
npm run preview
```

---

## 📁 專案結構

```
Ansible_Auto_Control_Hub/
├── backend/                      # 後端專案
│   ├── alembic/                  # 資料庫遷移檔案
│   │   ├── versions/             # 遷移版本
│   │   └── env.py                # Alembic 配置
│   ├── ansible/                  # Ansible 相關檔案
│   │   ├── playbooks/            # Playbook 暫存目錄
│   │   └── requirements.yml      # Galaxy Collections 配置
│   ├── app/
│   │   ├── models/               # SQLAlchemy 模型
│   │   │   └── __init__.py       # Group, Host, Inventory, Playbook, Task
│   │   ├── schemas/              # Pydantic Schemas
│   │   │   ├── group.py
│   │   │   ├── host.py
│   │   │   ├── inventory.py
│   │   │   └── playbook.py
│   │   ├── routers/              # API 路由
│   │   │   ├── inventories.py   # Inventory CRUD + SSH 測試
│   │   │   ├── playbooks.py     # Playbook CRUD + 執行
│   │   │   ├── groups.py         # 群組管理
│   │   │   ├── hosts.py          # Host 管理
│   │   │   ├── galaxy.py         # Galaxy Collections
│   │   │   └── ai_chat.py        # AI 對話
│   │   ├── database.py           # 資料庫連線
│   │   └── main.py               # FastAPI 應用程式
│   ├── alembic.ini               # Alembic 配置
│   ├── docker-compose.yml        # MySQL 容器配置
│   ├── requirements.txt          # Python 依賴
│   ├── seed_data.py              # 測試資料初始化
│   └── .env                      # 環境變數
│
├── frontend/                     # 前端專案
│   ├── src/
│   │   ├── api/                  # API 客戶端
│   │   │   ├── client.ts         # Axios 配置
│   │   │   ├── inventory.ts      # Inventory API
│   │   │   ├── playbook.ts       # Playbook API
│   │   │   ├── group.ts          # Group API
│   │   │   ├── galaxy.ts         # Galaxy API
│   │   │   └── ai.ts             # AI API
│   │   ├── components/           # Vue 元件
│   │   │   └── AppLayout.vue     # 主要版面佈局
│   │   ├── views/                # 頁面元件
│   │   │   ├── InventoriesView.vue        # Inventory 列表
│   │   │   ├── InventoryDetailView.vue    # Inventory 新增/編輯
│   │   │   ├── InventoryGroupsView.vue    # 群組管理
│   │   │   ├── PlaybookView.vue           # Playbook 列表
│   │   │   ├── PlaybookCreateView.vue     # Playbook 新增
│   │   │   ├── PlaybookEditView.vue       # Playbook 編輯
│   │   │   ├── GalaxyView.vue             # Galaxy Collections
│   │   │   └── AITalkView.vue             # AI 對話
│   │   ├── router/               # Vue Router
│   │   │   └── index.ts
│   │   ├── assets/               # 靜態資源
│   │   ├── App.vue               # 根元件
│   │   └── main.ts               # 應用程式入口
│   ├── docs/
│   │   └── api.md                # API 規格文件
│   ├── package.json              # Node.js 依賴
│   ├── vite.config.ts            # Vite 配置
│   ├── tsconfig.json             # TypeScript 配置
│   └── .env                      # 環境變數
│
└── README.md                     # 本文件
```

---

## 🔧 故障排除

### 後端問題

#### 1. 資料庫連線失敗
```bash
# 檢查 MySQL 容器狀態
docker ps

# 查看容器日誌
docker logs ansible_hub_db

# 重啟容器
docker-compose restart
```

#### 2. Alembic 遷移失敗
```bash
# 檢查目前版本
alembic current

# 查看遷移歷史
alembic history

# 強制標記為最新版 (謹慎使用)
alembic stamp head
```

#### 3. Ansible 執行失敗 (Windows)
```bash
# 確認 WSL 中 Ansible 已安裝
wsl ansible --version

# 測試 WSL 執行
wsl ansible-playbook --version

# 檢查 WSL 路徑轉換
wsl ls /mnt/c/Users/...
```

### 前端問題

#### 1. API 呼叫失敗
- 確認後端服務運行: `http://localhost:8000/health`
- 檢查瀏覽器 Console 錯誤訊息
- 確認 CORS 設定正確

#### 2. 建置失敗
```bash
# 清除快取
npm clean-cache --force

# 刪除 node_modules 重新安裝
rm -rf node_modules package-lock.json
npm install
```

---

## 📝 版本歷史

### v1.0.0 (2025-11-12)
- ✅ 完整的 Inventory 管理 (CRUD + SSH 測試)
- ✅ Playbook 視覺化編輯與執行
- ✅ Galaxy Collections 管理
- ✅ 伺服器群組管理
- ✅ AI 對話助手
- ✅ Alembic 資料庫遷移支援
- ✅ Docker + WSL 整合

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 LICENSE 檔案

---

## 👥 聯絡資訊

- 專案負責人: Edward
- GitHub: [@Edwarddev0723](https://github.com/Edwarddev0723)
- 專案連結: [https://github.com/Edwarddev0723/Ansible_Auto_Control_Hub](https://github.com/Edwarddev0723/Ansible_Auto_Control_Hub)

---

## 🙏 致謝

- [FastAPI](https://fastapi.tiangolo.com/) - 現代化的 Python Web 框架
- [Vue.js](https://vuejs.org/) - 漸進式 JavaScript 框架
- [Ansible](https://www.ansible.com/) - 強大的自動化工具
- [Tailwind CSS](https://tailwindcss.com/) - 實用優先的 CSS 框架







