<script setup>
import { ref } from 'vue'

const links = ref([
    {
        label: 'Mulai',
        to: '/canvas',
        icon: 'i-lucide-square-play'
    },
    {
        label: 'Pelajari lebih lanjut',
        to: '/docs/',
        color: 'neutral',
        variant: 'subtle',
        trailingIcon: 'i-lucide-arrow-right'
    }
])
</script>

<template>
    <div class="min-h-screen w-full bg-elevated/25 relative flex items-center">
        <!-- Soft Morning Mist Background -->
        <div class="absolute inset-0 z-0 pointer-events-none" style="
                background-image: 
                    radial-gradient(circle 600px at 0% 200px, #fce7f3, transparent),
                    radial-gradient(circle 600px at 100% 200px, #fce7f3, transparent)
        "></div>

        <div class="relative z-10 w-full">
            <UPageHero title="Spatio-Temporal Data Analysis"
                description="Sistem analisis aktivitas manusia berbasis video menggunakan integral ganda dan pendekatan numerik untuk menghitung kepadatan aktivitas secara spatio-temporal."
                headline="Kalkulus Integral" orientation="horizontal" :links="links">
                <img src="https://learndjango.com/static/images/django50_welcome.png" alt="App screenshot"
                    class="rounded-lg shadow-2xl ring ring-default" />
            </UPageHero>
        </div>
    </div>
</template>