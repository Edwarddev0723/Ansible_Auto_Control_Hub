import apiClient from './client'

export interface Host {
  id: number
  address: string
  created_at: string
}

export interface HostCreate {
  address: string
}

export interface HostResponse {
  success: boolean
  data: Host[]
}

// 獲取所有 Hosts
export const getHosts = async (): Promise<HostResponse> => {
  const response = await apiClient.get('/api/hosts')
  return response.data
}

// 創建 Host
export const createHost = async (data: HostCreate): Promise<{ success: boolean; data: Host; message: string }> => {
  const response = await apiClient.post('/api/hosts', data)
  return response.data
}
