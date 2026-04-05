<script setup>
import { ref } from 'vue'

const features = ref([
  {
    title: 'Format yang Didukung',
    description: 'Gunakan video berformat .mp4, .avi, .mov, atau .wmv dengan durasi minimal 30 detik untuk memperoleh hasil analisis yang lebih akurat.',
    icon: 'i-lucide-video',
  },
  {
    title: 'Resolusi Video',
    description: 'Gunakan video dengan resolusi minimal 720p dan pencahayaan yang memadai untuk meningkatkan akurasi deteksi aktivitas.',
    icon: 'i-lucide-a-large-small',
  },
  {
    title: 'Aktivitas Manusia',
    description: 'Sistem ini menganalisis aktivitas manusia seperti berjalan, berlari, duduk, dan berdiri untuk menghasilkan representasi data terhadap waktu.',
    icon: 'i-lucide-user',
  }
])

const uploadingVideo = ref(false)
</script>

<template>
  <UPageSection title="Analisis Spatio-Temporal Aktivitas Manusia"
    description="Unggah video untuk mengonversi aktivitas manusia menjadi data spatio-temporal yang dapat dianalisis menggunakan integral."
    :features="features" :ui="{ container: 'flex flex-col lg:grid py-8 sm:py-12 lg:py-16 gap-8 sm:gap-16' }" />
  <div class="flex justify-center cursor-pointer">
    <UFileUpload icon="i-lucide-video" label="Seret atau unggah video di sini"
      description="Format: .mp4, .avi, .mov, .wmv • Durasi minimal 30 detik" color="neutral" class="w-full min-h-48" />
  </div>
  <p class="text-sm text-center">Data aktivitas akan dikonversi menjadi fungsi terhadap waktu dan dianalisis menggunakan
    pendekatan integral numerik.</p>

  <!-- Overlay while video uploading, showing progress bar and fun fact -->
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" v-if="uploadingVideo">
    <div class="bg-white p-8 rounded-lg space-y-6 max-w-150">
      <p class="text-lg font-semibold">Mengupload video...</p>
      <UProgress :value="progress" />
      <div class="flex flex-col items-center justify-center">
        <div class="flex gap-1 items-center">
          <UIcon name="game-icons:light-bulb" class="size-5 text-yellow-400" />
          <p class="font-semibold text-center text-lg">Fakta menarik</p>
        </div>
        <p class="text-sm text-center">Tahukah Anda bahwa video pertama yang diunggah ke YouTube
          berjudul "Me at the zoo" memiliki durasi hanya 18 detik?</p>
      </div>
    </div>
  </div>
</template>
