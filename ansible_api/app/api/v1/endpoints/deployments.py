from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.base import get_db
from app.schemas import deployment as deployment_schema
from app.services.ansible_runner import run_ansible_playbook_async
from app.api.v1.deps import get_current_developer_user

router = APIRouter()

@router.post("/", response_model=deployment_schema.Deployment, status_code=status.HTTP_202_ACCEPTED)
def execute_deployment(
    *,
    db: Session = Depends(get_db),
    deployment_in: deployment_schema.DeploymentCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_developer_user) # Dev 以上可執行
):
    """
    (Dev+) 執行一個部署任務。
    
    這會立即返回一個 "pending" 狀態的 Job，並在背景執行 Ansible。
    """
    db_playbook = db.query(models.Playbook).filter(models.Playbook.id == deployment_in.playbook_id).first()
    if not db_playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    
    # (可選) 檢查 Host IDs 是否都存在...
    
    db_job = models.DeployJob(
        playbook_id=deployment_in.playbook_id,
        user_id=current_user.id,
        status=models.DeployJobStatus.pending
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # 使用後台任務執行實際的 Ansible 命令
    background_tasks.add_task(
        run_ansible_playbook_async, 
        job_id=db_job.id, 
        playbook_content=db_playbook.content, 
        host_ids=deployment_in.host_ids
    )

    return db_job

@router.get("/", response_model=List[deployment_schema.Deployment])
def read_deployment_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_developer_user) # Dev 以上可看紀錄
):
    """
    (Dev+) (模組 5) 獲取所有部署的歷史紀錄。
    """
    jobs = db.query(models.DeployJob).order_by(models.DeployJob.start_time.desc()).all()
    return jobs

@router.get("/{job_id}", response_model=deployment_schema.Deployment)
def get_deployment_status_and_logs(
    *,
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_developer_user)
):
    """
    (Dev+) (模組 5) 獲取單一部署任務的狀態與日誌 (供前端輪詢)。
    """
    db_job = db.query(models.DeployJob).filter(models.DeployJob.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job