<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { Network } from 'vue3-visjs'
import type { Edge, Node, Pokemon, GroupType } from "@/types/types.ts";
import type { Network as VisNetwork } from "vis-network";
const network = ref<InstanceType<typeof Network> | null>(null);

const onClickZoom = (params: any) => {
  const vis = network.value?.network;
  if (!vis) return;


  // clic dans le vide → reset vue
  if (!params.nodes || params.nodes.length === 0) {
    vis.fit({
      animation: { duration: 400, easingFunction: "easeInOutQuad" }
    });
    return;
  }


  const nodeId = params.nodes[0];
  const isGroup = nodeId >= 100000;


  vis.focus(nodeId, {
    scale: isGroup ? 1.2 : 1.8,
    animation: {
      duration: 500,
      easingFunction: "easeInOutQuad"
    }
  });
};


const props = defineProps<{
  pokemons: Pokemon[],
  filter: string,
  groupType: GroupType,
}>();

const emit = defineEmits<{
  (e: 'pokemonSelected', pokemon: Pokemon | null): void
}>();

const nodes = ref<Node[]>();
const edges = ref<Edge[]>();

const computeGraph = () => {
  const groupsToId = new Map<string, number>();
  let nodesBuilder: Node[] = [];
  let groupId = 100000;

  // Filter pokemons based on search
  const filteredPokemons = props.pokemons.filter(p =>
    p.pk.toLowerCase().includes(props.filter.toLowerCase())
  );

  // Build nodes based on group type
  filteredPokemons.forEach(p => {
    // Add pokemon node
    nodesBuilder.push({
      id: p.pk,
      label: p.pk
    });

    if (props.groupType === 'none') {
      return;
    }

    if (props.groupType === 'type1') {
      if (!groupsToId.has(p.type1)) {
        nodesBuilder.push({
          id: groupId,
          label: p.type1
        });
        groupsToId.set(p.type1, groupId);
        groupId++;
      }
    } else if (props.groupType === 'type2') {
      if(p.type2) {
        if (!groupsToId.has(p.type2)) {
          nodesBuilder.push({
            id: groupId,
            label: p.type2
          });
          groupsToId.set(p.type2, groupId);
          groupId++;
        }
      }
    } else if (props.groupType === 'all-types') {
      // Add both type1 and type2
      if (!groupsToId.has(p.type1)) {
        nodesBuilder.push({
          id: groupId,
          label: p.type1
        });
        groupsToId.set(p.type1, groupId);
        groupId++;
      }
      if(p.type2) {
        if (!groupsToId.has(p.type2)) {
          nodesBuilder.push({
            id: groupId,
            label: p.type2
          });
          groupsToId.set(p.type2, groupId);
          groupId++;
        }
      }
    } else if (props.groupType === 'generation') {
      if (!groupsToId.has(p.gen)) {
        nodesBuilder.push({
          id: groupId,
          label: p.gen
        });
        groupsToId.set(p.gen, groupId);
        groupId++;
      }
    } else if (props.groupType === 'famille') {
      if (!groupsToId.has(p.famille)) {
        nodesBuilder.push({
          id: groupId,
          label: p.famille
        });
        groupsToId.set(p.famille, groupId);
        groupId++;
      }
    }
  });

  nodes.value = nodesBuilder;

  // Build edges based on group type
  let edgesBuilder: Edge[] = [];

  if (props.groupType === 'none') {
    // No edges when no grouping
    edges.value = edgesBuilder;
    return;
  }

  filteredPokemons.forEach(p => {
    if (props.groupType === 'type1') {
      const groupNodeId = groupsToId.get(p.type1);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.pk,
          to: groupNodeId,
        });
      }
    } else if (props.groupType === 'type2') {
      const groupNodeId = groupsToId.get(p.type2);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.pk,
          to: groupNodeId,
        });
      }
    } else if (props.groupType === 'all-types') {
      const type1NodeId = groupsToId.get(p.type1);
      const type2NodeId = groupsToId.get(p.type2);
      if (type1NodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.pk,
          to: type1NodeId,
        });
      }
      if (type2NodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10 + 1,
          from: p.pk,
          to: type2NodeId,
        });
      }
    } else if (props.groupType === 'generation') {
      const groupNodeId = groupsToId.get(p.gen);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.pk,
          to: groupNodeId,
        });
      }
    } else if (props.groupType === 'famille') {
      const groupNodeId = groupsToId.get(p.famille);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.pk,
          to: groupNodeId,
        });
      }
    }
  });

  edges.value = edgesBuilder;
}

onMounted(computeGraph)
watch(() => [props.pokemons, props.filter, props.groupType], computeGraph, { deep: true })

const networkOptions = ref({
  nodes: {
    shape: 'circle',
  },
  layout: {
    improvedLayout: true
  }
});

function onNodeClick(event: { nodes: string[] }) {
  const selectedNodeId = event.nodes[0];
  if (selectedNodeId) {
    const foundPokemon = props.pokemons.find(p => p.pk === selectedNodeId);
    if (foundPokemon) {
      emit('pokemonSelected', foundPokemon);
    }
  } else {
    // Si on clique en dehors d'un noeud, on désélectionne
    emit('pokemonSelected', null);
  }
}

</script>

<template>
  <div class="graph">
    <Network
      class="network"
      ref="network"

      :nodes="nodes"
      :edges="edges"
      :options="networkOptions"
      @select-node="onNodeClick"
      @double-click="onClickZoom"
      @deselect-node="() => emit('pokemonSelected', null)"
    />
  </div>
</template>

<style scoped>
.graph {
  flex-grow: 1;
}
.graph .network {
  height: 100%;
}
</style>
