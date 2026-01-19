<script setup lang="ts">
import type { Pokemon } from '@/types/types';

defineProps<{
  team: Pokemon[]
}>();

const emit = defineEmits(['remove-from-team']);

function removePokemonFromTeam(pokemon: Pokemon) {
  emit('remove-from-team', pokemon);
}

</script>

<template>
  <div class="team-builder">
    <h2>Équipe Pokémon ({{ team.length }}/6)</h2>

    <div v-if="team.length > 0">
      <ul>
        <li v-for="pokemon in team" :key="pokemon.pk">
          <img :src="pokemon.image" :alt="pokemon.pk" class="pokemon-icon">
          <span>{{ pokemon.pk }}</span>
          <button class="remove-btn" @click="removePokemonFromTeam(pokemon)">X</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Aucun Pokémon dans l'équipe.</p>
    </div>
  </div>
</template>

<style scoped>
.team-builder {
  padding: 1rem;
  color: white;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  margin-top: auto; /* Pousse le composant vers le bas */
  justify-content: flex-end; /* Aligne le contenu (la liste) en bas */
}

h2 {
  margin-top: 0;
}

ul {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
}

.pokemon-icon {
  width: 32px;
  height: 32px;
  margin-right: 0.5rem;
  border-radius: 50%;
}

.remove-btn {
  background-color: #c01324;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  cursor: pointer;
}
</style>