# Git Configuration Guide

## 📋 概述

本專案已配置完整的 `.gitignore` 和 `.gitattributes` 文件，確保正確的版本控制和跨平台協作。

---

## 📁 文件結構

```
Ansible_Auto_Control_Hub/
├── .gitignore              # 根目錄：通用規則
├── .gitattributes          # 行尾符號和文件類型設定
├── backend/
│   ├── .gitignore          # Python/FastAPI 專用規則
│   └── .env.example        # 環境變數範例
└── frontend/
    ├── .gitignore          # Vue/TypeScript 專用規則
    └── .env.example        # 環境變數範例
```

---

## 🚫 已忽略的文件類型

### 根目錄 (`.gitignore`)

**作業系統文件：**
- macOS: `.DS_Store`, `._*`
- Windows: `Thumbs.db`, `Desktop.ini`, `$RECYCLE_BIN/`
- Linux: `*~`, `.directory`, `.Trash-*`

**IDE 配置：**
- VSCode: `.vscode/*` (保留部分設定檔)
- JetBrains: `.idea/`, `*.iml`
- Sublime: `*.sublime-project`, `*.sublime-workspace`

**敏感文件：**
- `.env.local`, `.env.*.local`
- `*.key`, `*.pem`, `*.cert`

**臨時文件：**
- 日誌: `logs/`, `*.log`
- 快取: `.cache/`, `tmp/`, `temp/`
- 備份: `*.bak`, `*.swp`

---

### 後端 (`backend/.gitignore`)

**Python 相關：**
- `__pycache__/`, `*.pyc`, `*.pyo`
- `.pytest_cache/`, `.coverage`
- `*.egg-info/`, `dist/`, `build/`

**虛擬環境：**
- `venv/`, `env/`, `.venv/`

**資料庫：**
- `*.db`, `*.sqlite`, `*.sqlite3`
- `*.sql` (備份文件)

**環境變數：**
- `.env` (實際配置文件，不提交)
- 保留 `.env.example` (範例文件，要提交)

**FastAPI/Uvicorn：**
- `*.log`, `logs/`

---

### 前端 (`frontend/.gitignore`)

**依賴套件：**
- `node_modules/`
- `package-lock.json` (已忽略，因團隊可能使用不同套件管理器)

**建置輸出：**
- `dist/`, `dist-ssr/`
- `.cache/`, `.vite/`

**測試：**
- `coverage/`, `.nyc_output/`
- `/cypress/videos/`, `/cypress/screenshots/`

**TypeScript：**
- `*.tsbuildinfo`, `tsconfig.tsbuildinfo`

**環境變數：**
- `.env`, `.env.local`, `.env.*.local`
- 保留 `.env.example`

**IDE：**
- `.vscode/*` (保留 `extensions.json` 等)
- `.idea/`, `*.suo`, `*.njsproj`

---

## 🔧 `.gitattributes` 配置

### 行尾符號設定

**Unix 格式 (LF)：**
- Python: `*.py`
- JavaScript/TypeScript: `*.js`, `*.ts`, `*.vue`
- JSON/YAML: `*.json`, `*.yaml`
- HTML/CSS: `*.html`, `*.css`
- Shell: `*.sh`, `*.bash`
- Markdown: `*.md`

**Windows 格式 (CRLF)：**
- Windows 腳本: `*.bat`, `*.cmd`, `*.ps1`

**自動檢測：**
- 其他文件類型: `* text=auto`

### 二進位文件

明確標記為 binary，避免 Git 嘗試合併：
- 圖片: `*.png`, `*.jpg`, `*.svg`
- 字型: `*.woff`, `*.ttf`
- 壓縮檔: `*.zip`, `*.tar`, `*.gz`
- 文件: `*.pdf`, `*.docx`
- 執行檔: `*.exe`, `*.dll`, `*.so`

---

## 📝 環境變數配置

### 後端 (`.env.example`)

包含以下配置項目：

**資料庫：**
```bash
DB_USER=ansible_user
DB_PASSWORD=ansible_pass
DB_HOST=localhost
DB_PORT=3307
DB_NAME=ansible_hub
```

**應用程式：**
```bash
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

**AI/MCP Server：**
```bash
MCP_SERVER_URL=http://localhost:3001/api/chat
MCP_HEALTH_URL=http://localhost:3001/health
```

**SSH：**
```bash
DEFAULT_SSH_USER=root
SSH_TIMEOUT=5
```

### 前端 (`.env.example`)

**API 配置：**
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

**功能開關：**
```bash
VITE_ENABLE_AI_CHAT=true
VITE_ENABLE_SSH_TEST=true
```

---

## 🚀 使用指南

### 1. 初始設定

**複製環境變數範例：**

```bash
# 後端
cd backend
cp .env.example .env
# 編輯 .env 填入實際配置

# 前端
cd frontend
cp .env.example .env
# 編輯 .env 填入實際配置
```

### 2. 檢查 Git 狀態

```bash
# 查看哪些文件被忽略
git status --ignored

# 查看哪些文件會被提交
git status

# 查看特定文件是否被忽略
git check-ignore -v filename
```

### 3. 強制添加被忽略的文件 (謹慎使用)

```bash
# 如果確實需要提交某個被忽略的文件
git add -f path/to/file
```

### 4. 更新 .gitignore 後清理

```bash
# 移除所有被忽略但已追蹤的文件
git rm -r --cached .
git add .
git commit -m "chore: update .gitignore and remove ignored files"
```

---

## ⚠️ 重要提醒

### ✅ 應該提交的文件

- `.gitignore`, `.gitattributes`
- `.env.example` (範例文件)
- 所有原始碼文件
- 配置文件範例
- README 和文檔
- 測試文件

### ❌ 不應該提交的文件

- `.env` (包含敏感資訊)
- `node_modules/` (可重新安裝)
- `venv/`, `__pycache__/` (可重新建立)
- `dist/`, `build/` (建置輸出)
- IDE 特定配置 (個人偏好)
- 日誌和臨時文件
- 資料庫文件 (`.db`, `.sqlite`)
- SSH 金鑰和憑證 (`.key`, `.pem`)

---

## 🔍 檢查清單

### 提交前檢查

- [ ] 確認 `.env` 沒有被提交
- [ ] 檢查沒有敏感資訊 (密碼、API keys)
- [ ] 確認 `node_modules/` 和 `venv/` 被忽略
- [ ] 檢查沒有個人 IDE 配置被提交
- [ ] 確認建置輸出 (`dist/`) 被忽略
- [ ] 驗證 `.env.example` 已更新且不含敏感資訊

### 定期維護

- [ ] 當添加新的檔案類型時更新 `.gitignore`
- [ ] 保持 `.env.example` 與 `.env` 同步 (移除敏感值)
- [ ] 定期清理未追蹤的文件: `git clean -fd`
- [ ] 檢查倉庫大小，移除誤提交的大文件

---

## 📚 參考資源

- [GitHub .gitignore Templates](https://github.com/github/gitignore)
- [Git Documentation - gitignore](https://git-scm.com/docs/gitignore)
- [Git Documentation - gitattributes](https://git-scm.com/docs/gitattributes)

---

## 🛠 故障排除

### 問題：文件仍被追蹤即使已在 .gitignore 中

**解決方案：**
```bash
# 從 Git 索引移除文件但保留本地副本
git rm --cached path/to/file

# 移除整個目錄
git rm -r --cached path/to/directory

# 提交變更
git commit -m "chore: remove tracked files that should be ignored"
```

### 問題：行尾符號警告 (LF/CRLF)

已通過 `.gitattributes` 配置處理，無需擔心。Git 會自動轉換：
- Windows: 檢出時 CRLF，提交時 LF
- macOS/Linux: 保持 LF

### 問題：意外提交了敏感文件

**立即處理：**
```bash
# 1. 從歷史中移除文件 (需要重寫歷史)
git filter-branch --tree-filter 'rm -f path/to/sensitive/file' HEAD

# 2. 或使用 BFG Repo-Cleaner (更快)
bfg --delete-files sensitive-file.txt

# 3. 強制推送 (警告：會影響其他協作者)
git push --force
```

**更新密碼/API Keys：** 一旦敏感資訊被提交，假設它已洩露，立即更換所有憑證。

---

## 🎯 最佳實踐

1. **在專案開始時設定 .gitignore** - 避免誤提交
2. **使用 .env.example** - 團隊成員知道需要哪些環境變數
3. **定期審查 git status** - 提交前檢查
4. **分層次的 .gitignore** - 根目錄 + 子目錄特定規則
5. **文檔化特殊規則** - 如果忽略了通常會提交的文件
6. **團隊協作** - 確保所有成員理解 .gitignore 規則
7. **自動化檢查** - 使用 pre-commit hooks 防止敏感文件提交

---

**最後更新：** 2025-11-12  
**維護者：** Development Team
