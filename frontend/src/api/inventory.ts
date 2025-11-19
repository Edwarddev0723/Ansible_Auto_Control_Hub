import apiClient from './client'

export interface Inventory {
  id: number
  name: string
  status: 'On' | 'Off'
  ssh_status: string
  group: string
  config?: string
  created_at: string
  updated_at: string
}

export interface InventoryCreate {
  name: string
  status?: 'On' | 'Off'
  ssh_status?: string
  config?: string
  group?: string
}

export interface InventoryUpdate {
  name?: string
  status?: 'On' | 'Off'
  ssh_status?: string
  config?: string
  group?: string
}

export interface InventoryListResponse {
  success: boolean
  data: {
    items: Inventory[]
    pagination: {
      page: number
      per_page: number
      total: number
      total_pages: number
    }
  }
}

export interface InventoryResponse {
  success: boolean
  data: Inventory
  message?: string
}

// 獲取 Inventory 列表
export const getInventories = async (params?: {
  search?: string
  page?: number
  per_page?: number
}): Promise<InventoryListResponse> => {
  const response = await apiClient.get('/api/inventories', { params })
  return response.data
}

// 獲取單一 Inventory
export const getInventory = async (id: number): Promise<InventoryResponse> => {
  const response = await apiClient.get(`/api/inventories/${id}`)
  return response.data
}

// 創建 Inventory
export const createInventory = async (data: InventoryCreate): Promise<InventoryResponse> => {
  const response = await apiClient.post('/api/inventories', data)
  return response.data
}

// 更新 Inventory
export const updateInventory = async (
  id: number,
  data: InventoryUpdate
): Promise<InventoryResponse> => {
  const response = await apiClient.put(`/api/inventories/${id}`, data)
  return response.data
}

// 刪除 Inventory
export const deleteInventory = async (id: number): Promise<{ success: boolean; message: string }> => {
  const response = await apiClient.delete(`/api/inventories/${id}`)
  return response.data
}

// SSH 連線測試
export interface SSHTestRequest {
  inventory_ids: number[]
}

export interface SSHTestResult {
  id: number
  name: string
  status: 'success' | 'error'
  message: string
}

export interface SSHTestResponse {
  success: boolean
  data: SSHTestResult[]
  message: string
}

export const testSSHConnection = async (data: SSHTestRequest): Promise<SSHTestResponse> => {
  const response = await apiClient.post('/api/inventories/test-ssh', data)
  return response.data
}
