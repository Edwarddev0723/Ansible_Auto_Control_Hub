<template>
  <AppLayout>
    <div class="min-h-screen bg-[#FAFBFD] p-6">
      <!-- Header -->
      <h1 class="mb-6 text-2xl font-semibold text-[#333B69]">Inventory 設定</h1>

      <!-- Main Content Card -->
      <div class="rounded-2xl bg-white p-6 shadow-sm">
        <!-- Ansible GUI Inventory Title -->
        <h2 class="mb-4 text-lg font-medium text-[#4379EE]">Ansible GUI Inventory</h2>

        <!-- Configuration Text Area -->
        <div class="mb-6">
          <textarea
            v-model="inventoryConfig"
            class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-4 font-mono text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            rows="15"
            placeholder="輸入 Ansible Inventory 配置..."
          ></textarea>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end gap-4">
          <!-- Cancel Button -->
          <button
            @click="handleCancel"
            class="rounded-lg bg-gray-400 px-8 py-3 font-medium text-white transition-colors hover:bg-gray-500"
          >
            Cancel
          </button>

          <!-- Save Button -->
          <button
            @click="handleSave"
            class="rounded-lg bg-[#1814F3] px-8 py-3 font-medium text-white transition-colors hover:bg-[#4379EE]"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const route = useRoute()

// Inventory configuration content
const inventoryConfig = ref('')

// Initialize with existing data if editing
onMounted(() => {
  const id = route.params.id
  if (id) {
    // Load existing inventory configuration
    // In a real app, this would fetch from an API
    inventoryConfig.value = 'server1 ansible_ssh_host=127.0.0.1 ansible_ssh_port=55000 ansible_ssh_pass=docker'
  }
})

// Handle Cancel action
const handleCancel = () => {
  router.push('/')
}

// Handle Save action
const handleSave = () => {
  // In a real app, this would save to an API
  console.log('Saving inventory configuration:', inventoryConfig.value)
  
  // Show success message (you can add a toast notification here)
  alert('Inventory 配置已儲存！')
  
  // Navigate back to inventories list
  router.push('/')
}
</script>
