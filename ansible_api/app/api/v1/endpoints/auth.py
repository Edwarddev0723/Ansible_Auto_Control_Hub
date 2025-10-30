from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.base import get_db
from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.core import security
from app.api.v1.deps import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    使用者登入以獲取 JWT Token。
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/create", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: user_schema.UserCreate,
    admin_user: models.User = Depends(get_current_admin_user) # 只有 Admin 能建立使用者
):
    """
    (Admin) 建立新使用者。
    """
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=user_schema.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    獲取當前登入使用者的資訊。
    """
    return current_user

@router.get("/users", response_model=List[user_schema.User])
def read_users(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user) # 只有 Admin 能看列表
):
    """
    (Admin) 獲取所有使用者列表。
    """
    return db.query(models.User).all()