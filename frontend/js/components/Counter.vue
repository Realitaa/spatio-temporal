<script setup>
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
    <div class="flex flex-col items-center justify-center space-y-2 mt-4">
        <p>Count: {{ count }}</p>
        <UButton @click="count++">Increment</UButton>
    </div>
</template>
