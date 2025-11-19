import apiClient from './client'

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface ChatRequest {
  messages: ChatMessage[]
  model?: string
  temperature?: number
}

export interface ToolCallResult {
  tool: string
  arguments: Record<string, any>
  result: any
}

export interface ChatResponse {
  success: boolean
  data: {
    role: string
    content: string
    tool_calls?: ToolCallResult[]
  }
  message: string
}

export interface AIHealthResponse {
  success: boolean
  data: {
    status: 'connected' | 'disconnected' | 'error'
    server?: string
  }
  message: string
}

// 發送 AI 聊天訊息
export const sendChatMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await apiClient.post('/api/ai/chat', request)
  return response.data
}

// 檢查 AI 服務健康狀態
export const checkAIHealth = async (): Promise<AIHealthResponse> => {
  const response = await apiClient.get('/api/ai/health')
  return response.data
}
