<script setup lang="ts">
import { ref, watch } from 'vue';
import type { GroupType } from '@/types/types';

const filter = defineModel<string>('filter', { default: '' });
const groupType = defineModel<GroupType>('groupType', { default: 'type1' });

const searchInput = ref<string>(filter.value);
let debounceTimeout: number | undefined;

// Debounce the search input
watch(searchInput, (newValue) => {
  if (debounceTimeout) {
    clearTimeout(debounceTimeout);
  }
  debounceTimeout = setTimeout(() => {
    filter.value = newValue;
  }, 300);
});

const groupOptions: { value: GroupType; label: string }[] = [
  { value: 'type1', label: 'Type 1' },
  { value: 'type2', label: 'Type 2' },
  { value: 'all-types', label: 'Tous les types' },
  { value: 'generation', label: 'Génération' },
  { value: 'famille', label: 'Famille' },
  { value: 'none', label: 'Aucun' },
];
</script>

<template>
  <header class="h-[50px] bg-gray-700 px-6 flex items-center justify-between gap-6">
    <h1 class="text-white text-xl font-bold whitespace-nowrap">Pokemon Explorer</h1>

    <div class="flex items-center gap-4 flex-1">
      <input
        v-model="searchInput"
        type="text"
        placeholder="Rechercher un Pokémon..."
        class="px-4 py-2 rounded-md border border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-w-[200px]"
      />

      <div class="flex gap-2 flex-wrap">
        <button
          v-for="option in groupOptions"
          :key="option.value"
          @click="groupType = option.value"
          :class="[
            'px-3 py-2 rounded-md text-sm font-medium transition-colors',
            groupType === option.value
              ? 'bg-blue-600 text-white'
              : 'bg-gray-500 text-white hover:bg-gray-600'
          ]"
        >
          {{ option.label }}
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
</style>
