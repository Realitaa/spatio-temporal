<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import ROISelectionTutorial from './ROISelectionTutorial.vue'

const isOpen = defineModel<boolean>('isOpen')

const props = defineProps({
  thumbnailUrl: String,
  canvasId: [String, Number],
  originalWidth: Number,
  originalHeight: Number
})

const emit = defineEmits(['roi-saved'])

// Tutorial state
const isShowTutorial = ref(true)

// ROI drawing state
const isDrawing = ref(false)
const startX = ref(0)
const startY = ref(0)
const currentX = ref(0)
const currentY = ref(0)
const hasROI = ref(false)

// Finalized ROI in display coordinates
const roiDisplay = ref({ x1: 0, y1: 0, x2: 0, y2: 0 })

// Image element ref for measuring displayed size
const imgRef = ref<HTMLImageElement | null>(null)

// Saving state
const isSaving = ref(false)

// Live rectangle style while drawing
const liveRect = computed(() => {
  if (!isDrawing.value) return null

  const x = Math.min(startX.value, currentX.value)
  const y = Math.min(startY.value, currentY.value)
  const w = Math.abs(currentX.value - startX.value)
  const h = Math.abs(currentY.value - startY.value)

  return { left: `${x}px`, top: `${y}px`, width: `${w}px`, height: `${h}px` }
})

// Finalized rectangle style
const finalRect = computed(() => {
  if (!hasROI.value) return null

  const { x1, y1, x2, y2 } = roiDisplay.value
  return {
    left: `${x1}px`,
    top: `${y1}px`,
    width: `${x2 - x1}px`,
    height: `${y2 - y1}px`
  }
})

// Get mouse position relative to the image
function getRelativePos(e: MouseEvent) {
  if (!imgRef.value) return { x: 0, y: 0 }

  const rect = imgRef.value.getBoundingClientRect()
  const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width))
  const y = Math.max(0, Math.min(e.clientY - rect.top, rect.height))

  return { x, y }
}

function onMouseDown(e: MouseEvent) {
  if (isShowTutorial.value) return

  const pos = getRelativePos(e)
  startX.value = pos.x
  startY.value = pos.y
  currentX.value = pos.x
  currentY.value = pos.y
  isDrawing.value = true
  hasROI.value = false
}

function onMouseMove(e: MouseEvent) {
  if (!isDrawing.value) return

  const pos = getRelativePos(e)
  currentX.value = pos.x
  currentY.value = pos.y
}

function onMouseUp(e: MouseEvent) {
  if (!isDrawing.value) return

  const pos = getRelativePos(e)
  currentX.value = pos.x
  currentY.value = pos.y
  isDrawing.value = false

  // Only register as ROI if the rect has meaningful size
  const x1 = Math.min(startX.value, currentX.value)
  const y1 = Math.min(startY.value, currentY.value)
  const x2 = Math.max(startX.value, currentX.value)
  const y2 = Math.max(startY.value, currentY.value)

  if (x2 - x1 > 5 && y2 - y1 > 5) {
    roiDisplay.value = { x1, y1, x2, y2 }
    hasROI.value = true
  }
}

// Convert display coordinates → original video coordinates and POST
async function saveROI() {
  if (!hasROI.value || !imgRef.value) return

  const displayedWidth = imgRef.value.clientWidth
  const displayedHeight = imgRef.value.clientHeight

  const scaleX = (props.originalWidth || displayedWidth) / displayedWidth
  const scaleY = (props.originalHeight || displayedHeight) / displayedHeight

  const payload = {
    x1: Math.round(roiDisplay.value.x1 * scaleX),
    y1: Math.round(roiDisplay.value.y1 * scaleY),
    x2: Math.round(roiDisplay.value.x2 * scaleX),
    y2: Math.round(roiDisplay.value.y2 * scaleY)
  }

  isSaving.value = true

  try {
    await axios.post(`/api/canvas/${props.canvasId}/set-roi/`, payload)
    emit('roi-saved')
    isOpen.value = false
  } catch (err) {
    console.error('Failed to save ROI:', err)
    alert('Gagal menyimpan ROI. Silakan coba lagi.')
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <UModal v-model:open="isOpen" fullscreen :dismissible="false" title="Pilih Area Region of Interest (ROI)">
    <template #body>
      <div class="relative w-full h-full flex flex-col items-center justify-center">
        <!-- Image container (positioned relative for ROI overlay) -->
        <div
          class="relative inline-block select-none"
          @mousedown.prevent="onMouseDown"
          @mousemove.prevent="onMouseMove"
          @mouseup.prevent="onMouseUp"
          @mouseleave="isDrawing && onMouseUp($event)"
        >
          <img
            ref="imgRef"
            :src="thumbnailUrl"
            class="max-w-full max-h-[70vh] object-contain rounded-lg pointer-events-none"
            draggable="false"
            alt="Thumbnail"
          >

          <!-- Live drawing rectangle -->
          <div
            v-if="isDrawing && liveRect"
            class="absolute border-2 border-dashed border-green-400 bg-green-400/20 pointer-events-none"
            :style="liveRect"
          />

          <!-- Finalized ROI rectangle -->
          <div
            v-if="hasROI && !isDrawing && finalRect"
            class="absolute border-3 border-green-400 bg-green-400/15 pointer-events-none"
            :style="finalRect"
          >
            <span class="absolute -top-7 left-0 text-xs bg-green-500 text-white px-2 py-0.5 rounded">
              ROI
            </span>
          </div>

          <!-- Tutorial overlay -->
          <ROISelectionTutorial
            v-if="isShowTutorial"
            @close="isShowTutorial = false"
          />
        </div>

        <!-- Action buttons -->
        <div class="mt-6 flex items-center gap-4">
          <UButton
            v-if="hasROI"
            label="Ulangi"
            color="neutral"
            variant="outline"
            icon="i-lucide-rotate-ccw"
            @click="hasROI = false"
          />

          <UButton
            label="Analisis"
            icon="i-lucide-scan-search"
            :disabled="!hasROI || isSaving"
            :loading="isSaving"
            @click="saveROI"
          />
        </div>
      </div>
    </template>
  </UModal>
</template>