import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import Dashboard from '@/views/Dashboard.vue'
import Login from '@/views/Login.vue'
import HostList from '@/views/inventory/HostList.vue'
import PlaybookList from '@/views/playbooks/PlaybookList.vue'
import PlaybookEditor from '@/views/playbooks/PlaybookEditor.vue'
import DeployExecute from '@/views/deployments/DeployExecute.vue'
import DeployHistory from '@/views/deployments/DeployHistory.vue'
import DeployDetail from '@/views/deployments/DeployDetail.vue'
import AiAssistant from '@/views/ai/AiAssistant.vue'
import UserManagement from '@/views/admin/UserManagement.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true } // 這個頁面需要登入
  },
  // (模組2)
  {
    path: '/inventory',
    name: 'Inventory',
    component: HostList,
    meta: { requiresAuth: true, requiresDev: true } // (Dev+)
  },
  // (模組3)
  {
    path: '/playbooks',
    name: 'PlaybookList',
    component: PlaybookList,
    meta: { requiresAuth: true, requiresDev: true }
  },
  {
    path: '/playbooks/new', // 建立
    name: 'PlaybookCreate',
    component: PlaybookEditor,
    meta: { requiresAuth: true, requiresDev: true }
  },
  {
    path: '/playbooks/edit/:id', // 編輯
    name: 'PlaybookEdit',
    component: PlaybookEditor,
    props: true, // 將 :id 作為 prop 傳入組件
    meta: { requiresAuth: true, requiresDev: true }
  },
  // (模組4)
  {
    path: '/deploy',
    name: 'DeployExecute',
    component: DeployExecute,
    meta: { requiresAuth: true, requiresDev: true }
  },
  // (模組5)
  {
    path: '/history',
    name: 'DeployHistory',
    component: DeployHistory,
    meta: { requiresAuth: true, requiresDev: true }
  },
  {
    path: '/history/:id', // 部署詳情
    name: 'DeployDetail',
    component: DeployDetail,
    props: true,
    meta: { requiresAuth: true, requiresDev: true }
  },
  // (模組7)
  {
    path: '/ai',
    name: 'AiAssistant',
    component: AiAssistant,
    meta: { requiresAuth: true, requiresDev: true }
  },
  // (模組1/6)
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, requiresAdmin: true } // (Admin)
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// (關鍵) 導航守衛 (Navigation Guard)
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 1. 檢查頁面是否需要登入
  if (to.meta.requiresAuth) {
    
    // 2. 如果使用者資訊還沒加載 (例如剛刷新頁面)，先嘗試獲取
    //    (我們已在 main.js 處理，但這裡做雙重保險)
    if (!authStore.user && authStore.token) {
      await authStore.fetchUser()
    }

    // 3. 檢查是否已登入
    if (!authStore.isAuthenticated) {
      return next({ name: 'Login' })
    }

    // 4. 檢查 Admin 權限
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
      return next({ name: 'Dashboard' })
    }
    
    // 5. 檢查 Developer 權限
    if (to.meta.requiresDev && !authStore.isDeveloper) {
      return next({ name: 'Dashboard' })
    }

    // 6. 權限足夠，放行
    return next()
    
  } else {
    // 頁面不需要登入 (例如登入頁)，直接放行
    return next()
  }
})

export default router