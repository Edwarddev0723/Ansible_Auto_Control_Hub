<template>
  <nav class="sidebar">
    <div class="logo">Ansible UI</div>
    <ul class="nav-links">
      <li><RouterLink to="/">儀表板</RouterLink></li>
      <li class="separator">執行</li>
      <li><RouterLink to="/deploy">執行部署</RouterLink></li>
      <li><RouterLink to="/history">部署紀錄</RouterLink></li>
      
      <li class="separator">設定</li>
      <li><RouterLink to="/playbooks">Playbooks</RouterLink></li>
      <li><RouterLink to="/inventory">Inventory</RouterLink></li>
      <li><RouterLink to="/ai">AI 助理</RouterLink></li>
      
      <li v-if="auth.isAdmin" class="admin-section">
        <li class="separator">管理</li>
        <RouterLink to="/admin/users">使用者管理</RouterLink>
      </li>
    </ul>
    <div class="user-info">
      <p>{{ auth.userEmail }}</p>
      <p>({{ auth.user?.role }})</p>
      <button @click="auth.logout()" class="btn-danger">登出</button>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  height: 100vh;
  flex-shrink: 0;
}
.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2rem;
}
.nav-links {
  list-style: none;
  padding: 0;
  flex-grow: 1;
}
.nav-links li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #bdc3c7;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s;
}
.nav-links li a:hover,
.nav-links li a.router-link-exact-active {
  background: #34495e;
  color: white;
}

.separator {
  font-size: 0.8rem;
  color: #7f8c8d;
  text-transform: uppercase;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  padding: 0 1rem;
}

.user-info {
  border-top: 1px solid #34495e;
  padding-top: 1rem;
  text-align: center;
}
.user-info p {
  font-size: 0.9rem;
  word-break: break-all;
  margin-bottom: 0.25rem;
}
.user-info button {
  padding: 0.5rem 1rem;
  margin-top: 0.5rem;
  width: 100%;
}
</style>