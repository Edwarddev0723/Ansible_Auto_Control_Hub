import client from './client'

export interface Collection {
  name: string
  version?: string
  source?: string
  path?: string
}

export interface InstalledCollection {
  name: string
  version: string
  path: string
}

export interface RequirementsData {
  collections: Collection[]
  roles?: any[]
  yaml: string
}

export interface InstallResult {
  success: boolean
  message: string
  output?: string
  error?: string
}

export interface PlaybookDependency {
  playbook_id: number
  playbook_name: string
  dependencies: {
    collection: string
    satisfied: boolean
    required: boolean
  }[]
  all_satisfied: boolean
}

// 列出已安裝的 collections
export async function listInstalledCollections(): Promise<InstalledCollection[]> {
  const response = await client.get('/api/galaxy/collections')
  return response.data.data
}

// 安裝單一 collection
export async function installCollection(
  name: string,
  version?: string
): Promise<InstallResult> {
  const response = await client.post('/api/galaxy/collections/install', {
    name,
    version,
  })
  return response.data
}

// 卸載 collection
export async function uninstallCollection(name: string): Promise<any> {
  const response = await client.delete(`/api/galaxy/collections/${name}`)
  return response.data
}

// 讀取 requirements.yml
export async function getRequirements(): Promise<RequirementsData> {
  const response = await client.get('/api/galaxy/requirements')
  return response.data.data
}

// 更新 requirements.yml
export async function updateRequirements(collections: Collection[]): Promise<any> {
  const response = await client.post('/api/galaxy/requirements', {
    collections,
  })
  return response.data
}

// 安裝 requirements.yml 中的所有 collections
export async function installRequirements(): Promise<InstallResult> {
  const response = await client.post('/api/galaxy/requirements/install')
  return response.data
}

// 檢查 Playbook 依賴
export async function checkPlaybookDependencies(
  playbookId: number
): Promise<PlaybookDependency> {
  const response = await client.get(`/api/galaxy/playbooks/${playbookId}/dependencies`)
  return response.data.data
}
