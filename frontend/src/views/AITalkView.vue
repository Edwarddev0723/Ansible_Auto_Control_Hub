<template>
  <div class="flex h-screen flex-col bg-[#FAFBFD]">
    <!-- Header -->
    <header class="h-[100px] border-b border-[#E6EFF5] bg-white px-4 lg:px-10 flex items-center">
      <h1 class="text-xl lg:text-[28px] font-semibold text-primary ml-12 lg:ml-0">AI Talk</h1>
    </header>

    <!-- Chat Container -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Chat Content -->
      <div class="flex flex-1 flex-col">
          <!-- Chat Header with Contact Name -->
          <div class="bg-white px-6 py-4 shadow-sm">
            <button @click="goBack" class="flex items-center gap-3 text-[#333B69] hover:text-[#4379EE] transition-colors">
              <svg class="w-5 h-5" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.5 15L7.5 10L12.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span class="text-lg font-semibold" style="font-family: 'Nunito Sans', sans-serif">Minerva Barnett</span>
            </button>
          </div>

          <!-- Messages Area -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto bg-[#F5F7FA] px-4 lg:px-8 py-6">
            <div class="mx-auto max-w-4xl space-y-4">
              <!-- Message Items -->
              <div
                v-for="message in messages"
                :key="message.id"
                :class="[
                  'flex',
                  message.isUser ? 'justify-end' : 'justify-start',
                ]"
              >
                <div
                  :class="[
                    'group relative max-w-[85%] lg:max-w-[800px] rounded-2xl px-5 py-4 shadow-sm',
                    message.isUser
                      ? 'bg-[#5B93FF] text-white'
                      : 'bg-white text-[#333B69]',
                  ]"
                >
                  <!-- Avatar for received messages -->
                  <div
                    v-if="!message.isUser"
                    class="absolute -left-12 top-0 hidden lg:flex h-10 w-10 items-center justify-center rounded-full bg-gray-300"
                  >
                    <svg class="h-6 w-6 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    </svg>
                  </div>

                  <!-- Message Content -->
                  <div
                    class="text-sm leading-relaxed break-words whitespace-pre-wrap overflow-hidden markdown-content"
                    style="font-family: 'Nunito Sans', sans-serif"
                    v-html="formatMessage(message.text)"
                  >
                  </div>

                  <!-- Tool Calls Display -->
                  <div v-if="message.toolCalls && message.toolCalls.length > 0" class="mt-3 space-y-2">
                    <div v-for="(tool, index) in message.toolCalls" :key="index" class="bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                      <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 flex items-center gap-2 text-xs font-semibold text-gray-700">
                        <svg class="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        Executed: {{ tool.tool }}
                      </div>
                      <details class="group">
                        <summary class="px-3 py-1 text-xs text-gray-500 cursor-pointer hover:bg-gray-50 select-none flex items-center gap-1">
                          <span>View Output</span>
                          <svg class="w-3 h-3 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                        </summary>
                        <div class="p-3 bg-gray-900 text-gray-100 text-xs font-mono overflow-x-auto">
                          <pre>{{ JSON.stringify(tool.result.data || tool.result, null, 2) }}</pre>
                        </div>
                      </details>
                    </div>
                  </div>

                  <!-- Time and Options -->
                  <div class="mt-2 flex items-center justify-end gap-2">
                    <span
                      :class="[
                        'text-xs',
                        message.isUser ? 'text-white text-opacity-80' : 'text-gray-500',
                      ]"
                      style="font-family: 'Nunito Sans', sans-serif"
                    >
                      {{ message.time }}
                    </span>
                    <button
                      class="opacity-0 group-hover:opacity-100 transition-opacity"
                      @click="showMessageOptions(message)"
                    >
                      <svg
                        :class="[
                          'h-4 w-4',
                          message.isUser ? 'text-white' : 'text-gray-500',
                        ]"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Loading Indicator -->
              <div v-if="loading" class="flex justify-start">
                <div class="bg-white rounded-2xl px-5 py-4 shadow-sm">
                  <div class="flex gap-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Reply Buttons (if suggestions exist) -->
          <div v-if="quickReplies.length > 0" class="bg-[#F5F7FA] px-4 lg:px-8 pb-4">
            <div class="mx-auto max-w-4xl flex justify-center gap-4">
              <button
                v-for="reply in quickReplies"
                :key="reply"
                @click="sendQuickReply(reply)"
                class="rounded-full border-2 border-[#5B93FF] bg-white px-8 py-2 text-sm font-semibold text-[#5B93FF] transition-all hover:bg-[#5B93FF] hover:text-white"
                style="font-family: 'Nunito Sans', sans-serif"
              >
                {{ reply }}
              </button>
            </div>
          </div>

          <!-- Input Area -->
          <div class="border-t border-[#E6EFF5] bg-white px-4 lg:px-8 py-4">
            <div class="mx-auto max-w-4xl">
              <div class="flex items-center gap-3">
                <!-- Voice Input Button -->
                <button
                  class="flex h-10 w-10 items-center justify-center rounded-full text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600"
                  @click="startVoiceInput"
                >
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                </button>

                <!-- Message Input -->
                <div class="flex-1 relative">
                  <input
                    v-model="newMessage"
                    type="text"
                    placeholder="Write message"
                    class="w-full rounded-full border border-gray-200 bg-[#F5F7FA] px-6 py-3 pr-24 text-sm text-[#333B69] placeholder-gray-400 focus:border-[#5B93FF] focus:outline-none focus:ring-2 focus:ring-[#5B93FF] focus:ring-opacity-20"
                    style="font-family: 'Nunito Sans', sans-serif"
                    @keyup.enter="sendMessage"
                  />
                  
                  <!-- Attachment Icons -->
                  <div class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
                    <!-- Link Attachment -->
                    <button
                      class="text-gray-400 transition-colors hover:text-gray-600"
                      @click="attachLink"
                    >
                      <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                      </svg>
                    </button>

                    <!-- Image Attachment -->
                    <button
                      class="text-gray-400 transition-colors hover:text-gray-600"
                      @click="attachImage"
                    >
                      <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Send Button -->
                <button
                  @click="sendMessage"
                  :disabled="!newMessage.trim()"
                  class="flex h-12 items-center gap-2 rounded-lg bg-[#5B93FF] px-6 text-sm font-semibold text-white transition-all hover:bg-[#4379EE] disabled:cursor-not-allowed disabled:opacity-50"
                  style="font-family: 'Nunito Sans', sans-serif"
                >
                  Send
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import { sendChatMessage, checkAIHealth, type ChatMessage as APIChatMessage } from '@/api/ai'

const router = useRouter()
const messagesContainer = ref<HTMLElement | null>(null)
const newMessage = ref('')
const quickReplies = ref(['Yes', 'No'])
const loading = ref(false)
const aiStatus = ref<'connected' | 'disconnected' | 'error'>('disconnected')

interface Message {
  id: number
  text: string
  time: string
  isUser: boolean
  toolCalls?: any[]
}

const messages = ref<Message[]>([
  {
    id: 1,
    text: 'Hello! I am your AI assistant for Ansible automation. How can I help you today?',
    time: getCurrentTime(),
    isUser: false,
  },
])

// 獲取當前時間格式化
function getCurrentTime(): string {
  const now = new Date()
  return now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

// Format message text (handle markdown)
const formatMessage = (text: string) => {
  try {
    return marked.parse(text)
  } catch (e) {
    return text.replace(/\n/g, '<br>')
  }
}

// 檢查 AI 服務狀態
const checkStatus = async () => {
  try {
    const response = await checkAIHealth()
    aiStatus.value = response.data.status
  } catch (error) {
    console.error('檢查 AI 狀態失敗:', error)
    aiStatus.value = 'error'
  }
}

onMounted(() => {
  scrollToBottom()
  checkStatus()
})

// Scroll to bottom when messages change
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 將聊天歷史轉換為 API 格式
const getChatHistory = (): APIChatMessage[] => {
  return messages.value.map(msg => ({
    role: msg.isUser ? ('user' as const) : ('assistant' as const),
    content: msg.text,
  }))
}

// Send message
const sendMessage = async () => {
  if (!newMessage.value.trim() || loading.value) return

  const userMessageText = newMessage.value
  const time = getCurrentTime()

  // 添加用戶訊息到介面
  messages.value.push({
    id: messages.value.length + 1,
    text: userMessageText,
    time,
    isUser: true,
  })

  newMessage.value = ''
  scrollToBottom()
  loading.value = true

  try {
    // 準備聊天歷史
    const chatHistory = getChatHistory()

    // 發送到 AI API
    const response = await sendChatMessage({
      messages: chatHistory,
      model: 'gpt-4',
      temperature: 0.7,
    })

    if (response.success) {
      // 添加 AI 回覆到介面
      messages.value.push({
        id: messages.value.length + 1,
        text: response.data.content,
        time: getCurrentTime(),
        isUser: false,
        toolCalls: response.data.tool_calls
      })
      
      // 簡單的規則：如果回覆以問號結尾，顯示 Yes/No 選項
      if (response.data.content.trim().endsWith('?')) {
        quickReplies.value = ['Yes', 'No']
      } else {
        quickReplies.value = []
      }
      
      scrollToBottom()
    }
  } catch (error: any) {
    console.error('發送訊息失敗:', error)
    
    // 顯示錯誤訊息
    let errorMessage = '抱歉，AI 服務目前無法使用。'
    if (error.code === 'ECONNABORTED') {
      errorMessage = '⏱️ 請求超時，請稍後再試。'
    } else if (error.response) {
      errorMessage = `❌ 服務錯誤: ${error.response.status}`
    } else if (error.request) {
      errorMessage = '❌ 無法連接到後端服務，請確認服務是否啟動。'
    }
    
    messages.value.push({
      id: messages.value.length + 1,
      text: errorMessage,
      time: getCurrentTime(),
      isUser: false,
    })
    scrollToBottom()
  } finally {
    loading.value = false
  }
}

// Send quick reply
const sendQuickReply = (reply: string) => {
  newMessage.value = reply
  sendMessage()
  // Remove quick replies after selection
  quickReplies.value = []
}

// Show message options
const showMessageOptions = (message: Message) => {
  console.log('Message options for:', message)
  // You can implement a dropdown menu here
}

// Voice input
const startVoiceInput = () => {
  console.log('Starting voice input...')
  // Implement voice input functionality
}

// Attach link
const attachLink = () => {
  console.log('Attach link')
  // Implement link attachment
}

// Attach image
const attachImage = () => {
  console.log('Attach image')
  // Implement image attachment
}

// Go back
const goBack = () => {
  router.push('/')
}
</script>

<style>
.markdown-content p {
  margin-bottom: 0.5em;
}
.markdown-content p:last-child {
  margin-bottom: 0;
}
.markdown-content ul {
  list-style-type: disc;
  padding-left: 1.5em;
  margin-bottom: 0.5em;
}
.markdown-content ol {
  list-style-type: decimal;
  padding-left: 1.5em;
  margin-bottom: 0.5em;
}
.markdown-content pre {
  background-color: #1a202c;
  color: #e2e8f0;
  padding: 0.75em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin-bottom: 0.5em;
  font-family: monospace;
}
.markdown-content code {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 0.1em 0.3em;
  border-radius: 0.2em;
  font-family: monospace;
  font-size: 0.9em;
}
.markdown-content pre code {
  background-color: transparent;
  padding: 0;
  color: inherit;
}
/* Dark mode adjustments for user messages */
.bg-\[\#5B93FF\] .markdown-content code {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}
.bg-\[\#5B93FF\] .markdown-content pre {
  background-color: rgba(0, 0, 0, 0.3);
}
</style>
