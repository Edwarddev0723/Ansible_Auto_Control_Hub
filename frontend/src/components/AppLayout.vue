<template>
  <div class="flex min-h-screen bg-white">
    <button
      @click="toggleSidebar"
      class="fixed top-4 left-4 z-50 lg:hidden bg-primary text-white p-2 rounded-lg"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>

    <aside
      :class="[
        'w-[250px] border-r border-[#E6EFF5] flex-shrink-0 bg-white',
        'lg:relative fixed inset-y-0 left-0 z-40 transition-transform duration-300',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <div class="px-[27px] py-[30px]">
        <div class="flex items-center gap-3">
          <div class="w-[38px] h-[37px] rounded-full bg-gradient-to-br from-teal-400 to-teal-500 flex items-center justify-center text-white font-bold text-xl flex-shrink-0">
            A
          </div>
          <h1 class="text-[22px] font-fredoka text-primary leading-none">AnsibleDash</h1>
        </div>
      </div>

      <nav class="mt-[51px]">

        <router-link
          to="/inventories-groups"
          class="nav-item"
          :class="{ active: $route.path === '/inventories-groups' }"
        >
          <svg
            class="w-[22px] h-[22px]"
            :class="$route.path === '/inventories-groups' ? 'fill-[#1814F3]' : 'fill-[#B1B1B1]'"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path fill-rule="evenodd" d="M3 6a3 3 0 013-3h2.25a3 3 0 013 3v2.25a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm9.75 0a3 3 0 013-3H18a3 3 0 013 3v2.25a3 3 0 01-3 3h-2.25a3 3 0 01-3-3V6zM3 15.75a3 3 0 013-3h2.25a3 3 0 013 3V18a3 3 0 01-3 3H6a3 3 0 01-3-3v-2.25zm9.75 0a3 3 0 013-3H18a3 3 0 013 3V18a3 3 0 01-3 3h-2.25a3 3 0 01-3-3v-2.25z" clip-rule="evenodd" />
          </svg>
          <span>Inventory 群組管理</span>
        </router-link>

        <router-link
          to="/"
          class="nav-item"
          :class="{ active: $route.path === '/' || $route.path.startsWith('/inventory') }"
        >
          <svg
            class="w-[22px] h-[22px]"
            :class="($route.path === '/' || $route.path.startsWith('/inventory')) ? 'fill-[#1814F3]' : 'fill-[#B1B1B1]'"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M11.47 3.84a.75.75 0 011.06 0l8.69 8.69a.75.75 0 101.06-1.06l-8.689-8.69a2.25 2.25 0 00-3.182 0l-8.69 8.69a.75.75 0 001.061 1.06l8.69-8.69z" />
            <path d="M12 5.432l8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 01-.75-.75v-4.5a.75.75 0 00-.75-.75h-3a.75.75 0 00-.75.75V21a.75.75 0 01-.75.75H5.625a1.875 1.875 0 01-1.875-1.875v-6.198a2.29 2.29 0 00.091-.086L12 5.43z" />
          </svg>
          <span>Inventories 清單</span>
        </router-link>

        <router-link
          to="/playbook"
          class="nav-item"
          :class="{ active: $route.path.startsWith('/playbook') }"
        >
          <svg
            class="w-[22px] h-[22px]"
            :class="$route.path.startsWith('/playbook') ? 'fill-[#1814F3]' : 'fill-[#B1B1B1]'"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path fill-rule="evenodd" d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625zM7.5 15a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5A.75.75 0 017.5 15zm.75 2.25a.75.75 0 000 1.5H12a.75.75 0 000-1.5H8.25z" clip-rule="evenodd" />
            <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z" />
          </svg>
          <span>PlayBook 管理與執行</span>
        </router-link>

        <router-link
          to="/ai-deploy"
          class="nav-item"
          :class="{ active: $route.path.startsWith('/ai-deploy') }"
        >
          <svg
            class="w-[22px] h-[22px]"
            :class="$route.path.startsWith('/ai-deploy') ? 'fill-[#1814F3]' : 'fill-[#B1B1B1]'"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path fill-rule="evenodd" d="M4.848 2.771A49.144 49.144 0 0112 2.25c2.43 0 4.817.178 7.152.52 1.978.292 3.348 2.024 3.348 3.97v6.02c0 1.946-1.37 3.678-3.348 3.97a48.901 48.901 0 01-3.476.383.39.39 0 00-.297.17l-2.755 4.133a.75.75 0 01-1.248 0l-2.755-4.133a.39.39 0 00-.297-.17 48.9 48.9 0 01-3.476-.384c-1.978-.29-3.348-2.024-3.348-3.97V6.741c0-1.946 1.37-3.68 3.348-3.97zM6.75 8.25a.75.75 0 01.75-.75h9a.75.75 0 010 1.5h-9a.75.75 0 01-.75-.75zm.75 2.25a.75.75 0 000 1.5H12a.75.75 0 000-1.5H7.5z" clip-rule="evenodd" />
          </svg>
          <span>AI 對話部署</span>
        </router-link>
      </nav>
    </aside>

    <div
      v-if="sidebarOpen"
      @click="toggleSidebar"
      class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
    ></div>

    <main class="flex-1 flex flex-col w-full">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<style scoped>
.nav-item {
  @apply flex items-center gap-[25px] px-[44px] py-[17px] text-[18px] font-medium text-[#B1B1B1] relative transition-colors;
  font-family: 'Inter', sans-serif;
}

.nav-item.active {
  @apply text-[#1814F3];
}

.nav-item.active::before {
  content: '';
  @apply absolute left-0 top-0 w-[6px] h-full bg-[#2D60FF] rounded-r-[10px];
}

.nav-item:hover {
  @apply text-[#1814F3];
}
</style>