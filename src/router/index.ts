import { createRouter, createWebHistory } from 'vue-router'
import InventoriesView from '../views/InventoriesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inventories',
      component: InventoriesView,
    },
    {
      path: '/playbook',
      name: 'playbook',
      component: () => import('../views/PlaybookView.vue'),
    },
    {
      path: '/playbook/new',
      name: 'playbook-new',
      component: () => import('../views/PlaybookCreateView.vue'),
    },
    {
      path: '/ai-deploy',
      name: 'ai-deploy',
      component: () => import('../views/AITalkView.vue'),
    },
    {
      path: '/inventory/new',
      name: 'inventory-new',
      component: () => import('../views/InventoryDetailView.vue'),
    },
    {
      path: '/inventory/edit/:id',
      name: 'inventory-edit',
      component: () => import('../views/InventoryDetailView.vue'),
    },
  ],
})

export default router
