<template>
  <AppLayout>
    <div class="px-[25px] py-[40px] flex-1">
      <!-- 標題 -->
      <div class="mb-[30px]">
        <h1 class="text-[28px] font-fredoka text-primary mb-[10px]">
          Ansible Galaxy Collections
        </h1>
        <p class="text-[#718EBF] text-[16px]">管理 Ansible Collections 和依賴套件</p>
      </div>

      <!-- Tab 切換 -->
      <div class="mb-[25px] border-b border-[#E6EFF5]">
        <div class="flex gap-[20px]">
          <button
            @click="activeTab = 'requirements'"
            :class="[
              'px-[20px] py-[12px] text-[16px] font-medium transition-colors relative',
              activeTab === 'requirements'
                ? 'text-[#1814F3]'
                : 'text-[#718EBF] hover:text-[#1814F3]',
            ]"
          >
            Requirements.yml
            <div
              v-if="activeTab === 'requirements'"
              class="absolute bottom-0 left-0 right-0 h-[3px] bg-[#1814F3] rounded-t"
            ></div>
          </button>
          <button
            @click="activeTab = 'installed'"
            :class="[
              'px-[20px] py-[12px] text-[16px] font-medium transition-colors relative',
              activeTab === 'installed'
                ? 'text-[#1814F3]'
                : 'text-[#718EBF] hover:text-[#1814F3]',
            ]"
          >
            已安裝 Collections
            <div
              v-if="activeTab === 'installed'"
              class="absolute bottom-0 left-0 right-0 h-[3px] bg-[#1814F3] rounded-t"
            ></div>
          </button>
        </div>
      </div>

      <!-- Requirements.yml 管理 -->
      <div v-if="activeTab === 'requirements'" class="space-y-[25px]">
        <!-- 操作按鈕 -->
        <div class="flex justify-between items-center">
          <h2 class="text-[20px] font-semibold text-primary">Collections 列表</h2>
          <div class="flex gap-[10px]">
            <button
              @click="loadRequirements"
              class="px-[20px] py-[10px] border border-[#DFEAF2] rounded-[15px] text-[#718EBF] hover:bg-gray-50 transition-colors"
              :disabled="loading"
            >
              🔄 重新載入
            </button>
            <button
              @click="installAllCollections"
              class="px-[20px] py-[10px] bg-[#1814F3] text-white rounded-[15px] hover:bg-[#1410C0] transition-colors"
              :disabled="loading || requirements.length === 0"
            >
              📦 全部安裝
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-[40px]">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#1814F3]"></div>
          <p class="mt-[15px] text-[#718EBF]">載入中...</p>
        </div>

        <!-- Collections 卡片列表 -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-[20px]">
          <div
            v-for="(col, index) in requirements"
            :key="index"
            class="bg-white border border-[#E6EFF5] rounded-[25px] p-[25px] hover:shadow-lg transition-shadow"
          >
            <div class="flex items-start justify-between mb-[15px]">
              <div class="flex-1">
                <h3 class="text-[18px] font-semibold text-primary mb-[5px]">
                  {{ col.name }}
                </h3>
                <p class="text-[14px] text-[#718EBF]">
                  版本: {{ col.version || 'latest' }}
                </p>
              </div>
              <button
                @click="removeCollection(index)"
                class="text-red-500 hover:text-red-700 transition-colors"
                title="移除"
              >
                ❌
              </button>
            </div>
            <div class="flex gap-[10px]">
              <button
                @click="installSingleCollection(col)"
                class="flex-1 px-[15px] py-[8px] bg-[#E7EDFF] text-[#1814F3] rounded-[10px] text-[14px] font-medium hover:bg-[#D0DBFF] transition-colors"
              >
                📥 安裝
              </button>
              <button
                @click="editCollection(index)"
                class="flex-1 px-[15px] py-[8px] border border-[#DFEAF2] text-[#718EBF] rounded-[10px] text-[14px] font-medium hover:bg-gray-50 transition-colors"
              >
                ✏️ 編輯
              </button>
            </div>
          </div>

          <!-- 新增 Collection 卡片 -->
          <div
            class="bg-gradient-to-br from-[#E7EDFF] to-[#F5F7FF] border-2 border-dashed border-[#1814F3] rounded-[25px] p-[25px] flex flex-col items-center justify-center cursor-pointer hover:border-solid transition-all"
            @click="showAddDialog = true"
          >
            <div class="text-[48px] text-[#1814F3] mb-[10px]">➕</div>
            <p class="text-[16px] font-medium text-[#1814F3]">新增 Collection</p>
          </div>
        </div>

        <!-- YAML 預覽 -->
        <div v-if="yamlPreview" class="bg-white border border-[#E6EFF5] rounded-[25px] p-[25px]">
          <h3 class="text-[18px] font-semibold text-primary mb-[15px]">
            requirements.yml 預覽
          </h3>
          <pre
            class="bg-gray-50 p-[15px] rounded-[15px] text-[14px] overflow-x-auto"
          ><code>{{ yamlPreview }}</code></pre>
        </div>
      </div>

      <!-- 已安裝 Collections -->
      <div v-if="activeTab === 'installed'" class="space-y-[25px]">
        <div class="flex justify-between items-center">
          <h2 class="text-[20px] font-semibold text-primary">已安裝的 Collections</h2>
          <button
            @click="loadInstalledCollections"
            class="px-[20px] py-[10px] border border-[#DFEAF2] rounded-[15px] text-[#718EBF] hover:bg-gray-50 transition-colors"
            :disabled="loading"
          >
            🔄 重新載入
          </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-[40px]">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#1814F3]"></div>
          <p class="mt-[15px] text-[#718EBF]">載入中...</p>
        </div>

        <!-- 已安裝列表 -->
        <div v-else-if="installedCollections.length > 0" class="bg-white border border-[#E6EFF5] rounded-[25px] overflow-hidden">
          <table class="w-full">
            <thead class="bg-[#F5F7FA]">
              <tr>
                <th class="px-[25px] py-[15px] text-left text-[14px] font-semibold text-[#718EBF]">
                  Collection
                </th>
                <th class="px-[25px] py-[15px] text-left text-[14px] font-semibold text-[#718EBF]">
                  版本
                </th>
                <th class="px-[25px] py-[15px] text-left text-[14px] font-semibold text-[#718EBF]">
                  路徑
                </th>
                <th class="px-[25px] py-[15px] text-left text-[14px] font-semibold text-[#718EBF]">
                  操作
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(col, index) in installedCollections"
                :key="index"
                class="border-t border-[#E6EFF5] hover:bg-[#F5F7FA] transition-colors"
              >
                <td class="px-[25px] py-[15px] text-[14px] text-primary font-medium">
                  {{ col.name }}
                </td>
                <td class="px-[25px] py-[15px] text-[14px] text-[#718EBF]">
                  {{ col.version }}
                </td>
                <td class="px-[25px] py-[15px] text-[14px] text-[#718EBF] truncate max-w-[300px]">
                  {{ col.path }}
                </td>
                <td class="px-[25px] py-[15px]">
                  <button
                    @click="uninstallSingleCollection(col.name)"
                    class="text-red-500 hover:text-red-700 text-[14px] font-medium"
                  >
                    🗑️ 卸載
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 空狀態 -->
        <div v-else class="text-center py-[60px]">
          <div class="text-[64px] mb-[15px]">📦</div>
          <p class="text-[18px] text-[#718EBF]">尚未安裝任何 Collections</p>
        </div>
      </div>
    </div>

    <!-- 新增/編輯 Collection 對話框 -->
    <div
      v-if="showAddDialog"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeAddDialog"
    >
      <div class="bg-white rounded-[25px] p-[30px] w-[500px] max-w-[90%]">
        <h3 class="text-[22px] font-semibold text-primary mb-[20px]">
          {{ editingIndex !== null ? '編輯' : '新增' }} Collection
        </h3>
        <div class="space-y-[15px]">
          <div>
            <label class="block text-[14px] font-medium text-[#718EBF] mb-[8px]">
              Collection 名稱 *
            </label>
            <input
              v-model="newCollection.name"
              type="text"
              placeholder="例如: community.docker"
              class="w-full px-[15px] py-[12px] border border-[#DFEAF2] rounded-[15px] focus:outline-none focus:border-[#1814F3]"
            />
          </div>
          <div>
            <label class="block text-[14px] font-medium text-[#718EBF] mb-[8px]">
              版本 (選填)
            </label>
            <input
              v-model="newCollection.version"
              type="text"
              placeholder="例如: 4.8.1 或留空使用 latest"
              class="w-full px-[15px] py-[12px] border border-[#DFEAF2] rounded-[15px] focus:outline-none focus:border-[#1814F3]"
            />
          </div>
        </div>
        <div class="flex gap-[10px] mt-[25px]">
          <button
            @click="closeAddDialog"
            class="flex-1 px-[20px] py-[12px] border border-[#DFEAF2] rounded-[15px] text-[#718EBF] hover:bg-gray-50 transition-colors"
          >
            取消
          </button>
          <button
            @click="saveCollection"
            class="flex-1 px-[20px] py-[12px] bg-[#1814F3] text-white rounded-[15px] hover:bg-[#1410C0] transition-colors"
            :disabled="!newCollection.name"
          >
            {{ editingIndex !== null ? '更新' : '新增' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 操作結果提示 -->
    <div
      v-if="showToast"
      class="fixed bottom-[30px] right-[30px] bg-white border border-[#E6EFF5] rounded-[20px] p-[25px] shadow-2xl z-50 w-[500px] max-w-[90vw]"
    >
      <div class="flex items-start gap-[15px]">
        <div class="text-[32px] flex-shrink-0">{{ toastData.icon }}</div>
        <div class="flex-1 min-w-0">
          <h4 class="text-[18px] font-semibold text-primary mb-[8px]">
            {{ toastData.title }}
          </h4>
          <p class="text-[14px] text-[#718EBF] break-words">{{ toastData.message }}</p>
          <pre
            v-if="toastData.details"
            class="mt-[12px] text-[12px] bg-gray-50 p-[12px] rounded-[10px] max-h-[200px] overflow-auto whitespace-pre-wrap break-words"
          >{{ toastData.details }}</pre>
        </div>
        <button @click="showToast = false" class="text-[#718EBF] hover:text-primary text-[20px] flex-shrink-0 ml-[10px]">
          ✕
        </button>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import {
  listInstalledCollections,
  installCollection,
  uninstallCollection,
  getRequirements,
  updateRequirements,
  installRequirements,
  type Collection,
  type InstalledCollection,
} from '../api/galaxy'

const activeTab = ref<'requirements' | 'installed'>('requirements')
const loading = ref(false)
const requirements = ref<Collection[]>([])
const installedCollections = ref<InstalledCollection[]>([])
const yamlPreview = ref('')

// 新增/編輯對話框
const showAddDialog = ref(false)
const editingIndex = ref<number | null>(null)
const newCollection = ref<Collection>({
  name: '',
  version: '',
})

// Toast 提示
const showToast = ref(false)
const toastData = ref({
  icon: '',
  title: '',
  message: '',
  details: '',
})

// 載入 requirements.yml
async function loadRequirements() {
  try {
    loading.value = true
    const data = await getRequirements()
    requirements.value = data.collections || []
    yamlPreview.value = data.yaml
  } catch (error: any) {
    showToastMessage('❌', '載入失敗', error.message || '無法載入 requirements.yml')
  } finally {
    loading.value = false
  }
}

// 載入已安裝的 collections
async function loadInstalledCollections() {
  try {
    loading.value = true
    installedCollections.value = await listInstalledCollections()
  } catch (error: any) {
    showToastMessage('❌', '載入失敗', error.message || '無法載入已安裝的 Collections')
  } finally {
    loading.value = false
  }
}

// 安裝所有 collections
async function installAllCollections() {
  if (!confirm('確定要安裝 requirements.yml 中的所有 Collections 嗎?')) return

  try {
    loading.value = true
    const result = await installRequirements()
    if (result.success) {
      showToastMessage(
        '✅',
        '安裝成功',
        '所有 Collections 已安裝',
        result.output || ''
      )
      await loadInstalledCollections()
    } else {
      showToastMessage('❌', '安裝失敗', result.message, result.error || '')
    }
  } catch (error: any) {
    showToastMessage('❌', '安裝失敗', error.message || '安裝過程發生錯誤')
  } finally {
    loading.value = false
  }
}

// 安裝單一 collection
async function installSingleCollection(col: Collection) {
  if (!confirm(`確定要安裝 ${col.name} 嗎?`)) return

  try {
    loading.value = true
    const result = await installCollection(col.name, col.version)
    if (result.success) {
      showToastMessage('✅', '安裝成功', `${col.name} 已安裝`)
      await loadInstalledCollections()
    } else {
      showToastMessage('❌', '安裝失敗', result.message, result.error || '')
    }
  } catch (error: any) {
    showToastMessage('❌', '安裝失敗', error.message || '安裝過程發生錯誤')
  } finally {
    loading.value = false
  }
}

// 卸載 collection
async function uninstallSingleCollection(name: string) {
  try {
    loading.value = true
    const result = await uninstallCollection(name)
    showToastMessage('ℹ️', '卸載資訊', result.message, result.note || '')
  } catch (error: any) {
    showToastMessage('❌', '操作失敗', error.message || '卸載過程發生錯誤')
  } finally {
    loading.value = false
  }
}

// 移除 collection (從 requirements)
function removeCollection(index: number) {
  if (!confirm('確定要從 requirements.yml 移除此 Collection 嗎?')) return
  requirements.value.splice(index, 1)
  saveRequirements()
}

// 編輯 collection
function editCollection(index: number) {
  editingIndex.value = index
  newCollection.value = { ...requirements.value[index] }
  showAddDialog.value = true
}

// 儲存 collection (新增或編輯)
function saveCollection() {
  if (!newCollection.value.name) {
    alert('請輸入 Collection 名稱')
    return
  }

  if (editingIndex.value !== null) {
    // 編輯模式
    requirements.value[editingIndex.value] = { ...newCollection.value }
  } else {
    // 新增模式
    requirements.value.push({ ...newCollection.value })
  }

  saveRequirements()
  closeAddDialog()
}

// 關閉對話框
function closeAddDialog() {
  showAddDialog.value = false
  editingIndex.value = null
  newCollection.value = { name: '', version: '' }
}

// 儲存 requirements.yml
async function saveRequirements() {
  try {
    loading.value = true
    await updateRequirements(requirements.value)
    await loadRequirements() // 重新載入以更新 YAML 預覽
    showToastMessage('✅', '儲存成功', 'requirements.yml 已更新')
  } catch (error: any) {
    showToastMessage('❌', '儲存失敗', error.message || '無法儲存 requirements.yml')
  } finally {
    loading.value = false
  }
}

// 顯示 Toast 提示
function showToastMessage(
  icon: string,
  title: string,
  message: string,
  details: string = ''
) {
  toastData.value = { icon, title, message, details }
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 5000)
}

// 初始化
onMounted(() => {
  loadRequirements()
  loadInstalledCollections()
})
</script>

<style scoped>
/* 自訂樣式 */
</style>
