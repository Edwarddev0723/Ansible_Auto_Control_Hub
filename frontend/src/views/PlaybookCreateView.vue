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
        <div v-else class="space-y-8">
          <div class="grid gap-8 lg:grid-cols-2">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="flex flex-col"
            >
              <!-- Task Header -->
              <div class="mb-2 flex items-center justify-between pr-2">
                <span class="text-sm font-medium text-gray-700">Task{{ task.id }}</span>
                <button
                  @click="task.enabled = !task.enabled"
                  :aria-pressed="task.enabled"
                  :class="[
                    'h-6 w-10 rounded-full transition-colors relative focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-[#4379EE]',
                    task.enabled ? 'bg-[#4379EE]' : 'bg-gray-200',
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
              <!-- Task Content -->
              <textarea
                v-model="task.content"
                :disabled="!task.enabled"
                class="min-h-[160px] w-full resize-y rounded-lg border border-gray-200 bg-white p-4 font-mono text-xs leading-relaxed text-black disabled:opacity-50 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              ></textarea>
            </div>
          </div>
          <button
            @click="addTask"
            class="mt-6 rounded-lg bg-[#4379EE] px-10 py-3 text-sm font-medium text-white transition-colors hover:bg-[#3868dd]"
          >
            新增 Task
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
}

const form = ref<PlaybookForm>({
  name: '',
  targetType: 'group',
  group: '',
  host: '',
  gatherFacts: false,
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
}

const tasks = ref<TaskItem[]>([
  {
    id: 1,
    enabled: true,
    content: `name: test1\ncommunity:\n  name: demo\nstate: absent`,
  },
  {
    id: 2,
    enabled: true,
    content: `name: test2\nCommunity2:\n  name: demo\nstate: absent`,
  },
  {
    id: 3,
    enabled: false,
    content: `name: test3\ndebug:\n  msg: "XXX"`,
  },
  {
    id: 4,
    enabled: false,
    content: `name: test4\ndebug:\n  msg: "XXX"`,
  },
])

const addTask = () => {
  tasks.value.push({
    id: tasks.value.length + 1,
    enabled: false,
    content: `name: test${tasks.value.length + 1}\ndebug:\n  msg: "XXX"`,
  })
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
  
  // 檢查每個啟用的 task 是否有內容
  for (const task of enabledTasks) {
    if (!task.content.trim()) {
      alert('所有啟用的 Task 都必須填寫內容')
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
          content: t.content,
          order: index,
        })),
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
