import axios from 'axios'

// 建立 Axios 實例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 請求攔截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在這裡添加 token 等認證資訊
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 響應攔截器
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 統一錯誤處理
    if (error.response) {
      // 伺服器回應錯誤
      console.error('API Error:', error.response.data)
    } else if (error.request) {
      // 請求已發送但沒有收到響應
      console.error('Network Error:', error.message)
    } else {
      // 其他錯誤
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default apiClient
