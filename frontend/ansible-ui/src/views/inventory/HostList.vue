<template>
  <div>
    <div class="page-header">
      <h1>Inventory 伺服器管理</h1>
      <button @click="showModal = true">新增伺服器</button>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>名稱</th>
          <th>IP 位址</th>
          <th>群組</th>
          <th>SSH 使用者</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td colspan="6">載入中...</td>
        </tr>
        <tr v-if="error">
          <td colspan="6" class="error-message">{{ error }}</td>
        </tr>
        <tr v-for="host in hosts" :key="host.id">
          <td>{{ host.id }}</td>
          <td>{{ host.name }}</td>
          <td>{{ host.ip_address }}</td>
          <td>{{ host.group }}</td>
          <td>{{ host.ssh_user }}:{{ host.ssh_port }}</td>
          <td>
            <button @click="editHost(host)" class="btn-secondary" style="margin-right: 5px;">編輯</button>
            <button @click="deleteHost(host.id)" class="btn-danger">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ isEditing ? '編輯' : '新增' }}伺服器</h2>
        <form @submit.prevent="handleSave">
          <div class="form-group">
            <label>名稱</label>
            <input v-model="currentHost.name" required />
          </div>
          <div class="form-group">
            <label>IP 位址</label>
            <input v-model="currentHost.ip_address" required />
          </div>
          <div class="form-group">
            <label>群組</label>
            <input v-model="currentHost.group" />
          </div>
          <div class="form-group">
            <label>SSH 使用者</label>
            <input v-model="currentHost.ssh_user" />
          </div>
          <div class="form-group">
            <label>SSH 埠號</label>
            <input v-model.number="currentHost.ssh_port" type="number" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">取消</button>
            <button type="submit">儲存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const hosts = ref([])
const loading = ref(false)
const error = ref(null)

const showModal = ref(false)
const isEditing = ref(false)
const currentHost = ref({
  name: '',
  ip_address: '',
  group: 'all',
  ssh_user: 'root',
  ssh_port: 22
})

const fetchHosts = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get('/inventory/')
    hosts.value = response.data
  } catch (err) {
    error.value = '讀取伺服器列表失敗'
  } finally {
    loading.value = false
  }
}

onMounted(fetchHosts)

const resetForm = () => {
  isEditing.value = false
  currentHost.value = {
    name: '',
    ip_address: '',
    group: 'all',
    ssh_user: 'root',
    ssh_port: 22
  }
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const handleSave = async () => {
  if (!auth.isAdmin) {
    alert('只有管理員可以執行此操作');
    return;
  }
  
  try {
    if (isEditing.value) {
      await apiClient.put(`/inventory/${currentHost.value.id}`, currentHost.value)
    } else {
      await apiClient.post('/inventory/', currentHost.value)
    }
    closeModal()
    fetchHosts() // 重新整理列表
  } catch (err) {
    alert('儲存失敗')
  }
}

const editHost = (host) => {
  isEditing.value = true
  currentHost.value = { ...host } // 複製一份，避免響應式汙染
  showModal.value = true
}

const deleteHost = async (id) => {
  if (!auth.isAdmin) {
    alert('只有管理員可以執行此操作');
    return;
  }
  if (confirm('您確定要刪除此伺服器嗎？')) {
    try {
      await apiClient.delete(`/inventory/${id}`)
      fetchHosts() // 重新整理列表
    } catch (err) {
      alert('刪除失敗')
    }
  }
}
</script>

<style scoped>
/* Modal 樣式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}
.modal-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>