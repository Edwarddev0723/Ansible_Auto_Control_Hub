from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ServerStatus(str, Enum):
    ON = "On"
    OFF = "Off"

class InventoryBase(BaseModel):
    name: str
    status: ServerStatus = ServerStatus.OFF
    ssh_status: str = "Unconnected"  # 改為字串類型
    group: str = "Default"  # 新增 group 欄位
    config: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ServerStatus] = None
    ssh_status: Optional[str] = None  # 改為字串類型
    group: Optional[str] = None  # 新增 group 欄位
    config: Optional[str] = None

class InventoryResponse(InventoryBase):
    id: int
    group: str  # 新增 group 欄位
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
