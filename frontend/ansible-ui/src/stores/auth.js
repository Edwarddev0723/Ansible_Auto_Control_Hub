import { defineStore } from 'pinia'
import apiClient from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  // 狀態：從 localStorage 讀取 token，以保持登入狀態
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null // 也保存 user 資訊
  }),

  // Getters (計算屬性)
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
    isDeveloper: (state) => state.user?.role === 'developer' || state.user?.role === 'admin',
    userEmail: (state) => state.user?.email || 'N/A'
  },

  // Actions (方法)
  actions: {
    async login(email, password) {
      try {
        // (模組1) 呼叫 /auth/token
        const params = new URLSearchParams()
        params.append('username', email)
        params.append('password', password)

        const response = await apiClient.post('/auth/token', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        
        // 登入成功
        const token = response.data.access_token
        this.token = token
        localStorage.setItem('token', token)
        
        // 登入後，立即獲取使用者資訊
        await this.fetchUser()

        // 導向到儀表板
        router.push('/')

      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    async fetchUser() {
      if (!this.token) return
      try {
        // (模組1) 呼叫 /auth/users/me
        const response = await apiClient.get('/auth/users/me')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (error) {
        console.error('Failed to fetch user:', error)
        // 如果獲取失敗 (例如 token 過期)，就登出
        this.logout()
      }
    },

    logout() {
      // 清除所有狀態並導向到登入頁
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
  }
})