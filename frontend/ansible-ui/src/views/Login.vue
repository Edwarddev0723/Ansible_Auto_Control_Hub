<template>
  <div class="login-box">
    <h2>Ansible 部署平台</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" :disabled="loading" style="width: 100%;">
        {{ loading ? '登入中...' : '登入' }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  loading.value = true
  error.value = null
  try {
    // 呼叫 store 中的 login action
    await authStore.login(email.value, password.value)
    // 登入成功會自動跳轉 (在 auth.js 中設定)
  } catch (err) {
    error.value = '登入失敗，請檢查帳號或密碼。'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-box {
  width: 360px;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}
</style>