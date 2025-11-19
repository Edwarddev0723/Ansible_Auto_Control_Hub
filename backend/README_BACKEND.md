# Ansible Auto Control Hub - 後端 API 開發指南

## 已完成的設置

### 1. 虛擬環境和依賴套件
- ✅ 建立 Python 虛擬環境 (venv)
- ✅ 安裝 FastAPI, SQLAlchemy, Alembic, PyMySQL 等套件
- ✅ 建立 requirements.txt

### 2. Docker MySQL 配置
- ✅ 建立 docker-compose.yml
- ✅ MySQL 8.0 配置
  - 資料庫名稱: ansible_hub
  - 使用者: ansible_user
  - 密碼: ansible_pass
  - Port: 3306

### 3. 環境變數
- ✅ 建立 .env 檔案
- DATABASE_URL 已配置

## 需要建立的檔案

請依照以下順序手動建立檔案或使用 IDE：

### 資料庫模型 (app/models/__init__.py)
需要的資料表：
1. **playbooks** - Playbook 主表
2. **tasks** - Task 任務表
3. **playbook_extra_fields** - 額外欄位表
4. **inventories** - Inventory 清單表
5. **groups** - Group 群組表
6. **hosts** - Host 主機表

### Pydantic Schemas (app/schemas/)
- playbook.py
- inventory.py  
- group.py
- host.py

### API Routes (app/routers/)
- playbooks.py
- inventories.py
- groups.py
- hosts.py

### CRUD Operations (app/crud/)
- playbook.py
- inventory.py
- group.py
- host.py

### 主應用程式
- app/main.py

## API 端點設計

### Playbooks
- GET /api/playbooks - 列出所有 playbooks
- POST /api/playbooks - 建立新 playbook
- GET /api/playbooks/{id} - 取得單一 playbook
- PUT /api/playbooks/{id} - 更新 playbook
- DELETE /api/playbooks/{id} - 刪除 playbook

### Inventories
- GET /api/inventories - 列出所有 inventories
- POST /api/inventories - 建立新 inventory
- GET /api/inventories/{id} - 取得單一 inventory
- PUT /api/inventories/{id} - 更新 inventory
- DELETE /api/inventories/{id} - 刪除 inventory

### Groups
- GET /api/groups - 取得所有群組列表
- POST /api/groups - 建立新群組

### Hosts  
- GET /api/hosts - 取得所有主機列表
- POST /api/hosts - 建立新主機

## 啟動步驟

1. 啟動 MySQL:
\\\ash
docker-compose up -d
\\\

2. 初始化 Alembic:
\\\ash
.\venv\Scripts\Activate.ps1
alembic init alembic
\\\

3. 建立初始 migration:
\\\ash
alembic revision --autogenerate -m \"Initial migration\"
\\\

4. 執行 migration:
\\\ash
alembic upgrade head
\\\

5. 啟動 FastAPI 伺服器:
\\\ash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\\\

## 初始測試資料

建議在 migration 或啟動腳本中加入：
- 4個預設 groups: webservers, databases, loadbalancers, all
- 5個預設 hosts: 192.168.1.10-12, server1.example.com, server2.example.com
- 2-3個範例 playbooks
- 2個範例 inventories

## 前端整合

前端需要更新以下檔案來呼叫 API：
- PlaybookCreateView.vue
- PlaybookEditView.vue
- PlaybookView.vue
- InventoriesView.vue
- InventoryDetailView.vue

改用 fetch 或 axios 呼叫 http://localhost:8000/api/* 端點

