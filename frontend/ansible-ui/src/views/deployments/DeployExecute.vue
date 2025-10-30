<template>
  <div>
    <h1>執行部署</h1>
    <p>選擇要執行的 Playbook 和目標伺服器。</p>

    <div v-if="loading" class="loading">載入 Playbooks 和 伺服器...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="handleDeploy" v-if="!loading && !error">
      <div class="form-group">
        <label for="playbook">選擇 Playbook</label>
        <select id="playbook" v-model="selectedPlaybook" required>
          <option disabled value="">請選擇</option>
          <option v-for="pb in playbooks" :key="pb.id" :value="pb.id">
            {{ pb.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>選擇伺服器 (可多選)</label>
        <select v-model="selectedHosts" multiple required class="host-select">
          <option v-for="host in hosts" :key="host.id" :value="host.id">
            {{ host.name }} ({{ host.ip_address }}) [{{ host.group }}]
          </option>
        </select>
      </div>
      
      <button type="submit" :disabled="deployLoading">
        {{ deployLoading ? '部署中...' : '開始執行' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

const router = useRouter()
const playbooks = ref([])
const hosts = ref([])
const loading = ref(false)
const deployLoading = ref(false)
const error = ref(null)

const selectedPlaybook = ref('')
const selectedHosts = ref([])

const fetchData = async () => {
  loading.value = true
  error.value = null
  try {
    // 同時獲取 Playbooks 和 Hosts
    const [pbResponse, hostResponse] = await Promise.all([
      apiClient.get('/playbooks/'),
      apiClient.get('/inventory/')
    ])
    playbooks.value = pbResponse.data
    hosts.value = hostResponse.data
  } catch (err) {
    error.value = '讀取資料失敗'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

const handleDeploy = async () => {
  deployLoading.value = true
  error.value = null
  try {
    const response = await apiClient.post('/deployments/', {
      playbook_id: selectedPlaybook.value,
      host_ids: selectedHosts.value
    })
    
    // 部署請求已接受 (202)，跳轉到該 Job 的詳情頁面
    const jobId = response.data.id
    router.push(`/history/${jobId}`)
    
  } catch (err) {
    error.value = '部署失敗'
  } finally {
    deployLoading.value = false
  }
}
</script>

<style scoped>
.host-select {
  height: 200px;
}
</style>