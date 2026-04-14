<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler
} from 'chart.js'

const props = defineProps({
  is_processing: Boolean,
  graph_data: Object
})

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler)

const chartData = computed(() => {
  if (!props.graph_data) {
    return {
      labels: [],
      datasets: []
    }
  }
  return {
    labels: props.graph_data.time.map(t => t.toFixed(1)),
    datasets: [
      {
        label: 'Kepadatan Aktivitas (Area ungu menunjukkan hasil integral/akumulasi)',
        data: props.graph_data.activity,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.2)',
        fill: true,
        tension: 0.4
      }
    ]
  }
})

const maxActivity = computed(() => {
  if (!props.graph_data || props.graph_data.activity.length === 0) return 0
  return Math.max(...props.graph_data.activity)
})

const peakTime = computed(() => {
  if (!props.graph_data || props.graph_data.activity.length === 0) return 0
  const maxIdx = props.graph_data.activity.indexOf(maxActivity.value)
  return props.graph_data.time[maxIdx]
})

const totalActivity = computed(() => {
  if (!props.graph_data || props.graph_data.activity.length === 0) return 0
  return props.graph_data.activity.reduce((a, b) => a + b, 0)
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Kepadatan Aktivitas (unit relatif)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Waktu (detik)'
      }
    }
  }
}
</script>

<template>
  <div class="mt-8 flex gap-4 w-full h-96">
    <UCard class="w-2/3 h-full flex flex-col" :ui="{ body: 'flex-1 min-h-0' }">
      <template #header>
        <h2 class="text-xl font-bold">
          {{ is_processing ? 'Membuat Grafik Aktivitas....' : 'Grafik Aktivitas Spatio-Temporal' }}
        </h2>
      </template>
      <div class="h-72 relative w-full flex justify-center items-center">
        <div v-if="is_processing" class="graphLoader"></div>
        <Line v-else-if="props.graph_data" :data="chartData" :options="chartOptions" />
        <div v-else class="text-gray-500 italic">Data grafik belum tersedia.</div>
      </div>
    </UCard>

    <UCard class="w-1/3 h-full overflow-y-auto">
      <template #header>
        <h2 class="text-xl font-bold">{{ is_processing ? 'Membuat Interpretasi....' : 'Interpretasi Grafik' }}</h2>
      </template>
      <div v-if="is_processing" class="flex flex-col gap-2">
        <USkeleton v-for="i in 10" class="h-5" :style="{ width: `${110 - i * 10}%` }" />
      </div>

      <div v-else-if="props.graph_data" class="space-y-4 text-gray-700 text-sm">
        <p>Grafik di samping memvisualisasikan kepadatan aktivitas dalam video selama durasi {{ props.graph_data.time.length > 0 ? props.graph_data.time[props.graph_data.time.length - 1].toFixed(2) : 0 }} detik.</p>
        <p><strong>Sumbu X</strong> merepresentasikan waktu (detik), dan <strong>Sumbu Y</strong> menunjukkan skala
          kepadatan relatif yang diekstrak dari analisis pergerakan per frame.</p>
        <p>Berdasarkan grafik, aktivitas memuncak pada interval detik ke-{{ peakTime.toFixed(2) }}, dengan nilai maksimal sebesar
          <strong>{{ maxActivity.toFixed(2) }} unit</strong>.
        </p>
        <p class="font-semibold text-lg">Estimasi total aktivitas: <span class="font-bold">{{ totalActivity.toFixed(2) }} unit</span>.
        </p>
      </div>
      
      <div v-else class="text-gray-500 italic text-sm">
        Data interpretasi belum tersedia.
      </div>
    </UCard>
  </div>
</template>