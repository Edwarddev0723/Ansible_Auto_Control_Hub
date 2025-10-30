<template>
  <div>
    <div class="page-header">
      <h1>Playbook 管理</h1>
      <RouterLink to="/playbooks/new">
        <button>建立新 Playbook</button>
      </RouterLink>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>名稱</th>
          <th>描述</th>
          <th>建立者</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td colspan="5">載入中...</td>
        </tr>
        <tr v-if="error">
          <td colspan="5" class="error-message">{{ error }}</td>
        </tr>
        <tr v-for="playbook in playbooks" :key="playbook.id">
          <td>{{ playbook.id }}</td>
          <td>{{ playbook.name }}</td>
          <td>{{ playbook.description }}</td>
          <td>{{ playbook.created_by }}</td>
          <td>
            <RouterLink :to="`/playbooks/edit/${playbook.id}`">
              <button class="btn-secondary" style="margin-right: 5px;">編輯</button>
            </RouterLink>
            <button @click="deletePlaybook(playbook.id)" class="btn-danger">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router'

const auth = useAuthStore()
const playbooks = ref([])
const loading = ref(false)
const error = ref(null)

const fetchPlaybooks = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get('/playbooks/')
    playbooks.value = response.data
  } catch (err) {
    error.value = '讀取 Playbook 列表失敗'
  } finally {
    loading.value = false
  }
}

onMounted(fetchPlaybooks)

const deletePlaybook = async (id) => {
  if (!auth.isAdmin) {
    alert('只有管理員可以刪除 Playbook');
    return;
  }
  if (confirm('您確定要刪除此 Playbook 嗎？')) {
    try {
      await apiClient.delete(`/playbooks/${id}`)
      fetchPlaybooks() // 重新整理列表
    } catch (err) {
      alert('刪除失敗')
    }
  }
}
</script>