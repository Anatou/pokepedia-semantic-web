<script setup lang="ts">
import type { Pokemon } from '@/types/types';
import { ref } from 'vue';

const { selectedPokemon } = defineProps<{
  selectedPokemon: Pokemon | null
}>();

const emit = defineEmits<{
  (e: 'highlightCoverage', pokemonNames: string[]): void
}>();

const isLoadingCoverage = ref(false);

const handleHighlightCoverage = async () => {
  if (!selectedPokemon) return;
  
  isLoadingCoverage.value = true;
  try {
    const response = await fetch(`http://localhost:8020/pokemon/${selectedPokemon.pk}/coverage`);
    if (!response.ok) throw new Error('Failed to fetch coverage');
    
    const data = await response.json();
    // Assuming the API returns an object with pokemon names to highlight
    const pokemonNames = data.coverage || [];
    emit('highlightCoverage', pokemonNames);
  } catch (error) {
    alert('Erreur lors de la récupération de la couverture');
  } finally {
    isLoadingCoverage.value = false;
  }
};
</script>

<template>
  <aside class="w-[300px] bg-gray-800 text-white p-4 flex-shrink-0 overflow-y-auto">
    <div v-if="selectedPokemon">
      <img 
        v-if="selectedPokemon.image" 
        :src="selectedPokemon.image" 
        :alt="'Image de ' + selectedPokemon.pk"
        class="w-32 h-32 mx-auto mb-4 rounded-full bg-gray-700"
      >
      <h2 class="text-2xl font-bold mb-4 text-center">{{ selectedPokemon.pk }}</h2>
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
      <button
        @click="handleHighlightCoverage"
        :disabled="isLoadingCoverage"
        class="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors"
      >
        {{ isLoadingCoverage ? 'Chargement...' : "Afficher les pokémons qu'il peut battre" }}
      </button>
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
