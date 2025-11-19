from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.core.mcp_gateway import get_gateway

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str

@router.post("/chat", response_model=ChatResponse)
async def ai_chat(request: ChatRequest):
    """
    AI 對話 API - 整合 Ollama 與 Ansible MCP
    """
    try:
        gateway = get_gateway()
        
        # 轉換訊息格式
        messages = [
            {
                "role": msg.role,
                "content": msg.content
            } 
            for msg in request.messages
        ]
        
        # 調用 Gateway
        response = await gateway.chat(messages, stream=request.stream)
        
        return {
            "success": True,
            "data": response,
            "message": "AI response received successfully"
        }
                
    except Exception as e:
        import traceback
        print(f"Chat Error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health", response_model=ChatResponse)
async def check_ai_health():
    """檢查 AI 服務健康狀態"""
    try:
        gateway = get_gateway()
        health_status = await gateway.check_health()
        
        return {
            "success": health_status["status"] != "error",
            "data": health_status,
            "message": f"Service status: {health_status['status']}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": {"status": "error", "error": str(e)},
            "message": "Health check failed"
        }
