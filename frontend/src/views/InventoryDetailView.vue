<template>
  <AppLayout>
    <div class="min-h-screen bg-[#FAFBFD] p-6">
      <!-- Header -->
      <h1 class="mb-6 text-2xl font-semibold text-[#333B69]">Inventory 設定</h1>

      <!-- Main Content Card -->
      <div class="rounded-2xl bg-white p-6 shadow-sm">
        <!-- Ansible GUI Inventory Title -->
        <h2 class="mb-4 text-lg font-medium text-[#4379EE]">
          {{ isEditMode ? inventoryName : '新增 Inventory' }}
        </h2>

        <!-- Configuration Form -->
        <div class="mb-6 space-y-4">
          <!-- Server Name -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">Inventory Name</label>
            <input
              v-model="formData.name"
              type="text"
              :disabled="isEditMode"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20 disabled:opacity-60 disabled:cursor-not-allowed"
              placeholder="例如: Ansible GUI Inventory"
            />
          </div>

          <!-- Server Status -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">伺服器狀態</label>
            <select
              v-model="formData.status"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            >
              <option value="On">On（運行中）</option>
              <option value="Off">Off（已停止）</option>
            </select>
          </div>

          <!-- Server Group -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">伺服器群組</label>
            <div class="flex gap-2">
              <select
                v-model="formData.group"
                class="flex-1 rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              >
                <option value="" disabled>請選擇群組</option>
                <option v-for="group in availableGroups" :key="group.id" :value="group.name">
                  {{ group.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Divider -->
          <div class="border-t border-gray-200 pt-4">
            <h3 class="mb-3 text-sm font-semibold text-gray-600">SSH 連線設定</h3>
          </div>

          <!-- Server Name -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">
              Server Name (主機別名)
              <span class="ml-2 text-xs text-gray-500">在 Playbook 中用來識別此伺服器</span>
            </label>
            <input
              v-model="formData.serverName"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              placeholder="例如: web-server-1, db-primary, nginx-proxy"
            />
          </div>

          <!-- SSH Host -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">
              SSH Host (IP Address)
              <span class="ml-2 text-xs text-gray-500">實際連線的 IP 位址</span>
            </label>
            <input
              v-model="formData.sshHost"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              placeholder="例如: 192.168.1.100 或 127.0.0.1"
            />
          </div>

          <!-- SSH Port -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">SSH Port</label>
            <input
              v-model="formData.sshPort"
              type="number"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              placeholder="例如: 22 或 55000"
            />
          </div>

          <!-- SSH User -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">SSH User</label>
            <input
              v-model="formData.sshUser"
              type="text"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              placeholder="例如: root, ubuntu, admin"
            />
          </div>

          <!-- SSH Password -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700">SSH Password</label>
            <input
              v-model="formData.sshPass"
              type="password"
              class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
              placeholder="輸入 SSH 密碼"
            />
          </div>

        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end gap-4">
          <!-- Cancel Button -->
          <button
            @click="handleCancel"
            class="rounded-lg bg-gray-400 px-8 py-3 font-medium text-white transition-colors hover:bg-gray-500"
          >
            Cancel
          </button>

          <!-- Save Button -->
          <button
            @click="handleSave"
            :disabled="loading"
            class="rounded-lg bg-[#1814F3] px-8 py-3 font-medium text-white transition-colors hover:bg-[#4379EE] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '儲存中...' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'
import { getInventory, createInventory, updateInventory } from '@/api/inventory'
import { getGroups, type Group } from '@/api/group'

const router = useRouter()
const route = useRoute()

// 表單資料
const formData = ref({
  name: '',
  status: 'Off' as 'On' | 'Off',
  group: 'Default',
  serverName: '',
  sshHost: '',
  sshPort: '',
  sshUser: 'root',  // 預設 root，但可修改
  sshPass: '',
})

const inventoryName = ref('')
const loading = ref(false)
const isEditMode = computed(() => !!route.params.id)
const availableGroups = ref<Group[]>([])

// 載入群組列表
const loadGroups = async () => {
  try {
    const response = await getGroups()
    if (response.success) {
      availableGroups.value = response.data
      // 如果是新增模式且有群組，預設選擇第一個
      if (!isEditMode.value && availableGroups.value.length > 0) {
        formData.value.group = availableGroups.value[0].name
      }
    }
  } catch (error) {
    console.error('載入群組失敗:', error)
  }
}

// 跳轉到群組管理頁面
const goToGroupManagement = () => {
  router.push('/inventory-groups')
}

// 生成 Ansible Inventory 配置字串
const generatedConfig = computed(() => {
  const { serverName, sshHost, sshPort, sshUser, sshPass } = formData.value
  if (!serverName || !sshHost || !sshPort || !sshUser || !sshPass) {
    return ''
  }
  return `${serverName} ansible_ssh_host=${sshHost} ansible_ssh_port=${sshPort} ansible_ssh_user=${sshUser} ansible_ssh_pass=${sshPass}`
})

// 解析現有配置
const parseConfig = (config: string) => {
  // 解析格式: server1 ansible_ssh_host=127.0.0.1 ansible_ssh_port=55000 ansible_ssh_user=root ansible_ssh_pass=docker
  const parts = config.split(' ')
  if (parts.length >= 4) {
    formData.value.serverName = parts[0]
    
    parts.slice(1).forEach(part => {
      if (part.includes('ansible_ssh_host=')) {
        formData.value.sshHost = part.split('=')[1]
      } else if (part.includes('ansible_ssh_port=')) {
        formData.value.sshPort = part.split('=')[1]
      } else if (part.includes('ansible_ssh_user=')) {
        formData.value.sshUser = part.split('=')[1]
      } else if (part.includes('ansible_ssh_pass=')) {
        formData.value.sshPass = part.split('=')[1]
      }
    })
  }
}

// Initialize with existing data if editing
onMounted(async () => {
  // 先載入群組列表
  await loadGroups()
  
  const id = route.params.id
  if (id) {
    try {
      loading.value = true
      const response = await getInventory(Number(id))
      if (response.success) {
        inventoryName.value = response.data.name
        formData.value.name = response.data.name
        formData.value.status = response.data.status
        formData.value.group = response.data.group
        if (response.data.config) {
          parseConfig(response.data.config)
        }
      }
    } catch (error) {
      console.error('載入 Inventory 失敗:', error)
      alert('載入資料失敗')
    } finally {
      loading.value = false
    }
  }
})

// Handle Cancel action
const handleCancel = () => {
  router.push('/')
}

// Handle Save action
const handleSave = async () => {
  // 驗證必填欄位
  if (!formData.value.name.trim()) {
    alert('請輸入 Inventory 名稱')
    return
  }
  
  if (!formData.value.group.trim()) {
    alert('請選擇伺服器群組')
    return
  }
  
  if (!formData.value.serverName.trim()) {
    alert('請輸入伺服器名稱')
    return
  }
  
  if (!formData.value.sshHost.trim()) {
    alert('請輸入 SSH Host')
    return
  }
  
  if (!formData.value.sshPort.trim()) {
    alert('請輸入 SSH Port')
    return
  }
  
  if (!formData.value.sshUser.trim()) {
    alert('請輸入 SSH 使用者名稱')
    return
  }
  
  if (!formData.value.sshPass.trim()) {
    alert('請輸入 SSH 密碼')
    return
  }
  
  if (!generatedConfig.value) {
    alert('請填寫所有 SSH 連線設定')
    return
  }

  try {
    loading.value = true
    
    if (isEditMode.value) {
      // 更新現有 Inventory
      const response = await updateInventory(Number(route.params.id), {
        status: formData.value.status,
        group: formData.value.group,
        config: generatedConfig.value,
      })
      
      if (response.success) {
        alert(response.message || 'Inventory 更新成功！')
        router.push('/')
      }
    } else {
      // 創建新 Inventory
      const response = await createInventory({
        name: formData.value.name,
        status: formData.value.status,
        group: formData.value.group,
        config: generatedConfig.value,
      })
      
      if (response.success) {
        alert(response.message || 'Inventory 創建成功！')
        router.push('/')
      }
    }
  } catch (error: any) {
    console.error('儲存失敗:', error)
    alert(error.response?.data?.message || '儲存失敗，請稍後再試')
  } finally {
    loading.value = false
  }
}
</script>
