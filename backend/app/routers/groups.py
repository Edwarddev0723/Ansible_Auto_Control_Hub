from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Group
from app.schemas.group import GroupCreate, GroupResponse

router = APIRouter()

@router.get("/", response_model=dict)
def get_groups(db: Session = Depends(get_db)):
    """獲取所有 Groups"""
    groups = db.query(Group).all()
    items = [GroupResponse.model_validate(g) for g in groups]
    return {
        "success": True,
        "data": items
    }

@router.post("/", response_model=dict, status_code=201)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    """創建 Group"""
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return {
        "success": True,
        "data": GroupResponse.model_validate(db_group),
        "message": "Group 創建成功"
    }

@router.delete("/{group_id}", response_model=dict)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """刪除 Group"""
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(db_group)
    db.commit()
    
    return {
        "success": True,
        "message": "Group 刪除成功"
    }
