<template>
  <AppLayout>
    <div class="min-h-screen bg-[#FAFBFD] p-6">
      <!-- Header -->
      <h1 class="mb-6 text-2xl font-semibold text-[#333B69]">編輯 Playbook</h1>

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

        <!-- 基礎資訊 Tab -->
        <div v-if="activeTab === 'info'" class="space-y-6">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Playbook 名稱</label>
            <input
              v-model="form.name"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">型態</label>
            <select
              v-model="form.type"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            >
              <option value="Machine">Machine</option>
              <option value="Other">Other</option>
            </select>
            <div v-if="form.type === 'Other'" class="mt-2">
              <input
                v-model="form.typeOther"
                type="text"
                class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
                placeholder="Other"
              />
            </div>
          </div>
          <div class="mt-8 flex justify-end gap-4">
            <button
              @click="router.push('/playbook')"
              class="rounded-lg bg-gray-400 px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-gray-500"
            >
              取消
            </button>
            <button
              @click="nextTab"
              class="rounded-lg bg-[#4379EE] px-6 py-2 text-sm font-semibold text-white hover:bg-[#3868dd]"
            >
              下一步
            </button>
          </div>
        </div>

        <!-- Main Tab -->
        <div v-if="activeTab === 'main'" class="space-y-6">
          <!-- Name -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Name</label>
            <input
              :value="form.name"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              readonly
            />
          </div>
          <!-- Hosts -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Hosts</label>
            <input
              v-model="form.hosts"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm text-black focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            />
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
          <div class="mt-8 flex justify-end gap-4">
            <button
              @click="activeTab = 'info'"
              class="rounded-lg bg-gray-400 px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-gray-500"
            >
              上一步
            </button>
            <button
              @click="nextTab"
              class="rounded-lg bg-[#4379EE] px-6 py-2 text-sm font-semibold text-white hover:bg-[#3868dd]"
            >
              下一步
            </button>
          </div>
        </div>

        <!-- Task Tab -->
        <div v-if="activeTab === 'task'" class="space-y-8">
          <div class="grid gap-8 lg:grid-cols-2">
            <div
              v-for="task in taskList"
              :key="task.id"
              class="flex flex-col"
            >
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
          <div class="mt-8 flex justify-end gap-4">
            <button
              @click="activeTab = 'main'"
              class="rounded-lg bg-gray-400 px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-gray-500"
            >
              上一步
            </button>
            <button
              @click="saveEdit"
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
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const route = useRoute()

const tabs = [
  { key: 'info', label: '基礎資訊' },
  { key: 'main', label: 'Main' },
  { key: 'task', label: 'Task' },
]
const activeTab = ref('info')

const form = ref({
  name: '',
  hosts: '',
  gatherFacts: false,
  type: 'Machine',
  typeOther: 'Other',
  main: '',
  task: '',
})

const mainList = ref([
  { id: 1, type: 'Machine', typeOther: 'Other', content: '' },
])
const taskList = ref([
  { id: 1, enabled: true, content: `name: test1\ncommunity:\n  name: demo\nstate: absent` },
  { id: 2, enabled: true, content: `name: test2\nCommunity2:\n  name: demo\nstate: absent` },
  { id: 3, enabled: false, content: `name: test3\ndebug:\n  msg: \"XXX\"` },
  { id: 4, enabled: false, content: `name: test4\ndebug:\n  msg: \"XXX\"` },
])

const addMain = () => {
  mainList.value.push({ id: mainList.value.length + 1, type: 'Machine', typeOther: 'Other', content: '' })
}
const addTask = () => {
  const nextId = taskList.value.length + 1;
  taskList.value.push({
    id: nextId,
    enabled: false,
    content: `name: test${nextId}\ndebug:\n  msg: \"XXX\"`,
  });
}

const nextTab = () => {
  const idx = tabs.findIndex(t => t.key === activeTab.value)
  if (idx < tabs.length - 1) activeTab.value = tabs[idx + 1].key
}
const prevTab = () => {
  const idx = tabs.findIndex(t => t.key === activeTab.value)
  if (idx > 0) activeTab.value = tabs[idx - 1].key
}

const saveEdit = () => {
  // TODO: 儲存 playbook 編輯內容
  router.push('/playbook')
}

const extraMainFields = ref<{ value: string; placeholder: string }[]>([])
const addMainField = () => {
  extraMainFields.value.push({ value: '', placeholder: '新增 Main 欄位' })
}
</script>
