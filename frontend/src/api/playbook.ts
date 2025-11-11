import apiClient from './client'

export interface Task {
  id?: number
  enabled: boolean
  content: string
  order?: number
}

export interface PlaybookMain {
  hosts: string
  gather_facts: boolean
}

export interface Playbook {
  id: number
  name: string
  type: 'Machine' | 'Other'
  status: 'Success' | 'Fail' | 'Not start'
  target_type: 'group' | 'host'
  group?: string
  host?: string
  main?: PlaybookMain
  tasks?: Task[]
  last_run_at?: string
  created_at: string
  updated_at: string
}

export interface PlaybookCreate {
  name: string
  type: 'Machine' | 'Other'
  target_type: 'group' | 'host'
  group?: string
  host?: string
  main: PlaybookMain
  tasks: Task[]
  extra_fields?: Record<string, any>
}

export interface PlaybookUpdate {
  name?: string
  type?: 'Machine' | 'Other'
  target_type?: 'group' | 'host'
  group?: string
  host?: string
  main?: PlaybookMain
  tasks?: Task[]
  extra_fields?: Record<string, any>
}

export interface PlaybookListResponse {
  success: boolean
  data: {
    items: Playbook[]
    pagination: {
      page: number
      per_page: number
      total: number
      total_pages: number
    }
  }
}

export interface PlaybookResponse {
  success: boolean
  data: Playbook
  message?: string
}

export interface PlaybookExecuteRequest {
  playbook_ids: number[]
  inventory_id?: number
  extra_vars?: Record<string, any>
}

// 獲取 Playbook 列表
export const getPlaybooks = async (params?: {
  search?: string
  type?: string
  status?: string
  page?: number
  per_page?: number
}): Promise<PlaybookListResponse> => {
  const response = await apiClient.get('/api/playbooks', { params })
  return response.data
}

// 獲取單一 Playbook
export const getPlaybook = async (id: number): Promise<PlaybookResponse> => {
  const response = await apiClient.get(`/api/playbooks/${id}`)
  return response.data
}

// 創建 Playbook
export const createPlaybook = async (data: PlaybookCreate): Promise<PlaybookResponse> => {
  const response = await apiClient.post('/api/playbooks', data)
  return response.data
}

// 更新 Playbook
export const updatePlaybook = async (
  id: number,
  data: PlaybookUpdate
): Promise<PlaybookResponse> => {
  const response = await apiClient.put(`/api/playbooks/${id}`, data)
  return response.data
}

// 刪除 Playbook
export const deletePlaybook = async (id: number): Promise<{ success: boolean; message: string }> => {
  const response = await apiClient.delete(`/api/playbooks/${id}`)
  return response.data
}

// 執行 Playbooks
export const executePlaybooks = async (
  data: PlaybookExecuteRequest
): Promise<{ success: boolean; data: any; message: string }> => {
  const response = await apiClient.post('/api/playbooks/execute', data)
  return response.data
}
