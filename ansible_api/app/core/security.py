from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings

# 密碼雜湊
# 使用 pbkdf2_sha256 作為預設密碼雜湊演算法，避免依賴 bcrypt C 擴充或其 72-byte 限制。
# 若你想使用更現代的 Argon2，可安裝 argon2-cffi 並把 schemes 改為 ["argon2"].
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """產生密碼雜湊"""
    return pwd_context.hash(password)

# JWT 權杖
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """建立 JWT Access Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt