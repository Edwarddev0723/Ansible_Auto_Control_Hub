from pydantic import BaseModel, EmailStr
from app.db.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.viewer

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True # pydantic v2: use from_attributes instead of orm_mode