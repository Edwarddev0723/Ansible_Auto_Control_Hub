from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "gpt-4"
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    success: bool
    data: dict
    message: str

@router.post("/chat", response_model=dict)
async def ai_chat(request: ChatRequest):
    """
    AI 對話 API - 串接外部 MCP server
    可以在這裡串接 OpenAI、Claude 或其他 MCP server
    """
    try:
        # 從環境變數獲取 MCP server URL
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:3001/api/chat')
        
        # 準備發送給 MCP server 的資料
        payload = {
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "model": request.model,
            "temperature": request.temperature,
        }
        
        # 發送請求到 MCP server
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(mcp_server_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "data": data,
                    "message": "AI response received successfully"
                }
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"MCP server error: {response.text}"
                )
                
    except httpx.ConnectError:
        # MCP server 無法連線時的備援方案
        return {
            "success": True,
            "data": {
                "role": "assistant",
                "content": "目前 AI 服務暫時無法使用。這是一個模擬回覆，實際部署時會串接到 MCP server。\n\n您的訊息已收到，請稍後再試或聯繫系統管理員。"
            },
            "message": "Using fallback response (MCP server not available)"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health", response_model=dict)
async def check_ai_health():
    """檢查 AI 服務健康狀態"""
    try:
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:3001/health')
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(mcp_server_url)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": {"status": "connected", "server": mcp_server_url},
                    "message": "MCP server is healthy"
                }
            else:
                return {
                    "success": False,
                    "data": {"status": "error", "server": mcp_server_url},
                    "message": f"MCP server returned status {response.status_code}"
                }
    except Exception:
        return {
            "success": False,
            "data": {"status": "disconnected"},
            "message": "MCP server is not reachable"
        }
