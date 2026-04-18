<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import ROISelectionDialog from '../components/ROISelectionDialog.vue'
import VideowithInsight from '../components/VideowithInsight.vue'
import Graph from '../components/Graph.vue'
import Explanation from '../components/Explanation.vue'

const props = defineProps({
  video_id: String,
  video_url: String,
  canvas_id: Number,
  canvas_name: String,
  has_roi: Boolean,
  thumbnail_url: String,
  original_width: Number,
  original_height: Number,
  analysis_result: Object
})

const is_processing = ref(false)
const isROISelectionDialogOpen = ref(false)
const thumbnailUrl = props.thumbnail_url

const insightData = ref(null)
const graphData = ref(null)

function setupData(data) {
  const summary = data.summary
  insightData.value = {
    duration: `${summary.duration.toFixed(2)} detik`,
    fps: `${summary.fps.toFixed(0)} fps`,
    frame_count: '-',
    average_intensity: `${summary.average.toFixed(2)} unit/detik`,
    max_intensity: `${summary.max.toFixed(2)}`,
    min_intensity: `${summary.min.toFixed(2)}`,
    peak_time: `detik ke-${summary.peak_time.toFixed(2)}`,
    total_intensity: `${summary.total_activity.toFixed(2)} unit`
  }
  graphData.value = data.graph
}

async function analyzeVideo() {
  is_processing.value = true
  try {
    const res = await axios.post(`/api/canvas/${props.canvas_id}/analyze/`)
    if (res.data.status === 'success') {
      setupData(res.data.data)
    }
  } catch (err) {
    console.error('Failed to analyze:', err)
    alert('Gagal memproses video.')
  } finally {
    is_processing.value = false
  }
}

onMounted(() => {
  if (props.analysis_result) {
    setupData(props.analysis_result)
  } else if (!props.has_roi) {
    isROISelectionDialogOpen.value = true
  } else {
    analyzeVideo()
  }
})

function onROISaved() {
  isROISelectionDialogOpen.value = false
  analyzeVideo()
}
</script>

<template>
  <ROISelectionDialog
    v-model:isOpen="isROISelectionDialogOpen"
    :thumbnailUrl="thumbnailUrl"
    :canvasId="props.canvas_id"
    :originalWidth="props.original_width"
    :originalHeight="props.original_height"
    @roi-saved="onROISaved"
  />
  <VideowithInsight :is_processing="is_processing" :video_url="props.video_url" :data="insightData" />
  <Graph :is_processing="is_processing" :graph_data="graphData" />
  <Explanation :is_processing="is_processing" />
</template>