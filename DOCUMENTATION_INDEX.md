# 📚 文件與腳本索引

## 🎯 快速導航

### 新手必讀 ⭐
1. **[快速參考卡](docs/QUICK_REFERENCE.md)** - 一頁式速查表
2. **[實用指南](docs/OLLMCP_USAGE.md)** - 詳細使用說明
3. **[更新通知](UPDATE_NOTES.md)** - 腳本更新說明

### 完整文件
4. **[Ansible + MCP 專案 README](README_ANSIBLE_MCP.md)** - 專案總覽
5. **[整合完成總結](docs/COMPLETION_SUMMARY.md)** - 實作狀態
6. **[問題修復說明](docs/MCP_FIX_SUMMARY.md)** - 技術細節

### 進階參考
7. **[完整整合指南](docs/OLLMCP_GUIDE.md)** - 深入說明
8. **[故障排除](docs/OLLMCP_TROUBLESHOOTING.md)** - 問題解決

---

## 📁 檔案清單

### 🚀 啟動與測試腳本

| 檔案 | 用途 | 執行方式 |
|------|------|----------|
| `start-ollmcp.sh` | ollmcp 啟動腳本（主要） | `./start-ollmcp.sh` |
| `test-project-registration.sh` | 測試專案註冊功能 | `./test-project-registration.sh` |
| `test-ollmcp.sh` | 測試 3 種連接方式 | `./test-ollmcp.sh` |
| `diagnose-and-fix.sh` | 自動診斷與修復 | `./diagnose-and-fix.sh` |

### 📖 核心文件（依閱讀順序）

#### 入門級（5-15 分鐘）
| 檔案 | 說明 | 適合對象 |
|------|------|----------|
| `docs/QUICK_REFERENCE.md` | 快速參考卡 | 所有使用者 ⭐ |
| `UPDATE_NOTES.md` | 腳本更新說明 | 首次使用者 ⭐ |
| `docs/OLLMCP_USAGE.md` | 實用使用指南 | 日常使用者 ⭐ |

#### 中級（20-30 分鐘）
| 檔案 | 說明 | 適合對象 |
|------|------|----------|
| `README_ANSIBLE_MCP.md` | Ansible + MCP 專案總覽 | 專案管理者 |
| `docs/COMPLETION_SUMMARY.md` | 整合完成總結 | 技術人員 |
| `docs/MCP_FIX_SUMMARY.md` | 問題修復詳細說明 | 除錯人員 |

#### 進階級（40-60 分鐘）
| 檔案 | 說明 | 適合對象 |
|------|------|----------|
| `docs/OLLMCP_GUIDE.md` | 完整整合指南（23 頁） | 深入學習者 |
| `docs/OLLMCP_TROUBLESHOOTING.md` | 詳細故障排除 | 系統管理員 |
| `docs/MCP_OLLAMA_INTEGRATION.md` | MCP Ollama 整合原理 | 開發人員 |

#### 參考文件
| 檔案 | 說明 | 用途 |
|------|------|------|
| `docs/MCP_QUICK_REFERENCE.md` | MCP 快速參考 | 速查 |
| `docs/OLLMCP_QUICK_REF.md` | ollmcp 快速參考 | 速查 |

---

## 🎓 學習路徑建議

### 路徑 1: 快速上手（總時間：15 分鐘）
```
1. docs/QUICK_REFERENCE.md      (5 分鐘)   - 看一遍常用指令
2. UPDATE_NOTES.md              (5 分鐘)   - 了解腳本更新
3. 執行 ./start-ollmcp.sh       (5 分鐘)   - 實際操作
```

### 路徑 2: 日常使用（總時間：30 分鐘）
```
1. docs/QUICK_REFERENCE.md      (5 分鐘)   - 快速參考
2. docs/OLLMCP_USAGE.md         (15 分鐘)  - 詳細使用方式
3. UPDATE_NOTES.md              (5 分鐘)   - 了解配置
4. 實際操作練習                  (5 分鐘)   - 執行 3-5 個指令
```

### 路徑 3: 完整學習（總時間：90 分鐘）
```
1. README_ANSIBLE_MCP.md        (20 分鐘)  - 專案概覽
2. docs/COMPLETION_SUMMARY.md   (15 分鐘)  - 實作狀態
3. docs/OLLMCP_USAGE.md         (15 分鐘)  - 使用方式
4. docs/MCP_FIX_SUMMARY.md      (15 分鐘)  - 技術細節
5. docs/OLLMCP_GUIDE.md         (20 分鐘)  - 深入原理
6. 實際操作練習                  (5 分鐘)   - 各種場景測試
```

### 路徑 4: 問題解決（依需求）
```
遇到問題時：
1. docs/QUICK_REFERENCE.md       - 檢查常見錯誤
2. docs/OLLMCP_TROUBLESHOOTING.md - 詳細故障排除
3. UPDATE_NOTES.md               - 確認配置正確
4. 使用 diagnose-and-fix.sh     - 自動診斷
```

---

## 📊 文件內容對照表

| 主題 | 快速參考 | 詳細說明 | 問題解決 |
|------|----------|----------|----------|
| **安裝設置** | QUICK_REFERENCE | OLLMCP_GUIDE | OLLMCP_TROUBLESHOOTING |
| **日常使用** | QUICK_REFERENCE | OLLMCP_USAGE | UPDATE_NOTES |
| **技術原理** | MCP_QUICK_REFERENCE | MCP_FIX_SUMMARY | OLLMCP_TROUBLESHOOTING |
| **專案管理** | QUICK_REFERENCE | COMPLETION_SUMMARY | UPDATE_NOTES |
| **工具列表** | QUICK_REFERENCE | README_ANSIBLE_MCP | OLLMCP_GUIDE |

---

## 🔍 按需求查找

### 我想要...

#### 快速開始使用
→ `docs/QUICK_REFERENCE.md` + `./start-ollmcp.sh`

#### 了解如何執行 playbook
→ `docs/OLLMCP_USAGE.md` (方式 1、2、3)

#### 解決 "No tools enabled" 錯誤
→ `docs/OLLMCP_TROUBLESHOOTING.md` + `docs/MCP_FIX_SUMMARY.md`

#### 解決 "No project specified" 錯誤
→ `UPDATE_NOTES.md` (已知問題與解決方案)

#### 了解腳本做了什麼
→ `UPDATE_NOTES.md` (更新內容)

#### 查看所有可用工具
→ `README_ANSIBLE_MCP.md` (38 個工具列表)

#### 學習最佳實踐
→ `docs/OLLMCP_USAGE.md` (提示與技巧)

#### 深入理解 MCP 架構
→ `docs/OLLMCP_GUIDE.md` + `docs/MCP_OLLAMA_INTEGRATION.md`

#### 自動化部署流程
→ `docs/COMPLETION_SUMMARY.md` (Ansible 專案整合)

#### 檢查系統狀態
→ `./diagnose-and-fix.sh`

---

## 🎯 文件特點對比

| 文件 | 長度 | 深度 | 實用性 | 適合場景 |
|------|------|------|--------|----------|
| QUICK_REFERENCE | 短 ⭐ | 淺 | 高 ⭐⭐⭐ | 日常速查 |
| OLLMCP_USAGE | 中 | 中 | 高 ⭐⭐⭐ | 學習使用 |
| UPDATE_NOTES | 中 | 中 | 高 ⭐⭐ | 了解更新 |
| README_ANSIBLE_MCP | 長 | 中 | 中 ⭐⭐ | 專案概覽 |
| COMPLETION_SUMMARY | 長 | 中 | 中 ⭐⭐ | 技術總結 |
| MCP_FIX_SUMMARY | 長 | 深 | 中 ⭐ | 技術細節 |
| OLLMCP_GUIDE | 很長 | 深 | 中 ⭐ | 深入學習 |
| OLLMCP_TROUBLESHOOTING | 中 | 深 | 高 ⭐⭐⭐ | 問題解決 |

---

## 💾 檔案大小與更新時間

```bash
# 查看所有文件大小
ls -lh docs/*.md *.md | awk '{print $9, $5}'

# 查看最近更新的文件
ls -lt docs/*.md *.md | head -10
```

**最後更新**: 2025-10-16  
**總文件數**: 15 個（12 個文件 + 3 個腳本）  
**總頁數**: 約 150 頁（如果印出來）  
**建議閱讀時間**: 15 分鐘（快速）到 90 分鐘（完整）

---

## 📌 快捷方式

### 在專案目錄下執行

```bash
# 查看快速參考
cat docs/QUICK_REFERENCE.md | less

# 查看使用指南
cat docs/OLLMCP_USAGE.md | less

# 查看更新說明
cat UPDATE_NOTES.md | less

# 查看專案 README
cat README_ANSIBLE_MCP.md | less

# 在瀏覽器中打開（macOS）
open docs/QUICK_REFERENCE.md  # 使用預設 Markdown 查看器
```

### 搜尋特定主題

```bash
# 搜尋所有文件中的特定關鍵字
grep -r "playbook" docs/*.md

# 搜尋錯誤訊息解決方案
grep -r "No tools enabled" docs/*.md

# 搜尋指令範例
grep -r "執行 playbook" docs/*.md
```

---

## 🔗 相關資源

### 外部連結
- [Ollama 官網](https://ollama.ai/)
- [ollmcp GitHub](https://github.com/chrishayuk/ollmcp)
- [MCP 協議](https://modelcontextprotocol.io/)
- [Ansible 文件](https://docs.ansible.com/)

### 內部專案文件
- `ansible_projects/infra_owner_deploy/README.md` - Ansible 專案說明
- `ansible_projects/infra_owner_deploy/DEPLOYMENT_SUMMARY.md` - 部署總結
- `mcp-ansible/README.md` - MCP Server 說明

---

## ✅ 文件完整性檢查

執行以下命令確認所有文件都存在：

```bash
cd /Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub

# 檢查必需文件
for file in \
  docs/QUICK_REFERENCE.md \
  docs/OLLMCP_USAGE.md \
  UPDATE_NOTES.md \
  README_ANSIBLE_MCP.md \
  start-ollmcp.sh
do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (缺失)"
  fi
done
```

---

**維護者**: GitHub Copilot + User  
**建立日期**: 2025-10-16  
**狀態**: ✅ 完整
