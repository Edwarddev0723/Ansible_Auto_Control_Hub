from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Playbook, Task, PlaybookExtraField
from app.schemas.playbook import (
    PlaybookCreate, PlaybookUpdate, PlaybookListResponse, 
    PlaybookDetailResponse, PlaybookExecuteRequest
)
import json

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
    
    # 轉換為 dict
    extra_dict = {field.key: field.value for field in extra_fields}
    
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
        for key, value in playbook.extra_fields.items():
            db_field = PlaybookExtraField(
                playbook_id=db_playbook.id,
                key=key,
                value=str(value)
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
        db.query(PlaybookExtraField).filter(
            PlaybookExtraField.playbook_id == playbook_id
        ).delete()
        for key, value in playbook.extra_fields.items():
            db_field = PlaybookExtraField(
                playbook_id=playbook_id,
                key=key,
                value=str(value)
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
    """執行 Playbooks (模擬)"""
    # TODO: 實際執行 Ansible playbook 的邏輯
    
    playbooks = db.query(Playbook).filter(
        Playbook.id.in_(request.playbook_ids)
    ).all()
    
    if not playbooks:
        raise HTTPException(status_code=404, detail="No playbooks found")
    
    # 模擬執行結果
    import uuid
    from datetime import datetime
    
    job_id = f"job-{uuid.uuid4().hex[:8]}"
    
    return {
        "success": True,
        "data": {
            "job_id": job_id,
            "status": "queued",
            "playbooks": [
                {
                    "id": p.id,
                    "name": p.name,
                    "status": "queued"
                } for p in playbooks
            ],
            "created_at": datetime.utcnow().isoformat()
        },
        "message": "Playbook 執行已排程"
    }
