<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { usePage } from "@inertiajs/vue3";
import { useCanvasStore } from "../stores/canvas";
import DeleteCanvasModal from "../components/DeleteCanvasModal.vue";

const openDeleteModal = ref(false);

const canvasStore = useCanvasStore();
onMounted(() => canvasStore.fetchCanvases());

const page = usePage();
const pageProps = computed(() => page.props);

// Canvas name inline edit
const canvasName = ref("");
const isEditingName = ref(false);
const isSavingName = ref(false);

watch(
  () => pageProps.value.canvas_name,
  (val) => {
    canvasName.value = val ?? "";
  },
  { immediate: true },
);

const currentCanvasId = computed(() => pageProps.value.video_id ?? null);
const isCanvasPage = computed(() => !!currentCanvasId.value);

async function saveName() {
  if (!currentCanvasId.value) return;
  const trimmed = canvasName.value.trim();
  if (!trimmed) return;
  isSavingName.value = true;
  try {
    await canvasStore.renameCanvas(currentCanvasId.value, trimmed);
    canvasName.value = trimmed;
  } finally {
    isSavingName.value = false;
    isEditingName.value = false;
  }
}

function onNameKeydown(e) {
  if (e.key === "Enter") saveName();
  if (e.key === "Escape") {
    canvasName.value = pageProps.value.canvas_name ?? "";
    isEditingName.value = false;
  }
}

const open = ref(true);

const menu = [
  {
    label: "Kanvas Baru",
    icon: "i-lucide-pencil",
    to: "/canvas/",
  },
  // {
  //   label: "Dataset",
  //   icon: "i-lucide-database",
  // },
  // {
  //   label: "Dokumentasi",
  //   icon: "i-lucide-book",
  // },
  // {
  //   label: "Tentang",
  //   icon: "i-lucide-info",
  // },
];

const canvasMenuItems = computed(() =>
  canvasStore.canvases.map((canvas) => ({
    label: canvas.name,
    to: `/canvas/${canvas.id}/`,
  })),
);

const user = ref({
  name: "Realitaa",
  avatar: {
    src: "https://github.com/realitaa.png",
    alt: "Realitaa",
  },
});

const userItems = computed(() => [
  [
    {
      label: "GitHub",
      icon: "i-simple-icons-github",
      to: "https://github.com/realitaa/spatio-temporal",
      target: "_blank",
    },
    {
      label: "Kembali",
      icon: "i-lucide-log-out",
      to: "/",
    },
  ],
]);
</script>

<template>
  <div
    class="absolute inset-0 z-0 pointer-events-none"
    style="
      background-image:
        radial-gradient(circle 600px at 0% 200px, #fce7f3, transparent),
        radial-gradient(circle 600px at 100% 200px, #fce7f3, transparent);
    "
  ></div>

  <div class="flex flex-1">
    <USidebar
      v-model:open="open"
      collapsible="icon"
      rail
      :ui="{
        container: 'h-full',
        inner: 'bg-elevated/25 divide-transparent',
        body: 'py-0',
      }"
    >
      <template #header="{ state }">
        <div class="w-full flex items-center justify-center">
          <UIcon
            name="i-lucide-camera"
            class="size-6"
            v-if="state === 'collapsed'"
          />
          <span class="text-sm font-bold" v-else
            >Spatio-Temporal Data Analysis</span
          >
        </div>
      </template>

      <template #default="{ state }">
        <UNavigationMenu
          :key="state"
          :items="menu"
          orientation="vertical"
          :ui="{ link: 'p-1.5 overflow-hidden' }"
        />
        <div class="h-full overflow-y-auto">
          <UNavigationMenu
            :key="state"
            :items="canvasMenuItems"
            orientation="vertical"
            v-if="state === 'expanded'"
            :ui="{ link: 'p-1.5 overflow-hidden' }"
          />
        </div>
      </template>

      <template #footer>
        <UDropdownMenu
          :items="userItems"
          :content="{ align: 'center', collisionPadding: 12 }"
          :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width) min-w-48' }"
        >
          <UButton
            v-bind="user"
            :label="user?.name"
            trailing-icon="i-lucide-chevrons-up-down"
            color="neutral"
            variant="ghost"
            square
            class="w-full data-[state=open]:bg-elevated overflow-hidden"
            :ui="{
              trailingIcon: 'text-dimmed ms-auto',
            }"
          />
        </UDropdownMenu>
      </template>
    </USidebar>

    <div class="flex-1 flex flex-col z-5">
      <div
        class="h-(--ui-header-height) shrink-0 flex items-center px-4 border-b border-default space-x-2"
      >
        <UButton
          icon="i-lucide-panel-left"
          color="neutral"
          variant="ghost"
          aria-label="Toggle sidebar"
          @click="open = !open"
        />
        <template v-if="isCanvasPage">
          <UInput
            v-if="isEditingName"
            v-model="canvasName"
            size="sm"
            autofocus
            :loading="isSavingName"
            class="font-bold"
            @blur="saveName"
            @keydown="onNameKeydown"
          />
          <button
            v-else
            class="text-sm font-bold border border-default hover:border-black px-2 py-1 rounded-lg min-w-45 truncate max-w-xs text-left"
            @click="isEditingName = true"
          >
            {{ canvasName || "Nama Kanvas" }}
          </button>
        </template>
        <span v-else class="text-sm font-bold">Spatio-Temporal</span>
        <div class="ml-auto" v-if="isCanvasPage">
          <UButton
            icon="i-lucide-trash-2"
            color="error"
            variant="ghost"
            square
            @click="openDeleteModal = true"
          />
        </div>
      </div>

      <div class="flex-1 p-4 z-5">
        <slot />
      </div>
    </div>
  </div>

  <!-- Modal delete canvas -->
  <DeleteCanvasModal
    v-model:open="openDeleteModal"
    :canvas-id="currentCanvasId"
  />
</template>
