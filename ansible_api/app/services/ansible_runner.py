import asyncio
import datetime
from app.db.base import SessionLocal
from app.db import models

async def run_ansible_playbook_async(job_id: int, playbook_content: str, host_ids: list[int]):
    """
    (模擬) 異步執行 Ansible Playbook。
    這是一個背景任務，它會更新資料庫中的 Job 狀態和日誌。
    """
    
    # 在背景任務中，必須建立自己的 DB session
    db = SessionLocal()
    try:
        # 1. 更新 Job 狀態為 "running"
        job = db.query(models.DeployJob).filter(models.DeployJob.id == job_id).first()
        if not job:
            print(f"Error: Job {job_id} not found.")
            return

        job.status = models.DeployJobStatus.running
        job.log_output = "--- [MOCK] Ansible Run Started ---\n"
        job.log_output += f"Playbook:\n{playbook_content}\n"
        job.log_output += f"Target Host IDs: {host_ids}\n"
        db.commit()

        # 2. 【真實邏輯】
        # 在這裡，您會：
        # a. 根據 host_ids 從資料庫查詢 IP 和連線資訊，產生一個暫時的 inventory 檔案。
        # b. 將 playbook_content 寫入一個暫時的 .yml 檔案。
        # c. 呼叫 `ansible_runner.run_async()` 
        #    並傳入 inventory 和 playbook 路徑。
        # d. 監聽 `ansible_runner` 的事件 (stdout, stderr) 並收集日誌。
        
        # 【模擬邏輯】
        # 我們用 sleep 模擬 10 秒鐘的執行時間
        await asyncio.sleep(10)
        
        # 模擬日誌
        mock_log = """
PLAY [Simulate Web Server Deploy] ********************************************

TASK [Gathering Facts] *******************************************************
ok: [192.168.1.10]
ok: [192.168.1.11]

TASK [Install Nginx] *********************************************************
changed: [192.168.1.10]
changed: [192.168.1.11]

PLAY RECAP *******************************************************************
192.168.1.10 : ok=2    changed=1    unreachable=0    failed=0    skipped=0
192.168.1.11 : ok=2    changed=1    unreachable=0    failed=0    skipped=0

--- [MOCK] Ansible Run Finished ---
"""
        # 3. 執行完成，更新 Job 狀態和最終日誌
        job.status = models.DeployJobStatus.success # (假設成功)
        job.end_time = datetime.datetime.utcnow()
        job.log_output += mock_log
        db.commit()

    except Exception as e:
        # 4. 處理錯誤
        if 'job' in locals() and db.is_active:
            job.status = models.DeployJobStatus.failed
            job.end_time = datetime.datetime.utcnow()
            job.log_output += f"\n--- [ERROR] ---\n{str(e)}"
            db.commit()
    finally:
        db.close()