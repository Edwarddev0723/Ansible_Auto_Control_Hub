<template>
  <div class="app-layout" v-if="auth.isAuthenticated">
    <NavBar />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
  
  <div class="login-layout" v-else>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'

const auth = useAuthStore()
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
}
.main-content {
  flex-grow: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: #f4f7f6;
}
.login-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
</style>