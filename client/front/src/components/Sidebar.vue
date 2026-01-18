<script setup lang="ts">
import type { Pokemon } from '@/types/types';

defineProps<{
  selectedPokemon: Pokemon | null
}>();

</script>

<template>
  <aside class="w-[300px] bg-gray-800 text-white p-4 flex-shrink-0 overflow-y-auto">
    <div v-if="selectedPokemon">
      <h2 class="text-2xl font-bold mb-4">{{ selectedPokemon.pk }}</h2>
      <div class="space-y-2">
        <p><strong>Numéro National:</strong> #{{ selectedPokemon.num }}</p>
        <p><strong>Type 1:</strong> {{ selectedPokemon.type1 }}</p>
        <p v-if="selectedPokemon.type2"><strong>Type 2:</strong> {{ selectedPokemon.type2 }}</p>
        <p><strong>Génération:</strong> {{ selectedPokemon.gen }}</p>
        <p><strong>Famille:</strong> {{ selectedPokemon.famille }}</p>
        <a
          v-if="selectedPokemon.url"
          :href="selectedPokemon.url"
          target="_blank"
          rel="noopener noreferrer"
          class="mt-4 inline-block text-blue-400 hover:text-blue-300 transition-colors"
        >
          Voir sur Poképédia ↗
        </a>
      </div>
    </div>
    <div v-else class="text-gray-400 text-center pt-10">
      <p>Cliquez sur un Pokémon dans le graphe pour voir ses détails.</p>
    </div>
  </aside>
</template>

<style scoped>
/* Le style est principalement géré par Tailwind CSS dans le template */
aside {
  flex: 0 0 300px; /* Empêche la sidebar de grandir ou rétrécir */
}
</style>
