<template>
  <div class="how-container">
    <div class="section-header">
      <el-icon :size="48" class="header-icon"><Setting /></el-icon>
      <h2>Ansible 運作方式</h2>
    </div>

    <div class="workflow-steps">
      <el-timeline>
        <el-timeline-item 
          timestamp="步驟 1" 
          placement="top"
          type="primary"
          :icon="Connection"
          size="large"
        >
          <el-card class="step-card">
            <h3>SSH 連接</h3>
            <p>控制節點（Control Node）透過 SSH 與被管理節點建立安全連線，無需在目標主機安裝代理程式。</p>
          </el-card>
        </el-timeline-item>

        <el-timeline-item 
          timestamp="步驟 2" 
          placement="top"
          type="success"
          :icon="Grid"
          size="large"
        >
          <el-card class="step-card">
            <h3>執行模組</h3>
            <p>使用內建或自訂模組（modules）執行特定任務，例如安裝套件、管理服務、配置系統等。</p>
          </el-card>
        </el-timeline-item>

        <el-timeline-item 
          timestamp="步驟 3" 
          placement="top"
          type="warning"
          :icon="DocumentCopy"
          size="large"
        >
          <el-card class="step-card">
            <h3>Playbook 編排</h3>
            <p>將多個任務寫在 Playbook 中，按照定義的順序執行，實現複雜的自動化流程。</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>

    <el-divider />

    <div class="info-section">
      <el-alert 
        title="無代理架構優勢" 
        type="info" 
        :closable="false"
        show-icon
      >
        <template #default>
          <p><strong>只需要 SSH 與 Python 環境</strong></p>
          <ul>
            <li>無需在目標主機安裝額外軟體</li>
            <li>減少維護成本與安全風險</li>
            <li>快速部署，立即可用</li>
          </ul>
        </template>
      </el-alert>
    </div>

    <div class="architecture-box">
      <h3>架構示意</h3>
      <div class="arch-diagram">
        <div class="arch-node control">
          <el-icon :size="40"><Monitor /></el-icon>
          <p>控制節點</p>
        </div>
        <div class="arch-arrow">
          <el-icon :size="32"><Right /></el-icon>
          <span>SSH</span>
        </div>
        <div class="arch-nodes-group">
          <div class="arch-node managed">
            <el-icon :size="32"><Platform /></el-icon>
            <p>主機 1</p>
          </div>
          <div class="arch-node managed">
            <el-icon :size="32"><Platform /></el-icon>
            <p>主機 2</p>
          </div>
          <div class="arch-node managed">
            <el-icon :size="32"><Platform /></el-icon>
            <p>主機 N</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Setting, Connection, Grid, DocumentCopy, Monitor, Platform, Right } from '@element-plus/icons-vue'

export default { 
  name: 'How',
  components: { Setting, Connection, Grid, DocumentCopy, Monitor, Platform, Right }
}
</script>

<style scoped>
.how-container {
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
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

.workflow-steps {
  margin: 32px 0;
}

.step-card {
  border-radius: 12px;
  border-left: 4px solid #667eea;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
}

.step-card h3 {
  font-size: 20px;
  color: #333;
  margin: 0 0 12px 0;
}

.step-card p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.info-section {
  margin: 32px 0;
}

.info-section ul {
  margin: 12px 0 0 20px;
  color: #666;
  line-height: 1.8;
}

.architecture-box {
  margin-top: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 100%);
  border-radius: 12px;
}

.architecture-box h3 {
  font-size: 22px;
  color: #333;
  margin: 0 0 24px 0;
  text-align: center;
}

.arch-diagram {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
}

.arch-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.arch-node.control {
  border: 3px solid #667eea;
}

.arch-node.managed {
  border: 2px solid #ddd;
}

.arch-node p {
  margin: 0;
  font-weight: 600;
  color: #333;
}

.arch-arrow {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #667eea;
}

.arch-arrow span {
  font-size: 14px;
  font-weight: 600;
}

.arch-nodes-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
</style>
