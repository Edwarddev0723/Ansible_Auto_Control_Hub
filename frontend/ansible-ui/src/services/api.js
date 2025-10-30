import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router' // 引入 router

// 建立 Axios 實例
const apiClient = axios.create({
  // 您的 FastAPI 後端 URL
  baseURL: 'http://127.0.0.1:8000/api/v1', 
  headers: {
    'Content-Type': 'application/json'
  }
})

// (關鍵) 請求攔截器 (Request Interceptor)
// 在 *每個* 請求發送前，自動附上 JWT Token
apiClient.interceptors.request.use(
  (config) => {
    // 從 Pinia store 獲取 auth 狀態
    const authStore = useAuthStore()
    const token = authStore.token

    if (token) {
      // 如果 token 存在，將其加入到 Authorization 標頭
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// (可選) 回應攔截器
// 可以在這裡集中處理 401/403 錯誤，例如自動登出
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const authStore = useAuthStore()
    
    if (error.response && error.response.status === 401) {
      // 如果收到 401 (未授權)，可能是 token 過期
      authStore.logout() // 觸發登出
    }
    
    if (error.response && error.response.status === 403) {
      // 如果收到 403 (禁止)，表示權限不足
      // 導向到首頁
      router.push('/')
    }
    
    return Promise.reject(error)
  }
)

export default apiClient