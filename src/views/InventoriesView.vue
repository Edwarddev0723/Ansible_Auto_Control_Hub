<template>
  <AppLayout>
    <header class="h-[100px] border-b border-[#E6EFF5] bg-white px-4 lg:px-10 flex items-center">
      <h1 class="text-xl lg:text-[28px] font-semibold text-primary ml-12 lg:ml-0">Inventories 清單</h1>
    </header>

    <div class="flex-1 bg-[#F5F7FA] p-4 lg:p-14">
      <div class="max-w-[1036px] mx-auto">
        <div class="flex flex-col lg:flex-row items-stretch lg:items-center gap-4 mb-8">
          <div class="relative w-full lg:w-[412px]">
            <svg
              class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-4 opacity-50"
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
                <path
                  d="M13.4663 10.5437L18.6405 14.5956"
                  stroke="black"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </g>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search"
              class="w-full h-[39px] pl-14 pr-4 bg-[#F5F6FA] border border-[#D5D5D5] rounded-[20px] text-sm font-normal text-[#202224] opacity-60 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-[#4379EE] placeholder:text-[#202224] placeholder:opacity-60"
            />
          </div>

          <div class="flex items-center gap-2 lg:gap-4 justify-end">
            <button
              @click="testSSHConnection"
              class="h-12 px-3 lg:px-4 bg-[#9643EE] text-white text-xs lg:text-sm font-bold rounded-md hover:bg-[#8639d9] transition-colors whitespace-nowrap"
              style="font-family: 'Nunito Sans', sans-serif"
            >
              SSH連線測試
            </button>
            <button
              @click="addNewInventory"
              class="h-12 px-5 lg:px-7 bg-[#4379EE] text-white text-xs lg:text-sm font-bold rounded-md hover:bg-[#3868dd] transition-colors whitespace-nowrap"
              style="font-family: 'Nunito Sans', sans-serif"
            >
              新增
            </button>
          </div>
        </div>

        <div class="bg-white rounded-[14px] border-[0.3px] border-[#B9B9B9] overflow-hidden">
          <div class="overflow-x-auto">
            <div class="px-4 lg:px-8 py-6 border-b-[0.8px] border-[#E0E0E0] min-w-[900px]">
              <div class="grid grid-cols-[auto,1fr,150px,150px,150px,150px] gap-4 items-center">
                <div class="w-5"></div>
                <div class="text-sm font-bold text-[#202224]" style="font-family: 'Nunito Sans', sans-serif">
                  伺服器名稱
                </div>
                <div
                  class="text-sm font-semibold text-[#202224] opacity-90"
                  style="font-family: 'Nunito Sans', sans-serif"
                >
                  伺服器狀態
                </div>
                <div
                  class="text-sm font-semibold text-[#202224] opacity-90"
                  style="font-family: 'Nunito Sans', sans-serif"
                >
                  SSH 連線狀態
                </div>
                <div
                  class="text-sm font-semibold text-[#202224] opacity-90"
                  style="font-family: 'Nunito Sans', sans-serif"
                >
                  伺服器群組
                </div>
                <div
                  class="text-sm font-semibold text-[#202224] opacity-70"
                  style="font-family: 'Nunito Sans', sans-serif"
                >
                  編輯
                </div>
              </div>
            </div>

            <div class="divide-y divide-[#E0E0E0] min-w-[900px]" style="border-top-width: 0.8px">
              <div
                v-for="inventory in filteredInventories"
                :key="inventory.id"
                class="px-4 lg:px-8 py-5 hover:bg-gray-50 transition-colors"
              >
                <div class="grid grid-cols-[auto,1fr,150px,150px,150px,150px] gap-4 items-center">
                  <input
                    type="checkbox"
                    v-model="inventory.selected"
                    class="w-5 h-4 rounded border-[1.2px] border-[#B3B3B3] cursor-pointer"
                  />
                  <div class="text-sm font-bold text-[#202224]" style="font-family: 'Nunito Sans', sans-serif">
                    {{ inventory.name }}
                  </div>
                  <div>
                    <span
                      :class="[
                        'inline-flex items-center justify-center px-3 py-1 text-xs font-semibold rounded-sm',
                        inventory.status === 'On'
                          ? 'bg-[#FD9A56] bg-opacity-20 text-[#FD9A56]'
                          : 'bg-[#5A8CFF] bg-opacity-20 text-[#5A8CFF]',
                      ]"
                      style="font-family: 'Nunito Sans', sans-serif"
                    >
                      {{ inventory.status }}
                    </span>
                  </div>
                  <div
                    class="text-sm font-semibold text-[#202224] opacity-90"
                    style="font-family: 'Nunito Sans', sans-serif"
                  >
                    {{ inventory.sshStatus }}
                  </div>
                  <div
                    class="text-sm font-semibold text-[#202224] opacity-90"
                    style="font-family: 'Nunito Sans', sans-serif"
                  >
                    {{ inventory.group }}
                  </div>
                  <div class="flex items-center gap-2">
                    <button
                      @click="editInventory(inventory)"
                      class="p-2 bg-[#FAFBFD] border border-[#D5D5D5] rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <svg
                        class="w-4 h-4 opacity-60"
                        viewBox="0 0 14 16"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          fill-rule="evenodd"
                          clip-rule="evenodd"
                          d="M7.19678 10.1239L4.72217 10.4779L5.07549 8.00258L11.4395 1.63856C12.0253 1.05277 12.975 1.05277 13.5608 1.63856C14.1466 2.22435 14.1466 3.17411 13.5608 3.75989L7.19678 10.1239Z"
                          stroke="black"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M10.7319 2.34595L12.8533 4.46729"
                          stroke="black"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M11 10.2V15.2C11 15.7522 10.5523 16.2 10 16.2H0C-0.552285 16.2 -1 15.7522 -1 15.2V5.19995C-1 4.64767 -0.552285 4.19995 0 4.19995H5"
                          stroke="black"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                    </button>
                    <div class="w-px h-8 bg-[#979797] opacity-70"></div>
                    <button
                      @click="deleteInventory(inventory)"
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

            <div
              class="px-4 lg:px-8 py-4 lg:py-6 flex flex-col lg:flex-row items-center justify-between gap-4 border-t-[0.8px] border-[#E0E0E0] min-w-[900px]"
            >
              <div
                class="text-sm font-semibold text-[#202224] opacity-60"
                style="font-family: 'Nunito Sans', sans-serif"
              >
                Showing {{ filteredInventories.length > 0 ? 1 : 0 }}-{{ filteredInventories.length }} of
                {{ inventories.length }} items
              </div>
              <div class="flex items-center">
                <button
                  @click="previousPage"
                  :disabled="currentPage === 1"
                  class="px-4 py-2 bg-[#FAFBFD] border border-[#D5D5D5] rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <svg class="w-6 h-6 opacity-60" viewBox="0 0 20 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M5.41 10.1663L0.83 5.75994L5.41 1.35351L4 -0.000122L-2 5.75994L4 11.5199L5.41 10.1663Z"
                      fill="#202224"
                    />
                  </svg>
                </button>
                <div class="w-px h-8 bg-[#979797] opacity-70 mx-2"></div>
                <button
                  @click="nextPage"
                  :disabled="currentPage >= totalPages"
                  class="px-4 py-2 bg-[#FAFBFD] border border-[#D5D5D5] rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <svg class="w-6 h-6 opacity-90" viewBox="0 0 8 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M0.59 10.1663L5.17 5.75994L0.59 1.35351L2 -0.000122L8 5.75994L2 11.5199L0.59 10.1663Z"
                      fill="#202224"
                    />
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const router = useRouter()

interface Inventory {
  id: number
  name: string
  status: 'On' | 'Off'
  sshStatus: string
  group: string
  selected: boolean
}

const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)

const inventories = ref<Inventory[]>([
  {
    id: 1,
    name: 'Ansible GUI Inventory',
    status: 'On',
    sshStatus: 'Connected',
    group: 'Default',
    selected: false,
  },
  {
    id: 2,
    name: 'Ansible introduction Inventory',
    status: 'Off',
    sshStatus: 'Unconnected',
    group: 'Default',
    selected: false,
  },
])

const filteredInventories = computed(() => {
  if (!searchQuery.value) {
    return inventories.value
  }
  return inventories.value.filter((inv) =>
    inv.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
  )
})

const totalPages = computed(() => {
  return Math.ceil(filteredInventories.value.length / itemsPerPage.value)
})

const testSSHConnection = () => {
  alert('SSH連線測試功能')
}

const addNewInventory = () => {
  router.push('/inventory/new')
}

const editInventory = (inventory: Inventory) => {
  router.push(`/inventory/edit/${inventory.id}`)
}

const deleteInventory = (inventory: Inventory) => {
  if (confirm(`確定要刪除 ${inventory.name}?`)) {
    const index = inventories.value.findIndex((inv) => inv.id === inventory.id)
    if (index > -1) {
      inventories.value.splice(index, 1)
    }
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}
</script>
