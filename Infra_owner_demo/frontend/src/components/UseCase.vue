<template>
  <div class="usecase-container">
    <div class="section-header">
      <el-icon :size="48" class="header-icon"><Suitcase /></el-icon>
      <h2>Ansible 使用情境</h2>
    </div>

    <div class="intro-text">
      <p>Ansible 在企業 IT 環境中有廣泛的應用場景，從基礎設施管理到應用部署，都能大幅提升自動化水平。</p>
    </div>

    <el-divider />

    <div class="usecases-grid">
      <el-card class="usecase-card" shadow="hover">
        <div class="usecase-icon">
          <el-icon :size="48" color="#409EFF"><Setting /></el-icon>
        </div>
        <h3>配置管理</h3>
        <p>批量設定大量伺服器的基礎環境，包括系統參數、安全設定、用戶權限等，確保環境一致性。</p>
        <el-divider />
        <div class="usecase-examples">
          <el-tag size="small">系統初始化</el-tag>
          <el-tag size="small">安全加固</el-tag>
          <el-tag size="small">合規檢查</el-tag>
        </div>
      </el-card>

      <el-card class="usecase-card" shadow="hover">
        <div class="usecase-icon">
          <el-icon :size="48" color="#67C23A"><Upload /></el-icon>
        </div>
        <h3>應用部署</h3>
        <p>自動化應用程式部署流程，支援滾動更新、藍綠部署等策略，減少停機時間。</p>
        <el-divider />
        <div class="usecase-examples">
          <el-tag size="small" type="success">零停機部署</el-tag>
          <el-tag size="small" type="success">版本回滾</el-tag>
          <el-tag size="small" type="success">A/B 測試</el-tag>
        </div>
      </el-card>

      <el-card class="usecase-card" shadow="hover">
        <div class="usecase-icon">
          <el-icon :size="48" color="#E6A23C"><Clock /></el-icon>
        </div>
        <h3>定期維運</h3>
        <p>定期執行維運任務，如資料備份、日誌清理、系統更新等，提升運維效率。</p>
        <el-divider />
        <div class="usecase-examples">
          <el-tag size="small" type="warning">定時備份</el-tag>
          <el-tag size="small" type="warning">日誌輪轉</el-tag>
          <el-tag size="small" type="warning">安全掃描</el-tag>
        </div>
      </el-card>

      <el-card class="usecase-card" shadow="hover">
        <div class="usecase-icon">
          <el-icon :size="48" color="#F56C6C"><MostlyCloudy /></el-icon>
        </div>
        <h3>雲端編排</h3>
        <p>與 AWS、Azure、GCP 等雲端平台整合，自動化資源配置與管理，實現基礎設施即代碼（IaC）。</p>
        <el-divider />
        <div class="usecase-examples">
          <el-tag size="small" type="danger">EC2 管理</el-tag>
          <el-tag size="small" type="danger">負載均衡</el-tag>
          <el-tag size="small" type="danger">Auto Scaling</el-tag>
        </div>
      </el-card>

      <el-card class="usecase-card" shadow="hover">
        <div class="usecase-icon">
          <el-icon :size="48" color="#909399"><Connection /></el-icon>
        </div>
        <h3>網路自動化</h3>
        <p>管理網路設備配置，包括路由器、交換機、防火牆等，實現網路基礎設施自動化。</p>
        <el-divider />
        <div class="usecase-examples">
          <el-tag size="small" type="info">配置備份</el-tag>
          <el-tag size="small" type="info">批量變更</el-tag>
          <el-tag size="small" type="info">合規審計</el-tag>
        </div>
      </el-card>

      <el-card class="usecase-card" shadow="hover">
        <div class="usecase-icon">
          <el-icon :size="48" color="#9C27B0"><Monitor /></el-icon>
        </div>
        <h3>容器編排</h3>
        <p>配合 Docker、Kubernetes 等容器技術，實現容器化應用的自動化部署與管理。</p>
        <el-divider />
        <div class="usecase-examples">
          <el-tag size="small" effect="dark">Docker 部署</el-tag>
          <el-tag size="small" effect="dark">K8s 配置</el-tag>
          <el-tag size="small" effect="dark">服務編排</el-tag>
        </div>
      </el-card>
    </div>

    <el-divider />

    <div class="integration-section">
      <h3>
        <el-icon><Link /></el-icon>
        整合生態系統
      </h3>
      <el-card class="integration-card" shadow="never">
        <p>Ansible 常與以下工具和平台整合，構建完整的 DevOps 工具鏈：</p>
        <div class="integration-tags">
          <el-tag effect="plain" size="large">Jenkins</el-tag>
          <el-tag effect="plain" size="large">GitLab CI</el-tag>
          <el-tag effect="plain" size="large">Docker</el-tag>
          <el-tag effect="plain" size="large">Kubernetes</el-tag>
          <el-tag effect="plain" size="large">AWS</el-tag>
          <el-tag effect="plain" size="large">Azure</el-tag>
          <el-tag effect="plain" size="large">Terraform</el-tag>
          <el-tag effect="plain" size="large">Prometheus</el-tag>
          <el-tag effect="plain" size="large">ELK Stack</el-tag>
        </div>
      </el-card>
    </div>

    <el-alert 
      class="summary-alert"
      type="info" 
      :closable="false"
    >
      <template #title>
        <div style="display: flex; align-items: center; gap: 8px;">
          <el-icon :size="20"><InfoFilled /></el-icon>
          <span style="font-size: 18px; font-weight: 600;">總結</span>
        </div>
      </template>
      <p style="margin-top: 12px; line-height: 1.8;">
        Ansible 以其簡單易用、無代理架構和強大的模組生態系統，成為現代 IT 自動化的首選工具。
        無論是小型團隊還是大型企業，都能透過 Ansible 實現高效的基礎設施管理和應用部署，
        大幅提升運維效率並降低人為錯誤。
      </p>
    </el-alert>
  </div>
</template>

<script>
import { Suitcase, Setting, Upload, Clock, MostlyCloudy, Connection, Monitor, Link, InfoFilled } from '@element-plus/icons-vue'

export default { 
  name: 'UseCase',
  components: { Suitcase, Setting, Upload, Clock, MostlyCloudy, Connection, Monitor, Link, InfoFilled }
}
</script>

<style scoped>
.usecase-container {
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

.usecases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin: 32px 0;
}

.usecase-card {
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #f0f0f0;
  transition: all 0.3s ease;
  text-align: center;
}

.usecase-card:hover {
  border-color: #667eea;
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
}

.usecase-icon {
  margin-bottom: 16px;
}

.usecase-card h3 {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.usecase-card p {
  color: #666;
  line-height: 1.8;
  margin: 0 0 16px 0;
  text-align: left;
}

.usecase-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.integration-section {
  margin: 32px 0;
}

.integration-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 22px;
  color: #333;
  margin-bottom: 16px;
}

.integration-card {
  border-radius: 12px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 100%);
}

.integration-card p {
  color: #666;
  line-height: 1.8;
  margin-bottom: 20px;
}

.integration-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.summary-alert {
  margin-top: 32px;
  border-radius: 12px;
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
  border: none;
}
</style>
