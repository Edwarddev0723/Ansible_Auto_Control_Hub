import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia()) // 啟用 Pinia
app.use(router)      // 啟用 Vue Router

// 應用程式啟動時，嘗試獲取使用者資訊
// 這樣刷新頁面時，登入狀態會被保留
const authStore = useAuthStore()
if (authStore.token) {
  authStore.fetchUser()
}

app.mount('#app')