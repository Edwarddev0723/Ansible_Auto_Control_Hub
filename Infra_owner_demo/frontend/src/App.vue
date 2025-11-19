<template>
  <div class="app-wrapper">
    <el-header class="top-header">
      <div class="header-content">
        <div class="brand">
          <el-icon :size="32" style="margin-right: 12px;"><Tools /></el-icon>
          <h1 class="brand-title">Ansible 自動化平台</h1>
        </div>
        <el-button type="primary" size="large" round @click="openDocs">
          <el-icon style="margin-right: 8px"><Document /></el-icon>
          官方文件
        </el-button>
      </div>

      <el-menu mode="horizontal" :default-active="activeIndex" class="top-menu" @select="onSelect">
        <el-menu-item index="1" >
          <el-icon><InfoFilled /></el-icon>
          <span>什麼是 Ansible</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><Setting /></el-icon>
          <span>運作方式</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><DocumentCopy /></el-icon>
          <span>Playbook 範例</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><Suitcase /></el-icon>
          <span>使用情境</span>
        </el-menu-item>
      </el-menu>
    </el-header>

    <div class="main-container">
      <el-main class="content-main">
        <transition name="fade" mode="out-in">
          <el-card class="content-card" :key="current" shadow="hover">
            <component :is="currentComponent" />
          </el-card>
        </transition>
      </el-main>
    </div>

    <el-footer class="app-footer">
      <div class="footer-content">
        <span>Created with Vue 3 + Element Plus</span>
        <span class="footer-divider">|</span>
        <span>© 2025 Ansible 介紹專案</span>
      </div>
    </el-footer>
  </div>
</template>

<script>
import { Tools, Document, InfoFilled, Setting, DocumentCopy, Suitcase } from '@element-plus/icons-vue'
import What from './components/What.vue'
import How from './components/How.vue'
import Playbook from './components/Playbook.vue'
import UseCase from './components/UseCase.vue'

export default {
  name: 'App',
  components: { What, How, Playbook, UseCase, Tools, Document, InfoFilled, Setting, DocumentCopy, Suitcase },
  data() {
    return { 
      current: 'what',
      activeIndex: '1'
    }
  },
  computed: {
    currentComponent() {
      return {
        what: 'What',
        how: 'How',
        playbook: 'Playbook',
        usecase: 'UseCase'
      }[this.current]
    }
  },
  methods: {
    select(k) { this.current = k },
    openDocs() { window.open('https://docs.ansible.com/', '_blank') },
    onSelect(index) {
      this.activeIndex = index
      const map = { '1': 'what', '2': 'how', '3': 'playbook', '4': 'usecase' }
      this.current = map[index] || 'what'
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.top-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 10px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  color: #667eea;
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.top-menu {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  margin: 10px -2px;
}

.top-menu .el-menu-item {
  padding: 0px 10px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;

}

.top-menu .el-menu-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.top-menu .el-menu-item.is-active {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
  border-bottom-color: #667eea;
}

.main-container {
  padding-top: 160px;
  padding-bottom: 80px;
  min-height: 100vh;
}

.content-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
}

.content-card {
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.content-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.app-footer {
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  color: white;
  padding: 24px;
  text-align: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.footer-divider {
  opacity: 0.5;
}

/* 過渡動畫 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
