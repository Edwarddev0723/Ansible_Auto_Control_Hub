from pydantic import BaseModel
from datetime import datetime

class HostBase(BaseModel):
    address: str

class HostCreate(HostBase):
    pass

class HostResponse(HostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
