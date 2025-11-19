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
          <!-- Name -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Name</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              :class="{ 'border-red-400': errors.name }"
            />
            <p v-if="errors.name" class="mt-1 text-xs text-red-500">{{ errors.name }}</p>
          </div>

          <!-- Hosts -->
            <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Hosts</label>
            <input
              v-model="form.hosts"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              :class="{ 'border-red-400': errors.hosts }"
            />
            <p v-if="errors.hosts" class="mt-1 text-xs text-red-500">{{ errors.hosts }}</p>
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
            <button
              @click="addMainField"
              class="mt-4 rounded-lg bg-[#4379EE] px-10 py-3 text-sm font-medium text-white transition-colors hover:bg-[#3868dd]"
            >
              新增 Main 欄位
            </button>
          </div>

          <div v-for="(field, idx) in extraMainFields" :key="idx" class="mt-4">
            <input
              v-model="field.value"
              :placeholder="field.placeholder"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            />
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()

interface PlaybookForm {
  name: string
  hosts: string
  gatherFacts: boolean
}

const form = ref<PlaybookForm>({
  name: '',
  hosts: '',
  gatherFacts: false,
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

const extraMainFields = ref<{ value: string; placeholder: string }[]>([])
const addMainField = () => {
  extraMainFields.value.push({ value: '', placeholder: '新增 Main 欄位' })
}

const addTask = () => {
  tasks.value.push({
    id: tasks.value.length + 1,
    enabled: false,
    content: `name: test${tasks.value.length + 1}\ndebug:\n  msg: "XXX"`,
  })
}

const validateMain = () => {
  errors.value = {}
  if (!form.value.name.trim()) errors.value.name = 'Name is required'
  if (!form.value.hosts.trim()) errors.value.hosts = 'Hosts is required'
  return Object.keys(errors.value).length === 0
}

const continueNext = () => {
  if (activeTab.value === 'main') {
    if (!validateMain()) return
    activeTab.value = 'tasks'
  } else {
    // Collect enabled tasks and simulate save
    const enabledTasks = tasks.value.filter(t => t.enabled)
    console.log('Saving playbook:', {
      main: form.value,
      tasks: enabledTasks,
    })
    alert(`Playbook 已建立，啟用任務: ${enabledTasks.length} (示意)`)    
    router.push('/playbook')
  }
}

const cancel = () => {
  router.push('/playbook')
}
</script>
