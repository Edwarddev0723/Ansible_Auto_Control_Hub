import apiClient from './client'

export interface Group {
  id: number
  name: string
  created_at: string
}

export interface GroupCreate {
  name: string
}

export interface GroupResponse {
  success: boolean
  data: Group[]
}

// 獲取所有 Groups
export const getGroups = async (): Promise<GroupResponse> => {
  const response = await apiClient.get('/api/groups')
  return response.data
}

// 創建 Group
export const createGroup = async (data: GroupCreate): Promise<{ success: boolean; data: Group; message: string }> => {
  const response = await apiClient.post('/api/groups', data)
  return response.data
}

// 刪除 Group
export const deleteGroup = async (id: number): Promise<{ success: boolean; message: string }> => {
  const response = await apiClient.delete(`/api/groups/${id}`)
  return response.data
}
