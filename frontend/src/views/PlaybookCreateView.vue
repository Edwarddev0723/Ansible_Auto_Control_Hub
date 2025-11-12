<template>
  <AppLayout>
    <div class="min-h-screen bg-[#FAFBFD] p-6">
      <!-- Header -->
      <h1 class="mb-6 text-2xl font-semibold text-[#333B69]">新增 Playbook</h1>

      <!-- Card -->
      <div class="rounded-2xl bg-white p-6 shadow-sm">
        <!-- Tabs -->
        <div class="mb-6 border-b border-gray-200">
          <nav class="flex gap-10">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'relative pb-3 text-sm font-semibold',
                activeTab === tab.key ? 'text-[#4379EE]' : 'text-gray-500',
              ]"
            >
              {{ tab.label }}
              <span
                v-if="activeTab === tab.key"
                class="absolute left-0 bottom-0 h-[2px] w-full bg-[#4379EE]"
              ></span>
            </button>
          </nav>
        </div>

        <!-- Main Tab Content -->
        <div v-if="activeTab === 'main'" class="space-y-6">
          <!-- Playbook 名稱 -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">
              Playbook 名稱 <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              placeholder="請輸入 Playbook 名稱"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              :class="{ 'border-red-400': errors.name }"
            />
            <p v-if="errors.name" class="mt-1 text-xs text-red-500">{{ errors.name }}</p>
          </div>

          <!-- Target Type Selection -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">
              目標類型 <span class="text-red-500">*</span>
            </label>
            <div class="flex gap-6">
              <label class="flex items-center">
                <input
                  v-model="form.targetType"
                  type="radio"
                  value="group"
                  class="mr-2 h-4 w-4 text-[#4379EE] focus:ring-[#4379EE]"
                />
                <span class="text-sm text-gray-700">Group</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="form.targetType"
                  type="radio"
                  value="host"
                  class="mr-2 h-4 w-4 text-[#4379EE] focus:ring-[#4379EE]"
                />
                <span class="text-sm text-gray-700">Host</span>
              </label>
            </div>
          </div>

          <!-- Group Dropdown (when group is selected) -->
          <div v-if="form.targetType === 'group'">
            <label class="mb-2 block text-sm font-medium text-gray-700">Group</label>
            <select
              v-model="form.group"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              :class="{ 'border-red-400': errors.group }"
            >
              <option value="">請選擇 Group</option>
              <option v-for="group in availableGroups" :key="group" :value="group">
                {{ group }}
              </option>
            </select>
            <p v-if="errors.group" class="mt-1 text-xs text-red-500">{{ errors.group }}</p>
          </div>

          <!-- Host Dropdown (when host is selected) -->
          <div v-if="form.targetType === 'host'">
            <label class="mb-2 block text-sm font-medium text-gray-700">Host</label>
            <select
              v-model="form.host"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              :class="{ 'border-red-400': errors.host }"
            >
              <option value="">請選擇 Host</option>
              <option v-for="host in availableHosts" :key="host" :value="host">
                {{ host }}
              </option>
            </select>
            <p v-if="errors.host" class="mt-1 text-xs text-red-500">{{ errors.host }}</p>
          </div>

          <!-- Gather Facts -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Gather_facts</label>
            <select
              v-model="form.gatherFacts"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            >
              <option :value="false">False</option>
              <option :value="true">True</option>
            </select>
          </div>

          <!-- Working Directory -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">
              工作目錄 (選填)
              <span class="text-xs text-gray-500 ml-2">設定後，Tasks 中的相對路徑會以此目錄為基準</span>
            </label>
            <input
              v-model="form.workingDirectory"
              type="text"
              placeholder="例如: C:\Users\user\Desktop\project 或 /mnt/c/Users/user/Desktop/project"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            />
            <p class="mt-1 text-xs text-gray-500">
              提示：設定工作目錄後，docker-compose.yaml 等檔案可以使用相對路徑（如 ./docker-compose.yaml）
            </p>
          </div>

          <div class="mt-10 flex justify-end gap-4">
            <button
              @click="cancel"
              class="rounded-lg bg-gray-400 px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-gray-500"
            >
              取消
            </button>
            <button
              @click="continueNext"
              class="rounded-lg bg-[#4379EE] px-6 py-2 text-sm font-semibold text-white hover:bg-[#3868dd]"
            >
              下一步
            </button>
          </div>
        </div>

        <!-- Tasks Tab Content -->
        <div v-else class="space-y-6">
          <div
            v-for="(task, index) in tasks"
            :key="task.id"
            class="rounded-lg border border-gray-200 bg-gray-50 p-4"
          >
            <!-- Task Header -->
            <div class="mb-4 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="text-sm font-semibold text-gray-700">Task {{ task.id }}</span>
                <button
                  @click="task.enabled = !task.enabled"
                  :class="[
                    'h-6 w-10 rounded-full transition-colors relative',
                    task.enabled ? 'bg-[#4379EE]' : 'bg-gray-300',
                  ]"
                >
                  <span
                    :class="[
                      'absolute top-1 left-1 h-4 w-4 rounded-full bg-white shadow transition-transform',
                      task.enabled ? 'translate-x-4' : 'translate-x-0',
                    ]"
                  ></span>
                </button>
              </div>
              <button
                @click="removeTask(index)"
                class="text-red-500 hover:text-red-700"
                title="刪除 Task"
              >
                🗑️
              </button>
            </div>

            <!-- Task Form -->
            <div v-if="task.enabled" class="space-y-4">
              <!-- Task Name -->
              <div>
                <label class="mb-1 block text-xs font-medium text-gray-600">Task 名稱</label>
                <input
                  v-model="task.parsed.name"
                  type="text"
                  placeholder="例如: 確保前端構建依賴項存在"
                  class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                />
              </div>

              <!-- Module Selection -->
              <div>
                <label class="mb-1 block text-xs font-medium text-gray-600">模塊類型</label>
                <select
                  v-model="task.parsed.module"
                  @change="onModuleChange(task)"
                  class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                >
                  <option value="command">command (執行命令)</option>
                  <option value="shell">shell (執行 shell 腳本)</option>
                  <option value="debug">debug (輸出訊息)</option>
                  <option value="community.docker.docker_compose_v2">docker_compose_v2 (Docker Compose)</option>
                  <option value="copy">copy (複製檔案)</option>
                  <option value="template">template (模板)</option>
                  <option value="file">file (檔案操作)</option>
                  <option value="custom">自訂 YAML</option>
                </select>
              </div>

              <!-- Module-specific Parameters -->
              <div v-if="task.parsed.module === 'command' || task.parsed.module === 'shell'" class="space-y-3">
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">
                    {{ task.parsed.module === 'command' ? '命令' : 'Shell 命令（支援多行）' }}
                    <span v-if="task.parsed.module === 'shell'" class="text-[#4379EE]">💡 多行指令會自動使用 bash 執行</span>
                  </label>
                  <textarea
                    v-model="task.parsed.params.cmd"
                    :rows="task.parsed.module === 'shell' ? 4 : 2"
                    :placeholder="task.parsed.module === 'shell' ? '例如:\nsource ~/.nvm/nvm.sh\nnpm install\nnpm run build' : '例如: npm install'"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  ></textarea>
                </div>
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">
                    工作目錄 (chdir)
                    <span class="text-[#4379EE]">📁 會自動轉換為 WSL 路徑</span>
                  </label>
                  <input
                    v-model="task.parsed.params.chdir"
                    type="text"
                    placeholder="C:\Users\user\Desktop\..."
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  />
                  <p v-if="task.parsed.params.chdir" class="mt-1 text-xs text-gray-500">
                    WSL 路徑: {{ convertToWSLPath(task.parsed.params.chdir) }}
                  </p>
                </div>
                <div v-if="task.parsed.module === 'shell'">
                  <label class="mb-1 block text-xs font-medium text-gray-600">
                    執行環境 (executable)
                    <span class="text-gray-500">預設: /bin/bash</span>
                  </label>
                  <input
                    v-model="task.parsed.params.executable"
                    type="text"
                    placeholder="/bin/bash"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  />
                </div>
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">註冊變數 (register)</label>
                  <input
                    v-model="task.parsed.params.register"
                    type="text"
                    placeholder="例如: npm_install"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  />
                </div>
              </div>

              <div v-else-if="task.parsed.module === 'debug'" class="space-y-3">
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">輸出訊息 (msg)</label>
                  <textarea
                    v-model="task.parsed.params.msg"
                    rows="2"
                    placeholder="例如: Compose 結果: {{ compose_up }}"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  ></textarea>
                </div>
              </div>

              <div v-else-if="task.parsed.module === 'community.docker.docker_compose_v2'" class="space-y-3">
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">
                    專案目錄 (project_src)
                    <span class="text-[#4379EE]">📁 會自動轉換為 WSL 路徑</span>
                  </label>
                  <input
                    v-model="task.parsed.params.project_src"
                    type="text"
                    placeholder="docker-compose.yaml 所在目錄"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  />
                  <p v-if="task.parsed.params.project_src" class="mt-1 text-xs text-gray-500">
                    WSL 路徑: {{ convertToWSLPath(task.parsed.params.project_src) }}
                  </p>
                </div>
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">建構行為 (build)</label>
                  <select
                    v-model="task.parsed.params.build"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  >
                    <option value="">不強制建構</option>
                    <option value="always">always (總是建構)</option>
                    <option value="never">never (從不建構)</option>
                  </select>
                </div>
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">狀態 (state)</label>
                  <select
                    v-model="task.parsed.params.state"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  >
                    <option value="present">present (啟動)</option>
                    <option value="absent">absent (停止並移除)</option>
                  </select>
                </div>
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">註冊變數 (register)</label>
                  <input
                    v-model="task.parsed.params.register"
                    type="text"
                    placeholder="例如: compose_up"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  />
                </div>
              </div>

              <div v-else-if="task.parsed.module === 'custom'" class="space-y-3">
                <div>
                  <label class="mb-1 block text-xs font-medium text-gray-600">自訂 YAML 內容</label>
                  <textarea
                    v-model="task.parsed.params.custom"
                    rows="6"
                    placeholder="輸入 YAML 格式的 task 內容..."
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-mono focus:border-[#4379EE] focus:outline-none focus:ring-1 focus:ring-[#4379EE]"
                  ></textarea>
                </div>
              </div>

              <!-- YAML Preview -->
              <div class="rounded-md bg-gray-100 p-3">
                <div class="mb-1 text-xs font-medium text-gray-600">📄 YAML 預覽:</div>
                <pre class="overflow-x-auto text-xs font-mono text-gray-800">{{ generateTaskYAML(task) }}</pre>
              </div>
            </div>

            <!-- Disabled State -->
            <div v-else class="text-sm text-gray-400">
              此 Task 已停用
            </div>
          </div>

          <!-- Add Task Button -->
          <button
            @click="addTask"
            class="w-full rounded-lg border-2 border-dashed border-gray-300 bg-white py-4 text-sm font-medium text-gray-600 transition-colors hover:border-[#4379EE] hover:text-[#4379EE]"
          >
            ➕ 新增 Task
          </button>

          <div class="mt-10 flex justify-end gap-4">
            <button
              @click="activeTab = 'main'"
              class="rounded-lg bg-gray-400 px-10 py-3 text-sm font-semibold text-white transition-colors hover:bg-gray-500"
            >
              上一步
            </button>
            <button
              @click="continueNext"
              class="rounded-lg bg-[#4379EE] px-6 py-2 text-sm font-semibold text-white hover:bg-[#3868dd]"
            >
              儲存並返回
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'
import { createPlaybook } from '@/api/playbook'
import { getGroups } from '@/api/group'
import { getInventories } from '@/api/inventory'

const router = useRouter()

interface PlaybookForm {
  name: string
  targetType: 'group' | 'host'
  group: string
  host: string
  gatherFacts: boolean
  workingDirectory: string
}

const form = ref<PlaybookForm>({
  name: '',
  targetType: 'group',
  group: '',
  host: '',
  gatherFacts: false,
  workingDirectory: '',
})

// 從 API 載入 groups 和 hosts
const availableGroups = ref<string[]>([])
const availableHosts = ref<string[]>([])
const loading = ref(false)

// 載入 Groups
const loadGroups = async () => {
  try {
    const response = await getGroups()
    if (response.success) {
      availableGroups.value = response.data.map(g => g.name)
    }
  } catch (error) {
    console.error('載入 Groups 失敗:', error)
  }
}

// 載入 Hosts (從 Inventories 獲取)
const loadHosts = async () => {
  try {
    const response = await getInventories({ per_page: 1000 })
    if (response.success) {
      // 使用 inventory name 作為 host 選項
      availableHosts.value = response.data.items.map(inv => inv.name)
    }
  } catch (error) {
    console.error('載入 Hosts 失敗:', error)
  }
}

// 組件掛載時載入資料
onMounted(() => {
  loadGroups()
  loadHosts()
})

const errors = ref<Record<string, string>>({})

const tabs = [
  { key: 'main', label: 'Main' },
  { key: 'tasks', label: 'Tasks' },
] as const

type TabKey = typeof tabs[number]['key']
const activeTab = ref<TabKey>('main')

// Tasks data
interface TaskItem {
  id: number
  enabled: boolean
  content: string
  parsed: {
    name: string
    module: string
    params: Record<string, any>
  }
}

const tasks = ref<TaskItem[]>([
  {
    id: 1,
    enabled: true,
    content: '',
    parsed: {
      name: '確保前端構建依賴項存在',
      module: 'command',
      params: {
        cmd: 'npm install',
        chdir: '',
        register: 'npm_install'
      }
    },
  },
])

// 路徑轉換函數
const convertToWSLPath = (path: string): string => {
  if (!path) return ''
  // C:\Users\... -> /mnt/c/Users/...
  const match = path.match(/^([A-Za-z]):[\\\/](.*)/)
  if (match) {
    const drive = match[1].toLowerCase()
    const restPath = match[2].replace(/\\/g, '/')
    return `/mnt/${drive}/${restPath}`
  }
  return path
}

// 生成 YAML 內容 (單個 task 的內容,不包含 list 的 "- ")
const generateTaskYAML = (task: TaskItem): string => {
  if (!task.enabled) return ''
  
  const { name, module, params } = task.parsed
  const lines: string[] = []
  
  // Task 的 name 屬性
  lines.push(`name: ${name || '未命名任務'}`)
  
  if (module === 'command' || module === 'shell') {
    const cmd = params.cmd || ''
    const isMultiLine = cmd.includes('\n')
    
    if (isMultiLine) {
      // 多行指令使用 | 格式
      lines.push(`${module}: |`)
      cmd.split('\n').forEach((line: string) => {
        lines.push(`  ${line}`)
      })
    } else {
      // 單行指令
      lines.push(`${module}: ${cmd}`)
    }
    
    if (params.chdir || (module === 'shell' && params.executable)) {
      lines.push(`args:`)
      if (params.chdir) {
        lines.push(`  chdir: "${convertToWSLPath(params.chdir)}"`)
      }
      if (module === 'shell' && params.executable) {
        lines.push(`  executable: ${params.executable}`)
      } else if (module === 'shell' && isMultiLine) {
        // 多行 shell 預設使用 bash
        lines.push(`  executable: /bin/bash`)
      }
    }
    
    if (params.register) {
      lines.push(`register: ${params.register}`)
    }
  } else if (module === 'debug') {
    lines.push(`debug:`)
    lines.push(`  msg: "${params.msg || ''}"`)
  } else if (module === 'community.docker.docker_compose_v2') {
    lines.push(`community.docker.docker_compose_v2:`)
    if (params.project_src) {
      lines.push(`  project_src: "${convertToWSLPath(params.project_src)}"`)
    }
    if (params.build) {
      lines.push(`  build: ${params.build}`)
    }
    if (params.state) {
      lines.push(`  state: ${params.state}`)
    }
    if (params.register) {
      lines.push(`register: ${params.register}`)
    }
  } else if (module === 'custom') {
    return params.custom || ''
  }
  
  return lines.join('\n')
}

// 模塊變更處理
const onModuleChange = (task: TaskItem) => {
  // 清空參數，保留 name
  const oldParams = { ...task.parsed.params }
  task.parsed.params = {}
  
  // 根據不同模塊設定預設值
  if (task.parsed.module === 'command' || task.parsed.module === 'shell') {
    task.parsed.params = {
      cmd: oldParams.cmd || '',
      chdir: oldParams.chdir || '',
      executable: oldParams.executable || (task.parsed.module === 'shell' ? '/bin/bash' : ''),
      register: oldParams.register || ''
    }
  } else if (task.parsed.module === 'debug') {
    task.parsed.params = {
      msg: oldParams.msg || 'Hello World'
    }
  } else if (task.parsed.module === 'community.docker.docker_compose_v2') {
    task.parsed.params = {
      project_src: oldParams.project_src || '',
      build: oldParams.build || 'always',
      state: oldParams.state || 'present',
      register: oldParams.register || ''
    }
  } else if (task.parsed.module === 'custom') {
    task.parsed.params = {
      custom: oldParams.custom || ''
    }
  }
}

const addTask = () => {
  const nextId = tasks.value.length + 1
  tasks.value.push({
    id: nextId,
    enabled: true,
    content: '',
    parsed: {
      name: `task${nextId}`,
      module: 'debug',
      params: {
        msg: 'Hello World'
      }
    }
  })
}

const removeTask = (index: number) => {
  if (confirm('確定要刪除這個 Task 嗎?')) {
    tasks.value.splice(index, 1)
    // 重新編號
    tasks.value.forEach((task, idx) => {
      task.id = idx + 1
    })
  }
}

const validateMain = () => {
  errors.value = {}
  
  if (!form.value.name.trim()) {
    errors.value.name = 'Playbook 名稱為必填'
    alert('請輸入 Playbook 名稱')
    return false
  }
  
  if (form.value.targetType === 'group' && !form.value.group.trim()) {
    errors.value.group = '請選擇目標群組'
    alert('請選擇目標群組')
    return false
  }
  
  if (form.value.targetType === 'host' && !form.value.host.trim()) {
    errors.value.host = '請選擇目標主機'
    alert('請選擇目標主機')
    return false
  }
  
  return Object.keys(errors.value).length === 0
}

const validateTasks = () => {
  const enabledTasks = tasks.value.filter(t => t.enabled)
  
  if (enabledTasks.length === 0) {
    alert('請至少啟用一個 Task')
    return false
  }
  
  // 檢查每個啟用的 task 是否有名稱
  for (const task of enabledTasks) {
    if (!task.parsed.name || !task.parsed.name.trim()) {
      alert('所有啟用的 Task 都必須填寫名稱')
      return false
    }
  }
  
  return true
}

const continueNext = async () => {
  if (activeTab.value === 'main') {
    if (!validateMain()) return
    activeTab.value = 'tasks'
  } else {
    // 在儲存前驗證所有必填欄位
    if (!validateMain()) {
      activeTab.value = 'main'
      return
    }
    
    if (!validateTasks()) {
      return
    }
    
    // 儲存 Playbook
    try {
      loading.value = true
      const enabledTasks = tasks.value.filter(t => t.enabled)
      
      const playbookData = {
        name: form.value.name,
        type: 'Machine' as const,
        target_type: form.value.targetType,
        group: form.value.targetType === 'group' ? form.value.group : undefined,
        host: form.value.targetType === 'host' ? form.value.host : undefined,
        main: {
          hosts: form.value.targetType === 'group' ? form.value.group : form.value.host,
          gather_facts: form.value.gatherFacts,
        },
        tasks: enabledTasks.map((t, index) => ({
          enabled: t.enabled,
          content: generateTaskYAML(t),
          order: index,
        })),
        extra_fields: {
          working_directory: form.value.workingDirectory || undefined
        }
      }
      
      const response = await createPlaybook(playbookData)
      
      if (response.success) {
        alert(response.message || 'Playbook 創建成功！')
        router.push('/playbook')
      }
    } catch (error: any) {
      console.error('建立 Playbook 失敗:', error)
      alert(error.response?.data?.message || '建立失敗，請稍後再試')
    } finally {
      loading.value = false
    }
  }
}

const cancel = () => {
  router.push('/playbook')
}
</script>
