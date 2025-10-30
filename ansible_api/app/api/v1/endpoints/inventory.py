from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.base import get_db
from app.schemas import host as host_schema
from app.api.v1.deps import get_current_developer_user, get_current_admin_user

router = APIRouter()

@router.post("/", response_model=host_schema.Host, status_code=status.HTTP_201_CREATED)
def create_host(
    *,
    db: Session = Depends(get_db),
    host_in: host_schema.HostCreate,
    current_user: models.User = Depends(get_current_admin_user) # 只有 Admin 能新增主機
):
    """
    (Admin) 新增一台伺服器 (Host) 到 Inventory。
    """
    db_host = models.Host(**host_in.dict())
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

@router.get("/", response_model=List[host_schema.Host])
def read_hosts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_developer_user) # Dev 以上可觀看
):
    """
    (Dev+) 獲取所有伺服器列表。
    """
    return db.query(models.Host).all()

@router.get("/{host_id}", response_model=host_schema.Host)
def read_host(
    *,
    db: Session = Depends(get_db),
    host_id: int,
    current_user: models.User = Depends(get_current_developer_user)
):
    """
    (Dev+) 獲取單一伺服器資訊。
    """
    db_host = db.query(models.Host).filter(models.Host.id == host_id).first()
    if not db_host:
        raise HTTPException(status_code=404, detail="Host not found")
    return db_host

@router.put("/{host_id}", response_model=host_schema.Host)
def update_host(
    *,
    db: Session = Depends(get_db),
    host_id: int,
    host_in: host_schema.HostCreate, # 用 Create schema 來更新
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    (Admin) 更新伺服器資訊。
    """
    db_host = db.query(models.Host).filter(models.Host.id == host_id).first()
    if not db_host:
        raise HTTPException(status_code=404, detail="Host not found")
    
    update_data = host_in.dict()
    for key, value in update_data.items():
        setattr(db_host, key, value)
        
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host

@router.delete("/{host_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_host(
    *,
    db: Session = Depends(get_db),
    host_id: int,
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    (Admin) 刪除伺服器。
    """
    db_host = db.query(models.Host).filter(models.Host.id == host_id).first()
    if not db_host:
        raise HTTPException(status_code=404, detail="Host not found")
        
    db.delete(db_host)
    db.commit()
    return