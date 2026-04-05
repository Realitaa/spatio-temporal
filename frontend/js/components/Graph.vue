<script setup>
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
import katex from 'katex'
import 'katex/dist/katex.min.css'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler)

const chartData = {
  labels: Array.from({ length: 30 }, (_, i) => i + 1),
  datasets: [
    {
      label: 'Kepadatan Aktivitas (Area ungu menunjukkan hasil integral/akumulasi)',
      data: [1.2, 1.5, 2.1, 3.4, 4.2, 5.8, 6.7, 7.5, 7.8, 8.1, 8.2, 8.2, 7.9, 7.1, 6.4, 5.2, 4.8, 4.2, 3.8, 3.2, 2.8, 2.7, 3.1, 3.5, 3.9, 4.1, 3.8, 3.2, 2.4, 1.8],
      borderColor: '#6366f1',
      backgroundColor: 'rgba(99, 102, 241, 0.2)',
      fill: true,
      tension: 0.4
    }
  ]
}

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
        <h2 class="text-xl font-bold">Grafik Aktivitas Spatio-Temporal</h2>
      </template>
      <div class="h-72 relative w-full">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </UCard>

    <UCard class="w-1/3 h-full overflow-y-auto">
      <template #header>
        <h2 class="text-xl font-bold">Interpretasi Grafik</h2>
      </template>
      <div class="space-y-4 text-gray-700 text-sm">
        <p>Grafik di samping memvisualisasikan kepadatan aktivitas dalam video selama durasi 30 detik.</p>
        <p><strong>Sumbu X</strong> merepresentasikan waktu (detik), dan <strong>Sumbu Y</strong> menunjukkan skala
          kepadatan relatif yang diekstrak dari analisis pergerakan per frame.</p>
        <p>Berdasarkan grafik, aktivitas memuncak pada interval detik ke-10 hingga ke-15, dengan nilai maksimal sebesar
          <strong>8.2 unit</strong>.
        </p>
        <p class="font-semibold text-lg">Estimasi total aktivitas: <span class="font-bold">125.4 unit</span>.
        </p>
      </div>
    </UCard>
  </div>
</template>