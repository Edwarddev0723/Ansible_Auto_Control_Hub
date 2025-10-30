from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models
from app.db.base import get_db
from app.schemas import token as token_schema

# 這是 FastAPI 會在 /docs 介面上顯示的登入 URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    解析 JWT token 並返回當前登入的使用者。
    這是一個依賴項，可用於保護需要登入的路由。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = token_schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# --- (模組 1) 權限管理依賴 ---

def get_current_developer_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    確保使用者至少是「開發者」
    """
    if current_user.role not in [models.UserRole.admin, models.UserRole.developer]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have developer privileges"
        )
    return current_user

def get_current_admin_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    確保使用者必須是「管理員」
    """
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have admin privileges"
        )
    return current_user