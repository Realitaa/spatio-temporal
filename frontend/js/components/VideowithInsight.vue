<script setup>
const props = defineProps({
  is_processing: Boolean,
  video_url: String,
  data: Object
})

const items = [
  {
    icon: 'i-lucide-info',
    title: 'Ringkasan',
    data: [
      { label: 'Durasi', value: props.data.duration },
      { label: 'Frame', value: props.data.frame_count },
      { label: 'Rata-rata', value: props.data.average_intensity }
    ]
  },
  {
    icon: 'i-lucide-activity',
    title: 'Aktivitas',
    data: [
      { label: 'Maksimum', value: props.data.max_intensity },
      { label: 'Minimum', value: props.data.min_intensity },
      { label: 'Paling aktif', value: props.data.peak_time }
    ]
  },
  {
    icon: 'i-lucide-calculator',
    title: 'Integral',
    data: [
      { label: 'Total', value: props.data.total_intensity },
      { label: 'Metode', value: 'Riemann Sum' },
    ]
  }
]
</script>

<template>
  <div class="flex gap-4 w-full">
    <iframe width="40%" height="250" src="https://www.youtube.com/embed/DjdUEyjx8GM?si=xDZRnk_ebAUrUhmO"
      title="YouTube video player" frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

    <UCard class="w-[60%]">
      <template #header>
        <h1 class="text-xl font-bold">{{ is_processing ? 'Sedang Melakukan Analisis....' : 'Ringkasan Analisis' }}</h1>
      </template>

      <div v-if="!is_processing" class="flex shrink-0">
        <div v-for="item in items" class="min-w-60">
          <div class="flex gap-2 items-center mb-2">
            <UIcon :name="item.icon" class="size-5" />
            <h2 class="text-xl font-bold text-gray-800">{{ item.title }}</h2>
          </div>
          <ul class="space-y-3 text-gray-600">
            <li v-for="data in item.data" class="flex gap-2">
              <span class="font-semibold text-gray-900">&bull;&nbsp; {{ data.label }}:</span>
              <span>{{ data.value }}</span>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="is_processing" class="space-y-2 w-full">
        <!-- Start with w-[100%] and shrink by 10 every loop -->
        <USkeleton v-for="i in 5" class="h-5" :style="{ width: `${110 - i * 10}%` }" />
      </div>
    </UCard>
  </div>
</template>