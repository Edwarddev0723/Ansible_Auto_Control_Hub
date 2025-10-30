<template>
  <div>
    <div class="page-header">
      <h1>使用者管理</h1>
      <button @click="showModal = true">建立新使用者</button>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>角色 (Role)</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td colspan="4">載入中...</td>
        </tr>
        <tr v-if="error">
          <td colspan="4" class="error-message">{{ error }}</td>
        </tr>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <button class_="btn-danger" @click="deleteUser(user.id)">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>建立新使用者</h2>
        <form @submit.prevent="handleCreateUser">
          <div class="form-group">
            <label>Email</label>
            <input v-model="newUser.email" type="email" required />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="newUser.password" type="password" required />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="newUser.role" required>
              <option value="viewer">Viewer</option>
              <option value="developer">Developer</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">取消</button>
            <button type="submit">建立</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api'

const users = ref([])
const loading = ref(false)
const error = ref(null)
const showModal = ref(false)

const newUser = ref({
  email: '',
  password: '',
  role: 'viewer'
})

const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get('/auth/users')
    users.value = response.data
  } catch (err) {
    error.value = '讀取使用者列表失敗'
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)

const closeModal = () => {
  showModal.value = false
  newUser.value = { email: '', password: '', role: 'viewer' }
}

const handleCreateUser = async () => {
  try {
    await apiClient.post('/auth/users/create', newUser.value)
    closeModal()
    fetchUsers()
  } catch (err) {
    alert('建立失敗')
  }
}

const deleteUser = (id) => {
  alert('刪除使用者的 API 尚未實作')
  // (後端尚未提供 DELETE /auth/users/{id} 路由，但可以預留)
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