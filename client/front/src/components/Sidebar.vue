<script setup lang="ts">
import type { Pokemon } from '@/types/types';
import { ref, computed } from 'vue';

const props = defineProps<{
  selectedPokemon: Pokemon | null,
  team: Pokemon[] // Ajout de la prop 'team'
}>();

const emit = defineEmits<{
  (e: 'highlightCoverage', pokemonNames: string[]): void
  (e: 'highlightDisadvantage', pokemonNames: string[]): void
  (e: 'addToTeam', pokemon: Pokemon): void // Ajout de l'événement 'addToTeam'
}>();

const isLoadingCoverage = ref(false);
const isLoadingDisadvantage = ref(false);

// Logique pour vérifier si le pokémon est dans l'équipe ou si l'équipe est pleine
const isPokemonInTeam = computed(() => {
  if (!props.selectedPokemon) return false;
  return props.team.some(p => p.pk === props.selectedPokemon?.pk);
});

const isTeamFull = computed(() => props.team.length >= 6);

function addToTeam() {
  if (props.selectedPokemon) {
    emit('addToTeam', props.selectedPokemon);
  }
}

const handleHighlightCoverage = async () => {
  if (!props.selectedPokemon) return;
  
  isLoadingCoverage.value = true;
  try {
    const response = await fetch(`http://localhost:8020/pokemon/${props.selectedPokemon.pk}/coverage`);
    if (!response.ok) throw new Error('Failed to fetch coverage');
    
    const data = await response.json();
    const pokemonNames = data.coverage || [];
    emit('highlightCoverage', pokemonNames);
  } catch (error) {
    alert('Erreur lors de la récupération de la couverture');
  } finally {
    isLoadingCoverage.value = false;
  }
};
const handleHighlightDisadvantage = async () => {
  if (!props.selectedPokemon) return;
  
  isLoadingDisadvantage.value = true;
  try {
    const response = await fetch(`http://localhost:8020/pokemon/${props.selectedPokemon.pk}/disadvantage`);
    if (!response.ok) throw new Error('Failed to fetch disadvantage');
    
    const data = await response.json();
    // Assuming the API returns an object with pokemon names to highlight
    const pokemonNames = data.coverage || [];
    emit('highlightDisadvantage', pokemonNames);
  } catch (error) {
    alert('Erreur lors de la récupération des désavantages');
  } finally {
    isLoadingDisadvantage.value = false;
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
        @click="addToTeam"
        :disabled="isPokemonInTeam || isTeamFull"
        class="w-full mt-6 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors"
      >
        <span v-if="isPokemonInTeam">Déjà dans l'équipe</span>
        <span v-else-if="isTeamFull">Équipe complète</span>
        <span v-else>Ajouter à l'équipe</span>
      </button>
      <button
        @click="handleHighlightCoverage"
        :disabled="isLoadingCoverage"
        class="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors"
      >
        {{ isLoadingCoverage ? 'Chargement...' : "Afficher les pokémons qu'il peut battre" }}
      </button>
      <button
        @click="handleHighlightDisadvantage"
        :disabled="isLoadingDisadvantage"
        class="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors"
      >
        {{ isLoadingDisadvantage ? 'Chargement...' : "Afficher les pokémons qui peuvent nous battre" }}
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
