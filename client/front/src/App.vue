<script setup lang="ts">
import Graph from './components/Graph.vue'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import TeamBuilder from './components/TeamBuilder.vue' // Importer le nouveau composant
import {ref, onMounted, computed} from "vue";
import type {Pokemon, GroupType, Coverage, PokemonWithCoverage} from "@/types/types.ts";

const pokemons = ref<Pokemon[]>();
const filter = ref<string>("");
const groupType = ref<GroupType>('type1');
const selectedPokemon = ref<Pokemon | null>(null);


const coverage = ref<Coverage>({advantages: [], disadvantages: []});
const team = ref<PokemonWithCoverage[]>([]); // Ajout de la ref pour l'équipe

// Computed qui combine team + teamCoverage
const coverageTeam = computed(() => {
  const advantagesSet = new Set<string>();
  const disadvantagesSet = new Set<string>();
  
  team.value.forEach(pokemonCoverage => {
    pokemonCoverage.coverage.advantages.forEach(adv => advantagesSet.add(adv));
    pokemonCoverage.coverage.disadvantages.forEach(dis => disadvantagesSet.add(dis));
  });

  // Filtrer les désavantages pour éviter les intersections avec les avantages
  const filteredDisadvantages = Array.from(disadvantagesSet).filter(dis => !advantagesSet.has(dis));

  return {
    advantages: Array.from(advantagesSet),
    disadvantages: filteredDisadvantages
  };
});

function handlePokemonSelected(pokemon: Pokemon | null) {
  console.log("Pokemon selected", pokemon)
  selectedPokemon.value = pokemon;
}
function handleUpdateCoverage(new_coverage: Coverage) {
  console.log("updating coverage to ", new_coverage)
  // Making sure there is no intersection between advantages and disadvantages,
  // With the priority for advantage.
  const advantagesSet = new Set(new_coverage.advantages);
  coverage.value = {
    advantages: new_coverage.advantages,
    disadvantages: new_coverage.disadvantages.filter(d => !advantagesSet.has(d))
  };
}

function handleAddToTeam(pokemon: Pokemon) {
  if (team.value.length < 6 && !team.value.some(p => p.pokemon.pk === pokemon.pk)) {
    team.value.push({pokemon, coverage: coverage.value});
  }
}

function handleRemoveFromTeam(pokemon: Pokemon) {
  team.value = team.value.filter(p => p.pokemon.pk !== pokemon.pk);
}

onMounted(() => {
  fetch("http://localhost:8020/pokemons").then((r) => {
    r.json().then(r => {
      pokemons.value = r.pokemons;
    }).catch(e => {
      console.log(e);
    })
  }).catch(e => {
    console.log(e)
    alert("Error loading pokemons: " + e)
  })
})


</script>

<template>
  <Header v-model:filter="filter" v-model:group-type="groupType"/>

  <main>
    <Graph
      v-if="pokemons"
      :pokemons="pokemons"
      :filter="filter"
      :group-type="groupType"
      :coverage="coverageTeam"
      @pokemon-selected="handlePokemonSelected"
    />
    <div class="grow" v-else>Chargement des pokemons...</div>
    <div class="sidebar-container">
      <Sidebar
        :selected-pokemon="selectedPokemon"
        :team="team"
        @update-coverage="handleUpdateCoverage"
        @add-to-team="handleAddToTeam"
      />
      <TeamBuilder :team="team" :pokemons="pokemons" @add-to-team="handleAddToTeam" @remove-from-team="handleRemoveFromTeam" />
    </div>
  </main>
</template>

<style scoped>
main {
  width: 100vw;
  display: flex;
  justify-content: stretch;
  align-items: stretch;
  flex-direction: row;
  gap: 1px;
  height: calc(100vh - 50px);
  background-color: gray;
}
main > * {
  background-color: black;
}

.sidebar-container {
  display: flex;
  flex-direction: column;
  gap: 1px;
  overflow: hidden; /* Empêche le conteneur de déborder */
}

.sidebar-container > :first-child { /* Cible la Sidebar */
  flex-grow: 1;
  overflow-y: auto; /* Permet le défilement interne si nécessaire */
}

.sidebar-container > * {
  background-color: black;
}
</style>
