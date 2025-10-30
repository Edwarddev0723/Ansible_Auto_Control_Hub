<template>
  <div>
    <h1>部署紀錄</h1>

    <table class="data-table">
      <thead>
        <tr>
          <th>Job ID</th>
          <th>Playbook</th>
          <th>執行者</th>
          <th>狀態</th>
          <th>開始時間</th>
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
        <tr v-for="job in jobs" :key="job.id">
          <td>{{ job.id }}</td>
          <td>{{ job.playbook.name }}</td>
          <td>{{ job.executor.email }}</td>
          <td>
            <span :class="`status-${job.status}`">{{ job.status }}</span>
          </td>
          <td>{{ new Date(job.start_time).toLocaleString() }}</td>
          <td>
            <RouterLink :to="`/history/${job.id}`">
              <button class="btn-secondary">查看日誌</button>
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import apiClient from '@/services/api'

const jobs = ref([])
const loading = ref(false)
const error = ref(null)

const fetchHistory = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await apiClient.get('/deployments/')
    jobs.value = response.data
  } catch (err) {
    error.value = '讀取部署紀錄失敗'
  } finally {
    loading.value = false
  }
}

onMounted(fetchHistory)
</script>

<style scoped>
/* 狀態顏色 */
.status-pending, .status-running {
  color: #f39c12;
  font-weight: bold;
}
.status-success {
  color: #2ecc71;
  font-weight: bold;
}
.status-failed {
  color: #e74c3c;
  font-weight: bold;
}
</style>