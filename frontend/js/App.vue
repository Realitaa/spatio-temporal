<script setup>
defineProps({
    inertiaApp: {
        type: Object,
        required: true,
    },
    inertiaProps: {
        type: Object,
        required: true,
    },
});
</script>

<template>
    <div id="vue-root">
        <component :is="inertiaApp" v-bind="inertiaProps" />
    </div>
</template>
