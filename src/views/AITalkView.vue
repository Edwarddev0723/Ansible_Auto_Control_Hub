<template>
  <AppLayout>
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
                    'group relative max-w-[80%] lg:max-w-[600px] rounded-2xl px-5 py-4 shadow-sm',
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
                  <p
                    class="text-sm leading-relaxed"
                    style="font-family: 'Nunito Sans', sans-serif"
                  >
                    {{ message.text }}
                  </p>

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
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const router = useRouter()
const messagesContainer = ref<HTMLElement | null>(null)
const newMessage = ref('')
const quickReplies = ref(['Yes', 'No'])

interface Message {
  id: number
  text: string
  time: string
  isUser: boolean
}

const messages = ref<Message[]>([
  {
    id: 1,
    text: 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters.',
    time: '6:30 pm',
    isUser: false,
  },
  {
    id: 2,
    text: 'There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour.',
    time: '6:34 pm',
    isUser: true,
  },
  {
    id: 3,
    text: 'The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default.Contrary to popular belief, Lorem Ipsum is not simply random text is the model text for your company.',
    time: '6:38 pm',
    isUser: false,
  },
])

// Scroll to bottom when messages change
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  scrollToBottom()
})

// Send message
const sendMessage = () => {
  if (!newMessage.value.trim()) return

  const now = new Date()
  const time = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })

  messages.value.push({
    id: messages.value.length + 1,
    text: newMessage.value,
    time,
    isUser: true,
  })

  newMessage.value = ''
  scrollToBottom()

  // Simulate AI response after a delay
  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      text: 'Thank you for your message. How can I assist you further?',
      time,
      isUser: false,
    })
    scrollToBottom()
  }, 1000)
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
