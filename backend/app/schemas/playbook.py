from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PlaybookType(str, Enum):
    Machine = "Machine"
    Other = "Other"

class ExecutionStatus(str, Enum):
    Success = "Success"
    Fail = "Fail"
    NotStart = "Not start"

class TaskBase(BaseModel):
    enabled: bool = True
    content: str

class TaskCreate(TaskBase):
    order: int = 0

class TaskResponse(TaskBase):
    id: int
    order: int

    class Config:
        from_attributes = True

class PlaybookMainBase(BaseModel):
    hosts: str
    gather_facts: bool = False

class PlaybookBase(BaseModel):
    name: str
    type: PlaybookType = PlaybookType.Machine
    target_type: str = "group"  # 'group' or 'host'
    group: Optional[str] = None
    host: Optional[str] = None

class PlaybookCreate(PlaybookBase):
    main: PlaybookMainBase
    tasks: List[TaskCreate] = []
    extra_fields: Optional[Dict[str, Any]] = None

class PlaybookUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[PlaybookType] = None
    target_type: Optional[str] = None
    group: Optional[str] = None
    host: Optional[str] = None
    main: Optional[PlaybookMainBase] = None
    tasks: Optional[List[TaskCreate]] = None
    extra_fields: Optional[Dict[str, Any]] = None

class PlaybookListResponse(PlaybookBase):
    id: int
    status: ExecutionStatus
    last_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PlaybookDetailResponse(PlaybookListResponse):
    main: PlaybookMainBase
    tasks: List[TaskResponse]
    extra_fields: Optional[Dict[str, Any]] = None

class PlaybookExecuteRequest(BaseModel):
    playbook_ids: List[int]
    inventory_id: Optional[int] = None
    extra_vars: Optional[Dict[str, Any]] = None
