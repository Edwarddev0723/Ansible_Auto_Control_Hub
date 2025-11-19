"""
FastAPI Backend Setup Script
自動生成完整的 FastAPI 後端結構
"""
import os

def create_file(path, content):
    """建立檔案並寫入內容"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

# 1. 建立 app/database.py
database_content = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://ansible_user:ansible_pass@localhost:3306/ansible_hub')

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

create_file('app/database.py', database_content)
print('Setup script created database.py')
