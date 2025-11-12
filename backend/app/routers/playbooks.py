from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Playbook, Task, PlaybookExtraField, Inventory, ExecutionStatus
from app.schemas.playbook import (
    PlaybookCreate, PlaybookUpdate, PlaybookListResponse, 
    PlaybookDetailResponse, PlaybookExecuteRequest
)
import json
import tempfile
import os
import yaml
from datetime import datetime
import uuid
import platform
import subprocess

# 自定義 YAML 多行字串輸出格式（保留 | 格式）
def str_presenter(dumper, data):
    if '\n' in data:  # 如果字串包含換行，使用 literal block scalar
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

router = APIRouter()

@router.get("/", response_model=dict)
def get_playbooks(
    search: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    """獲取 Playbook 列表"""
    query = db.query(Playbook)
    
    if search:
        query = query.filter(Playbook.name.contains(search))
    if type:
        query = query.filter(Playbook.type == type)
    if status:
        query = query.filter(Playbook.status == status)
    
    total = query.count()
    playbooks = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # 轉換為 Pydantic schemas
    items = [PlaybookListResponse.model_validate(p) for p in playbooks]
    
    return {
        "success": True,
        "data": {
            "items": items,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        }
    }

@router.get("/execution-info", response_model=dict)
def get_execution_info():
    """獲取 Playbook 執行環境資訊"""
    try:
        is_windows = platform.system() == 'Windows'
        
        # 取得臨時目錄位置
        temp_base = tempfile.gettempdir()
        
        # 取得當前工作目錄
        current_dir = os.getcwd()
        
        # 取得專案根目錄
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 執行方式說明
        execution_method = "WSL (Windows Subsystem for Linux)" if is_windows else "Direct (Native)"
        
        # Ansible 安裝檢查
        ansible_path = "未檢測"
        ansible_version = "未檢測"
        
        try:
            ansible_check = subprocess.run(
                ["wsl", "which", "ansible-playbook"] if is_windows else ["which", "ansible-playbook"],
                capture_output=True,
                text=True,
                timeout=5
            )
            ansible_path = ansible_check.stdout.strip() if ansible_check.returncode == 0 else "未安裝或無法找到"
        except Exception as e:
            ansible_path = f"檢測失敗: {str(e)}"
        
        # Ansible 版本檢查
        try:
            version_check = subprocess.run(
                ["wsl", "ansible-playbook", "--version"] if is_windows else ["ansible-playbook", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            ansible_version = version_check.stdout.split('\n')[0] if version_check.returncode == 0 else "無法取得版本"
        except Exception as e:
            ansible_version = f"檢測失敗: {str(e)}"
        
        # 路徑轉換範例 (Windows)
        path_conversion_example = None
        if is_windows:
            example_path = os.path.join(temp_base, "playbook.yml")
            wsl_path = example_path.replace('\\', '/')
            if ':' in wsl_path:
                drive = wsl_path[0].lower()
                rest = wsl_path[2:]
                wsl_path = f"/mnt/{drive}{rest}"
            path_conversion_example = {
                "windows_path": example_path,
                "wsl_path": wsl_path
            }
        
        return {
            "success": True,
            "data": {
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "python_version": platform.python_version()
                },
                "execution": {
                    "method": execution_method,
                    "current_directory": current_dir,
                    "project_root": project_root,
                    "temp_directory_base": temp_base,
                    "temp_directory_note": "每次執行時會在此目錄下建立臨時子目錄"
                },
                "ansible": {
                    "path": ansible_path,
                    "version": ansible_version,
                    "command_prefix": "wsl ansible-playbook" if is_windows else "ansible-playbook"
                },
                "path_conversion": path_conversion_example,
                "execution_flow": {
                    "step1": "建立臨時目錄 (使用 Python tempfile.TemporaryDirectory())",
                    "step2": "在臨時目錄中生成 inventory.ini 和 playbook.yml",
                    "step3": f"執行命令: {'wsl ansible-playbook -i <wsl_path>/inventory.ini <wsl_path>/playbook.yml' if is_windows else 'ansible-playbook -i <path>/inventory.ini <path>/playbook.yml'}",
                    "step4": "執行完成後自動清理臨時目錄",
                    "note": "臨時目錄在執行完成後會自動刪除,無法直接訪問"
                }
            }
        }
    except Exception as e:
        # 如果發生任何錯誤,返回基本資訊
        return {
            "success": True,
            "data": {
                "platform": {
                    "system": platform.system(),
                    "release": "Unknown",
                    "version": "Unknown",
                    "machine": "Unknown",
                    "python_version": platform.python_version()
                },
                "execution": {
                    "method": "Unknown",
                    "current_directory": os.getcwd(),
                    "project_root": "Unknown",
                    "temp_directory_base": tempfile.gettempdir(),
                    "temp_directory_note": "每次執行時會在此目錄下建立臨時子目錄"
                },
                "ansible": {
                    "path": "檢測失敗",
                    "version": "檢測失敗",
                    "command_prefix": "ansible-playbook"
                },
                "path_conversion": None,
                "execution_flow": {
                    "step1": "建立臨時目錄",
                    "step2": "生成配置檔案",
                    "step3": "執行 Ansible Playbook",
                    "step4": "清理臨時目錄",
                    "note": f"發生錯誤: {str(e)}"
                }
            }
        }

@router.get("/{playbook_id}", response_model=dict)
def get_playbook(playbook_id: int, db: Session = Depends(get_db)):
    """獲取單一 Playbook 詳細資料"""
    playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    
    # 組合完整資料
    tasks = db.query(Task).filter(Task.playbook_id == playbook_id).order_by(Task.order).all()
    extra_fields = db.query(PlaybookExtraField).filter(
        PlaybookExtraField.playbook_id == playbook_id
    ).all()
    
    # 轉換為 dict（從 JSON 字串解析）
    import json
    extra_dict = {}
    if extra_fields and len(extra_fields) > 0:
        try:
            extra_dict = json.loads(extra_fields[0].field_value)
        except:
            extra_dict = {}
    
    response_data = {
        "id": playbook.id,
        "name": playbook.name,
        "type": playbook.type,
        "status": playbook.status,
        "target_type": playbook.target_type,
        "group": playbook.group,
        "host": playbook.host,
        "main": {
            "hosts": playbook.host or playbook.group or "all",
            "gather_facts": playbook.gather_facts
        },
        "tasks": [
            {
                "id": task.id,
                "enabled": task.enabled,
                "content": task.content,
                "order": task.order
            } for task in tasks
        ],
        "extra_fields": extra_dict if extra_dict else None,
        "last_run_at": playbook.last_run_at,
        "created_at": playbook.created_at,
        "updated_at": playbook.updated_at
    }
    
    return {
        "success": True,
        "data": response_data
    }

@router.post("/", response_model=dict, status_code=201)
def create_playbook(playbook: PlaybookCreate, db: Session = Depends(get_db)):
    """創建 Playbook"""
    # 創建 Playbook
    db_playbook = Playbook(
        name=playbook.name,
        type=playbook.type,
        target_type=playbook.target_type,
        group=playbook.group,
        host=playbook.host,
        gather_facts=playbook.main.gather_facts
    )
    db.add(db_playbook)
    db.flush()  # 取得 ID
    
    # 創建 Tasks
    for idx, task in enumerate(playbook.tasks):
        db_task = Task(
            playbook_id=db_playbook.id,
            order=task.order if hasattr(task, 'order') else idx,
            enabled=task.enabled,
            content=task.content
        )
        db.add(db_task)
    
    # 創建 Extra Fields
    if playbook.extra_fields:
        import json
        # 將 extra_fields 轉為 JSON 字串存入 field_value
        db_field = PlaybookExtraField(
            playbook_id=db_playbook.id,
            field_value=json.dumps(playbook.extra_fields)
        )
        db.add(db_field)
    
    db.commit()
    db.refresh(db_playbook)
    
    # 回傳時也轉換為 schema
    tasks = db.query(Task).filter(Task.playbook_id == db_playbook.id).order_by(Task.order).all()
    response_data = PlaybookDetailResponse(
        id=db_playbook.id,
        name=db_playbook.name,
        type=db_playbook.type,
        status=db_playbook.status,
        target_type=db_playbook.target_type,
        group=db_playbook.group,
        host=db_playbook.host,
        main={"hosts": db_playbook.host or db_playbook.group or "all", "gather_facts": db_playbook.gather_facts},
        tasks=[{"id": t.id, "enabled": t.enabled, "content": t.content, "order": t.order} for t in tasks],
        extra_fields={},
        last_run_at=db_playbook.last_run_at,
        created_at=db_playbook.created_at,
        updated_at=db_playbook.updated_at
    )
    
    return {
        "success": True,
        "data": response_data,
        "message": "Playbook 創建成功"
    }

@router.put("/{playbook_id}", response_model=dict)
def update_playbook(
    playbook_id: int,
    playbook: PlaybookUpdate,
    db: Session = Depends(get_db)
):
    """更新 Playbook"""
    db_playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not db_playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    
    # 更新基本資訊
    if playbook.name is not None:
        db_playbook.name = playbook.name
    if playbook.type is not None:
        db_playbook.type = playbook.type
    if playbook.target_type is not None:
        db_playbook.target_type = playbook.target_type
    if playbook.group is not None:
        db_playbook.group = playbook.group
    if playbook.host is not None:
        db_playbook.host = playbook.host
    if playbook.main is not None:
        db_playbook.gather_facts = playbook.main.gather_facts
    
    # 更新 Tasks (刪除舊的，新增新的)
    if playbook.tasks is not None:
        db.query(Task).filter(Task.playbook_id == playbook_id).delete()
        for idx, task in enumerate(playbook.tasks):
            db_task = Task(
                playbook_id=playbook_id,
                order=task.order if hasattr(task, 'order') else idx,
                enabled=task.enabled,
                content=task.content
            )
            db.add(db_task)
    
    # 更新 Extra Fields
    if playbook.extra_fields is not None:
        import json
        # 刪除舊的 extra_fields
        db.query(PlaybookExtraField).filter(
            PlaybookExtraField.playbook_id == playbook_id
        ).delete()
        # 新增新的 extra_fields（轉為 JSON 字串）
        if playbook.extra_fields:
            db_field = PlaybookExtraField(
                playbook_id=playbook_id,
                field_value=json.dumps(playbook.extra_fields)
            )
            db.add(db_field)
    
    db.commit()
    db.refresh(db_playbook)
    
    # 回傳時也轉換為 schema
    tasks = db.query(Task).filter(Task.playbook_id == playbook_id).order_by(Task.order).all()
    response_data = PlaybookDetailResponse(
        id=db_playbook.id,
        name=db_playbook.name,
        type=db_playbook.type,
        status=db_playbook.status,
        target_type=db_playbook.target_type,
        group=db_playbook.group,
        host=db_playbook.host,
        main={"hosts": db_playbook.host or db_playbook.group or "all", "gather_facts": db_playbook.gather_facts},
        tasks=[{"id": t.id, "enabled": t.enabled, "content": t.content, "order": t.order} for t in tasks],
        extra_fields={},
        last_run_at=db_playbook.last_run_at,
        created_at=db_playbook.created_at,
        updated_at=db_playbook.updated_at
    )
    
    return {
        "success": True,
        "data": response_data,
        "message": "Playbook 更新成功"
    }

@router.delete("/{playbook_id}", response_model=dict)
def delete_playbook(playbook_id: int, db: Session = Depends(get_db)):
    """刪除 Playbook"""
    db_playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not db_playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    
    db.delete(db_playbook)  # 關聯的 Tasks 和 ExtraFields 會被級聯刪除
    db.commit()
    
    return {
        "success": True,
        "message": "Playbook 刪除成功"
    }

@router.post("/execute", response_model=dict)
def execute_playbooks(request: PlaybookExecuteRequest, db: Session = Depends(get_db)):
    """執行 Playbooks"""
    # 查詢要執行的 Playbooks
    playbooks = db.query(Playbook).filter(
        Playbook.id.in_(request.playbook_ids)
    ).all()
    
    if not playbooks:
        raise HTTPException(status_code=404, detail="No playbooks found")
    
    job_id = f"job-{uuid.uuid4().hex[:8]}"
    execution_results = []
    
    for playbook in playbooks:
        try:
            # 1. 準備 Inventory 檔案和確定目標主機名稱
            inventory_content = ""
            target_hostname = None  # 用於 playbook 的 hosts 欄位
            
            if request.inventory_id:
                # 使用指定的 Inventory
                inventory = db.query(Inventory).filter(
                    Inventory.id == request.inventory_id
                ).first()
                if not inventory or not inventory.config:
                    execution_results.append({
                        "id": playbook.id,
                        "name": playbook.name,
                        "status": "error",
                        "message": "Inventory not found or empty"
                    })
                    continue
                inventory_content = inventory.config
                
                # 從 config 中提取主機名
                config_parts = inventory.config.strip().split()
                target_hostname = config_parts[0] if config_parts else "all"
                
            else:
                # 使用 Playbook 中定義的目標
                if playbook.target_type.value == "group":
                    if not playbook.group:
                        execution_results.append({
                            "id": playbook.id,
                            "name": playbook.name,
                            "status": "error",
                            "message": "Group not specified in playbook"
                        })
                        continue
                    
                    # 查詢該 group 下的所有 inventories
                    inventories_in_group = db.query(Inventory).filter(
                        Inventory.group == playbook.group
                    ).all()
                    
                    if not inventories_in_group:
                        execution_results.append({
                            "id": playbook.id,
                            "name": playbook.name,
                            "status": "error",
                            "message": f"No inventories found in group '{playbook.group}'"
                        })
                        continue
                    
                    # 生成 inventory 內容：[group_name] 下列出所有主機
                    inventory_lines = [f"[{playbook.group}]"]
                    for inv in inventories_in_group:
                        if inv.config:
                            inventory_lines.append(inv.config)
                    
                    inventory_content = "\n".join(inventory_lines)
                    target_hostname = playbook.group
                    
                elif playbook.target_type.value == "host":
                    if not playbook.host:
                        execution_results.append({
                            "id": playbook.id,
                            "name": playbook.name,
                            "status": "error",
                            "message": "Host not specified in playbook"
                        })
                        continue
                    
                    # 從 Inventories 表中查找對應的主機配置
                    inventory_by_name = db.query(Inventory).filter(
                        Inventory.name == playbook.host
                    ).first()
                    
                    if inventory_by_name and inventory_by_name.config:
                        # 找到對應的 Inventory,使用其 config
                        inventory_content = inventory_by_name.config
                        
                        # 從 config 中提取主機名稱 (第一個單詞)
                        # 格式: hostname ansible_host=... ansible_port=...
                        config_parts = inventory_by_name.config.strip().split()
                        target_hostname = config_parts[0] if config_parts else playbook.host
                    else:
                        # 如果沒找到,嘗試作為直接的主機名使用
                        inventory_content = playbook.host
                        target_hostname = playbook.host
            
            # 2. 準備 Playbook YAML 內容
            tasks = db.query(Task).filter(
                Task.playbook_id == playbook.id,
                Task.enabled == True
            ).order_by(Task.order).all()
            
            if not tasks:
                execution_results.append({
                    "id": playbook.id,
                    "name": playbook.name,
                    "status": "error",
                    "message": "No enabled tasks found"
                })
                continue
            
            # 將 task content 轉換為 Ansible task 格式
            ansible_tasks = []
            for task in tasks:
                print(f"\n=== Processing Task {task.order} ===")
                print(f"Raw content:\n{repr(task.content)}\n")
                try:
                    # 嘗試解析 task content 為 YAML
                    task_dict = yaml.safe_load(task.content)
                    print(f"Parsed type: {type(task_dict)}")
                    print(f"Parsed value: {task_dict}\n")
                    
                    if isinstance(task_dict, dict):
                        ansible_tasks.append(task_dict)
                    else:
                        # 如果不是字典，包裝成 debug task 並記錄錯誤
                        print(f"WARNING: Task {task.order} parsed but not a dict")
                        ansible_tasks.append({
                            "name": f"Task {task.order}",
                            "debug": {"msg": str(task.content)}
                        })
                except Exception as e:
                    # 解析失敗，包裝成 debug task 並記錄錯誤
                    print(f"ERROR: Task {task.order} YAML parse failed: {str(e)}")
                    ansible_tasks.append({
                        "name": f"Task {task.order}",
                        "debug": {"msg": f"YAML Parse Error: {str(e)}\\n\\nOriginal content:\\n{task.content}"}
                    })
            
            # 構建完整的 Playbook 結構
            playbook_content = [{
                "name": playbook.name,
                "hosts": target_hostname or "all",
                "gather_facts": playbook.gather_facts,
                "tasks": ansible_tasks
            }]
            
            # 加入 extra_vars
            if request.extra_vars:
                playbook_content[0]['vars'] = request.extra_vars
            
            # 取得工作目錄設定
            working_directory = None
            extra_fields = db.query(PlaybookExtraField).filter(
                PlaybookExtraField.playbook_id == playbook.id
            ).first()
            if extra_fields and extra_fields.field_value:
                import json
                try:
                    extra_data = json.loads(extra_fields.field_value)
                    working_directory = extra_data.get('working_directory', '').strip()
                except:
                    working_directory = None
            
            # 3. 執行 Playbook (跨平台方案)
            if working_directory:
                # 使用指定的工作目錄
                is_windows = platform.system() == 'Windows'
                
                # 轉換 Windows 路徑為 WSL 路徑（如果需要）
                if is_windows and working_directory.startswith('C:'):
                    # C:\Users\... -> /mnt/c/Users/...
                    working_directory = working_directory.replace('\\', '/')
                    if ':' in working_directory:
                        drive = working_directory[0].lower()
                        rest = working_directory[2:]
                        working_directory = f"/mnt/{drive}{rest}"
                
                # 確保目錄存在
                if is_windows:
                    check_cmd = ["wsl", "test", "-d", working_directory]
                else:
                    check_cmd = ["test", "-d", working_directory]
                
                dir_check = subprocess.run(check_cmd, capture_output=True)
                if dir_check.returncode != 0:
                    execution_results.append({
                        "id": playbook.id,
                        "name": playbook.name,
                        "status": "error",
                        "message": f"Working directory does not exist: {working_directory}"
                    })
                    continue
                
                # 在工作目錄中建立 playbook.yml 和 inventory.ini
                # 注意：WSL 路徑不能用 os.path.join，直接字串拼接
                if is_windows:
                    playbook_file = f"{working_directory}/playbook.yml"
                    inventory_file = f"{working_directory}/inventory.ini"
                else:
                    playbook_file = os.path.join(working_directory, "playbook.yml")
                    inventory_file = os.path.join(working_directory, "inventory.ini")
                
                # 寫入檔案（使用 WSL 命令）
                if is_windows:
                    # 寫入 inventory
                    inventory_cmd = f"echo '{inventory_content}' > {inventory_file}"
                    subprocess.run(["wsl", "bash", "-c", inventory_cmd], check=True, encoding='utf-8', errors='replace')
                    
                    # 寫入 playbook
                    playbook_yaml = yaml.dump(
                        playbook_content, 
                        default_flow_style=False, 
                        allow_unicode=True,
                        sort_keys=False
                    )
                    playbook_cmd = f"cat > {playbook_file} << 'EOF'\n{playbook_yaml}\nEOF"
                    subprocess.run(["wsl", "bash", "-c", playbook_cmd], check=True, encoding='utf-8', errors='replace')
                else:
                    # macOS/Linux: 直接寫入
                    with open(inventory_file, 'w', encoding='utf-8') as f:
                        f.write(inventory_content)
                    with open(playbook_file, 'w', encoding='utf-8') as f:
                        yaml.dump(
                            playbook_content, f, 
                            default_flow_style=False, 
                            allow_unicode=True,
                            sort_keys=False
                        )
                
                # 執行 ansible-playbook（在工作目錄下）
                result = _execute_with_subprocess(
                    playbook_file, inventory_file, playbook, db, execution_results, working_directory
                )
                
            else:
                # 使用臨時目錄（原本的方式）
                with tempfile.TemporaryDirectory() as temp_dir:
                    # 寫入 inventory 檔案
                    inventory_file = os.path.join(temp_dir, "inventory.ini")
                    with open(inventory_file, 'w', encoding='utf-8') as f:
                        f.write(inventory_content)
                    
                    # 寫入 playbook 檔案
                    playbook_file = os.path.join(temp_dir, "playbook.yml")
                    with open(playbook_file, 'w', encoding='utf-8') as f:
                        yaml.dump(
                            playbook_content, f, 
                            default_flow_style=False, 
                            allow_unicode=True,
                            sort_keys=False
                        )
                    
                    # 使用 subprocess 執行 (Windows 使用 WSL，macOS/Linux 直接執行)
                    result = _execute_with_subprocess(
                        playbook_file, inventory_file, playbook, db, execution_results
                    )
                
        except Exception as e:
            playbook.status = ExecutionStatus.FAIL
            playbook.last_run_at = datetime.utcnow()
            db.commit()
            execution_results.append({
                "id": playbook.id,
                "name": playbook.name,
                "status": "error",
                "message": str(e)
            })
    
    return {
        "success": True,
        "data": {
            "job_id": job_id,
            "results": execution_results,
            "created_at": datetime.utcnow().isoformat()
        },
        "message": "Playbook execution completed"
    }


def _execute_with_subprocess(playbook_file, inventory_file, playbook, db, execution_results, working_directory=None):
    """使用 subprocess 執行 (傳統方案，需要安裝 Ansible CLI)"""
    try:
        # 檢測作業系統
        is_windows = platform.system() == 'Windows'
        
        # 構建命令
        if is_windows:
            # Windows: 轉換為 WSL 路徑
            # C:/Users/... -> /mnt/c/Users/...
            def win_to_wsl_path(win_path):
                # 將 Windows 路徑轉換為 WSL 路徑
                wsl_path = win_path.replace('\\', '/')
                if ':' in wsl_path:
                    # C:/Users/... -> /mnt/c/Users/...
                    drive = wsl_path[0].lower()
                    rest = wsl_path[2:]  # 跳過 "C:"
                    wsl_path = f"/mnt/{drive}{rest}"
                return wsl_path
            
            wsl_playbook = win_to_wsl_path(playbook_file)
            wsl_inventory = win_to_wsl_path(inventory_file)
            
            # 如果有工作目錄，加上 chdir
            if working_directory:
                cmd = [
                    "wsl",
                    "bash", "-c",
                    f"cd {working_directory} && ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i {wsl_inventory} {wsl_playbook}"
                ]
            else:
                cmd = [
                    "wsl",
                    "ansible-playbook",
                    "-i", wsl_inventory,
                    wsl_playbook
                ]
        else:
            # macOS/Linux: 直接使用 ansible-playbook
            if working_directory:
                cmd = [
                    "bash", "-c",
                    f"cd {working_directory} && ansible-playbook -i {inventory_file} {playbook_file}"
                ]
            else:
                cmd = [
                    "ansible-playbook",
                    "-i", inventory_file,
                    playbook_file
                ]
        
        # 執行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 分鐘超時
        )
        
        # 更新狀態
        if result.returncode == 0:
            playbook.status = ExecutionStatus.SUCCESS
            playbook.last_run_at = datetime.utcnow()
            execution_results.append({
                "id": playbook.id,
                "name": playbook.name,
                "status": "success",
                "message": "Execution completed successfully",
                "output": result.stdout[:1000] if result.stdout else "No output"
            })
        else:
            playbook.status = ExecutionStatus.FAIL
            playbook.last_run_at = datetime.utcnow()
            execution_results.append({
                "id": playbook.id,
                "name": playbook.name,
                "status": "failed",
                "message": "Execution failed",
                "error": result.stderr[:500] if result.stderr else "Unknown error",
                "output": result.stdout[:1000] if result.stdout else "No output"
            })
        
        db.commit()
        return True
        
    except subprocess.TimeoutExpired:
        playbook.status = ExecutionStatus.FAIL
        playbook.last_run_at = datetime.utcnow()
        db.commit()
        execution_results.append({
            "id": playbook.id,
            "name": playbook.name,
            "status": "timeout",
            "message": "Execution timeout (exceeded 5 minutes)"
        })
        return False
        
    except FileNotFoundError as e:
        error_msg = "Ansible not found. "
        if platform.system() == 'Windows':
            error_msg += "Please install WSL and Ansible."
        else:
            error_msg += "Please install Ansible."
        
        execution_results.append({
            "id": playbook.id,
            "name": playbook.name,
            "status": "error",
            "message": error_msg
        })
        return False


# 全局變數來儲存正在執行的 job (實際應使用 Redis 或資料庫)
active_jobs = {}


@router.post("/jobs/{job_id}/abort", response_model=dict)
def abort_job(job_id: str, db: Session = Depends(get_db)):
    """中止正在執行的 Job"""
    if job_id not in active_jobs:
        return {
            "success": False,
            "message": f"Job {job_id} not found or already completed"
        }
    
    try:
        # 標記 job 為已中止
        active_jobs[job_id]['aborted'] = True
        
        # TODO: 實際中止 Ansible 執行
        # 如果使用 subprocess,可以使用 process.terminate()
        
        return {
            "success": True,
            "message": f"Job {job_id} abort request sent",
            "data": {
                "job_id": job_id,
                "status": "aborting"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to abort job: {str(e)}"
        }


@router.get("/jobs/{job_id}/status", response_model=dict)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """獲取 Job 執行狀態"""
    if job_id not in active_jobs:
        return {
            "success": False,
            "message": f"Job {job_id} not found"
        }
    
    job_info = active_jobs[job_id]
    
    return {
        "success": True,
        "data": {
            "job_id": job_id,
            "status": job_info.get('status', 'unknown'),
            "progress": job_info.get('progress', 0),
            "results": job_info.get('results', []),
            "started_at": job_info.get('started_at'),
            "completed_at": job_info.get('completed_at')
        }
    }
