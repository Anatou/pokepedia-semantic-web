<script setup lang="ts">
import {ref} from "vue";
import {Network} from 'vue3-visjs'

const networkEvents = ref('')
const networkEvent = (eventName: string) => {
  if (networkEvents.value.length > 500) networkEvents.value = '';
  networkEvents.value += `${eventName}, `;
}
const networkNodes = ref([
  {id: 1, label: 'Node 1'},
  {id: 2, label: 'Node 2'},
  {id: 3, label: 'Node 3'},
  {id: 4, label: 'Node 4'},
  {id: 5, label: 'Node 5'},
])
const networkEdges = ref([
  {id: 1, from: 1, to: 3},
  {id: 2, from: 1, to: 2},
  {id: 3, from: 2, to: 4},
  {id: 4, from: 2, to: 5},
  {id: 5, from: 3, to: 3},
])
const networkOptions = ref({
  nodes: {
    shape: 'circle',
  },
})


function addNode() {
  const id = Date.now();
  //networkValue.value.nodes.push({ id, label: 'New node' });
  // $refs.network.network.body.emitter.emit("_dataChanged");
}

function addEdge() {
  const n1 = Math.floor(Math.random() * networkNodes.value.length);
  const n2 = Math.floor(Math.random() * networkNodes.value.length);
  if (networkNodes.value[n1] && networkNodes.value[n2]) {
    networkEdges.value.push({
      id: Date.now(),
      from: networkNodes.value[n1].id,
      to: networkNodes.value[n2].id,
    });
  }
}

function resetNetwork() {
  networkNodes.value = [
    {id: 1, label: 'Node 1'},
    {id: 2, label: 'Node 2'},
    {id: 3, label: 'Node 3'},
    {id: 4, label: 'Node 4'},
    {id: 5, label: 'Node 5'}
  ];
  networkEdges.value = [
    {id: 1, from: 1, to: 3},
    {id: 2, from: 1, to: 2},
    {id: 3, from: 2, to: 4},
    {id: 4, from: 2, to: 5},
    {id: 5, from: 3, to: 3}
  ];
}

function removeNode() {
  networkNodes.value.splice(0, 1);
}

function removeEdge() {
  networkEdges.value.splice(0, 1);
}

</script>

<template>

</template>

<style scoped>

</style>
