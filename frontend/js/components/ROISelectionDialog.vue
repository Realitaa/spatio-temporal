<script setup lang="ts">
import { ref } from 'vue'
import ROISelectionTutorial from './ROISelectionTutorial.vue'

const isOpen = defineModel<boolean>('isOpen')
const props = defineProps({
  thumbnailUrl: String
})

const isShowTutorial = ref(true)
</script>

<template>
  <UModal v-model:open="isOpen" fullscreen :dismissible="false" title="Pilih Area Region of Interest (ROI)">
    <template #body>
      <div class="relative w-full h-full rounded-lg">
        <img :src="thumbnailUrl" class="w-full h-full object-contain" alt="Thumbnail">
        
        <ROISelectionTutorial
          v-if="isShowTutorial"
          @close="isShowTutorial = false"
        />
      </div>
    </template>
  </UModal>
</template>