from pydantic import BaseModel
from typing import Optional

class PlaybookBase(BaseModel):
    name: str
    description: Optional[str] = None

class PlaybookCreate(PlaybookBase):
    content: str  # 手動從無到有建立時必須提供

class PlaybookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None # 允許只更新內容

class Playbook(PlaybookBase):
    id: int
    content: str 
    created_by: str

    class Config:
        from_attributes = True