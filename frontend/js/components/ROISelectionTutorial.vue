<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

defineEmits(['close'])

const example_width = ref('1%')
const example_height = ref('1%')

// every 30ms, increase the width and height by 1% till 70%
let interval: any
let timeout: any
const runAnimation = () => {
  interval = setInterval(() => {
    let currentWidth = parseInt(example_width.value)
    if (currentWidth < 70) {
      currentWidth += 1
      example_width.value = currentWidth + '%'
      example_height.value = currentWidth + '%'
    } else {
      clearInterval(interval)
      timeout = setTimeout(() => {
        example_width.value = '1%'
        example_height.value = '1%'
        runAnimation()
      }, 2000)
    }
  }, 30)
}

onMounted(() => {
  runAnimation()
})

onUnmounted(() => {
  clearInterval(interval)
  clearTimeout(timeout)
})
</script>

<template>
  <div class="absolute inset-0 z-20 flex flex-col items-center justify-between p-12 overflow-hidden">
    <div class="z-30 text-center space-y-2 rounded-3xl border border-primary bg-black/80 p-4">
      <h1 class="text-3xl font-semibold text-white">Klik dan Seret untuk Memilih Area Region of Interest</h1>
      <p class="text-white">Region of Interest (ROI) adalah area yang akan diproses agar dapat dianalisis untuk memperoleh data aktivitas manusia</p>
    </div>

    <div class="absolute inset-0 z-10 pointer-events-none overflow-hidden">
      <div
        class="border-4 border-green-400 top-[19%] left-[16%] absolute ring-3000 ring-black/50 shadow-2xl"
        :style="{ width: example_width, height: example_height }"
      >
        <UIcon name="whh:cursor" class="size-10 text-white absolute -bottom-11 -right-9" />
      </div>
    </div>

    <UButton
      label="Mengerti"
      size="xl"
      class="bg-white z-30 text-black hover:bg-gray-200 transition-colors"
      @click="$emit('close')"
    />
  </div>
</template>
