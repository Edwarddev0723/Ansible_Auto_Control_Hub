from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.db.models import DeployJobStatus
from .user import User
from .playbook import Playbook

class DeploymentCreate(BaseModel):
    playbook_id: int
    host_ids: List[int] # 執行部署的目標主機 ID 列表

class Deployment(BaseModel):
    id: int
    status: DeployJobStatus
    start_time: datetime
    end_time: Optional[datetime]
    log_output: str
    
    executor: User # 顯示執行者資訊
    playbook: Playbook # 顯示 playbook 資訊

    class Config:
        from_attributes = True