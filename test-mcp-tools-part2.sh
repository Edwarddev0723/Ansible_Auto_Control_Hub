#!/bin/bash
# 完整的 MCP Ansible 工具測試腳本 - 剩餘部分
# 此文件包含第5-8組測試，應該附加到主測試腳本中

# ============================================================
# 5. 執行與管理工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        第五組：執行與管理工具測試 (3個)               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 15: ansible-remote-command (ansible-ad-hoc)
test_tool "ansible-remote-command" \
    "在遠端主機執行臨時命令" \
'print_section("執行遠端命令")
module = "command"
module_args = "echo Hello from MCP Ansible Test"
host_pattern = "localhost"
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"

print(f"模組: {module}")
print(f"參數: {module_args}")
print(f"目標: {host_pattern}")
print(f"Inventory: {inventory_path}")

result = ansible_ad_hoc(
    module=module,
    module_args=module_args,
    host_pattern=host_pattern,
    inventory=inventory_path,
    connection="local"
)

print("\n📊 執行結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("stdout"):
    print(f"\n標準輸出:")
    print(result["stdout"][:500])

if result.get("results"):
    print(f"\n主機結果:")
    print_result(result["results"], max_lines=20)

if not result.get("ok"):
    raise Exception(f"遠端命令執行失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 16: ansible-task (使用 setup 模組)
test_tool "ansible-task" \
    "執行單個 Ansible 任務（使用 setup 模組收集事實）" \
'print_section("執行 Ansible 任務")
module = "setup"
module_args = "filter=ansible_os_family"
host_pattern = "localhost"
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"

print(f"模組: {module}")
print(f"參數: {module_args}")
print(f"目標: {host_pattern}")

result = ansible_ad_hoc(
    module=module,
    module_args=module_args,
    host_pattern=host_pattern,
    inventory=inventory_path,
    connection="local"
)

print("\n📊 任務執行結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("stdout"):
    stdout_lines = result["stdout"].split("\\n")
    print(f"\n收集的事實 (前 25 行):")
    for line in stdout_lines[:25]:
        print(f"  {line}")

if not result.get("ok"):
    raise Exception(f"任務執行失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 17: ansible-service-manager
skip_tool "ansible-service-manager" "需要實際的服務管理權限和 systemd 環境"

# ============================================================
# 6. 分析與審計工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         第六組：分析與審計工具測試 (1個)              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

skip_tool "ansible-log-hunter" "需要實際的 Ansible 執行日誌檔案"
skip_tool "ansible-network-matrix" "需要多主機網路測試環境"
skip_tool "ansible-performance-baseline" "需要多次執行測試，耗時較長"

# Test 18: ansible-security-audit
test_tool "ansible-security-audit" \
    "對 Ansible 專案進行安全審計" \
'print_section("執行安全審計")
project_root = ANSIBLE_PROJECT

print(f"專案根目錄: {project_root}")

result = ansible_security_audit(project_root=project_root)

print("\n📊 安全審計結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("findings"):
    findings = result["findings"]
    print(f"  發現問題: {len(findings)} 個")
    
    # 按嚴重程度分類
    by_severity = {}
    for finding in findings:
        severity = finding.get("severity", "unknown")
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(finding)
    
    print(f"\n問題分類:")
    for severity in ["critical", "high", "medium", "low", "info"]:
        if severity in by_severity:
            count = len(by_severity[severity])
            print(f"  {severity.upper()}: {count} 個")
    
    print(f"\n詳細發現 (前 5 個):")
    for i, finding in enumerate(findings[:5], 1):
        print(f"\n  {i}. [{finding.get(\"severity\", \"N/A\").upper()}] {finding.get(\"title\", \"N/A\")}")
        print(f"     訊息: {finding.get(\"message\", \"N/A\")[:100]}...")
        if finding.get("file"):
            print(f"     檔案: {finding[\"file\"]}")
        if finding.get("line"):
            print(f"     行號: {finding[\"line\"]}")
    
    if len(findings) > 5:
        print(f"\n  ... 還有 {len(findings) - 5} 個發現")
else:
    print("  ✓ 未發現安全問題")

if result.get("summary"):
    print(f"\n摘要:")
    print_result(result["summary"], max_lines=10)

if not result.get("ok"):
    raise Exception(f"安全審計失敗: {result.get(\"error\", \"Unknown error\")}")'

# ============================================================
# 7. Vault 相關工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          第七組：Vault 相關工具測試 (4個)             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 19: vault-encrypt
test_tool "vault-encrypt" \
    "使用 Ansible Vault 加密檔案" \
'import tempfile
import os

print_section("加密檔案")

# 創建測試檔案
temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
secret_data = """
database_password: super_secret_password_123
api_key: sk-1234567890abcdef
ssh_private_key: |
  -----BEGIN RSA PRIVATE KEY-----
  (this is test data, not a real key)
  -----END RSA PRIVATE KEY-----
"""
temp_file.write(secret_data)
temp_file.close()

print(f"測試檔案: {temp_file.name}")
print(f"原始內容大小: {len(secret_data)} 字元")
print(f"Vault 密碼: testpass123")

result = vault_encrypt(
    file_path=temp_file.name,
    vault_password="testpass123"
)

print("\n📊 加密結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  訊息: {result.get(\"message\", \"N/A\")}")

# 讀取加密後的內容
if os.path.exists(temp_file.name):
    with open(temp_file.name, "r") as f:
        encrypted_content = f.read()
    
    print(f"\n加密後內容大小: {len(encrypted_content)} 字元")
    print(f"加密後內容預覽 (前 200 字元):")
    print(encrypted_content[:200])
    
    # 驗證是否真的加密了
    if "$ANSIBLE_VAULT" in encrypted_content:
        print(f"\n✓ 檔案已成功加密（包含 $ANSIBLE_VAULT 標記）")
    else:
        raise Exception("檔案未被正確加密")
    
    # 保存加密檔案路徑供後續測試使用
    encrypted_file_path = temp_file.name
    with open(f"{TEST_OUTPUT_DIR}/encrypted_file_path.txt", "w") as f:
        f.write(encrypted_file_path)
else:
    raise Exception("加密後檔案不存在")

if not result.get("ok"):
    raise Exception(f"加密失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 20: vault-view
test_tool "vault-view" \
    "查看加密檔案的內容（不解密到磁碟）" \
'import os

print_section("查看加密檔案")

# 讀取之前加密的檔案路徑
encrypted_file_path = None
path_file = f"{TEST_OUTPUT_DIR}/encrypted_file_path.txt"
if os.path.exists(path_file):
    with open(path_file, "r") as f:
        encrypted_file_path = f.read().strip()

if not encrypted_file_path or not os.path.exists(encrypted_file_path):
    raise Exception("找不到之前加密的測試檔案")

print(f"加密檔案: {encrypted_file_path}")
print(f"Vault 密碼: testpass123")

result = vault_view(
    file_path=encrypted_file_path,
    vault_password="testpass123"
)

print("\n📊 查看結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("content"):
    content = result["content"]
    print(f"\n解密後的內容:")
    print("="*60)
    print(content)
    print("="*60)
    
    # 驗證內容是否正確
    if "database_password" in content and "super_secret_password_123" in content:
        print(f"\n✓ 內容解密正確")
    else:
        raise Exception("解密內容不正確")
else:
    print("  (無內容)")

if not result.get("ok"):
    raise Exception(f"查看失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 21: vault-rekey
test_tool "vault-rekey" \
    "更改加密檔案的 Vault 密碼" \
'import os

print_section("更改 Vault 密碼")

# 讀取之前加密的檔案路徑
encrypted_file_path = None
path_file = f"{TEST_OUTPUT_DIR}/encrypted_file_path.txt"
if os.path.exists(path_file):
    with open(path_file, "r") as f:
        encrypted_file_path = f.read().strip()

if not encrypted_file_path or not os.path.exists(encrypted_file_path):
    raise Exception("找不到之前加密的測試檔案")

print(f"加密檔案: {encrypted_file_path}")
print(f"舊密碼: testpass123")
print(f"新密碼: newpass456")

result = vault_rekey(
    file_path=encrypted_file_path,
    old_vault_password="testpass123",
    new_vault_password="newpass456"
)

print("\n📊 Rekey 結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  訊息: {result.get(\"message\", \"N/A\")}")

# 驗證新密碼可以查看檔案
if result.get("ok"):
    print(f"\n驗證新密碼...")
    view_result = vault_view(
        file_path=encrypted_file_path,
        vault_password="newpass456"
    )
    if view_result.get("ok") and view_result.get("content"):
        print(f"✓ 新密碼驗證成功")
    else:
        raise Exception("新密碼無法解密檔案")

if not result.get("ok"):
    raise Exception(f"Rekey 失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 22: vault-decrypt
test_tool "vault-decrypt" \
    "解密 Vault 加密的檔案" \
'import os

print_section("解密檔案")

# 讀取之前加密的檔案路徑
encrypted_file_path = None
path_file = f"{TEST_OUTPUT_DIR}/encrypted_file_path.txt"
if os.path.exists(path_file):
    with open(path_file, "r") as f:
        encrypted_file_path = f.read().strip()

if not encrypted_file_path or not os.path.exists(encrypted_file_path):
    raise Exception("找不到之前加密的測試檔案")

print(f"加密檔案: {encrypted_file_path}")
print(f"Vault 密碼: newpass456 (使用 rekey 後的密碼)")

# 讀取解密前的內容
with open(encrypted_file_path, "r") as f:
    before_content = f.read()

result = vault_decrypt(
    file_path=encrypted_file_path,
    vault_password="newpass456"
)

print("\n📊 解密結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  訊息: {result.get(\"message\", \"N/A\")}")

# 讀取解密後的內容
if os.path.exists(encrypted_file_path):
    with open(encrypted_file_path, "r") as f:
        after_content = f.read()
    
    print(f"\n解密後內容:")
    print("="*60)
    print(after_content)
    print("="*60)
    
    # 驗證是否真的解密了
    if "$ANSIBLE_VAULT" not in after_content and "database_password" in after_content:
        print(f"\n✓ 檔案已成功解密")
    else:
        raise Exception("檔案未被正確解密")
    
    # 清理測試檔案
    os.remove(encrypted_file_path)
    print(f"\n🧹 清理: 測試檔案已刪除")
else:
    raise Exception("解密後檔案不存在")

if not result.get("ok"):
    raise Exception(f"解密失敗: {result.get(\"error\", \"Unknown error\")}")'

# ============================================================
# 8. 其他實用工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║            第八組：其他實用工具測試 (2個)             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 23: validate-yaml
test_tool "validate-yaml" \
    "驗證 YAML 檔案格式正確性" \
'import tempfile
import os

print_section("驗證 YAML 格式")

# 創建有效的 YAML 檔案
valid_yaml_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yml")
valid_yaml_content = """---
# Test YAML configuration
application:
  name: test_app
  version: "1.0.0"
  settings:
    debug: true
    port: 8080
    hosts:
      - localhost
      - 127.0.0.1
    database:
      host: db.example.com
      port: 5432
      credentials:
        username: admin
        password: "{{ vault_db_password }}"
"""
valid_yaml_file.write(valid_yaml_content)
valid_yaml_file.close()

print(f"測試檔案: {valid_yaml_file.name}")
print(f"內容大小: {len(valid_yaml_content)} 字元")

result = validate_yaml(file_path=valid_yaml_file.name)

print("\n📊 驗證結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  有效: {\"是\" if result.get(\"valid\") else \"否\"}")

if result.get("parsed_data"):
    print(f"\n解析後的數據:")
    print_result(result["parsed_data"], max_lines=20)

if result.get("errors"):
    print(f"\n錯誤:")
    print_result(result["errors"], max_lines=10)

# 測試無效的 YAML
print(f"\n---\n測試無效 YAML...")
invalid_yaml_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yml")
invalid_yaml_content = """---
broken:
  - item1
    - item2
  invalid syntax here
"""
invalid_yaml_file.write(invalid_yaml_content)
invalid_yaml_file.close()

invalid_result = validate_yaml(file_path=invalid_yaml_file.name)
print(f"無效 YAML 檢測: {\"正確\" if not invalid_result.get(\"valid\") else \"失敗\"}，應該檢測為無效")

if invalid_result.get("errors"):
    print(f"錯誤訊息: {invalid_result[\"errors\"][0] if invalid_result[\"errors\"] else \"N/A\"}")

# 清理
os.remove(valid_yaml_file.name)
os.remove(invalid_yaml_file.name)
print(f"\n🧹 清理: 測試檔案已刪除")

if not result.get("ok") or not result.get("valid"):
    raise Exception(f"YAML 驗證失敗: {result.get(\"error\", \"Unknown error\")}")'

skip_tool "project-bootstrap" "會創建新的專案結構，可能干擾現有環境"
skip_tool "ansible-test-idempotence" "需要執行 playbook 兩次並比較結果，耗時較長"
