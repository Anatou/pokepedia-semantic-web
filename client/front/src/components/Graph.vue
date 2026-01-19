<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { Network } from 'vue3-visjs'
import type { Edge, Node, Pokemon, GroupType, Coverage } from "@/types/types.ts";
import type { Network as VisNetwork } from "vis-network";
const network = ref<InstanceType<typeof Network> | null>(null);

const onClickZoom = (params: any) => {
  const vis = network.value?.network;
  if (!vis) return;


  // clic dans le vide → reset vue
  if (!params.nodes || params.nodes.length === 0) {
    vis.fit({
      animation: {duration: 400, easingFunction: "easeInOutQuad"}
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
  coverage: Coverage,
  coverageTeam: Coverage
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
          label: p.type1,
          color: {
            background: 'lightgray',
            border: 'gray'
          },
          font: {
            size: 24
          }
        });
        groupsToId.set(p.type1, groupId);
        groupId++;
      }
    } else if (props.groupType === 'type2') {
      if (p.type2) {
        if (!groupsToId.has(p.type2)) {
          nodesBuilder.push({
            id: groupId,
            label: p.type2,
            color: {
              background: 'lightgray',
              border: 'gray'
            },
            font: {
              size: 24
            }
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
          label: p.type1,
          color: {
            background: 'lightgray',
            border: 'gray'
          },
          font: {
            size: 24
          }
        });
        groupsToId.set(p.type1, groupId);
        groupId++;
      }
      if (p.type2) {
        if (!groupsToId.has(p.type2)) {
          nodesBuilder.push({
            id: groupId,
            label: p.type2,
            color: {
              background: 'lightgray',
              border: 'gray'
            },
            font: {
              size: 24
            }
          });
          groupsToId.set(p.type2, groupId);
          groupId++;
        }
      }
    } else if (props.groupType === 'generation') {
      if (!groupsToId.has(p.gen)) {
        nodesBuilder.push({
          id: groupId,
          label: p.gen,
          color: {
            background: 'lightgray',
            border: 'gray'
          },
          font: {
            size: 24
          }
        });
        groupsToId.set(p.gen, groupId);
        groupId++;
      }
    } else if (props.groupType === 'famille') {
      if (!groupsToId.has(p.famille)) {
        nodesBuilder.push({
          id: groupId,
          label: p.famille,
          color: {
            background: 'lightgray',
            border: 'gray'
          },
          font: {
            size: 24
          }
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
watch(() => [props.pokemons, props.filter, props.groupType], computeGraph, {deep: true})
watch(
  () => props.coverage,
  (new_coverage, old_coverage) => {
    const BG_ADV = 'greenyellow';
    const BR_ADV = 'darkgreen';
    const BG_DIS = 'red';
    const BR_DIS = 'darkred';

    const vis = network.value?.network;
    if (!vis) {
      return;
    }
    const nodesDS = vis.body.data.nodes;
    const existingIds = new Set(nodesDS.getIds());

    const old_nodes = old_coverage.advantages.map(pk => [pk, true])
      .concat(old_coverage.disadvantages.map(pk => [pk, false]));
    const new_nodes = new_coverage.advantages.map(pk => [pk, true])
      .concat(new_coverage.disadvantages.map(pk => [pk, false]));
    console.log("old nodes", old_nodes)
    nodesDS.update(old_nodes
      .filter(([pk, _adv]) => existingIds.has(pk))
      .filter(([pk, adv]) => adv ? nodesDS.get(pk)?.color?.background == BG_ADV : nodesDS.get(pk)?.color?.background == BG_DIS)
      .map(([pk, _adv]) => {
        return {
          id: pk,
          color: {
            background: 'lightblue',
            border: 'blue'
          }
        }
      }));
    console.log("new nodes", new_nodes)
    nodesDS.update(new_nodes
      .filter(([pk, _adv]) => existingIds.has(pk))
      .map(([pk, adv]) => {
        return {
          id: pk,
          color: {
            background: adv ? BG_ADV : BG_DIS,
            border: adv ? BR_ADV : BR_DIS
          }
        }
      }));
  },
  {deep: true}
);
watch(
  () => props.coverageTeam,
  (new_coverageTeam, old_coverageTeam) => {
    const BG_ADV = 'greenyellow';
    const BR_ADV = 'darkgreen';
    const BG_DIS = 'red';
    const BR_DIS = 'darkred';

    const vis = network.value?.network;
    if (!vis) {
      return;
    }
    const nodesDS = vis.body.data.nodes;
    const existingIds = new Set(nodesDS.getIds());

    const old_nodes = old_coverageTeam.advantages.map(pk => [pk, true])
      .concat(old_coverageTeam.disadvantages.map(pk => [pk, false]));
    const new_nodes = new_coverageTeam.advantages.map(pk => [pk, true])
      .concat(new_coverageTeam.disadvantages.map(pk => [pk, false]));
    console.log("old nodes", old_nodes)
    nodesDS.update(old_nodes
      .filter(([pk, _adv]) => existingIds.has(pk))
      .filter(([pk, adv]) => adv ? nodesDS.get(pk)?.color?.background == BG_ADV : nodesDS.get(pk)?.color?.background == BG_DIS)
      .map(([pk, _adv]) => {
        return {
          id: pk,
          color: {
            background: 'lightblue',
            border: 'blue'
          }
        }
      }));
    console.log("new nodes", new_nodes)
    nodesDS.update(new_nodes
      .filter(([pk, _adv]) => existingIds.has(pk))
      .map(([pk, adv]) => {
        return {
          id: pk,
          color: {
            background: adv ? BG_ADV : BG_DIS,
            border: adv ? BR_ADV : BR_DIS
          }
        }
      }));
  },
  {deep: true}
);

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
  <div class="grow">
    <Network
      class="h-full"
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
</style>
