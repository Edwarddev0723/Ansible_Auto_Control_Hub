<template>
  <div>
    <h1>{{ isEditing ? '編輯 Playbook' : '建立新 Playbook' }}</h1>
    <form @submit.prevent="savePlaybook">
        <div class="form-group">
          <label for="name">名稱</label>
          <input id="name" v-model="playbook.name" required />
        </div>
        <div class="form-group">
          <label for="description">描述</label>
          <input id="description" v-model="playbook.description" />
        </div>

        <!-- 簡易任務建構器：減少手動輸入 YAML -->
        <section class="task-builder">
          <h2>任務建構器（快速新增）</h2>
          <div class="builder-row">
            <label>常用片段</label>
            <select v-model="snippetKey">
              <option value="">選擇片段...</option>
              <option value="update">Update all packages</option>
              <option value="install_nginx">Install Nginx</option>
              <option value="restart_service">Restart Service</option>
            </select>
            <button type="button" @click="insertSnippet">插入片段</button>
          </div>

          <div class="builder-row">
            <label for="taskName">任務名稱</label>
            <input id="taskName" v-model="taskName" placeholder="例如：Install nginx" />
          </div>

          <div class="builder-row">
            <label for="module">模組</label>
            <select id="module" v-model="moduleName">
              <option value="ansible.builtin.ping">ping</option>
              <option value="ansible.builtin.apt">apt</option>
              <option value="ansible.builtin.service">service</option>
              <option value="ansible.builtin.copy">copy</option>
              <option value="ansible.builtin.shell">shell</option>
              <option value="ansible.builtin.command">command</option>
              <option value="ansible.builtin.template">template</option>
            </select>
          </div>

          <div class="builder-row">
            <label for="params">參數（key: value，逗號分隔）</label>
            <input id="params" v-model="params" placeholder="name: nginx, state: present" />
          </div>

          <div class="builder-row">
            <button type="button" @click="addTask">加入任務到 Playbook</button>
          </div>

          <div v-if="addedTasks.length" class="added-tasks">
            <h3>已加入的任務</h3>
            <ul>
              <li v-for="(t, idx) in addedTasks" :key="idx">
                <pre>{{ t }}</pre>
                <button type="button" @click="removeTask(idx)">移除</button>
              </li>
            </ul>
          </div>
        </section>

        <div class="form-group">
          <label for="content">Playbook 內容 (YAML) — 預覽 / 手動編輯</label>
          <textarea id="content" v-model="playbook.content" rows="20" required></textarea>
        </div>

        <div class="actions">
          <button type="submit" :disabled="loading">
            {{ loading ? '儲存中...' : '儲存 Playbook' }}
          </button>
          <RouterLink to="/playbooks" class="cancel-btn">取消</RouterLink>
        </div>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import apiClient from '@/services/api'

const props = defineProps({
  id: {
    type: String,
    default: null
  }
})

const router = useRouter()
const isEditing = ref(false)
const loading = ref(false)
const error = ref(null)

const playbook = ref({
  name: '',
  description: '',
  content: '- name: New Playbook\n  hosts: all\n  tasks:\n    - name: Ping\n      ansible.builtin.ping:\n'
})

// Task builder state
const taskName = ref('')
const moduleName = ref('ansible.builtin.ping')
const params = ref('')
const addedTasks = ref([])
const snippetKey = ref('')

// baseHeader: playbook header up to "tasks:\n"（包含 tasks:）
const baseHeader = ref('')

const _ensureBaseHeader = () => {
  const content = playbook.value.content || ''
  const idx = content.indexOf('\n  tasks:\n')
  if (idx !== -1) {
    baseHeader.value = content.slice(0, idx + '\n  tasks:\n'.length)
    // 若後面已經有內容，保留為單個 block（不嘗試精準解析），當做原始內容保留
    const rest = content.slice(idx + '\n  tasks:\n'.length)
    if (rest.trim()) {
      // 將原始 tasks 片段放入 addedTasks（簡單切割，以 "\n    - " 為界）
      const parts = rest.split('\n    - ').filter(p => p.trim())
      addedTasks.value = parts.map(p => '    - ' + p.trim())
    }
  } else {
    baseHeader.value = '- name: New Playbook\n  hosts: all\n  tasks:\n'
  }
}

const rebuildContentFromTasks = () => {
  playbook.value.content = baseHeader.value + (addedTasks.value.length ? '\n' + addedTasks.value.join('\n') + '\n' : '')
}

const parseParamsToYaml = (paramsStr) => {
  // paramsStr 範例: "name: nginx, state: present"
  const out = []
  if (!paramsStr) return ''
  const pairs = paramsStr.split(',').map(s => s.trim()).filter(Boolean)
  pairs.forEach(p => {
    // 如果已經有 key: value 格式就原樣放
    if (p.includes(':')) {
      out.push(p)
    } else if (p.includes('=')) {
      const [k, v] = p.split('=').map(x => x.trim())
      out.push(`${k}: ${v}`)
    } else {
      // 單一值，難以斷定 key，放成 arg: value
      out.push(p)
    }
  })
  return out.join('\n        ')
}

const addTask = () => {
  const name = taskName.value || 'Task'
  const moduleLine = Object.prototype.hasOwnProperty.call({}, moduleName.value) ? moduleName.value : moduleName.value
  const paramsYaml = parseParamsToYaml(params.value)
  let taskYaml = `    - name: ${name}\n      ${moduleName.value}:` + (paramsYaml ? `\n        ${paramsYaml}` : '\n')
  addedTasks.value.push(taskYaml)
  rebuildContentFromTasks()
  // 清除 builder
  taskName.value = ''
  params.value = ''
}

const removeTask = (idx) => {
  addedTasks.value.splice(idx, 1)
  rebuildContentFromTasks()
}

const insertSnippet = () => {
  if (snippetKey.value === 'update') {
    const s = `    - name: Update all packages\n      ansible.builtin.apt:\n        update_cache: yes\n        upgrade: dist\n`
    addedTasks.value.push(s)
  } else if (snippetKey.value === 'install_nginx') {
    const s = `    - name: Install Nginx\n      ansible.builtin.apt:\n        name: nginx\n        state: present\n`
    addedTasks.value.push(s)
  } else if (snippetKey.value === 'restart_service') {
    const s = `    - name: Restart nginx\n      ansible.builtin.service:\n        name: nginx\n        state: restarted\n`
    addedTasks.value.push(s)
  }
  rebuildContentFromTasks()
  snippetKey.value = ''
}

onMounted(() => {
  if (props.id) {
    isEditing.value = true
    fetchPlaybookData(props.id)
  }
  // 初始化 baseHeader 與已加入任務（如果 content 有）
  _ensureBaseHeader()
})

const fetchPlaybookData = async (id) => {
  loading.value = true
  try {
    const response = await apiClient.get(`/playbooks/${id}`)
    playbook.value = response.data
  } catch (err) {
    error.value = '讀取 Playbook 資料失敗'
  } finally {
    loading.value = false
  }
}

const savePlaybook = async () => {
  loading.value = true
  error.value = null
  try {
    if (isEditing.value) {
      // 更新 (PUT)
      await apiClient.put(`/playbooks/${props.id}`, playbook.value)
    } else {
      // 建立 (POST)
      await apiClient.post('/playbooks/', playbook.value)
    }
    // 成功後返回列表頁
    router.push('/playbooks')
  } catch (err) {
    error.value = '儲存失敗'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.cancel-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>