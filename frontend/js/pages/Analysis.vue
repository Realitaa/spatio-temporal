<script setup>
import { onMounted, ref } from 'vue'
import ROISelectionDialog from '../components/ROISelectionDialog.vue'
import VideowithInsight from '../components/VideowithInsight.vue'
import Graph from '../components/Graph.vue'
import Explanation from '../components/Explanation.vue'

const props = defineProps({
  // is_processing: Boolean,
  video_id: String
})

const video_url = `/media/videos/${props.video_id}.mp4`
const data = {
  duration: '30 detik',
  frame_count: '900',
  average_intensity: '4.18 unit/detik',
  max_intensity: '8.2 (detik ke-12)',
  min_intensity: '0.5',
  peak_time: '10–15 detik',
  total_intensity: '125.4 unit'
}

const is_processing = ref(false)
const isROISelectionDialogOpen = ref(false)
const thumbnailUrl = '/image.png'

onMounted(() => {
  setTimeout(() => {
    isROISelectionDialogOpen.value = true
  }, 1000)
})
</script>

<template>
  <ROISelectionDialog v-model:isOpen="isROISelectionDialogOpen" :thumbnailUrl="thumbnailUrl" />
  <VideowithInsight :is_processing="is_processing" :video_url="video_url" :data="data" />
  <Graph :is_processing="is_processing" />
  <Explanation :is_processing="is_processing" />
</template>