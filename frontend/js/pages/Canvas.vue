<script setup>
import { ref, reactive, watch } from "vue";
import axios from "axios";

/* =========================
   CONFIG
========================= */
const MAX_FILE_SIZE = 200 * 1024 * 1024; // 200MB

const ACCEPTED_VIDEO_TYPES = [
  "video/mp4",
  "video/avi",
  "video/quicktime",
  "video/x-ms-wmv",
];

const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return (
    Number.parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i]
  );
};

/* =========================
   STATE
========================= */
const state = reactive({
  video: undefined,
});

const uploadingVideo = ref(false);
const progress = ref(0);
const validationError = ref("");

/* =========================
   FEATURES
========================= */
const features = ref([
  {
    title: "Format yang Didukung",
    description:
      "Gunakan video berformat .mp4, .avi, .mov, atau .wmv dengan durasi minimal 30 detik untuk memperoleh hasil analisis yang lebih akurat.",
    icon: "i-lucide-video",
  },
  {
    title: "Resolusi Video",
    description:
      "Gunakan video dengan resolusi minimal 720p dan pencahayaan yang memadai untuk meningkatkan akurasi deteksi aktivitas.",
    icon: "i-lucide-a-large-small",
  },
  {
    title: "Aktivitas Manusia",
    description:
      "Sistem ini menganalisis aktivitas manusia seperti berjalan, berlari, duduk, dan berdiri untuk menghasilkan representasi data terhadap waktu.",
    icon: "i-lucide-user",
  },
]);

/* =========================
   VALIDATION
========================= */
function validate(file) {
  if (!(file instanceof File)) {
    return "Silakan pilih file video.";
  }
  if (file.size > MAX_FILE_SIZE) {
    return `Ukuran video terlalu besar (max ${formatBytes(MAX_FILE_SIZE)}).`;
  }
  if (!ACCEPTED_VIDEO_TYPES.includes(file.type)) {
    return "Format video tidak didukung. Gunakan .mp4, .avi, .mov, atau .wmv.";
  }
  return null;
}

/* =========================
   UPLOAD
========================= */
async function uploadFile(file) {
  validationError.value = "";

  const error = validate(file);
  if (error) {
    validationError.value = error;
    state.video = undefined;
    return;
  }

  uploadingVideo.value = true;
  progress.value = 0;

  const formData = new FormData();
  formData.append("video", file);

  try {
    const res = await axios.post("/api/canvas/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (event) => {
        if (event.total) {
          progress.value = Math.round((event.loaded * 100) / event.total);
        }
      },
    });

    const videoId = res.data.video_id;
    window.location.href = `/canvas/${videoId}/`;
  } catch (err) {
    console.error(err);
    alert("Upload gagal. Silakan coba lagi.");
    state.video = undefined;
  } finally {
    uploadingVideo.value = false;
  }
}

/* =========================
   WATCH — trigger upload immediately
========================= */
watch(
  () => state.video,
  (file) => {
    if (file) {
      uploadFile(file);
    }
  },
);
</script>

<template>
  <!-- HEADER -->
  <UPageSection
    title="Analisis Spatio-Temporal Aktivitas Manusia"
    description="Unggah video untuk mengonversi aktivitas manusia menjadi data spatio-temporal yang dapat dianalisis menggunakan integral."
    :features="features"
    :ui="{
      container: 'flex flex-col lg:grid py-8 sm:py-12 lg:py-16 gap-8 sm:gap-16',
    }"
  />

  <!-- FILE UPLOAD -->
  <div class="flex flex-col items-center gap-3">
    <UFileUpload
      v-model="state.video"
      icon="i-lucide-video"
      label="Seret atau pilih video di sini"
      description="Format: .mp4, .avi, .mov, .wmv • Disarankan ≥30 detik"
      class="w-full min-h-48"
      accept="video/*"
      :disabled="uploadingVideo"
    />

    <!-- Validation error -->
    <p v-if="validationError" class="text-sm text-red-500 text-center">
      {{ validationError }}
    </p>
  </div>

  <p class="text-sm text-center text-gray-500">
    Video akan diunggah otomatis setelah dipilih. Data aktivitas akan dikonversi
    menjadi fungsi terhadap waktu dan dianalisis menggunakan pendekatan integral
    numerik.
  </p>

  <!-- UPLOAD OVERLAY -->
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    v-if="uploadingVideo"
  >
    <div class="bg-white p-8 rounded-lg space-y-6 max-w-150 w-full">
      <p class="text-lg font-semibold">Mengupload video...</p>

      <UProgress v-model="progress" />

      <p class="text-center text-sm">{{ progress }}%</p>

      <div class="flex flex-col items-center justify-center">
        <div class="flex gap-1 items-center">
          <UIcon name="game-icons:light-bulb" class="size-5 text-yellow-400" />
          <p class="font-semibold text-center text-lg">Fakta menarik</p>
        </div>
        <p class="text-sm text-center">
          Tahukah Anda bahwa video pertama di YouTube berjudul "Me at the zoo"
          hanya berdurasi 18 detik?
        </p>
      </div>
    </div>
  </div>
</template>
