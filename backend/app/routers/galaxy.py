from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import subprocess
import json
import yaml
import os
import platform
from pathlib import Path
from app.database import get_db
from app.models import Playbook, Task

router = APIRouter()


class Collection(BaseModel):
    name: str
    version: Optional[str] = None
    source: Optional[str] = None


class RequirementsYml(BaseModel):
    collections: List[Collection]


class InstallRequest(BaseModel):
    name: str
    version: Optional[str] = None


class InstallResponse(BaseModel):
    success: bool
    message: str
    output: Optional[str] = None
    error: Optional[str] = None


def run_ansible_galaxy_command(args: List[str], timeout: int = 300) -> dict:
    """執行 ansible-galaxy 命令 (跨平台)"""
    try:
        is_windows = platform.system() == 'Windows'
        
        if is_windows:
            # Windows: 使用 WSL
            cmd = ["wsl", "ansible-galaxy"] + args
        else:
            # macOS/Linux: 直接執行
            cmd = ["ansible-galaxy"] + args
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timeout (exceeded {timeout} seconds)",
            "returncode": -1
        }
    except FileNotFoundError:
        error_msg = "Ansible not found. "
        if platform.system() == 'Windows':
            error_msg += "Please install WSL and Ansible."
        else:
            error_msg += "Please install Ansible."
        return {
            "success": False,
            "stdout": "",
            "stderr": error_msg,
            "returncode": -1
        }


def get_requirements_file_path() -> Path:
    """取得 requirements.yml 檔案路徑"""
    # 假設 requirements.yml 在專案根目錄的 ansible 資料夾
    base_path = Path(__file__).parent.parent.parent
    requirements_path = base_path / "ansible" / "requirements.yml"
    
    # 如果不存在,建立目錄和檔案
    requirements_path.parent.mkdir(parents=True, exist_ok=True)
    if not requirements_path.exists():
        # 建立預設的 requirements.yml
        default_content = {
            "collections": []
        }
        with open(requirements_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_content, f, default_flow_style=False, allow_unicode=True)
    
    return requirements_path


@router.get("/collections", response_model=dict)
def list_installed_collections():
    """列出已安裝的 collections"""
    result = run_ansible_galaxy_command(["collection", "list", "--format", "json"])
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail={
            "message": "Failed to list collections",
            "error": result["stderr"]
        })
    
    try:
        # 解析 JSON 輸出
        collections_data = json.loads(result["stdout"]) if result["stdout"] else {}
        
        # 轉換為列表格式
        collections = []
        for path, items in collections_data.items():
            for name, info in items.items():
                collections.append({
                    "name": name,
                    "version": info.get("version", "unknown"),
                    "path": path
                })
        
        return {
            "success": True,
            "data": collections
        }
    except json.JSONDecodeError:
        # 如果 JSON 解析失敗,返回空列表
        return {
            "success": True,
            "data": []
        }


@router.post("/collections/install", response_model=InstallResponse)
def install_collection(request: InstallRequest):
    """安裝單一 collection"""
    collection_spec = f"{request.name}"
    if request.version:
        collection_spec += f":{request.version}"
    
    result = run_ansible_galaxy_command([
        "collection", "install", collection_spec, "--force"
    ])
    
    return InstallResponse(
        success=result["success"],
        message="Installation completed" if result["success"] else "Installation failed",
        output=result["stdout"][:1000] if result["stdout"] else None,
        error=result["stderr"][:500] if result["stderr"] else None
    )


@router.delete("/collections/{collection_name:path}", response_model=dict)
def uninstall_collection(collection_name: str):
    """卸載 collection (需手動刪除)"""
    # ansible-galaxy 沒有內建的 uninstall 命令
    # 這裡提供資訊讓使用者知道如何手動刪除
    
    # 先列出已安裝的找到路徑
    result = run_ansible_galaxy_command(["collection", "list", "--format", "json"])
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail="Failed to list collections")
    
    try:
        collections_data = json.loads(result["stdout"]) if result["stdout"] else {}
        
        for path, items in collections_data.items():
            if collection_name in items:
                collection_path = Path(path) / collection_name.replace('.', '/')
                return {
                    "success": True,
                    "message": f"Collection found at: {collection_path}",
                    "path": str(collection_path),
                    "note": "Please manually delete this directory to uninstall"
                }
        
        raise HTTPException(status_code=404, detail="Collection not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse collection list")


@router.get("/requirements", response_model=dict)
def get_requirements():
    """讀取 requirements.yml"""
    try:
        requirements_path = get_requirements_file_path()
        
        with open(requirements_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        return {
            "success": True,
            "data": {
                "collections": content.get("collections", []),
                "roles": content.get("roles", []),
                "yaml": yaml.dump(content, default_flow_style=False, allow_unicode=True)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/requirements", response_model=dict)
def update_requirements(requirements: RequirementsYml):
    """更新 requirements.yml"""
    try:
        requirements_path = get_requirements_file_path()
        
        # 讀取現有內容保留 roles (如果有)
        existing_content = {}
        if requirements_path.exists():
            with open(requirements_path, 'r', encoding='utf-8') as f:
                existing_content = yaml.safe_load(f) or {}
        
        # 更新 collections
        content = {
            "collections": [col.dict(exclude_none=True) for col in requirements.collections]
        }
        
        # 保留 roles
        if "roles" in existing_content:
            content["roles"] = existing_content["roles"]
        
        # 寫入檔案
        with open(requirements_path, 'w', encoding='utf-8') as f:
            yaml.dump(content, f, default_flow_style=False, allow_unicode=True)
        
        return {
            "success": True,
            "message": "Requirements updated successfully",
            "data": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/requirements/install", response_model=InstallResponse)
def install_requirements():
    """執行 ansible-galaxy collection install -r requirements.yml"""
    try:
        requirements_path = get_requirements_file_path()
        
        if not requirements_path.exists():
            raise HTTPException(status_code=404, detail="requirements.yml not found")
        
        # 轉換路徑 (Windows WSL)
        if platform.system() == 'Windows':
            # C:/Users/... -> /mnt/c/Users/...
            wsl_path = str(requirements_path).replace('\\', '/')
            if ':' in wsl_path:
                drive = wsl_path[0].lower()
                rest = wsl_path[2:]
                wsl_path = f"/mnt/{drive}{rest}"
            
            result = run_ansible_galaxy_command([
                "collection", "install", "-r", wsl_path, "--force"
            ])
        else:
            result = run_ansible_galaxy_command([
                "collection", "install", "-r", str(requirements_path), "--force"
            ])
        
        return InstallResponse(
            success=result["success"],
            message="Installation completed" if result["success"] else "Installation failed",
            output=result["stdout"][:1000] if result["stdout"] else None,
            error=result["stderr"][:500] if result["stderr"] else None
        )
    except Exception as e:
        return InstallResponse(
            success=False,
            message="Installation failed",
            error=str(e)
        )


@router.get("/playbooks/{playbook_id}/dependencies", response_model=dict)
def check_playbook_dependencies(playbook_id: int, db: Session = Depends(get_db)):
    """檢查 Playbook 依賴的 collections 是否已安裝"""
    # 查詢 Playbook
    playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    
    # 取得所有 tasks
    tasks = db.query(Task).filter(
        Task.playbook_id == playbook_id,
        Task.enabled == True
    ).all()
    
    # 分析使用的 modules (簡單的模式匹配)
    used_modules = set()
    for task in tasks:
        try:
            task_dict = yaml.safe_load(task.content)
            if isinstance(task_dict, dict):
                # 找出可能是 module 的 key (例如 community.docker.docker_container)
                for key in task_dict.keys():
                    if '.' in key and key not in ['name', 'vars', 'when', 'register']:
                        # 提取 collection 名稱 (例如 community.docker)
                        parts = key.split('.')
                        if len(parts) >= 2:
                            collection = f"{parts[0]}.{parts[1]}"
                            used_modules.add(collection)
        except:
            pass
    
    # 取得已安裝的 collections
    result = run_ansible_galaxy_command(["collection", "list", "--format", "json"])
    installed_collections = set()
    
    if result["success"]:
        try:
            collections_data = json.loads(result["stdout"]) if result["stdout"] else {}
            for path, items in collections_data.items():
                installed_collections.update(items.keys())
        except:
            pass
    
    # 檢查依賴
    dependencies = []
    for module in used_modules:
        dependencies.append({
            "collection": module,
            "satisfied": module in installed_collections,
            "required": True
        })
    
    return {
        "success": True,
        "data": {
            "playbook_id": playbook_id,
            "playbook_name": playbook.name,
            "dependencies": dependencies,
            "all_satisfied": all(d["satisfied"] for d in dependencies)
        }
    }
