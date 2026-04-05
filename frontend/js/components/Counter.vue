<script setup>
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
    <div class="flex flex-col items-center justify-center space-y-2 mt-4">
        <p>Count: {{ count }}</p>
        <button @click="count++" class="bg-sky-500 rounded-lg px-2 py-1 text-white hover:bg-sky-600">Increment</button>
    </div>
</template>
