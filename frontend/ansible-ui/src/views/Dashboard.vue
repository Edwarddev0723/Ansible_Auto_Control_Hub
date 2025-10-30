<template>
  <div>
    <h1>儀表板</h1>
    <h2>歡迎回來, {{ auth.userEmail }}!</h2>
    <p>請從左側導航欄選擇一項操作。</p>

    <div class="dashboard-grid">
      <RouterLink to="/deploy" class="dash-card">
        <h3>執行部署</h3>
        <p>選擇一個 Playbook 並執行。</p>
      </RouterLink>
      <RouterLink to="/history" class="dash-card">
        <h3>部署紀錄</h3>
        <p>查看過去所有的部署任務。</p>
      </RouterLink>
      <RouterLink to="/playbooks" class="dash-card">
        <h3>Playbook 管理</h3>
        <p>建立或編輯自動化腳本。</p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}
.dash-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  text-decoration: none;
  color: #333;
  transition: transform 0.3s, box-shadow 0.3s;
}
.dash-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.dash-card h3 {
  color: #3498db;
  margin-bottom: 0.5rem;
}
</style>