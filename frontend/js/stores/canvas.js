import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useCanvasStore = defineStore('canvas', () => {
  const canvases = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchCanvases() {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/canvas/')
      canvases.value = response.data.canvases
    } catch (err) {
      error.value = err.message || 'Failed to fetch canvases'
    } finally {
      loading.value = false
    }
  }

  return { canvases, loading, error, fetchCanvases }
})
