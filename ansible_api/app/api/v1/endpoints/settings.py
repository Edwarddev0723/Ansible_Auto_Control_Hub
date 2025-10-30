from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.v1.deps import get_current_admin_user
from app.db import models

router = APIRouter()

class SystemSettings(BaseModel):
    ssh_key_name: str
    vault_password_set: bool
    
class SSHKey(BaseModel):
    name: str
    public_key: str
    fingerprint: str

@router.get("/security", response_model=SystemSettings)
def get_security_settings(
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    (Admin) (模擬) 獲取系統安全設定 (如 SSH 金鑰、Vault 狀態)。
    """
    # 這裡是模擬，真實情況應從安全儲存中讀取
    return SystemSettings(ssh_key_name="default_admin_key", vault_password_set=True)

@router.post("/ssh-keys", response_model=SSHKey)
def add_ssh_key(
    key_in: SSHKey,
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    (Admin) (模擬) 新增用於 Ansible 的 SSH 金鑰。
    """
    # 這裡的真實邏輯是將金鑰儲存到安全的金鑰管理器 (Vault)
    print(f"Adding new SSH key: {key_in.name}")
    return key_in