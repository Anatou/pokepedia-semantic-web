<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import {Network} from 'vue3-visjs'
import type {Edge, Node, Pokemon, GroupType} from "@/types/types.ts";

const props = defineProps<{
  pokemons: Pokemon[],
  filter: string,
  groupType: GroupType,
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
      id: p.num,
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
          from: p.num,
          to: groupNodeId,
        });
      }
    } else if (props.groupType === 'type2') {
      const groupNodeId = groupsToId.get(p.type2);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.num,
          to: groupNodeId,
        });
      }
    } else if (props.groupType === 'all-types') {
      const type1NodeId = groupsToId.get(p.type1);
      const type2NodeId = groupsToId.get(p.type2);
      if (type1NodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.num,
          to: type1NodeId,
        });
      }
      if (type2NodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10 + 1,
          from: p.num,
          to: type2NodeId,
        });
      }
    } else if (props.groupType === 'generation') {
      const groupNodeId = groupsToId.get(p.gen);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.num,
          to: groupNodeId,
        });
      }
    } else if (props.groupType === 'famille') {
      const groupNodeId = groupsToId.get(p.famille);
      if (groupNodeId !== undefined) {
        edgesBuilder.push({
          id: p.num * 10,
          from: p.num,
          to: groupNodeId,
        });
      }
    }
  });

  edges.value = edgesBuilder;
}

onMounted(computeGraph)
watch(() => [props.pokemons, props.filter, props.groupType], computeGraph, { deep: true })


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
  // {id: 1, from: 1, to: 3},
  // {id: 2, from: 1, to: 2},
  // {id: 3, from: 2, to: 4},
  // {id: 4, from: 2, to: 5},
  // {id: 5, from: 3, to: 3},
])
const networkOptions = ref({
  nodes: {
    shape: 'circle',
  },
  layout: {
    improvedLayout: true
  }
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
  <div class="graph">
    <network
      class="network"
      ref="network"
      :nodes="nodes"
      :edges="edges"
      :options="networkOptions"
      @click="networkEvent('click')"
      @double-click="networkEvent('doubleClick')"
      @oncontext="networkEvent('oncontext')"
      @hold="networkEvent('hold')"
      @release="networkEvent('release')"
      @select="networkEvent('select')"
      @select-node="networkEvent('selectNode')"
      @select-edge="networkEvent('selectEdge')"
      @deselect-node="networkEvent('deselectNode')"
      @deselect-edge="networkEvent('deselectEdge')"
      @drag-start="networkEvent('dragStart')"
      @dragging="networkEvent('dragging')"
      @drag-end="networkEvent('dragEnd')"
      @hover-node="networkEvent('hoverNode')"
      @blur-node="networkEvent('blurNode')"
      @hover-edge="networkEvent('hoverEdge')"
      @blur-edge="networkEvent('blurEdge')"
      @zoom="networkEvent('zoom')"
      @show-popup="networkEvent('showPopup')"
      @hide-popup="networkEvent('hidePopup')"
      @start-stabilizing="networkEvent('startStabilizing')"
      @stabilization-progress="networkEvent('stabilizationProgress')"
      @stabilization-iterations-done="networkEvent('stabilizationIterationsDone')"
      @stabilized="networkEvent('stabilized')"
      @resize="networkEvent('resize')"
      @init-redraw="networkEvent('initRedraw')"
      @before-drawing="networkEvent('beforeDrawing')"
      @after-drawing="networkEvent('afterDrawing')"
      @animation-finished="networkEvent('animationFinished')"
      @config-change="networkEvent('configChange')"
      @nodes-mounted="networkEvent('nodes-mounted')"
      @nodes-add="networkEvent('nodes-add')"
      @nodes-update="networkEvent('nodes-update')"
      @nodes-remove="networkEvent('nodes-remove')"
      @edges-mounted="networkEvent('edges-mounted')"
      @edges-add="networkEvent('edges-add')"
      @edges-update="networkEvent('edges-update')"
      @edges-remove="networkEvent('edges-remove')">
    </network>

    <!--    <button @click="addNode">Add node</button>-->
    <!--    <button @click="addEdge">Add edge</button>-->
    <!--    <button @click="resetNetwork">Reset Network</button>-->
    <!--    <button @click="removeNode">Remove Node</button>-->
    <!--    <button @click="removeEdge">Remove Edge</button>-->
    <!--    <div class="events">-->
    <!--      <p>-->
    <!--        Network events: <br/>-->
    <!--        {{ networkEvents }}-->
    <!--      </p>-->
    <!--    </div>-->
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
