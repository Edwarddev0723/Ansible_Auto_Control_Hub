from pydantic import BaseModel

class HostBase(BaseModel):
    name: str
    ip_address: str
    group: str = "all"
    ssh_port: int = 22
    ssh_user: str = "root"

class HostCreate(HostBase):
    pass

class Host(HostBase):
    id: int

    class Config:
        from_attributes = True