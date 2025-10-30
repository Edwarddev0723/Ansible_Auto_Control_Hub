<template>
  <div>
    <h1>AI 智能助理</h1>
    <p>請用自然語言描述您的部署需求：</p>

    <form @submit.prevent="generatePlaybook">
      <div class="form-group">
        <label for="prompt">您的指令</label>
        <input id="prompt" v-model="prompt" placeholder="例如：幫我安裝 nginx 並啟動服務" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'AI 思考中...' : '生成 Playbook' }}
      </button>
    </form>
    
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="generatedContent" class="result-box">
      <h2>AI 產生的 Playbook</h2>
      <pre class="yaml-viewer">{{ generatedContent }}</pre>
      <div class="actions">
        <button @click="savePlaybook" :disabled="saveLoading">
          {{ saveLoading ? '儲存中...' : '儲存到 Playbook 管理' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

const router = useRouter()
const prompt = ref('')
const generatedContent = ref(null)
const loading = ref(false)
const saveLoading = ref(false)
const error = ref(null)

const generatePlaybook = async () => {
  loading.value = true
  error.value = null
  generatedContent.value = null
  try {
    const response = await apiClient.post('/ai/generate-playbook', {
      prompt: prompt.value
    })
    generatedContent.value = response.data.generated_playbook_content
  } catch (err) {
    error.value = 'AI 生成失敗'
  } finally {
    loading.value = false
  }
}

const savePlaybook = async () => {
  saveLoading.value = true
  error.value = null
  try {
    await apiClient.post('/ai/save-ai-playbook', {
      prompt: prompt.value,
      generated_playbook_content: generatedContent.value
    })
    // 儲存成功，跳轉到 Playbook 列表
    router.push('/playbooks')
  } catch (err) {
    error.value = '儲存 AI Playbook 失敗'
  } finally {
    saveLoading.value = false
  }
}
</script>

<style scoped>
.result-box {
  margin-top: 2rem;
}
.yaml-viewer {
  background: #fdf6e3; /* 不同的日誌顏色 */
  color: #657b83;
  padding: 1rem;
  border: 1px solid #eee8d5;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
}
.actions {
  margin-top: 1rem;
}
</style>