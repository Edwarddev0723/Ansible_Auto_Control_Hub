<template>
  <AppLayout>
    <header class="h-[100px] border-b border-[#E6EFF5] bg-white px-10 flex items-center">
      <h1 class="text-[28px] font-semibold text-primary">{{ pageTitle }}</h1>
    </header>

    <div class="flex-1 bg-[#F5F7FA] flex items-center justify-center">
      <div class="text-center">
        <div class="text-6xl mb-4">🚧</div>
        <h2 class="text-2xl font-semibold text-[#343C6A] mb-2">頁面建置中</h2>
        <p class="text-[#B1B1B1]">此頁面尚未完成，請繼續提示以填充內容</p>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const route = useRoute()

const pageTitle = computed(() => {
  switch (route.name) {
    case 'playbook':
      return 'PlayBook 管理與執行'
    case 'ai-deploy':
      return 'AI 對話部屬'
    default:
      return '頁面'
  }
})
</script>
