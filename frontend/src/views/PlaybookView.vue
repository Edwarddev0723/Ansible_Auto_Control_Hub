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
              @click="showExecutionInfo"
              class="h-12 whitespace-nowrap rounded-md bg-[#718EBF] px-5 text-xs font-bold text-white transition-colors hover:bg-[#5a7199] lg:text-sm"
              style="font-family: 'Nunito Sans', sans-serif"
            >
              執行系統資訊
            </button>
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
                      @click="previewYaml(item)"
                      class="rounded-lg border border-[#D5D5D5] bg-[#FAFBFD] p-2 transition-colors hover:bg-blue-50"
                      title="預覽 YAML"
                    >
                      <svg class="h-4 w-4 opacity-60" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 3C4.5 3 1.5 5.5 0.5 8C1.5 10.5 4.5 13 8 13C11.5 13 14.5 10.5 15.5 8C14.5 5.5 11.5 3 8 3Z" stroke="black" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="8" cy="8" r="2.5" stroke="black" stroke-width="1.2"/>
                      </svg>
                    </button>
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

    <!-- YAML 預覽對話框 -->
    <div
      v-if="showYamlPreview"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      @click.self="closeYamlPreview"
    >
      <div class="relative mx-4 w-full max-w-4xl rounded-lg bg-white p-6 shadow-xl">
        <!-- 標題列 -->
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-xl font-semibold text-[#333B69]">
            Playbook YAML 預覽: {{ selectedPlaybookName }}
          </h2>
          <button
            @click="closeYamlPreview"
            class="rounded-lg p-2 transition-colors hover:bg-gray-100"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 載入中 -->
        <div v-if="loadingYaml" class="py-20 text-center">
          <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
          <p class="mt-4 text-gray-600">載入中...</p>
        </div>

        <!-- YAML 內容 -->
        <div v-else-if="yamlContent" class="max-h-[70vh] overflow-auto">
          <pre class="rounded-lg bg-gray-900 p-4 text-sm text-green-400"><code>{{ yamlContent }}</code></pre>
        </div>

        <!-- 錯誤訊息 -->
        <div v-else-if="yamlError" class="rounded-lg bg-red-50 p-4 text-red-600">
          <p class="font-semibold">載入失敗</p>
          <p class="mt-2">{{ yamlError }}</p>
        </div>

        <!-- 操作按鈕 -->
        <div class="mt-6 flex justify-end gap-3">
          <button
            @click="copyYamlToClipboard"
            class="rounded-md border border-[#4379EE] bg-white px-4 py-2 text-sm font-semibold text-[#4379EE] transition-colors hover:bg-blue-50"
          >
            複製 YAML
          </button>
          <button
            @click="downloadYaml"
            class="rounded-md bg-[#4379EE] px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-[#3868dd]"
          >
            下載 YAML
          </button>
          <button
            @click="closeYamlPreview"
            class="rounded-md bg-gray-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-gray-600"
          >
            關閉
          </button>
        </div>
      </div>
    </div>

    <!-- 執行進度對話框 -->
    <div
      v-if="showExecutionProgress"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="relative mx-4 w-full max-w-3xl rounded-lg bg-white p-6 shadow-xl">
        <!-- 標題列 -->
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-xl font-semibold text-[#333B69]">
            執行 Playbook
          </h2>
          <button
            v-if="executionProgress === 100 || executionAborted"
            @click="closeExecutionProgress"
            class="rounded-lg p-2 transition-colors hover:bg-gray-100"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 整體進度條 -->
        <div class="mb-6">
          <div class="mb-2 flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700">{{ executionStatus }}</span>
            <span class="text-sm font-medium text-gray-700">{{ executionProgress }}%</span>
          </div>
          <div class="h-3 w-full overflow-hidden rounded-full bg-gray-200">
            <div
              class="h-full transition-all duration-500 ease-out"
              :class="[
                executionProgress === 100 ? 'bg-green-500' : 'bg-blue-500',
                executionAborted ? 'bg-red-500' : ''
              ]"
              :style="{ width: `${executionProgress}%` }"
            ></div>
          </div>
        </div>

        <!-- Job ID -->
        <div v-if="currentJobId" class="mb-4 rounded-lg bg-gray-50 p-3">
          <span class="text-xs text-gray-600">Job ID: </span>
          <span class="text-xs font-mono text-gray-800">{{ currentJobId }}</span>
        </div>

        <!-- Playbook 執行列表 -->
        <div class="max-h-96 space-y-3 overflow-auto">
          <div
            v-for="playbook in executingPlaybooks"
            :key="playbook.id"
            class="rounded-lg border p-4 transition-colors"
            :class="[
              playbook.status === 'success' ? 'border-green-300 bg-green-50' :
              playbook.status === 'failed' || playbook.status === 'error' ? 'border-red-300 bg-red-50' :
              playbook.status === 'aborted' ? 'border-orange-300 bg-orange-50' :
              'border-gray-300 bg-gray-50'
            ]"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <!-- 狀態圖示 -->
                  <span class="text-lg">
                    <span v-if="playbook.status === 'success'">✅</span>
                    <span v-else-if="playbook.status === 'failed' || playbook.status === 'error'">❌</span>
                    <span v-else-if="playbook.status === 'aborted'">⚠️</span>
                    <span v-else>
                      <div class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-solid border-blue-500 border-r-transparent"></div>
                    </span>
                  </span>
                  <h3 class="font-semibold text-gray-900">{{ playbook.name }}</h3>
                </div>
                <p class="mt-1 text-sm text-gray-600">{{ playbook.message }}</p>
                <p v-if="playbook.error" class="mt-1 text-xs text-red-600">{{ playbook.error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按鈕 -->
        <div class="mt-6 flex justify-end gap-3">
          <button
            v-if="executionProgress < 100 && !executionAborted"
            @click="stopExecution"
            class="rounded-md bg-red-500 px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-600"
          >
            強制停止
          </button>
          <button
            v-if="executionProgress === 100 || executionAborted"
            @click="closeExecutionProgress"
            class="rounded-md bg-[#4379EE] px-6 py-2 text-sm font-semibold text-white transition-colors hover:bg-[#3868dd]"
          >
            關閉
          </button>
        </div>
      </div>
    </div>

    <!-- 執行資訊對話框 -->
    <div
      v-if="showExecutionInfoDialog"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      @click.self="closeExecutionInfo"
    >
      <div class="max-h-[90vh] w-[900px] max-w-[95vw] overflow-auto rounded-[25px] bg-white p-[30px]">
        <div class="mb-[25px] flex items-center justify-between">
          <h2 class="text-[24px] font-bold text-primary">Playbook 執行環境資訊</h2>
          <button
            @click="closeExecutionInfo"
            class="text-[#718EBF] hover:text-primary transition-colors text-[24px]"
          >
            ✕
          </button>
        </div>

        <div v-if="loadingExecutionInfo" class="py-[40px] text-center">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#1814F3]"></div>
          <p class="mt-[15px] text-[#718EBF]">載入中...</p>
        </div>

        <div v-else-if="executionInfo" class="space-y-[20px]">
          <!-- 平台資訊 -->
          <div class="rounded-[20px] border border-[#E6EFF5] bg-[#F5F7FA] p-[20px]">
            <h3 class="mb-[15px] text-[18px] font-semibold text-primary">🖥️ 平台資訊</h3>
            <div class="grid grid-cols-2 gap-[12px] text-[14px]">
              <div><span class="font-medium text-[#718EBF]">作業系統:</span> <span class="text-primary">{{ executionInfo.platform.system }}</span></div>
              <div><span class="font-medium text-[#718EBF]">版本:</span> <span class="text-primary">{{ executionInfo.platform.release }}</span></div>
              <div><span class="font-medium text-[#718EBF]">架構:</span> <span class="text-primary">{{ executionInfo.platform.machine }}</span></div>
              <div><span class="font-medium text-[#718EBF]">Python:</span> <span class="text-primary">{{ executionInfo.platform.python_version }}</span></div>
            </div>
          </div>

          <!-- 執行環境 -->
          <div class="rounded-[20px] border border-[#E6EFF5] bg-white p-[20px]">
            <h3 class="mb-[15px] text-[18px] font-semibold text-primary">⚙️ 執行環境</h3>
            <div class="space-y-[12px] text-[14px]">
              <div>
                <span class="font-medium text-[#718EBF]">執行方式:</span>
                <span class="ml-[10px] rounded-md bg-[#E7EDFF] px-[12px] py-[4px] text-[#1814F3] font-medium">{{ executionInfo.execution.method }}</span>
              </div>
              <div><span class="font-medium text-[#718EBF]">當前目錄:</span> <code class="ml-[10px] rounded bg-gray-100 px-[8px] py-[2px] text-[12px] text-primary">{{ executionInfo.execution.current_directory }}</code></div>
              <div><span class="font-medium text-[#718EBF]">專案根目錄:</span> <code class="ml-[10px] rounded bg-gray-100 px-[8px] py-[2px] text-[12px] text-primary">{{ executionInfo.execution.project_root }}</code></div>
              <div><span class="font-medium text-[#718EBF]">臨時目錄:</span> <code class="ml-[10px] rounded bg-gray-100 px-[8px] py-[2px] text-[12px] text-primary">{{ executionInfo.execution.temp_directory_base }}</code></div>
              <div class="text-[13px] text-[#718EBF] italic">💡 {{ executionInfo.execution.temp_directory_note }}</div>
            </div>
          </div>

          <!-- Ansible 資訊 -->
          <div class="rounded-[20px] border border-[#E6EFF5] bg-[#FFF9F5] p-[20px]">
            <h3 class="mb-[15px] text-[18px] font-semibold text-primary">🔧 Ansible 資訊</h3>
            <div class="space-y-[12px] text-[14px]">
              <div><span class="font-medium text-[#718EBF]">安裝路徑:</span> <code class="ml-[10px] rounded bg-gray-100 px-[8px] py-[2px] text-[12px] text-primary">{{ executionInfo.ansible.path }}</code></div>
              <div><span class="font-medium text-[#718EBF]">版本:</span> <span class="ml-[10px] text-primary">{{ executionInfo.ansible.version }}</span></div>
              <div><span class="font-medium text-[#718EBF]">執行命令:</span> <code class="ml-[10px] rounded bg-gray-100 px-[8px] py-[2px] text-[12px] text-primary">{{ executionInfo.ansible.command_prefix }}</code></div>
            </div>
          </div>

          <!-- 路徑轉換 (Windows) -->
          <div v-if="executionInfo.path_conversion" class="rounded-[20px] border border-[#E6EFF5] bg-[#F5FFF9] p-[20px]">
            <h3 class="mb-[15px] text-[18px] font-semibold text-primary">🔄 路徑轉換 (Windows → WSL)</h3>
            <div class="space-y-[12px] text-[14px]">
              <div>
                <div class="font-medium text-[#718EBF] mb-[5px]">Windows 路徑:</div>
                <code class="block rounded bg-gray-100 px-[12px] py-[8px] text-[12px] text-primary break-all">{{ executionInfo.path_conversion.windows_path }}</code>
              </div>
              <div class="text-center text-[20px]">⬇️</div>
              <div>
                <div class="font-medium text-[#718EBF] mb-[5px]">WSL 路徑:</div>
                <code class="block rounded bg-gray-100 px-[12px] py-[8px] text-[12px] text-green-700 break-all">{{ executionInfo.path_conversion.wsl_path }}</code>
              </div>
            </div>
          </div>

          <!-- 執行流程 -->
          <div class="rounded-[20px] border border-[#E6EFF5] bg-white p-[20px]">
            <h3 class="mb-[15px] text-[18px] font-semibold text-primary">📋 執行流程</h3>
            <div class="space-y-[10px]">
              <div class="flex items-start gap-[12px]">
                <span class="flex-shrink-0 flex h-[24px] w-[24px] items-center justify-center rounded-full bg-[#1814F3] text-[12px] font-bold text-white">1</span>
                <p class="text-[14px] text-primary">{{ executionInfo.execution_flow.step1 }}</p>
              </div>
              <div class="flex items-start gap-[12px]">
                <span class="flex-shrink-0 flex h-[24px] w-[24px] items-center justify-center rounded-full bg-[#1814F3] text-[12px] font-bold text-white">2</span>
                <p class="text-[14px] text-primary">{{ executionInfo.execution_flow.step2 }}</p>
              </div>
              <div class="flex items-start gap-[12px]">
                <span class="flex-shrink-0 flex h-[24px] w-[24px] items-center justify-center rounded-full bg-[#1814F3] text-[12px] font-bold text-white">3</span>
                <p class="text-[14px] text-primary break-all">{{ executionInfo.execution_flow.step3 }}</p>
              </div>
              <div class="flex items-start gap-[12px]">
                <span class="flex-shrink-0 flex h-[24px] w-[24px] items-center justify-center rounded-full bg-[#1814F3] text-[12px] font-bold text-white">4</span>
                <p class="text-[14px] text-primary">{{ executionInfo.execution_flow.step4 }}</p>
              </div>
              <div class="mt-[15px] rounded-md bg-[#FFF9F5] border border-orange-200 p-[12px]">
                <p class="text-[13px] text-orange-700"><strong>⚠️ 注意:</strong> {{ executionInfo.execution_flow.note }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-[25px] flex justify-end">
          <button
            @click="closeExecutionInfo"
            class="rounded-[15px] bg-[#1814F3] px-[25px] py-[12px] text-white font-semibold hover:bg-[#1410C0] transition-colors"
          >
            關閉
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'
import { getPlaybooks, deletePlaybook as apiDeletePlaybook, executePlaybooks, getPlaybook, abortJob, getExecutionInfo } from '@/api/playbook'

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

// YAML 預覽相關
const showYamlPreview = ref(false)
const loadingYaml = ref(false)
const yamlContent = ref('')
const yamlError = ref('')
const selectedPlaybookName = ref('')
const selectedPlaybookId = ref<number | null>(null)

// 執行資訊對話框
const showExecutionInfoDialog = ref(false)
const executionInfo = ref<any>(null)
const loadingExecutionInfo = ref(false)

// 執行進度相關
const showExecutionProgress = ref(false)
const executionProgress = ref(0)
const executionStatus = ref('')
const executingPlaybooks = ref<any[]>([])
const currentJobId = ref<string | null>(null)
const executionAborted = ref(false)

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
  
  // 初始化執行狀態
  showExecutionProgress.value = true
  executionProgress.value = 0
  executionStatus.value = '準備執行...'
  executionAborted.value = false
  executingPlaybooks.value = selected.map(s => ({
    id: s.id,
    name: s.name,
    status: 'pending',
    message: '等待執行'
  }))
  
  try {
    executionStatus.value = '正在執行 Playbooks...'
    executionProgress.value = 10
    
    const response = await executePlaybooks({
      playbook_ids: selected.map(s => s.id),
    })
    
    console.log('執行回應:', response)
    
    if (response.success && response.data && response.data.results) {
      currentJobId.value = response.data.job_id
      
      // 模擬進度更新（實際應該輪詢後端狀態）
      const totalPlaybooks = response.data.results.length
      let completedCount = 0
      
      // 更新每個 playbook 的狀態
      response.data.results.forEach((result, index) => {
        completedCount++
        executionProgress.value = 10 + Math.floor((completedCount / totalPlaybooks) * 80)
        
        const playbookIndex = executingPlaybooks.value.findIndex(p => p.id === result.id)
        if (playbookIndex !== -1) {
          executingPlaybooks.value[playbookIndex].status = result.status
          executingPlaybooks.value[playbookIndex].message = result.message
          executingPlaybooks.value[playbookIndex].error = result.error
        }
      })
      
      executionProgress.value = 100
      executionStatus.value = '執行完成！'
      
      // 3 秒後自動關閉進度框
      setTimeout(() => {
        if (!executionAborted.value) {
          showExecutionProgress.value = false
          loadPlaybooks() // 重新載入列表以更新狀態
        }
      }, 3000)
    } else {
      executionStatus.value = '執行完成，但無法取得詳細結果'
      executionProgress.value = 100
      setTimeout(() => {
        showExecutionProgress.value = false
        loadPlaybooks()
      }, 2000)
    }
  } catch (error: any) {
    console.error('執行失敗:', error)
    executionStatus.value = '執行失敗'
    executionProgress.value = 0
    
    const errorMsg = error.response?.data?.message || error.message || '執行失敗，請稍後再試'
    
    // 更新所有 playbook 為失敗狀態
    executingPlaybooks.value.forEach(p => {
      if (p.status === 'pending') {
        p.status = 'error'
        p.message = errorMsg
      }
    })
    
    setTimeout(() => {
      showExecutionProgress.value = false
    }, 3000)
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

// YAML 預覽函數
const previewYaml = async (item: PlaybookItem) => {
  showYamlPreview.value = true
  loadingYaml.value = true
  yamlError.value = ''
  yamlContent.value = ''
  selectedPlaybookName.value = item.name
  selectedPlaybookId.value = item.id

  try {
    const response = await getPlaybook(item.id)
    if (response.success && response.data) {
      const playbook = response.data
      
      // 構建 YAML 結構
      let yaml = `---\n`
      yaml += `- name: ${playbook.name}\n`
      
      // 安全訪問 main 屬性
      if (playbook.main) {
        yaml += `  hosts: ${playbook.main.hosts || 'all'}\n`
        yaml += `  gather_facts: ${playbook.main.gather_facts ?? true}\n`
      }
      
      if (playbook.tasks && playbook.tasks.length > 0) {
        yaml += `  tasks:\n`
        playbook.tasks.forEach((task: any, index: number) => {
          // task.content 是 YAML 格式的字串，直接使用
          const taskContent = task.content || ''
          
          // 將每一行加上適當的縮排
          const lines = taskContent.split('\n')
          let isFirstLine = true
          
          lines.forEach((line: string) => {
            const trimmedLine = line.trim()
            if (!trimmedLine) return // 跳過空行
            
            if (isFirstLine) {
              // 第一行：確保以 "- name:" 開頭
              if (trimmedLine.startsWith('name:')) {
                yaml += `    - ${trimmedLine}\n`
              } else if (trimmedLine.startsWith('- name:')) {
                yaml += `    ${trimmedLine}\n`
              } else {
                // 如果第一行不是 name，先加上默認 name
                yaml += `    - name: Task ${index + 1}\n`
                yaml += `      ${trimmedLine}\n`
              }
              isFirstLine = false
            } else {
              // 後續行：保持適當縮排
              yaml += `      ${trimmedLine}\n`
            }
          })
        })
      }
      
      yamlContent.value = yaml
    } else {
      yamlError.value = '無法載入 Playbook 資料'
    }
  } catch (error: any) {
    console.error('載入 YAML 失敗:', error)
    yamlError.value = error.response?.data?.message || error.message || '載入失敗'
  } finally {
    loadingYaml.value = false
  }
}

const closeYamlPreview = () => {
  showYamlPreview.value = false
  yamlContent.value = ''
  yamlError.value = ''
  selectedPlaybookName.value = ''
  selectedPlaybookId.value = null
}

const copyYamlToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(yamlContent.value)
    alert('YAML 已複製到剪貼簿')
  } catch (error) {
    console.error('複製失敗:', error)
    alert('複製失敗，請手動複製')
  }
}

const downloadYaml = () => {
  try {
    const blob = new Blob([yamlContent.value], { type: 'text/yaml;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${selectedPlaybookName.value.replace(/\s+/g, '_')}.yml`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下載失敗:', error)
    alert('下載失敗，請稍後再試')
  }
}

// 顯示執行資訊
const showExecutionInfo = async () => {
  try {
    loadingExecutionInfo.value = true
    showExecutionInfoDialog.value = true
    const response = await getExecutionInfo()
    if (response.success) {
      executionInfo.value = response.data
    }
  } catch (error: any) {
    console.error('載入執行資訊失敗:', error)
    alert('載入執行資訊失敗: ' + (error.message || '未知錯誤'))
  } finally {
    loadingExecutionInfo.value = false
  }
}

const closeExecutionInfo = () => {
  showExecutionInfoDialog.value = false
  executionInfo.value = null
}

// 停止執行
const stopExecution = async () => {
  if (!currentJobId.value) {
    showExecutionProgress.value = false
    return
  }
  
  if (!confirm('確定要強制停止執行嗎？')) {
    return
  }
  
  try {
    executionStatus.value = '正在停止執行...'
    executionAborted.value = true
    
    // 調用後端 API 停止執行
    const response = await abortJob(currentJobId.value)
    
    if (response.success) {
      executionStatus.value = '執行已停止'
      executingPlaybooks.value.forEach(p => {
        if (p.status === 'pending') {
          p.status = 'aborted'
          p.message = '使用者停止執行'
        }
      })
      
      setTimeout(() => {
        showExecutionProgress.value = false
        loadPlaybooks()
      }, 2000)
    } else {
      executionStatus.value = '停止失敗: ' + response.message
      setTimeout(() => {
        executionAborted.value = false
      }, 2000)
    }
  } catch (error: any) {
    console.error('停止執行失敗:', error)
    executionStatus.value = '停止執行失敗'
    const errorMsg = error.response?.data?.message || error.message
    alert(`停止執行失敗: ${errorMsg}`)
    executionAborted.value = false
  }
}

// 關閉進度框
const closeExecutionProgress = () => {
  showExecutionProgress.value = false
  currentJobId.value = null
  executionProgress.value = 0
  executingPlaybooks.value = []
  loadPlaybooks()
}

// 監聽搜尋變化
const handleSearch = () => {
  currentPage.value = 1
  loadPlaybooks()
}
</script>
