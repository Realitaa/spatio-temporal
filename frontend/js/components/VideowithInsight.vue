<script setup>
const items = [
  {
    icon: 'i-lucide-info',
    title: 'Ringkasan',
    data: [
      { label: 'Durasi', value: '30 detik' },
      { label: 'Frame', value: '900' },
      { label: 'Rata-rata', value: '4.18 unit/detik' }
    ]
  },
  {
    icon: 'i-lucide-activity',
    title: 'Aktivitas',
    data: [
      { label: 'Maksimum', value: '8.2 (detik ke-12)' },
      { label: 'Minimum', value: '0.5' },
      { label: 'Paling aktif', value: '10–15 detik' }
    ]
  },
  {
    icon: 'i-lucide-calculator',
    title: 'Integral',
    data: [
      { label: 'Total', value: '125.4 unit' },
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
        <h1 class="text-xl font-bold">Ringkasan Analisis</h1>
      </template>

      <div class="flex shrink-0">
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
    </UCard>
  </div>
</template>