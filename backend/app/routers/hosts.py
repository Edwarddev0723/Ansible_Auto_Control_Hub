from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Host
from app.schemas.host import HostCreate, HostResponse

router = APIRouter()

@router.get("/", response_model=dict)
def get_hosts(db: Session = Depends(get_db)):
    """獲取所有 Hosts"""
    hosts = db.query(Host).all()
    items = [HostResponse.model_validate(h) for h in hosts]
    return {
        "success": True,
        "data": items
    }

@router.post("/", response_model=dict, status_code=201)
def create_host(host: HostCreate, db: Session = Depends(get_db)):
    """創建 Host"""
    db_host = Host(address=host.address)
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    
    return {
        "success": True,
        "data": HostResponse.model_validate(db_host),
        "message": "Host 創建成功"
    }
