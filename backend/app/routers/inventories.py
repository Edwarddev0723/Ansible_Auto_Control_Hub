from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
import paramiko
import socket
from pydantic import BaseModel

router = APIRouter()

@router.get("/", response_model=dict)
def get_inventories(
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db)
):
    """獲取 Inventory 列表"""
    query = db.query(Inventory)
    
    if search:
        query = query.filter(Inventory.name.contains(search))
    
    total = query.count()
    inventories = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # 轉換為 Pydantic schemas
    items = [InventoryResponse.model_validate(inv) for inv in inventories]
    
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

@router.get("/{inventory_id}", response_model=dict)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """獲取單一 Inventory"""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    return {
        "success": True,
        "data": InventoryResponse.model_validate(inventory)
    }

@router.post("/", response_model=dict, status_code=201)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    """創建 Inventory"""
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    
    return {
        "success": True,
        "data": InventoryResponse.model_validate(db_inventory),
        "message": "Inventory 創建成功"
    }

@router.put("/{inventory_id}", response_model=dict)
def update_inventory(
    inventory_id: int,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db)
):
    """更新 Inventory"""
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    for key, value in inventory.dict(exclude_unset=True).items():
        setattr(db_inventory, key, value)
    
    db.commit()
    db.refresh(db_inventory)
    
    return {
        "success": True,
        "data": InventoryResponse.model_validate(db_inventory),
        "message": "Inventory 更新成功"
    }

@router.delete("/{inventory_id}", response_model=dict)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """刪除 Inventory"""
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    db.delete(db_inventory)
    db.commit()
    
    return {
        "success": True,
        "message": "Inventory 刪除成功"
    }

class SSHTestRequest(BaseModel):
    inventory_ids: List[int]

@router.post("/test-ssh", response_model=dict)
def test_ssh_connection(request: SSHTestRequest, db: Session = Depends(get_db)):
    """測試 SSH 連線"""
    results = []
    
    for inventory_id in request.inventory_ids:
        inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inventory:
            results.append({
                "id": inventory_id,
                "name": "Unknown",
                "status": "error",
                "message": "Inventory not found"
            })
            continue
        
        # 解析 inventory config 獲取 SSH 資訊
        # 格式: server1 ansible_ssh_host=192.168.1.100 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=password
        # 也支援簡寫: ansible_host, ansible_port, ansible_user, ansible_password
        try:
            config_parts = inventory.config.split() if inventory.config else []
            ssh_host = None
            ssh_port = 22
            ssh_user = None
            ssh_pass = None
            
            for part in config_parts:
                # 支援完整格式和簡寫格式
                if part.startswith('ansible_ssh_host=') or part.startswith('ansible_host='):
                    ssh_host = part.split('=', 1)[1]
                elif part.startswith('ansible_ssh_port=') or part.startswith('ansible_port='):
                    ssh_port = int(part.split('=', 1)[1])
                elif part.startswith('ansible_ssh_user=') or part.startswith('ansible_user='):
                    ssh_user = part.split('=', 1)[1]
                elif part.startswith('ansible_ssh_pass=') or part.startswith('ansible_password='):
                    ssh_pass = part.split('=', 1)[1]
            
            if not ssh_host:
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "error",
                    "message": "SSH host not configured"
                })
                continue
            
            # 檢查必要的 SSH 參數
            if not ssh_user:
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "error",
                    "message": "SSH user not configured (use ansible_ssh_user or ansible_user)"
                })
                continue
            
            if not ssh_pass:
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "error",
                    "message": "SSH password not configured (use ansible_ssh_pass or ansible_password)"
                })
                continue
            
            # 測試 SSH 連線
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                client.connect(
                    hostname=ssh_host,
                    port=ssh_port,
                    username=ssh_user,  # 使用從 config 解析的使用者名稱
                    password=ssh_pass,
                    timeout=5
                )
                
                # 執行簡單命令測試
                stdin, stdout, stderr = client.exec_command('echo "SSH Test Successful"')
                output = stdout.read().decode().strip()
                
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "success",
                    "message": f"Connection successful: {output}"
                })
                
                # 更新 ssh_status 為 Connected
                inventory.ssh_status = "Connected"
                db.commit()
                
            except paramiko.AuthenticationException:
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "error",
                    "message": "Authentication failed"
                })
                inventory.ssh_status = "Authentication Failed"
                db.commit()
                
            except socket.timeout:
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "error",
                    "message": "Connection timeout"
                })
                inventory.ssh_status = "Timeout"
                db.commit()
                
            except Exception as e:
                results.append({
                    "id": inventory.id,
                    "name": inventory.name,
                    "status": "error",
                    "message": str(e)
                })
                inventory.ssh_status = "Connection Failed"
                db.commit()
                
            finally:
                client.close()
                
        except Exception as e:
            results.append({
                "id": inventory.id,
                "name": inventory.name,
                "status": "error",
                "message": f"Config parsing error: {str(e)}"
            })
    
    return {
        "success": True,
        "data": results,
        "message": f"Tested {len(results)} inventory connections"
    }
