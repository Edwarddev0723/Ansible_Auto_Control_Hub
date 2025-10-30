"""AI service client

這個模組會先嘗試呼叫外部 AI core（由另一個專案提供的 API），
若沒有設定 `AI_CORE_URL` 或遠端呼叫失敗，則回退到內建的 mock generator。
"""

from typing import Optional
import httpx
from app.core.config import settings


async def _mock_generate(prompt: str) -> str:
  """保留原本的 mock 行為作為 fallback。"""
  mock_yaml = f"""
# AI Generated Playbook for: "{prompt}"
# (This is a mock response)
- name: AI Generated Task based on prompt
  hosts: all
  become: yes
  tasks:
"""
  if "update" in prompt.lower() or "upgrade" in prompt.lower():
    mock_yaml += """
  - name: Update all packages
    ansible.builtin.apt:
    update_cache: yes
    upgrade: dist
"""
  elif "install nginx" in prompt.lower():
    mock_yaml += """
  - name: Install Nginx
    ansible.builtin.apt:
    name: nginx
    state: present
"""
  elif "restart" in prompt.lower():
    service = "nginx"
    if "database" in prompt.lower():
      service = "mysql"
    mock_yaml += f"""
  - name: Restart service {service}
    ansible.builtin.service:
    name: {service}
    state: restarted
"""
  else:
    mock_yaml += """
  - name: Debug prompt
    ansible.builtin.debug:
    msg: "AI could not determine a specific action for your prompt."
"""
  return mock_yaml


async def generate_playbook_from_prompt(prompt: str) -> str:
  """根據 prompt 產生 playbook。

  行為:
  - 若 `settings.AI_CORE_URL` 設定存在，會做 POST 請求到該 URL 的 `/generate_playbook` endpoint (JSON)，
    並期待回傳 JSON 格式 {"playbook": "...yaml..."}。
  - 若未設定或 HTTP 呼叫失敗，回退至本地 mock。
  """

  ai_url: Optional[str] = settings.AI_CORE_URL
  if not ai_url:
    return await _mock_generate(prompt)

  endpoint = ai_url.rstrip("/") + "/generate_playbook"
  headers = {"Accept": "application/json"}
  if settings.AI_CORE_API_KEY:
    headers["Authorization"] = f"Bearer {settings.AI_CORE_API_KEY}"

  try:
    async with httpx.AsyncClient(timeout=30.0) as client:
      resp = await client.post(endpoint, json={"prompt": prompt}, headers=headers)
      resp.raise_for_status()
      data = resp.json()
      # 預期回傳格式 {"playbook": "..."}
      if isinstance(data, dict) and "playbook" in data:
        return data.get("playbook") or ""
      # 如果回傳不同格式，嘗試把整個 body 當作文字
      if isinstance(data, str):
        return data
      return str(data)
  except Exception:
    # 任何錯誤都回退到 mock，避免整個流程崩潰
    return await _mock_generate(prompt)