<script setup lang="ts">
import Graph from './components/Graph.vue'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import {ref, onMounted} from "vue";
import type {Pokemon, GroupType} from "@/types/types.ts";

const pokemons = ref<Pokemon[]>();
const filter = ref<string>("");
const groupType = ref<GroupType>('type1');
const selectedPokemon = ref<Pokemon | null>(null);
const highlightedPokemons = ref<string[]>([]);

function handlePokemonSelected(pokemon: Pokemon | null) {
  selectedPokemon.value = pokemon;
}

function handleHighlightCoverage(pokemonNames: string[]) {
  highlightedPokemons.value = pokemonNames;
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
      :highlighted-pokemons="highlightedPokemons"
      @pokemon-selected="handlePokemonSelected"
    />
    <div v-else>Chargement des pokemons...</div>
    <Sidebar :selected-pokemon="selectedPokemon" @highlight-coverage="handleHighlightCoverage" />
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
</style>
