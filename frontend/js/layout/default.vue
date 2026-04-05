<script setup>
import { ref, computed } from 'vue'

const open = ref(true)

const menu = [
  {
    label: 'Kanvas Baru',
    icon: 'i-lucide-pencil',
  },
  {
    label: 'Dataset',
    icon: 'i-lucide-database'
  },
  {
    label: 'Dokumentasi',
    icon: 'i-lucide-book'
  },
  {
    label: 'Tentang',
    icon: 'i-lucide-info',
  }
]

const menu50item = computed(() => {
  const menu = []
  for (let i = 0; i < 50; i++) {
    menu.push({
      label: 'Kanvas ' + i,
      to: '/canvas/' + i,
    })
  }
  return menu
})

const user = ref({
  name: 'Realitaa',
  avatar: {
    src: 'https://github.com/realitaa.png',
    alt: 'Realitaa'
  }
})

const userItems = computed(() => [
  [
    {
      label: 'GitHub',
      icon: 'i-simple-icons-github',
      to: 'https://github.com/realitaa/spatio-temporal',
      target: '_blank'
    },
    {
      label: 'Kembali',
      icon: 'i-lucide-log-out',
      to: '/'
    }
  ]
])
</script>

<template>
  <div class="absolute inset-0 z-0 pointer-events-none" style="
        background-image: 
            radial-gradient(circle 600px at 0% 200px, #fce7f3, transparent),
            radial-gradient(circle 600px at 100% 200px, #fce7f3, transparent)
    "></div>

  <div class="flex flex-1">
    <USidebar v-model:open="open" collapsible="icon" rail :ui="{
      container: 'h-full',
      inner: 'bg-elevated/25 divide-transparent',
      body: 'py-0'
    }">
      <template #header="{ state }">
        <div class="w-full flex items-center justify-center">
          <UIcon name="i-lucide-camera" class="size-6" v-if="state === 'collapsed'" />
          <span class="text-sm font-bold" v-else>Spatio-Temporal Data Analysis</span>
        </div>
      </template>

      <template #default="{ state }">
        <UNavigationMenu :key="state" :items="menu" orientation="vertical" :ui="{ link: 'p-1.5 overflow-hidden' }" />
        <div class="h-full overflow-y-auto">
          <UNavigationMenu :key="state" :items="menu50item" orientation="vertical" v-if="state === 'expanded'"
            :ui="{ link: 'p-1.5 overflow-hidden' }" />
        </div>
      </template>

      <template #footer>
        <UDropdownMenu :items="userItems" :content="{ align: 'center', collisionPadding: 12 }"
          :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width) min-w-48' }">
          <UButton v-bind="user" :label="user?.name" trailing-icon="i-lucide-chevrons-up-down" color="neutral"
            variant="ghost" square class="w-full data-[state=open]:bg-elevated overflow-hidden" :ui="{
              trailingIcon: 'text-dimmed ms-auto'
            }" />
        </UDropdownMenu>
      </template>
    </USidebar>

    <div class="flex-1 flex flex-col z-5">
      <div class="h-(--ui-header-height) shrink-0 flex items-center px-4 border-b border-default space-x-2">
        <UButton icon="i-lucide-panel-left" color="neutral" variant="ghost" aria-label="Toggle sidebar"
          @click="open = !open" />
        <span class="text-sm font-bold">Nama Kanvas</span>
      </div>

      <div class="flex-1 p-4 z-5">
        <slot />
      </div>
    </div>
  </div>
</template>
