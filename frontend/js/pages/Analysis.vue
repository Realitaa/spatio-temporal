<script setup>
import VideowithInsight from '../components/VideowithInsight.vue'
import Graph from '../components/Graph.vue'
import Explanation from '../components/Explanation.vue'

defineProps({
  video_id: String
})
</script>

<template>
  <VideowithInsight />
  <Graph />
  <Explanation />
</template>
