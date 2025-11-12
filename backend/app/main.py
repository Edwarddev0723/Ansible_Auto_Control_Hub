from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inventories, playbooks, groups, hosts, ai_chat, galaxy
from app.database import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ansible Auto Control Hub API", version="1.0.0")

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(inventories.router, prefix="/api/inventories", tags=["inventories"])
app.include_router(playbooks.router, prefix="/api/playbooks", tags=["playbooks"])
app.include_router(groups.router, prefix="/api/groups", tags=["groups"])
app.include_router(hosts.router, prefix="/api/hosts", tags=["hosts"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["ai"])
app.include_router(galaxy.router, prefix="/api/galaxy", tags=["galaxy"])

@app.get("/")
def read_root():
    return {"message": "Ansible Auto Control Hub API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
