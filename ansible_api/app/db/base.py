from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoSuchModuleError
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# 嘗試使用設定的 DATABASE_URL 建立資料庫引擎；若缺少 driver，退回至 sqlite 開發檔案
def _create_engine_with_fallback(database_url: str):
    try:
        # 對 sqlite 給予特別的 connect_args
        if database_url.startswith("sqlite"):
            return create_engine(database_url, connect_args={"check_same_thread": False})

        # 其他（例如 MySQL、Postgres）使用 pool_pre_ping
        return create_engine(database_url, pool_pre_ping=True)
    except NoSuchModuleError as e:
        logger.warning("Database driver for URL %s not available: %s. Falling back to sqlite.", database_url, e)
    except ImportError as e:
        logger.warning("Import error when loading database driver for %s: %s. Falling back to sqlite.", database_url, e)
    except Exception as e:
        logger.warning("Unexpected error creating engine for %s: %s. Falling back to sqlite.", database_url, e)

    # fallback
    fallback = "sqlite:///./ansible_api.db"
    logger.info("Using fallback database: %s", fallback)
    return create_engine(fallback, connect_args={"check_same_thread": False})


engine = _create_engine_with_fallback(settings.DATABASE_URL)

# 建立資料庫 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Declarative Base
Base = declarative_base()

# FastAPI 依賴注入 (Dependency Injection)
def get_db():
    """
    提供一個資料庫 session 給 API 路由。
    確保 session 在請求結束後總是會被關閉。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()