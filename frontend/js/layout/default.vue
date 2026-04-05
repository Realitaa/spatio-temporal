<script setup>
import { Link } from "@inertiajs/vue3";
</script>

<template>
  <div>
    <nav class="flex items-start justify-center">
      <ul class="flex space-x-4">
        <li>
          <Link href="/" class="underline text-sky-600">Home</Link>
        </li>
        <li>
          <Link href="/about" class="underline text-sky-600">About</Link>
        </li>
      </ul>
    </nav>
    <div class="flex items-center justify-center mt-32">
      <slot />
    </div>
  </div>
</template>
