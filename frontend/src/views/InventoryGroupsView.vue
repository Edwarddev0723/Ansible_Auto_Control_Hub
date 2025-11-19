<template>
  <AppLayout>
    <header class="h-[100px] border-b border-[#E6EFF5] bg-white px-4 lg:px-10 flex items-center">
      <h1 class="text-xl lg:text-[28px] font-semibold text-primary ml-12 lg:ml-0">Inventory 群組管理</h1>
    </header>

    <div class="flex-1 bg-[#F5F7FA] p-4 lg:p-14">
      <div class="max-w-[1036px] mx-auto">
        <div class="flex flex-col lg:flex-row items-stretch lg:items-center gap-4 mb-8">
          <div class="flex-1"></div>
          <div class="flex items-center gap-2 lg:gap-4 justify-end">
            <button
              @click="showAddDialog = true"
              class="h-12 px-5 lg:px-7 bg-[#4379EE] text-white text-xs lg:text-sm font-bold rounded-md hover:bg-[#3868dd] transition-colors whitespace-nowrap"
              style="font-family: 'Nunito Sans', sans-serif"
            >
              新增群組
            </button>
          </div>
        </div>

        <div class="bg-white rounded-[14px] border-[0.3px] border-[#B9B9B9] overflow-hidden">
          <div class="overflow-x-auto">
            <div class="px-4 lg:px-8 py-6 border-b-[0.8px] border-[#E0E0E0] min-w-[600px]">
              <div class="grid grid-cols-[1fr,200px,150px] gap-4 items-center">
                <div class="text-sm font-bold text-[#202224]" style="font-family: 'Nunito Sans', sans-serif">
                  群組名稱
                </div>
                <div class="text-sm font-semibold text-[#202224] opacity-90" style="font-family: 'Nunito Sans', sans-serif">
                  建立時間
                </div>
                <div class="text-sm font-semibold text-[#202224] opacity-70" style="font-family: 'Nunito Sans', sans-serif">
                  操作
                </div>
              </div>
            </div>

            <div v-if="loading" class="px-8 py-12 text-center text-gray-500">
              載入中...
            </div>

            <div v-else-if="groups.length === 0" class="px-8 py-12 text-center text-gray-500">
              尚無群組，請新增第一個群組
            </div>

            <div v-else class="divide-y divide-[#E0E0E0] min-w-[600px]" style="border-top-width: 0.8px">
              <div
                v-for="group in groups"
                :key="group.id"
                class="px-4 lg:px-8 py-5 hover:bg-gray-50 transition-colors"
              >
                <div class="grid grid-cols-[1fr,200px,150px] gap-4 items-center">
                  <div class="text-sm font-bold text-[#202224]" style="font-family: 'Nunito Sans', sans-serif">
                    {{ group.name }}
                  </div>
                  <div class="text-sm font-semibold text-[#202224] opacity-90" style="font-family: 'Nunito Sans', sans-serif">
                    {{ formatDate(group.created_at) }}
                  </div>
                  <div class="flex items-center gap-2">
                    <button
                      @click="deleteGroupItem(group)"
                      class="p-2 bg-[#FAFBFD] border border-[#D5D5D5] rounded-lg hover:bg-red-50 transition-colors"
                    >
                      <svg class="w-4 h-4" viewBox="0 0 13 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M11.2001 14.0999H2.8001C2.13736 14.0999 1.6001 13.5626 1.6001 12.8999V1.99995H12.4001V12.8999C12.4001 13.5626 11.8628 14.0999 11.2001 14.0999Z"
                          stroke="#EF3826"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M5.20032 10.5V5.69995"
                          stroke="#EF3826"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M8.80035 10.5V5.69995"
                          stroke="#EF3826"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M-0.799805 2.09995H14.8002"
                          stroke="#EF3826"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M8.8 -0.300049H5.2C4.53726 -0.300049 4 0.237207 4 0.899951V2.09995H10V0.899951C10 0.237207 9.46274 -0.300049 8.8 -0.300049Z"
                          stroke="#EF3826"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增群組對話框 -->
    <div
      v-if="showAddDialog"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAddDialog = false"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
        <h3 class="text-xl font-semibold text-[#333B69] mb-4">新增群組</h3>
        
        <div class="mb-6">
          <label class="mb-2 block text-sm font-medium text-gray-700">群組名稱</label>
          <input
            v-model="newGroupName"
            type="text"
            class="w-full rounded-lg border border-gray-200 bg-[#FAFBFD] p-3 text-sm text-gray-700 focus:border-[#4379EE] focus:outline-none focus:ring-2 focus:ring-[#4379EE] focus:ring-opacity-20"
            placeholder="例如: Production, Testing, Development"
            @keyup.enter="handleAddGroup"
          />
        </div>

        <div class="flex justify-end gap-4">
          <button
            @click="showAddDialog = false"
            class="rounded-lg bg-gray-400 px-6 py-2 font-medium text-white transition-colors hover:bg-gray-500"
          >
            取消
          </button>
          <button
            @click="handleAddGroup"
            :disabled="!newGroupName.trim() || addingGroup"
            class="rounded-lg bg-[#1814F3] px-6 py-2 font-medium text-white transition-colors hover:bg-[#4379EE] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ addingGroup ? '新增中...' : '新增' }}
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { getGroups, createGroup, deleteGroup, type Group } from '@/api/group'

const groups = ref<Group[]>([])
const loading = ref(false)
const showAddDialog = ref(false)
const newGroupName = ref('')
const addingGroup = ref(false)

// 載入群組
const loadGroups = async () => {
  try {
    loading.value = true
    const response = await getGroups()
    if (response.success) {
      groups.value = response.data
    }
  } catch (error) {
    console.error('載入群組失敗:', error)
    alert('載入群組失敗，請確認後端服務是否正常運行')
  } finally {
    loading.value = false
  }
}

// 新增群組
const handleAddGroup = async () => {
  if (!newGroupName.value.trim()) {
    alert('請輸入群組名稱')
    return
  }

  try {
    addingGroup.value = true
    const response = await createGroup({ name: newGroupName.value.trim() })
    if (response.success) {
      alert(response.message || '群組新增成功')
      showAddDialog.value = false
      newGroupName.value = ''
      loadGroups()
    }
  } catch (error: any) {
    console.error('新增群組失敗:', error)
    alert(error.response?.data?.message || '新增失敗，請稍後再試')
  } finally {
    addingGroup.value = false
  }
}

// 刪除群組
const deleteGroupItem = async (group: Group) => {
  if (confirm(`確定要刪除群組 "${group.name}"？\n\n注意：此操作無法復原`)) {
    try {
      const response = await deleteGroup(group.id)
      if (response.success) {
        alert(response.message || '群組刪除成功')
        loadGroups()
      }
    } catch (error: any) {
      console.error('刪除群組失敗:', error)
      alert(error.response?.data?.message || '刪除失敗，請稍後再試')
    }
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  loadGroups()
})
</script>
