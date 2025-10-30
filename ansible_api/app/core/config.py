import os
from dotenv import load_dotenv
from typing import Optional

# 載入 .env 檔（若存在）
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    # AI Core (external project) settings - 當此值存在時，會嘗試呼叫外部 AI Core API
    AI_CORE_URL: Optional[str] = os.getenv("AI_CORE_URL")
    # 若外部 AI Core 需要 API key，可放在這裡；否則可留空
    AI_CORE_API_KEY: Optional[str] = os.getenv("AI_CORE_API_KEY")

settings = Settings()