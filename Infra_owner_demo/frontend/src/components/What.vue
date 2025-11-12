<template>
  <div class="what-container">
    <div class="section-header">
      <el-icon :size="48" class="header-icon"><InfoFilled /></el-icon>
      <h2>什麼是 Ansible？</h2>
    </div>
    
    <div class="intro-text">
      <p>Ansible 是一個開源的自動化工具，用於配置管理、應用程式部署及工作流程編排。它以簡單、無代理（agentless）和聲明式的方式來管理多台主機。</p>
    </div>

    <el-divider />

    <div class="features-grid">
      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="32" color="#67C23A"><CircleCheck /></el-icon>
            <span>無代理架構</span>
          </div>
        </template>
        <p>不需要在目標主機上安裝任何代理程式，僅需 SSH 與 Python 即可運行</p>
      </el-card>

      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="32" color="#409EFF"><Document /></el-icon>
            <span>YAML Playbooks</span>
          </div>
        </template>
        <p>使用簡單易讀的 YAML 格式編寫自動化腳本，降低學習門檻</p>
      </el-card>

      <el-card class="feature-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon :size="32" color="#E6A23C"><Box /></el-icon>
            <span>模組豐富</span>
          </div>
        </template>
        <p>內建數千個模組，涵蓋系統管理、雲端服務、網路設備等各種場景</p>
      </el-card>
    </div>

    <div class="tags-section">
      <el-tag type="success" size="large" effect="dark">無代理</el-tag>
      <el-tag type="primary" size="large" effect="dark">YAML Playbooks</el-tag>
      <el-tag type="warning" size="large" effect="dark">模組豐富</el-tag>
      <el-tag type="danger" size="large" effect="dark">開源免費</el-tag>
      <el-tag type="info" size="large" effect="dark">冪等性</el-tag>
    </div>
  </div>
</template>

<script>
import { InfoFilled, CircleCheck, Document, Box } from '@element-plus/icons-vue'

export default { 
  name: 'What',
  components: { InfoFilled, CircleCheck, Document, Box }
}
</script>

<style scoped>
.what-container {
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.header-icon {
  color: #667eea;
}

.section-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.intro-text {
  font-size: 18px;
  line-height: 1.8;
  color: #666;
  margin-bottom: 24px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin: 32px 0;
}

.feature-card {
  border-radius: 12px;
  border: 2px solid #f0f0f0;
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: #667eea;
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}
</style>
