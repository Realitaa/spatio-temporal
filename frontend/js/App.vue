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
    <UApp>
        <div id="vue-root">
            <component :is="inertiaApp" v-bind="inertiaProps" />
        </div>
    </UApp>
</template>
