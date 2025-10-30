from pydantic import BaseModel

class AIChatRequest(BaseModel):
    prompt: str

class AIChatResponse(BaseModel):
    prompt: str
    generated_playbook_content: str # AI 生成的 YAML 內容