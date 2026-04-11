import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useCanvasStore = defineStore("canvas", () => {
  const canvases = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function fetchCanvases() {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get("/api/canvas/");
      canvases.value = response.data.canvases;
    } catch (err) {
      error.value = err.message || "Failed to fetch canvases";
    } finally {
      loading.value = false;
    }
  }

  async function renameCanvas(id, name) {
    try {
      const response = await axios.patch(`/api/canvas/${id}/rename/`, { name });
      const updated = response.data;
      const index = canvases.value.findIndex((c) => c.id === updated.id);
      if (index !== -1) {
        canvases.value[index] = {
          ...canvases.value[index],
          name: updated.name,
        };
      }
      return updated;
    } catch (err) {
      throw err;
    }
  }

  async function deleteCanvas(id) {
    await axios.delete(`/api/canvas/${id}/delete/`);
    canvases.value = canvases.value.filter((c) => c.id !== Number(id));
  }

  return {
    canvases,
    loading,
    error,
    fetchCanvases,
    renameCanvas,
    deleteCanvas,
  };
});
