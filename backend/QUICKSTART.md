# Ansible Auto Control Hub - Backend 快速啟動指南

## 📋 已完成的檔案

### ✅ 核心配置
- `app/database.py` - SQLAlchemy 資料庫連接
- `app/models/__init__.py` - 資料模型 (Playbook, Task, Inventory, Group, Host 等)
- `app/main.py` - FastAPI 主應用程式
- `docker-compose.yml` - MySQL 容器
- `.env` - 環境變數
- `requirements.txt` - Python 依賴

### ✅ Schemas (Pydantic 驗證)
- `app/schemas/inventory.py` - Inventory 請求/響應模型
- `app/schemas/playbook.py` - Playbook 請求/響應模型
- `app/schemas/group.py` - Group 模型
- `app/schemas/host.py` - Host 模型

### ✅ Routers (API 端點)
- `app/routers/inventories.py` - Inventory CRUD API
- `app/routers/playbooks.py` - Playbook CRUD + Execute API
- `app/routers/groups.py` - Groups API
- `app/routers/hosts.py` - Hosts API

### ✅ 資料初始化
- `seed_data.py` - 種子資料腳本

---

## 🚀 啟動步驟

### 1. 啟動 MySQL 容器
```powershell
docker-compose up -d
```

**確認容器運行:**
```powershell
docker ps
```

應該看到 `ansible_hub_mysql` 容器在運行

---

### 2. 建立資料表
FastAPI 會在啟動時自動建立資料表 (在 `main.py` 中已配置)

---

### 3. 初始化種子資料
```powershell
python seed_data.py
```

**預期輸出:**
```
開始初始化資料庫...
--------------------------------------------------
✅ 已新增 4 個 Groups
✅ 已新增 5 個 Hosts
✅ 已新增 2 個 Inventories
✅ 已新增 2 個 Playbooks
--------------------------------------------------
✅ 資料庫初始化完成！
```

---

### 4. 啟動 FastAPI 伺服器
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**預期輸出:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🧪 測試 API

### 方法 1: 使用瀏覽器訪問 Swagger UI
```
http://localhost:8000/docs
```

這裡可以看到所有 API 端點並直接測試

---

### 方法 2: 使用 PowerShell 測試

#### 測試健康檢查
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

#### 獲取 Groups 列表
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/groups
```

**預期輸出:**
```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "webservers"},
    {"id": 2, "name": "databases"},
    {"id": 3, "name": "loadbalancers"},
    {"id": 4, "name": "all"}
  ]
}
```

#### 獲取 Hosts 列表
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/hosts
```

#### 獲取 Inventories 列表
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/inventories
```

#### 獲取 Playbooks 列表
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/playbooks
```

#### 獲取單一 Playbook 詳細資料
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/playbooks/1
```

---

## 📚 API 端點總覽

### Inventories
- `GET /api/inventories` - 獲取列表 (支援搜尋、分頁)
- `GET /api/inventories/{id}` - 獲取單一項目
- `POST /api/inventories` - 創建
- `PUT /api/inventories/{id}` - 更新
- `DELETE /api/inventories/{id}` - 刪除

### Playbooks
- `GET /api/playbooks` - 獲取列表 (支援搜尋、分頁、類型篩選)
- `GET /api/playbooks/{id}` - 獲取單一項目 (含 tasks)
- `POST /api/playbooks` - 創建
- `PUT /api/playbooks/{id}` - 更新
- `DELETE /api/playbooks/{id}` - 刪除
- `POST /api/playbooks/execute` - 執行 Playbooks

### Groups
- `GET /api/groups` - 獲取所有 Groups
- `POST /api/groups` - 新增 Group

### Hosts
- `GET /api/hosts` - 獲取所有 Hosts
- `POST /api/hosts` - 新增 Host

---

## 🔧 資料庫管理

### 連接到 MySQL 容器
```powershell
docker exec -it ansible_hub_mysql mysql -u ansible_user -p
```

密碼: `ansible_pass`

### 查看資料表
```sql
USE ansible_hub;
SHOW TABLES;
```

### 查看資料
```sql
SELECT * FROM groups;
SELECT * FROM hosts;
SELECT * FROM inventories;
SELECT * FROM playbooks;
SELECT * FROM tasks;
```

---

## 🛑 停止服務

### 停止 FastAPI
按 `CTRL + C`

### 停止 MySQL 容器
```powershell
docker-compose down
```

### 完全移除 (包含資料)
```powershell
docker-compose down -v
```

---

## ⚠️ 常見問題

### 1. 虛擬環境未啟動
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. MySQL 容器無法啟動
確認 Docker Desktop 正在運行

### 3. 端口已被佔用
修改 `docker-compose.yml` 中的端口映射:
```yaml
ports:
  - "3307:3306"  # 改用 3307
```

然後更新 `.env`:
```
DATABASE_URL=mysql+pymysql://ansible_user:ansible_pass@localhost:3307/ansible_hub
```

### 4. 資料表不存在
手動建立:
```powershell
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine); print('Tables created!')"
```

---

## 📝 下一步

### 前端整合
1. 在 `frontend/src/api/` 建立 API 客戶端
2. 使用 Axios 調用後端 API
3. 替換 mock 資料為真實 API 調用

### 功能增強
- [ ] 實作 SSH 連線測試
- [ ] 實作 Playbook 實際執行
- [ ] 實作 AI 對話功能
- [ ] 添加使用者認證 (JWT)
- [ ] 添加錯誤日誌
- [ ] 添加單元測試

---

## 🎉 完成！

您的 FastAPI 後端已經完全設置好了。所有 CRUD 操作都已實現，可以開始與前端整合！
