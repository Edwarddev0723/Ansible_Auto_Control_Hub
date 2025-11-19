import os

# 建立 app/models/__init__.py
models_content = """from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class TargetType(str, enum.Enum):
    GROUP = "group"
    HOST = "host"

class PlaybookType(str, enum.Enum):
    MACHINE = "Machine"
    OTHER = "Other"

class ExecutionStatus(str, enum.Enum):
    SUCCESS = "Success"
    FAIL = "Fail"
    NOT_START = "Not start"

class ServerStatus(str, enum.Enum):
    ON = "On"
    OFF = "Off"

class Playbook(Base):
    __tablename__ = "playbooks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    target_type = Column(Enum(TargetType), nullable=False, default=TargetType.GROUP)
    group = Column(String(255), nullable=True)
    host = Column(String(255), nullable=True)
    gather_facts = Column(Boolean, default=False)
    type = Column(Enum(PlaybookType), default=PlaybookType.MACHINE)
    type_other = Column(String(255), nullable=True)
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.NOT_START)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tasks = relationship("Task", back_populates="playbook", cascade="all, delete-orphan")
    extra_fields = relationship("PlaybookExtraField", back_populates="playbook", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    playbook_id = Column(Integer, ForeignKey("playbooks.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    playbook = relationship("Playbook", back_populates="tasks")

class PlaybookExtraField(Base):
    __tablename__ = "playbook_extra_fields"
    id = Column(Integer, primary_key=True, index=True)
    playbook_id = Column(Integer, ForeignKey("playbooks.id", ondelete="CASCADE"), nullable=False)
    field_value = Column(Text, nullable=False)
    playbook = relationship("Playbook", back_populates="extra_fields")

class Inventory(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    status = Column(Enum(ServerStatus), default=ServerStatus.OFF)
    ssh_status = Column(String(50), default="Unconnected")
    group = Column(String(255), nullable=False, default="Default")
    config = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Host(Base):
    __tablename__ = "hosts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    ip_address = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
"""

with open('app/models/__init__.py', 'w', encoding='utf-8') as f:
    f.write(models_content)
    
print("Models file created!")
