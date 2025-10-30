<template>
  <pre class="log-viewer">{{ log }}</pre>
</template>

<script setup>
defineProps({
  log: {
    type: String,
    default: 'No logs available.'
  }
})
</script>

<style scoped>
.log-viewer {
  background: #2b303b;
  color: #c0c5ce;
  padding: 1.5rem;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap; /* 保持換行 */
  word-wrap: break-word; /* 處理長字串 */
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>