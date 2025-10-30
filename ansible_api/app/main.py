from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.db.base import Base, engine

# 這是為了在開發/演示時快速建立資料表
# 在正式環境中，您應該使用 Alembic 進行資料庫遷移 (migration)
def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ansible 自動化網站部署管理系統 API",
    description="一個整合 Ansible 與 AI 助理的 API 平台",
    version="1.0.0"
)

# 設定 CORS (跨來源資源共用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在正式環境中，應指定前端的來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 在應用程式啟動時建立資料表
@app.on_event("startup")
def on_startup():
    create_tables()

# 包含 v1 版本的 API 路由
app.include_router(api_router, prefix="/api/v1")

# 根路由 (用於健康檢查)
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to Ansible API"}