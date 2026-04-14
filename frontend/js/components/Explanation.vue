<script setup>
import { ref, onMounted } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

defineProps({
  is_processing: Boolean
})

const mathFormula = ref(null)

onMounted(() => {
  if (mathFormula.value) {
    katex.render("V = \\int_{t_0}^{t_1} \\int \\int_A I(x, y, t) \\, dx \\, dy \\, dt \\approx \\sum_{k=1}^{N} \\left( \\sum_{i} \\sum_{j} I(x_i, y_j, t_k) \\Delta x \\Delta y \\right) \\Delta t", mathFormula.value, {
      throwOnError: false,
      displayMode: true
    })
  }
})
</script>

<template>
  <UCard class="mt-8 w-full">
    <template #header>
      <h2 class="text-xl font-bold">Dasar Matematis: Pendekatan Integral Numerik</h2>
    </template>
    <div class="space-y-6 text-gray-700">
      <p>Metode perhitungan yang digunakan pada sistem ini bertumpu pada <strong>Kalkulus Integral</strong> untuk ruang
        spatio-temporal. Intensitas aktivitas dievaluasi menggunakan menggunakan integral tiga dimensi (triple integral)
        terhadap ruang (x, y) dan waktu (t)</p>
      <div class="py-4">
        <div ref="mathFormula"></div>
      </div>
      <p>Dalam implementasinya, perhitungan direalisasikan melalui metode numerik <strong>Riemann Sum</strong>:</p>
      <ul class="list-disc ml-6 space-y-2">
        <li>Domain gambar diamati sebagai grid diskrit berukuran piksel (merepresentasikan $x$ dan $y$).</li>
        <li>Waktu divariasikan menurut serangkaian frame interval (invers dari frame rate).</li>
        <li>Fungsi intensitas merupakan output dari deteksi optikal pada koordinat dan waktu tertentu.</li>
      </ul>
      <p>Akumulasi perhitungan di atas menghasilkan total unit perpindahan dinamis yang diinterpretasikan sebagai
        tingkat
        kepadatan aktivitas secara keseluruhan.</p>
    </div>
  </UCard>
</template>