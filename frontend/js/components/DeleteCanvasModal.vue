<script setup>
import { ref } from "vue";
import { router } from "@inertiajs/vue3";
import { useCanvasStore } from "../stores/canvas";

const props = defineProps({
  canvasId: {
    type: [String, Number],
    default: null,
  },
});

const open = defineModel("open", { default: false });

const canvasStore = useCanvasStore();
const isDeleting = ref(false);

async function deleteCanvas() {
  if (!props.canvasId) return;
  isDeleting.value = true;
  try {
    await canvasStore.deleteCanvas(props.canvasId);
    open.value = false;
    router.visit("/canvas/");
  } catch (e) {
    console.error(e);
  } finally {
    isDeleting.value = false;
  }
}
</script>

<template>
  <UModal v-model:open="open">
      <template #header>
        <span class="text-base font-bold">Hapus Kanvas</span>
      </template>

      <template #body>
        <p class="text-sm text-muted">
          Apakah Anda yakin ingin menghapus kanvas ini? Tindakan ini tidak dapat
          dibatalkan.
        </p>
      </template>

      <template #footer>
        <div class="flex w-full justify-end gap-2">
          <UButton
            color="neutral"
            variant="ghost"
            :disabled="isDeleting"
            @click="open = false"
          >
            Batal
          </UButton>
          <UButton
            color="error"
            icon="i-lucide-trash-2"
            :loading="isDeleting"
            @click="deleteCanvas"
          >
            Hapus
          </UButton>
        </div>
      </template>
  </UModal>
</template>
