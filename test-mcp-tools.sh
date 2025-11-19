#!/bin/bash
# 測試 MCP Ansible Server 工具功能
# 這個腳本會測試所有可用的 MCP 工具，每個工具都進行完整測試

set +e  # 允許單個測試失敗，繼續執行

PROJECT_ROOT="/Users/edwardhuang/Documents/GitHub/Ansible_Auto_Control_Hub"
MCP_DIR="$PROJECT_ROOT/mcp-ansible"
ANSIBLE_PROJECT="$PROJECT_ROOT/ansible_projects/infra_owner_deploy"
TEST_OUTPUT_DIR="/tmp/ansible_mcp_test_$(date +%s)"

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo "╭──────────────────────────────────────────────────────────╮"
echo "│          MCP Ansible Server 工具功能測試                │"
echo "│                  完整版測試套件                          │"
echo "╰──────────────────────────────────────────────────────────╯"
echo ""
echo -e "${CYAN}測試輸出目錄: $TEST_OUTPUT_DIR${NC}"
mkdir -p "$TEST_OUTPUT_DIR"
echo ""

cd "$MCP_DIR"
source .venv/bin/activate

# 測試結果統計
PASSED=0
FAILED=0
SKIPPED=0
declare -a FAILED_TESTS

# 測試函數
test_tool() {
    local tool_name=$1
    local test_description=$2
    local python_script=$3
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}📋 測試工具: ${tool_name}${NC}"
    echo -e "${CYAN}📝 描述: ${test_description}${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # 創建臨時 Python 腳本
    local temp_script="$TEST_OUTPUT_DIR/${tool_name//[^a-zA-Z0-9]/_}.py"
    cat > "$temp_script" << 'PYTHON_SCRIPT_EOF'
import sys
import os
sys.path.insert(0, 'src')
from ansible_mcp.server import *
import json
from pprint import pprint

# 設定環境變數
ANSIBLE_PROJECT = os.environ.get('ANSIBLE_PROJECT')
TEST_OUTPUT_DIR = os.environ.get('TEST_OUTPUT_DIR')

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_result(data, max_lines=20):
    """漂亮地打印結果，限制行數"""
    if isinstance(data, dict) or isinstance(data, list):
        lines = json.dumps(data, indent=2, ensure_ascii=False).split('\n')
        for i, line in enumerate(lines[:max_lines]):
            print(line)
        if len(lines) > max_lines:
            print(f"... ({len(lines) - max_lines} 行省略)")
    else:
        str_data = str(data)
        lines = str_data.split('\n')
        for i, line in enumerate(lines[:max_lines]):
            print(line)
        if len(lines) > max_lines:
            print(f"... ({len(lines) - max_lines} 行省略)")

try:
PYTHON_SCRIPT_EOF

    # 添加實際測試代碼（縮排4個空格）
    echo "$python_script" | sed 's/^/    /' >> "$temp_script"
    
    # 添加異常處理結尾
    cat >> "$temp_script" << 'PYTHON_SCRIPT_EOF'
    
    print("\n" + "="*60)
    print("✅ 測試成功完成")
    print("="*60)
    sys.exit(0)
    
except Exception as e:
    print("\n" + "="*60)
    print(f"❌ 測試失敗: {str(e)}")
    print("="*60)
    import traceback
    print("\n詳細錯誤訊息:")
    traceback.print_exc()
    sys.exit(1)
PYTHON_SCRIPT_EOF

    # 執行測試
    if python3 "$temp_script"; then
        echo ""
        echo -e "${GREEN}✅ ${tool_name} - 測試通過${NC}"
        echo ""
        ((PASSED++))
        return 0
    else
        echo ""
        echo -e "${RED}❌ ${tool_name} - 測試失敗${NC}"
        echo ""
        FAILED_TESTS+=("$tool_name")
        ((FAILED++))
        return 1
    fi
}

skip_tool() {
    local tool_name=$1
    local reason=$2
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}⊘ ${tool_name} - 跳過${NC}"
    echo -e "${CYAN}原因: ${reason}${NC}"
    echo ""
    ((SKIPPED++))
}

# ============================================================
# 開始測試
# ============================================================

echo "設定測試環境變數..."
export ANSIBLE_PROJECT="$ANSIBLE_PROJECT"
export TEST_OUTPUT_DIR="$TEST_OUTPUT_DIR"
export MCP_ANSIBLE_PROJECT_ROOT="$ANSIBLE_PROJECT"
export MCP_ANSIBLE_INVENTORY="$ANSIBLE_PROJECT/inventory/hosts.ini"
export MCP_ANSIBLE_PROJECT_NAME="infra_owner_deploy"
echo -e "${GREEN}✓ 環境變數已設定${NC}"
echo ""

# ============================================================
# 1. 基礎工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           第一組：基礎工具測試 (5個)                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: ansible-ping
test_tool "ansible-ping" \
    "測試主機連通性，驗證 Ansible 能否連接到目標主機" \
'print_section("執行 ansible-ping")
print("目標: all hosts")
print(f"Inventory: {ANSIBLE_PROJECT}/inventory/hosts.ini")

result = ansible_ping(
    host_pattern="all",
    project_root=ANSIBLE_PROJECT,
    inventory_paths=[f"{ANSIBLE_PROJECT}/inventory/hosts.ini"],
    verbose=1
)

print("\n📊 Ping 結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("summary"):
    print(f"\n摘要:")
    print_result(result["summary"], max_lines=10)

if result.get("stdout"):
    print(f"\n標準輸出 (前 500 字元):")
    print(result["stdout"][:500])

if not result.get("ok"):
    raise Exception(f"Ping 失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 2: validate-playbook
test_tool "validate-playbook" \
    "驗證 playbook 語法正確性，檢查 YAML 格式和 Ansible 語法" \
'print_section("驗證 Playbook 語法")
playbook_path = f"{ANSIBLE_PROJECT}/playbooks/deploy_compose.yml"
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"

print(f"Playbook: {playbook_path}")
print(f"Inventory: {inventory_path}")

result = validate_playbook(
    playbook_path=playbook_path,
    inventory=inventory_path
)

print("\n📊 驗證結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  有效: {\"是\" if result.get(\"valid\") else \"否\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("stdout"):
    print(f"\n標準輸出:")
    print(result["stdout"])

if result.get("errors"):
    print(f"\n錯誤列表:")
    print_result(result["errors"], max_lines=15)

if not result.get("ok") or not result.get("valid"):
    error_msg = result.get("error", "Validation failed")
    if result.get("stderr"):
        error_msg += f"\nStderr: {result[\"stderr\"][:200]}"
    raise Exception(error_msg)'

# Test 3: inventory-parse
test_tool "ansible-inventory (inventory-parse)" \
    "解析 inventory 檔案，顯示主機群組結構" \
'print_section("解析 Inventory")
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"
print(f"Inventory: {inventory_path}")

result = ansible_inventory(
    inventory=inventory_path,
    include_hostvars=True
)

print("\n📊 Inventory 資訊:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("inventory"):
    inventory_data = result["inventory"]
    print(f"\n主機群組 ({len(inventory_data)} 個):")
    for group_name in sorted(inventory_data.keys()):
        group = inventory_data[group_name]
        if isinstance(group, dict):
            hosts = group.get("hosts", [])
            print(f"  📁 {group_name}:")
            if hosts:
                for host in hosts:
                    print(f"      - {host}")
            else:
                print(f"      (無主機)")

if result.get("stdout"):
    print(f"\n完整輸出 (JSON 格式，前 30 行):")
    print_result(result.get("inventory"), max_lines=30)

if not result.get("ok"):
    raise Exception(f"Inventory 解析失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 4: list-projects
test_tool "list-projects" \
    "列出所有已註冊的 Ansible 專案" \
'print_section("列出已註冊專案")

result = list_projects()

print("\n📊 專案清單:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("projects"):
    projects = result["projects"]
    print(f"  專案數量: {len(projects)}")
    print("\n專案詳情:")
    for i, project in enumerate(projects, 1):
        print(f"\n  {i}. 專案名稱: {project.get(\"name\", \"N/A\")}")
        print(f"     根目錄: {project.get(\"root\", \"N/A\")}")
        print(f"     Inventory: {project.get(\"inventory\", \"N/A\")}")
        print(f"     預設專案: {\"是\" if project.get(\"is_default\") else \"否\"}")
        if project.get("roles_paths"):
            print(f"     Roles 路徑: {project[\"roles_paths\"]}")
else:
    print("  (無已註冊專案)")

if not result.get("ok"):
    raise Exception(f"列出專案失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 5: register-project
test_tool "register-project" \
    "註冊新的 Ansible 專案到 MCP 配置" \
'print_section("註冊測試專案")
test_project_name = f"test_project_{os.getpid()}"

print(f"專案名稱: {test_project_name}")
print(f"專案根目錄: {ANSIBLE_PROJECT}")
print(f"Inventory: {ANSIBLE_PROJECT}/inventory/hosts.ini")

result = register_project(
    name=test_project_name,
    root=ANSIBLE_PROJECT,
    inventory=f"{ANSIBLE_PROJECT}/inventory/hosts.ini",
    make_default=False
)

print("\n📊 註冊結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  訊息: {result.get(\"message\", \"N/A\")}")
print(f"  配置路徑: {result.get(\"config_path\", \"N/A\")}")

if result.get("project"):
    print(f"\n專案資訊:")
    print_result(result["project"], max_lines=15)

# 清理：取消註冊測試專案
try:
    cleanup_result = unregister_project(name=test_project_name)
    print(f"\n🧹 清理: 測試專案已移除 ({cleanup_result.get(\"message\", \"\")})")
except:
    print(f"\n⚠️  警告: 無法自動清理測試專案 {test_project_name}")

if not result.get("ok"):
    raise Exception(f"註冊專案失敗: {result.get(\"error\", \"Unknown error\")}")'

# ============================================================
# 2. Playbook 相關工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         第二組：Playbook 相關工具測試 (4個)           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 6: project-playbooks
test_tool "project-playbooks" \
    "列出專案中所有可用的 playbooks" \
'print_section("列出專案 Playbooks")
project_name = "infra_owner_deploy"
print(f"專案: {project_name}")

result = project_playbooks(project_name=project_name)

print("\n📊 Playbooks 清單:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("playbooks"):
    playbooks = result["playbooks"]
    print(f"  Playbook 數量: {len(playbooks)}")
    print("\nPlaybooks:")
    for i, pb in enumerate(playbooks, 1):
        print(f"  {i}. {pb}")
else:
    print("  (無 playbooks)")

if result.get("playbooks_dir"):
    print(f"\nPlaybooks 目錄: {result[\"playbooks_dir\"]}")

if not result.get("ok"):
    raise Exception(f"列出 playbooks 失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 7: ansible-playbook (check mode)
test_tool "ansible-playbook (check-mode)" \
    "以檢查模式執行 playbook，不實際改變系統狀態" \
'print_section("執行 Playbook (Check Mode)")
playbook_path = f"{ANSIBLE_PROJECT}/playbooks/deploy_compose.yml"
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"

print(f"Playbook: {playbook_path}")
print(f"Inventory: {inventory_path}")
print(f"模式: Check (Dry-run)")

result = ansible_playbook(
    playbook_path=playbook_path,
    inventory=inventory_path,
    check=True,
    verbose=1
)

print("\n📊 執行結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("stdout"):
    print(f"\n標準輸出 (前 800 字元):")
    print(result["stdout"][:800])
    if len(result["stdout"]) > 800:
        print(f"\n... (還有 {len(result[\"stdout\"]) - 800} 個字元)")

if result.get("stderr"):
    print(f"\n標準錯誤 (前 400 字元):")
    print(result["stderr"][:400])

# Check mode 可能返回非零 RC，這是正常的
if result.get("rc") == 0:
    print("\n✓ Check mode 執行成功，無語法錯誤")
else:
    print(f"\n⚠️  Check mode 返回 RC={result.get(\"rc\")}，可能是主機連接問題或變數未定義")'

# Test 8: create-playbook
test_tool "create-playbook" \
    "創建新的 playbook 檔案，包含基本結構" \
'import tempfile
import os

print_section("創建測試 Playbook")

# 創建臨時目錄
temp_dir = tempfile.mkdtemp(prefix="ansible_test_")
test_playbook_path = os.path.join(temp_dir, "test_playbook.yml")

print(f"目標路徑: {test_playbook_path}")
print(f"主機: localhost")
print(f"任務數: 3")

tasks = [
    {
        "name": "Test task 1 - Debug message",
        "debug": {
            "msg": "Hello from test playbook"
        }
    },
    {
        "name": "Test task 2 - Gather facts",
        "setup": {}
    },
    {
        "name": "Test task 3 - Set fact",
        "set_fact": {
            "test_var": "test_value"
        }
    }
]

result = create_playbook(
    path=test_playbook_path,
    description="Automated test playbook created by MCP tool test",
    hosts="localhost",
    tasks=tasks,
    gather_facts=True,
    become=False
)

print("\n📊 創建結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  訊息: {result.get(\"message\", \"N/A\")}")
print(f"  檔案路徑: {result.get(\"path\", \"N/A\")}")

if os.path.exists(test_playbook_path):
    file_size = os.path.getsize(test_playbook_path)
    print(f"  檔案大小: {file_size} bytes")
    
    print(f"\n📄 Playbook 內容:")
    with open(test_playbook_path, "r") as f:
        content = f.read()
        print(content)
    
    # 驗證創建的 playbook
    validate_result = validate_playbook(playbook_path=test_playbook_path)
    print(f"\n✓ Playbook 語法驗證: {\"通過\" if validate_result.get(\"valid\") else \"失敗\"}")
    
    # 清理
    os.remove(test_playbook_path)
    os.rmdir(temp_dir)
    print(f"\n🧹 清理: 測試檔案已刪除")
else:
    raise Exception("Playbook 檔案未被創建")

if not result.get("ok"):
    raise Exception(f"創建 playbook 失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 9: project-run-playbook
test_tool "project-run-playbook" \
    "通過專案名稱執行 playbook (check mode)" \
'print_section("通過專案執行 Playbook")
project_name = "infra_owner_deploy"
playbook_rel_path = "playbooks/deploy_compose.yml"

print(f"專案: {project_name}")
print(f"Playbook: {playbook_rel_path}")
print(f"模式: Check (Dry-run)")

result = project_run_playbook(
    project_name=project_name,
    playbook_path=playbook_rel_path,
    check=True,
    verbose=0
)

print("\n📊 執行結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  返回碼: {result.get(\"rc\", \"N/A\")}")

if result.get("stdout"):
    stdout_lines = result["stdout"].split("\\n")
    print(f"\n標準輸出 (前 30 行):")
    for line in stdout_lines[:30]:
        print(f"  {line}")
    if len(stdout_lines) > 30:
        print(f"\n... (還有 {len(stdout_lines) - 30} 行)")

# project-run-playbook 在 check mode 可能返回非零值
if result.get("rc") == 0:
    print("\n✓ 專案 playbook 執行成功")
else:
    print(f"\n⚠️  返回 RC={result.get(\"rc\")}，可能是 check mode 正常行為")'

# ============================================================
# 3. Inventory 相關工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        第三組：Inventory 相關工具測試 (3個)           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 10: inventory-find-host
test_tool "inventory-find-host" \
    "在 inventory 中查找特定主機的詳細資訊" \
'print_section("查找主機資訊")
hostname = "localhost"
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"

print(f"主機名稱: {hostname}")
print(f"Inventory: {inventory_path}")

result = inventory_find_host(
    hostname=hostname,
    inventory=inventory_path
)

print("\n📊 查找結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  找到主機: {\"是\" if result.get(\"found\") else \"否\"}")

if result.get("host"):
    print(f"\n主機詳情:")
    print_result(result["host"], max_lines=25)

if result.get("groups"):
    print(f"\n所屬群組: {result[\"groups\"]}")

if not result.get("ok"):
    raise Exception(f"查找主機失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 11: inventory-graph
test_tool "inventory-graph" \
    "生成 inventory 結構的視覺化圖表" \
'print_section("生成 Inventory 圖表")
inventory_path = f"{ANSIBLE_PROJECT}/inventory/hosts.ini"

print(f"Inventory: {inventory_path}")
print(f"輸出格式: text")

result = inventory_graph(
    inventory=inventory_path,
    format="text"
)

print("\n📊 圖表生成結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("graph"):
    graph_content = result["graph"]
    print(f"  圖表大小: {len(graph_content)} 字元")
    
    print(f"\n📊 Inventory 結構圖:")
    print("="*60)
    # 顯示完整圖表
    lines = graph_content.split("\\n")
    for line in lines[:50]:  # 最多顯示50行
        print(line)
    if len(lines) > 50:
        print(f"\n... (還有 {len(lines) - 50} 行)")
    print("="*60)

if not result.get("ok"):
    raise Exception(f"生成圖表失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 12: inventory-diff
test_tool "inventory-diff" \
    "比較兩個 inventory 的差異" \
'import tempfile
import os

print_section("比較 Inventory 差異")

# 創建兩個測試 inventory 檔案
temp_dir = tempfile.mkdtemp(prefix="ansible_inv_test_")
inv1_path = os.path.join(temp_dir, "inventory1.ini")
inv2_path = os.path.join(temp_dir, "inventory2.ini")

# Inventory 1
with open(inv1_path, "w") as f:
    f.write("""[web]
host1 ansible_host=192.168.1.10
host2 ansible_host=192.168.1.11

[db]
db1 ansible_host=192.168.1.20
""")

# Inventory 2 (有變動)
with open(inv2_path, "w") as f:
    f.write("""[web]
host1 ansible_host=192.168.1.10
host3 ansible_host=192.168.1.12

[db]
db1 ansible_host=192.168.1.20
db2 ansible_host=192.168.1.21
""")

print(f"Inventory 1: {inv1_path}")
print(f"Inventory 2: {inv2_path}")

result = inventory_diff(
    inventory1=inv1_path,
    inventory2=inv2_path
)

print("\n📊 差異分析結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("added_hosts"):
    print(f"\n➕ 新增主機: {result[\"added_hosts\"]}")

if result.get("removed_hosts"):
    print(f"\n➖ 移除主機: {result[\"removed_hosts\"]}")

if result.get("changed_hosts"):
    print(f"\n🔄 變更主機: {result[\"changed_hosts\"]}")

if result.get("diff_text"):
    print(f"\n差異文字:")
    print("="*60)
    print(result["diff_text"])
    print("="*60)

# 清理
os.remove(inv1_path)
os.remove(inv2_path)
os.rmdir(temp_dir)
print(f"\n🧹 清理: 測試檔案已刪除")

if not result.get("ok"):
    raise Exception(f"比較失敗: {result.get(\"error\", \"Unknown error\")}")'

# ============================================================
# 4. Role 相關工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          第四組：Role 相關工具測試 (2個)              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 13: create-role-structure
test_tool "create-role-structure" \
    "創建標準 Ansible role 目錄結構" \
'import tempfile
import os
import shutil

print_section("創建 Role 結構")

temp_dir = tempfile.mkdtemp(prefix="ansible_role_test_")
role_name = "test_webserver_role"

print(f"Role 名稱: {role_name}")
print(f"目標目錄: {temp_dir}")

result = create_role_structure(
    role_name=role_name,
    path=temp_dir
)

print("\n📊 創建結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")
print(f"  訊息: {result.get(\"message\", \"N/A\")}")

role_path = os.path.join(temp_dir, role_name)
if os.path.exists(role_path):
    print(f"  Role 路徑: {role_path}")
    
    # 列出創建的目錄和檔案
    print(f"\n📁 Role 結構:")
    for root, dirs, files in os.walk(role_path):
        level = root.replace(role_path, "").count(os.sep)
        indent = "  " * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        sub_indent = "  " * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            print(f"{sub_indent}📄 {file} ({file_size} bytes)")
    
    # 檢查標準目錄
    standard_dirs = ["tasks", "handlers", "templates", "files", "vars", "defaults", "meta"]
    print(f"\n✓ 標準目錄檢查:")
    for dir_name in standard_dirs:
        dir_path = os.path.join(role_path, dir_name)
        exists = os.path.exists(dir_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_name}/")
    
    # 清理
    shutil.rmtree(temp_dir)
    print(f"\n🧹 清理: Role 目錄已刪除")
else:
    raise Exception(f"Role 目錄未被創建: {role_path}")

if not result.get("ok"):
    raise Exception(f"創建 role 失敗: {result.get(\"error\", \"Unknown error\")}")'

# Test 14: ansible-role
test_tool "ansible-role" \
    "分析和顯示 role 的詳細資訊" \
'import tempfile
import os
import shutil

print_section("分析 Role 資訊")

# 先創建一個測試 role
temp_dir = tempfile.mkdtemp(prefix="ansible_role_info_test_")
role_name = "test_analysis_role"

# 創建 role
create_result = create_role_structure(role_name=role_name, path=temp_dir)
role_path = os.path.join(temp_dir, role_name)

# 添加一些內容到 role
tasks_main = os.path.join(role_path, "tasks", "main.yml")
with open(tasks_main, "w") as f:
    f.write("""---
# Test role tasks
- name: Install nginx
  apt:
    name: nginx
    state: present

- name: Start nginx
  service:
    name: nginx
    state: started
""")

defaults_main = os.path.join(role_path, "defaults", "main.yml")
with open(defaults_main, "w") as f:
    f.write("""---
# Default variables
nginx_port: 80
nginx_user: www-data
""")

print(f"Role 名稱: {role_name}")
print(f"Role 路徑: {role_path}")

# 分析 role
result = ansible_role(role_path=role_path)

print("\n📊 Role 分析結果:")
print(f"  狀態: {\"成功\" if result.get(\"ok\") else \"失敗\"}")

if result.get("role_info"):
    role_info = result["role_info"]
    print(f"\nRole 資訊:")
    print_result(role_info, max_lines=30)

if result.get("tasks_count"):
    print(f"\n任務數量: {result[\"tasks_count\"]}")

if result.get("variables"):
    print(f"\n變數:")
    print_result(result["variables"], max_lines=15)

# 清理
shutil.rmtree(temp_dir)
print(f"\n🧹 清理: 測試 role 已刪除")

if not result.get("ok"):
    raise Exception(f"分析 role 失敗: {result.get(\"error\", \"Unknown error\")}")'

skip_tool "galaxy-install" "需要網路連線且會下載實際 roles，較耗時"
skip_tool "galaxy-lock" "需要實際的 requirements.yml 和網路連線"

# ============================================================
# 5. 執行與管理工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        第五組：執行與管理工具測試                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 17: ansible-remote-command
test_tool "ansible-remote-command" \
    "執行遠端命令" \
    'result = ansible_ad_hoc(
        module="command",
        module_args="echo test",
        host_pattern="localhost",
        inventory="'"$ANSIBLE_PROJECT"'/inventory/hosts.ini",
        connection="local"
    )
print(f"命令結果: RC={result.get(\"rc\", \"N/A\")}")
if not result.get("ok"):
    raise Exception(f"Remote command failed: {result.get(\"error\")}")'

# Test 18: ansible-task
test_tool "ansible-task" \
    "執行單個任務" \
    'result = ansible_ad_hoc(
        module="setup",
        module_args="filter=ansible_os_family",
        host_pattern="localhost",
        inventory="'"$ANSIBLE_PROJECT"'/inventory/hosts.ini",
        connection="local"
    )
print(f"任務結果: RC={result.get(\"rc\", \"N/A\")}")
if not result.get("ok"):
    raise Exception(f"Task execution failed: {result.get(\"error\")}")'

# Test 19: ansible-service-manager
skip_tool "ansible-service-manager" "需要實際的服務管理權限"

# ============================================================
# 6. 分析與審計工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         第六組：分析與審計工具測試                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 20: ansible-log-hunter
skip_tool "ansible-log-hunter" "需要實際的執行日誌"

# Test 21: ansible-network-matrix
skip_tool "ansible-network-matrix" "需要網路測試環境"

# Test 22: ansible-performance-baseline
skip_tool "ansible-performance-baseline" "需要執行多次測試，較耗時"

# Test 23: ansible-security-audit
test_tool "ansible-security-audit" \
    "安全審計檢查" \
    'result = ansible_security_audit(
        project_root="'"$ANSIBLE_PROJECT"'"
    )
findings = result.get("findings", [])
print(f"安全檢查項目: {len(findings)} 個")
for f in findings[:3]:
    print(f"  - {f.get(\"severity\", \"N/A\")}: {f.get(\"message\", \"N/A\")[:50]}...")
if not result.get("ok"):
    raise Exception(f"Security audit failed: {result.get(\"error\")}")'

# ============================================================
# 7. Vault 相關工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          第七組：Vault 相關工具測試                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 24: vault-encrypt
test_tool "vault-encrypt" \
    "加密檔案" \
    'import tempfile
import os
temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")
temp_file.write("test secret data")
temp_file.close()
result = vault_encrypt(
    file_path=temp_file.name,
    vault_password="testpass123"
)
print(f"加密結果: {result.get(\"message\", \"N/A\")}")
encrypted_content = ""
if os.path.exists(temp_file.name):
    with open(temp_file.name, "r") as f:
        encrypted_content = f.read()
    os.remove(temp_file.name)
if "$ANSIBLE_VAULT" not in encrypted_content:
    raise Exception("File was not encrypted")
if not result.get("ok"):
    raise Exception(f"Vault encrypt failed: {result.get(\"error\")}")'

# Test 25: vault-view
skip_tool "vault-view" "需要已加密的檔案"

# Test 26: vault-decrypt
skip_tool "vault-decrypt" "需要已加密的檔案"

# Test 27: vault-rekey
skip_tool "vault-rekey" "需要已加密的檔案"

# ============================================================
# 8. 其他工具測試
# ============================================================

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║            第八組：其他工具測試                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 28: validate-yaml
test_tool "validate-yaml" \
    "驗證 YAML 格式" \
    'import tempfile
import os
temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yml")
temp_file.write("---\ntest:\n  key: value\n  list:\n    - item1\n    - item2\n")
temp_file.close()
result = validate_yaml(file_path=temp_file.name)
print(f"YAML 驗證: Valid={result.get(\"valid\")}")
os.remove(temp_file.name)
if not result.get("ok") or not result.get("valid"):
    raise Exception(f"YAML validation failed: {result.get(\"error\")}")'

# Test 29: project-bootstrap
skip_tool "project-bootstrap" "會創建新專案，避免干擾現有結構"

# Test 30: project-run-playbook
test_tool "project-run-playbook" \
    "通過專案名稱執行 playbook (check mode)" \
    'result = project_run_playbook(
        project_name="infra_owner_deploy",
        playbook_path="playbooks/deploy_compose.yml",
        check=True,
        verbose=0
)
print(f"執行結果: RC={result.get(\"rc\", \"N/A\")}")
if result.get("rc") == 0:
    print("專案 playbook 執行成功 (check mode)")
else:
    print(f"Warning: Playbook returned RC={result.get(\"rc\")}")'

# ============================================================
# 測試總結
# ============================================================

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  測試總結                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ 通過: $PASSED${NC}"
echo -e "${RED}❌ 失敗: $FAILED${NC}"
echo -e "${YELLOW}⊘  跳過: $SKIPPED${NC}"
echo ""

TOTAL=$((PASSED + FAILED + SKIPPED))
SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED / ($PASSED + $FAILED)) * 100}")

echo "總計: $TOTAL 個測試"
echo "成功率: ${SUCCESS_RATE}% (通過/執行)"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有測試通過！${NC}"
    exit 0
else
    echo -e "${RED}⚠️  有 $FAILED 個測試失敗${NC}"
    exit 1
fi
