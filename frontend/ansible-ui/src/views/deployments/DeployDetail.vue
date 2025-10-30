<template>
  <div>
    <h1>部署紀錄 #{{ id }}</h1>
    <div v-if="loading && !job">載入中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="job" class="job-details">
      <div class="job-summary">
        <div><strong>Playbook:</strong> {{ job.playbook.name }}</div>
        <div><strong>執行者:</strong> {{ job.executor.email }}</div>
        <div><strong>開始時間:</strong> {{ new Date(job.start_time).toLocaleString() }}</div>
        <div><strong>結束時間:</strong> {{ job.end_time ? new Date(job.end_time).toLocaleString() : 'N/A' }}</div>
        <div>
          <strong>狀態:</strong> 
          <span :class="`status-${job.status}`">{{ job.status }}</span>
        </div>
      </div>

      <h2>Ansible 執行日誌</h2>
      <LogViewer :log="job.log_output" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import apiClient from '@/services/api'
import LogViewer from '@/components/LogViewer.vue'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const job = ref(null)
const loading = ref(false)
const error = ref(null)
let pollInterval = null // 儲存輪詢的計時器

const fetchJobDetails = async () => {
  try {
    const response = await apiClient.get(`/deployments/${props.id}`)
    job.value = response.data
    
    // 如果任務還在執行中，繼續輪詢
    if (job.value.status === 'pending' || job.value.status === 'running') {
      startPolling()
    } else {
      stopPolling() // 任務完成，停止輪詢
    }
    
  } catch (err) {
    error.value = '讀取部署詳情失敗'
    stopPolling()
  } finally {
    loading.value = false
  }
}

const startPolling = () => {
  // 如果計時器已存在，先清除
  stopPolling()
  // 每 3 秒鐘抓取一次
  pollInterval = setInterval(fetchJobDetails, 3000)
}

const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

onMounted(() => {
  loading.value = true
  fetchJobDetails() // 立即抓取第一次
})

onUnmounted(() => {
  stopPolling() // 組件銷毀時，務必停止輪詢
})
</script>

<style scoped>
.job-summary {
  background: #f9f9f9;
  border: 1px solid #eee;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.job-summary div {
  font-size: 1.1rem;
}

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