from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.base import get_db
from app.schemas import playbook as playbook_schema
from app.api.v1.deps import get_current_developer_user, get_current_admin_user

router = APIRouter()

@router.post("/", response_model=playbook_schema.Playbook, status_code=status.HTTP_201_CREATED)
def create_playbook(
    *,
    db: Session = Depends(get_db),
    playbook_in: playbook_schema.PlaybookCreate,
    current_user: models.User = Depends(get_current_developer_user) # Dev 以上可建立
):
    """
    (Dev+) 從無到有建立一個新的 Playbook (手動模式)。
    """
    db_playbook = models.Playbook(
        name=playbook_in.name,
        description=playbook_in.description,
        content=playbook_in.content,
        created_by=f"user:{current_user.email}"
    )
    db.add(db_playbook)
    db.commit()
    db.refresh(db_playbook)
    return db_playbook

@router.get("/", response_model=List[playbook_schema.Playbook])
def read_playbooks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_developer_user)
):
    """
    (Dev+) 獲取所有 Playbook 列表。
    """
    return db.query(models.Playbook).all()

@router.get("/{playbook_id}", response_model=playbook_schema.Playbook)
def read_playbook(
    *,
    db: Session = Depends(get_db),
    playbook_id: int,
    current_user: models.User = Depends(get_current_developer_user)
):
    """
    (Dev+) 獲取單一 Playbook 內容。
    """
    db_playbook = db.query(models.Playbook).filter(models.Playbook.id == playbook_id).first()
    if not db_playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    return db_playbook

@router.put("/{playbook_id}", response_model=playbook_schema.Playbook)
def update_playbook(
    *,
    db: Session = Depends(get_db),
    playbook_id: int,
    playbook_in: playbook_schema.PlaybookUpdate,
    current_user: models.User = Depends(get_current_developer_user) # Dev 以上可更新
):
    """
    (Dev+) 更新一個現有的 Playbook (手動編輯)。
    """
    db_playbook = db.query(models.Playbook).filter(models.Playbook.id == playbook_id).first()
    if not db_playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
        
    update_data = playbook_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_playbook, key, value)
        
    db.add(db_playbook)
    db.commit()
    db.refresh(db_playbook)
    return db_playbook

@router.delete("/{playbook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playbook(
    *,
    db: Session = Depends(get_db),
    playbook_id: int,
    current_user: models.User = Depends(get_current_admin_user) # 只有 Admin 能刪除
):
    """
    (Admin) 刪除一個 Playbook。
    """
    db_playbook = db.query(models.Playbook).filter(models.Playbook.id == playbook_id).first()
    if not db_playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
        
    db.delete(db_playbook)
    db.commit()
    return