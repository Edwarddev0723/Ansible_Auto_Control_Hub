from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
import datetime

# --- (模組 1) 使用者與權限 ---
class UserRole(str, enum.Enum):
    admin = "admin"
    developer = "developer"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # 為 String 指定長度
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    # 使用 native_enum 效能更好
    role = Column(Enum(UserRole, native_enum=True), default=UserRole.viewer, nullable=False)
    
    jobs = relationship("DeployJob", back_populates="executor")

# --- (模組 2) 伺服器 (Inventory) ---
class Host(Base):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True, index=True)
    # 為 String 指定長度
    name = Column(String(255), index=True, nullable=False)
    ip_address = Column(String(45), unique=True, nullable=False) # 45 for IPv6
    group = Column(String(100), default="all", index=True)
    ssh_port = Column(Integer, default=22)
    ssh_user = Column(String(100), default="root")
    
# --- (模組 3) Playbook 管理 ---
class Playbook(Base):
    __tablename__ = "playbooks"
    id = Column(Integer, primary_key=True, index=True)
    # 為 String 指定長度
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text)
    content = Column(Text, nullable=False) # Text 型別不需要長度
    created_by = Column(String(255), nullable=False) 

# --- (模組 4 & 5) 部署任務與紀錄 ---
class DeployJobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"

class DeployJob(Base):
    __tablename__ = "deploy_jobs"
    id = Column(Integer, primary_key=True, index=True)
    
    playbook_id = Column(Integer, ForeignKey("playbooks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 使用 native_enum 效能更好
    status = Column(Enum(DeployJobStatus, native_enum=True), default=DeployJobStatus.pending, nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    
    log_output = Column(Text, default="") # Text 型別不需要長度
    
    executor = relationship("User", back_populates="jobs")
    playbook = relationship("Playbook")
    ai_task = relationship("AiTask", back_populates="job", uselist=False)

# --- (模組 7) AI 助理任務 ---
class AiTask(Base):
    __tablename__ = "ai_tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_prompt = Column(Text, nullable=False)
    generated_playbook_content = Column(Text, nullable=False)
    
    job_id = Column(Integer, ForeignKey("deploy_jobs.id"), nullable=True)
    job = relationship("DeployJob", back_populates="ai_task")