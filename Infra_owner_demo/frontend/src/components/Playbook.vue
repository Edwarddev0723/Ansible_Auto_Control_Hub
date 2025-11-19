<template>
  <div class="playbook-container">
    <div class="section-header">
      <el-icon :size="48" class="header-icon"><DocumentCopy /></el-icon>
      <h2>Playbook 範例</h2>
    </div>

    <div class="intro-text">
      <p>Playbook 是 Ansible 的核心概念，使用 YAML 格式編寫，描述要在目標主機上執行的任務序列。</p>
    </div>

    <el-divider />

    <div class="example-section">
      <h3>
        <el-icon><Reading /></el-icon>
        基礎範例：安裝並啟動 Nginx
      </h3>
      
      <el-card class="code-card" shadow="hover">
        <div class="code-header">
          <el-tag type="success">nginx-setup.yml</el-tag>
          <el-button 
            size="small" 
            type="primary" 
            :icon="CopyDocument"
            @click="copyCode"
          >
            複製
          </el-button>
        </div>
        <pre class="code-block"><code>---
- name: 安裝並啟動 Nginx 伺服器
  hosts: webservers
  become: yes
  
  tasks:
    - name: 更新 APT 套件快取
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: 安裝 Nginx
      apt:
        name: nginx
        state: present
    
    - name: 確保 Nginx 服務啟動並開機自動執行
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: 複製自訂設定檔
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: 重啟 Nginx
  
  handlers:
    - name: 重啟 Nginx
      service:
        name: nginx
        state: restarted</code></pre>
      </el-card>
    </div>

    <el-divider />

    <div class="features-section">
      <h3>Playbook 關鍵概念</h3>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="concept-card" shadow="hover">
            <template #header>
              <div class="concept-header">
                <el-icon :size="24" color="#409EFF"><List /></el-icon>
                <span>Tasks</span>
              </div>
            </template>
            <p>定義具體要執行的操作，每個 task 調用一個模組完成特定功能。</p>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="concept-card" shadow="hover">
            <template #header>
              <div class="concept-header">
                <el-icon :size="24" color="#67C23A"><Checked /></el-icon>
                <span>Idempotent</span>
              </div>
            </template>
            <p>冪等性保證：多次執行同一 Playbook 結果一致，不會造成重複變更。</p>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="concept-card" shadow="hover">
            <template #header>
              <div class="concept-header">
                <el-icon :size="24" color="#E6A23C"><Bell /></el-icon>
                <span>Handlers</span>
              </div>
            </template>
            <p>當任務觸發變更時執行的特殊任務，常用於重啟服務。</p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-alert 
      class="tip-alert"
      title="💡 最佳實踐" 
      type="success" 
      :closable="false"
    >
      <ul>
        <li>使用有意義的任務名稱（name），方便除錯和維護</li>
        <li>善用變數和模板，提高 Playbook 的重用性</li>
        <li>執行前先用 <code>--check</code> 模式進行乾跑測試</li>
        <li>將複雜邏輯拆分為多個角色（roles）以提高可維護性</li>
      </ul>
    </el-alert>
  </div>
</template>

<script>
import { DocumentCopy, Reading, CopyDocument, List, Checked, Bell } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default { 
  name: 'Playbook',
  components: { DocumentCopy, Reading, CopyDocument, List, Checked, Bell },
  methods: {
    copyCode() {
      const code = document.querySelector('.code-block code').textContent
      navigator.clipboard.writeText(code).then(() => {
        ElMessage.success('程式碼已複製到剪貼簿')
      }).catch(() => {
        ElMessage.error('複製失敗')
      })
    }
  }
}
</script>

<style scoped>
.playbook-container {
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

.example-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 22px;
  color: #333;
  margin-bottom: 16px;
}

.code-card {
  border-radius: 12px;
  background: #1e1e1e;
  border: none;
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #3a3a3a;
}

.code-block {
  margin: 0;
  padding: 0;
  background: transparent;
  overflow-x: auto;
}

.code-block code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #d4d4d4;
  display: block;
  white-space: pre;
}

.features-section {
  margin: 32px 0;
}

.features-section h3 {
  font-size: 22px;
  color: #333;
  margin-bottom: 20px;
}

.concept-card {
  border-radius: 12px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.concept-card:hover {
  transform: translateY(-4px);
}

.concept-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.concept-card p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.tip-alert {
  margin-top: 32px;
  border-radius: 12px;
}

.tip-alert ul {
  margin: 12px 0 0 20px;
  line-height: 1.8;
}

.tip-alert code {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
}
</style>
