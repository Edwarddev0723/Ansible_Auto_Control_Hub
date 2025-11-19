# 🚀 ollmcp 快速參考卡

## 一鍵啟動

```bash
./start-ollmcp.sh
```

---

## 🎯 自然語言範例

### 部署操作
```
部署應用程式到 web 伺服器
部署到埠號 8080
驗證 playbook 語法
執行乾運行測試
```

### 狀態檢查
```
檢查 Docker 服務狀態
測試 HTTP 端點
顯示所有主機
ping web 伺服器
```

### 管理操作
```
查看部署日誌
顯示容器日誌
停止服務
重啟服務
```

---

## ⌨️ 互動式指令

| 指令 | 快捷鍵 | 說明 |
|------|--------|------|
| `help` | `h` | 顯示幫助 |
| `tools` | `t` | 管理工具 |
| `model` | `m` | 切換模型 |
| `model-config` | `mc` | 進階配置 |
| `thinking-mode` | `tm` | 思考模式 |
| `show-metrics` | `sm` | 效能指標 |
| `human-in-loop` | `hil` | HIL 確認 |
| `save-config` | `sc` | 儲存配置 |
| `reload-servers` | `rs` | 熱重載 |
| `clear` | `cc` | 清除歷史 |
| `quit` | `q` | 退出 |

---

## 🛠️ 工具選擇快捷鍵

在工具選擇介面（按 `t`）：

- **數字**: `1,3,5` - 切換指定工具
- **範圍**: `5-8` - 切換連續工具
- **伺服器**: `S1` - 切換整個伺服器
- **全部**: `a` - 啟用所有
- **無**: `n` - 停用所有
- **描述**: `d` - 顯示描述
- **儲存**: `s` - 儲存變更
- **取消**: `q` - 取消變更

---

## ⚙️ 推薦模型配置

### Ansible 部署專用
```
System Prompt: "你是 Ansible 自動化專家..."
Temperature: 0.3
Top P: 0.5
Seed: 42
Context: 4096
```

輸入 `mc` 進入配置介面

---

## 🧑‍💻 Human-in-the-Loop

每次工具執行前都會詢問：
- **`a`** - 批准執行
- **`s`** - 跳過
- **`d`** - 停用 HIL
- **`q`** - 取消

輸入 `hil` 切換 HIL 開關

---

## 📊 效能指標

輸入 `sm` 顯示：
- Total Duration
- Token Counts
- Generation Rates

---

## 💾 配置管理

```bash
# 儲存配置
save-config ansible-deploy

# 載入配置
load-config ansible-deploy

# 預設位置
~/.config/ollmcp/config.json
```

---

## 🔧 快速除錯

### Ollama 無回應
```bash
pkill ollama
ollama serve
```

### 重新安裝 ollmcp
```bash
pip install --upgrade ollmcp
```

### 檢查環境變數
```bash
echo $MCP_ANSIBLE_PROJECT_ROOT
```

### 使用啟動腳本
```bash
./start-ollmcp.sh  # 自動設定一切
```

---

## 📚 文件連結

- **完整指南**: `docs/OLLMCP_GUIDE.md`
- **部署指南**: `ansible_projects/infra_owner_deploy/README.md`
- **API 規格**: `specs/002-mcp-ansible-infra/contracts/mcp-tool-api.json`

---

## 🎓 快速開始流程

1. ✅ 執行 `./start-ollmcp.sh`
2. ✅ 等待 ollmcp TUI 啟動
3. ✅ 輸入自然語言指令
4. ✅ 按 `a` 批准工具執行（HIL）
5. ✅ 查看結果和指標

---

**提示**: 按 `Tab` 鍵使用自動完成！

**更新日期**: 2025-10-16
