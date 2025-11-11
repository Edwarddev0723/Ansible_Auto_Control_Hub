<template>
  <AppLayout>
    <!-- Header -->
    <header class="h-[100px] border-b border-[#E6EFF5] bg-white px-4 lg:px-10 flex items-center">
      <h1 class="text-xl lg:text-[28px] font-semibold text-primary ml-12 lg:ml-0">Playbook 管理與執行</h1>
    </header>

    <div class="flex-1 bg-[#F5F7FA] p-4 lg:p-14">
      <div class="mx-auto max-w-[1036px]">
        <!-- Search + Actions -->
        <div class="mb-6 flex flex-col items-stretch gap-4 lg:flex-row lg:items-center">
          <div class="relative w-full lg:w-[412px]">
            <svg
              class="absolute left-4 top-1/2 h-4 w-5 -translate-y-1/2 opacity-50"
              viewBox="0 0 20 16"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g opacity="0.5">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M11.3589 11.658C14.7499 10.5296 16.3306 7.46249 14.8894 4.8074C13.4483 2.15231 9.53101 0.914669 6.13999 2.04306C2.74897 3.17144 1.16828 6.23856 2.60943 8.89365C4.05058 11.5487 7.96783 12.7864 11.3589 11.658Z"
                  stroke="black"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path d="M13.4663 10.5437L18.6405 14.5956" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </g>
            </svg>
            <input
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              type="text"
              placeholder="Search"
              class="h-[39px] w-full rounded-[20px] border border-[#D5D5D5] bg-[#F5F6FA] pl-14 pr-4 text-sm font-normal text-[#202224] opacity-60 placeholder:text-[#202224] placeholder:opacity-60 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-[#4379EE]"
            />
          </div>

          <div class="flex justify-end gap-2 lg:gap-4">
            <button
              @click="runSelected"
              class="h-12 whitespace-nowrap rounded-md bg-[#EF3826] px-5 text-xs font-bold text-white transition-colors hover:bg-[#d52f1f] lg:text-sm"
              style="font-family: 'Nunito Sans', sans-serif"
            >
              執行
            </button>
            <button
              @click="createPlaybook"
              class="h-12 whitespace-nowrap rounded-md bg-[#4379EE] px-5 text-xs font-bold text-white transition-colors hover:bg-[#3868dd] lg:text-sm"
              style="font-family: 'Nunito Sans', sans-serif"
            >
              新增
            </button>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-hidden rounded-[14px] border-[0.3px] border-[#B9B9B9] bg-white">
          <div class="overflow-x-auto">
            <div class="min-w-[900px] border-b-[0.8px] border-[#E0E0E0] px-4 py-6 lg:px-8">
              <div class="grid grid-cols-[40px,1fr,150px,150px,150px] items-center gap-4">
                <div class="w-5"></div>
                <div class="text-sm font-bold text-[#202224]" style="font-family: 'Nunito Sans', sans-serif">名稱</div>
                <div class="text-sm font-semibold text-[#202224] opacity-90" style="font-family: 'Nunito Sans', sans-serif">型態</div>
                <div class="text-sm font-semibold text-[#202224] opacity-90" style="font-family: 'Nunito Sans', sans-serif">結果狀態</div>
                <div class="text-sm font-semibold text-[#202224] opacity-70" style="font-family: 'Nunito Sans', sans-serif">編輯</div>
              </div>
            </div>

            <div class="min-w-[900px] divide-y divide-[#E0E0E0]" style="border-top-width: 0.8px">
              <div
                v-for="item in filteredItems"
                :key="item.id"
                class="px-4 py-5 transition-colors hover:bg-gray-50 lg:px-8"
              >
                <div class="grid grid-cols-[40px,1fr,150px,150px,150px] items-center gap-4">
                  <input type="checkbox" v-model="item.selected" class="h-4 w-5 cursor-pointer rounded border-[1.2px] border-[#B3B3B3]" />

                  <div class="text-sm font-bold text-[#202224]" style="font-family: 'Nunito Sans', sans-serif">{{ item.name }}</div>

                  <div class="text-sm font-semibold text-[#202224] opacity-90" style="font-family: 'Nunito Sans', sans-serif">{{ item.type }}</div>

                  <div>
                    <span
                      :class="[
                        'inline-flex items-center justify-center rounded-sm px-3 py-1 text-xs font-semibold',
                        item.status === 'Success'
                          ? 'bg-[#FD9A56] bg-opacity-20 text-[#FD9A56]'
                          : item.status === 'Fail'
                          ? 'bg-[#5A8CFF] bg-opacity-20 text-[#5A8CFF]'
                          : 'bg-[#B0B7C3] bg-opacity-20 text-[#7A8899]',
                      ]"
                      style="font-family: 'Nunito Sans', sans-serif"
                    >
                      {{ item.status }}
                    </span>
                  </div>

                  <div class="flex items-center gap-2">
                    <button
                      @click="editItem(item)"
                      class="rounded-lg border border-[#D5D5D5] bg-[#FAFBFD] p-2 transition-colors hover:bg-gray-100"
                    >
                      <svg class="h-4 w-4 opacity-60" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M7.19678 10.1239L4.72217 10.4779L5.07549 8.00258L11.4395 1.63856C12.0253 1.05277 12.975 1.05277 13.5608 1.63856C14.1466 2.22435 14.1466 3.17411 13.5608 3.75989L7.19678 10.1239Z"
                          stroke="black"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path d="M10.7319 2.34595L12.8533 4.46729" stroke="black" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
                        <path d="M11 10.2V15.2C11 15.7522 10.5523 16.2 10 16.2H0C-0.552285 16.2 -1 15.7522 -1 15.2V5.19995C-1 4.64767 -0.552285 4.19995 0 4.19995H5" stroke="black" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
                      </svg>
                    </button>
                    <div class="h-8 w-px bg-[#979797] opacity-70"></div>
                    <button
                      @click="deleteItem(item)"
                      class="rounded-lg border border-[#D5D5D5] bg-[#FAFBFD] p-2 transition-colors hover:bg-red-50"
                    >
                      <svg class="h-4 w-4" viewBox="0 0 13 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M11.2001 14.0999H2.8001C2.13736 14.0999 1.6001 13.5626 1.6001 12.8999V1.99995H12.4001V12.8999C12.4001 13.5626 11.8628 14.0999 11.2001 14.0999Z"
                          stroke="#EF3826"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path d="M5.20032 10.5V5.69995" stroke="#EF3826" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
                        <path d="M8.80035 10.5V5.69995" stroke="#EF3826" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
                        <path d="M-0.799805 2.09995H14.8002" stroke="#EF3826" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
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

            <!-- Footer -->
            <div class="flex min-w-[900px] flex-col items-center justify-between gap-4 border-t-[0.8px] border-[#E0E0E0] px-4 py-4 lg:flex-row lg:py-6 lg:px-8">
              <div class="text-sm font-semibold text-[#202224] opacity-60" style="font-family: 'Nunito Sans', sans-serif">
                Showing {{ filteredItems.length > 0 ? 1 : 0 }}-{{ filteredItems.length }} of {{ items.length }} items
              </div>
              <div class="flex items-center">
                <button
                  @click="previousPage"
                  :disabled="currentPage === 1"
                  class="rounded-lg border border-[#D5D5D5] bg-[#FAFBFD] px-4 py-2 transition-colors hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  <svg class="h-6 w-6 opacity-60" viewBox="0 0 20 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5.41 10.1663L0.83 5.75994L5.41 1.35351L4 -0.000122L-2 5.75994L4 11.5199L5.41 10.1663Z" fill="#202224" />
                  </svg>
                </button>
                <div class="mx-2 h-8 w-px bg-[#979797] opacity-70"></div>
                <button
                  @click="nextPage"
                  :disabled="currentPage >= totalPages"
                  class="rounded-lg border border-[#D5D5D5] bg-[#FAFBFD] px-4 py-2 transition-colors hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  <svg class="h-6 w-6 opacity-90" viewBox="0 0 8 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0.59 10.1663L5.17 5.75994L0.59 1.35351L2 -0.000122L8 5.75994L2 11.5199L0.59 10.1663Z" fill="#202224" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'
import { getPlaybooks, deletePlaybook as apiDeletePlaybook, executePlaybooks } from '@/api/playbook'

interface PlaybookItem {
  id: number
  name: string
  type: 'Machine' | 'Other'
  status: 'Success' | 'Fail' | 'Not start'
  selected: boolean
}

const router = useRouter()
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const items = ref<PlaybookItem[]>([])
const loading = ref(false)
const totalItems = ref(0)

// 載入 Playbooks
const loadPlaybooks = async () => {
  try {
    loading.value = true
    const response = await getPlaybooks({
      search: searchQuery.value || undefined,
      page: currentPage.value,
      per_page: itemsPerPage.value,
    })
    
    if (response.success) {
      items.value = response.data.items.map(item => ({
        id: item.id,
        name: item.name,
        type: item.type,
        status: item.status,
        selected: false,
      }))
      totalItems.value = response.data.pagination.total
    }
  } catch (error) {
    console.error('載入 Playbooks 失敗:', error)
    alert('載入資料失敗，請確認後端服務是否正常運行')
  } finally {
    loading.value = false
  }
}

// 組件掛載時載入資料
onMounted(() => {
  loadPlaybooks()
})

const filteredItems = computed(() => {
  return items.value
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value) || 1)

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    loadPlaybooks()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadPlaybooks()
  }
}

const runSelected = async () => {
  const selected = items.value.filter((i) => i.selected)
  if (selected.length === 0) {
    alert('請至少選擇一個 Playbook')
    return
  }
  
  try {
    const response = await executePlaybooks({
      playbook_ids: selected.map(s => s.id),
    })
    
    if (response.success) {
      alert(`${response.message}\nJob ID: ${response.data.job_id}`)
      // 重新載入列表以更新狀態
      loadPlaybooks()
    }
  } catch (error) {
    console.error('執行失敗:', error)
    alert('執行失敗，請稍後再試')
  }
}

const createPlaybook = () => {
  router.push('/playbook/new')
}

const editItem = (item: PlaybookItem) => {
  router.push(`/playbook/edit/${item.id}`)
}

const deleteItem = async (item: PlaybookItem) => {
  if (confirm(`確定刪除 ${item.name} ?`)) {
    try {
      const response = await apiDeletePlaybook(item.id)
      if (response.success) {
        alert(response.message || 'Playbook 刪除成功')
        loadPlaybooks()
      }
    } catch (error) {
      console.error('刪除失敗:', error)
      alert('刪除失敗，請稍後再試')
    }
  }
}

// 監聽搜尋變化
const handleSearch = () => {
  currentPage.value = 1
  loadPlaybooks()
}
</script>
