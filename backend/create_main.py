# 建立 app/main.py
main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inventories, playbooks, groups, hosts
from app.database import engine, Base

# 建立資料表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ansible Auto Control Hub API", version="1.0.0")

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(inventories.router, prefix="/api/inventories", tags=["inventories"])
app.include_router(playbooks.router, prefix="/api/playbooks", tags=["playbooks"])
app.include_router(groups.router, prefix="/api/groups", tags=["groups"])
app.include_router(hosts.router, prefix="/api/hosts", tags=["hosts"])

@app.get("/")
def read_root():
    return {"message": "Ansible Auto Control Hub API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
"""

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(main_content)
print("Main app created!")
