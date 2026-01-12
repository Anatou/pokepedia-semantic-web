<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import {Graph2d, Timeline, Network} from 'vue3-visjs'
import {ref} from "vue";

const graphdata = {
  groups: [
    {
      id: 0,
      content: 'Group 1'
    }
  ],
  items: [
    {
      id: 0,
      group: 0,
      start: new Date(),
      content: 'Item 1'
    }
  ],
  options: {
    editable: true
  }
};


const graph2dEvents = ref('');

function graph2dEvent(eventName: string) {
  if (graph2dEvents.value.length > 500) graph2dEvents.value = '';
  graph2dEvents.value += `${eventName}, `;
}

const graph2dGroups = ref([
  {
    id: 0,
    content: 'SquareShaded',
    options: {
      drawPoints: {
        style: 'square', // square, circle
      },
      shaded: {
        orientation: 'bottom', // top, bottom
      },
    },
  },
  {
    id: 1,
    content: 'Bargraph',
    options: {
      style: 'bar',
    },
  },
  {
    id: 2,
    content: 'Blank',
    options: {drawPoints: false},
  },
  {
    id: 3,
    content: 'CircleShaded',
    options: {
      drawPoints: {
        style: 'circle', // square, circle
      },
      shaded: {
        orientation: 'top', // top, bottom
      },
    },
  },
]);

const graph2dItems = ref([
  {x: '2014-06-13', y: 60},
  {x: '2014-06-14', y: 40},
  {x: '2014-06-15', y: 55},
  {x: '2014-06-16', y: 40},
  {x: '2014-06-17', y: 50},
  {x: '2014-06-13', y: 30, group: 0},
  {x: '2014-06-14', y: 10, group: 0},
  {x: '2014-06-15', y: 15, group: 1},
  {x: '2014-06-16', y: 30, group: 1},
  {x: '2014-06-17', y: 10, group: 1},
  {x: '2014-06-18', y: 15, group: 1},
  {x: '2014-06-19', y: 52, group: 1},
  {x: '2014-06-20', y: 10, group: 1},
  {x: '2014-06-21', y: 20, group: 2},
  {x: '2014-06-22', y: 60, group: 2},
  {x: '2014-06-23', y: 10, group: 2},
  {x: '2014-06-24', y: 25, group: 2},
  {x: '2014-06-25', y: 30, group: 2},
  {x: '2014-06-26', y: 20, group: 3},
  {x: '2014-06-27', y: 60, group: 3},
  {x: '2014-06-28', y: 10, group: 3},
  {x: '2014-06-29', y: 25, group: 3},
  {x: '2014-06-30', y: 30, group: 3},
]);
const graph2dOptions = ref({
  defaultGroup: 'ungrouped',
  legend: true,
  start: '2014-06-10',
  end: '2014-07-04',
});


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
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125"/>
    <div class="wrapper">
      <HelloWorld msg="You did it!"/>
    </div>

    <graph-2d
      ref="graph2d"
      :items="graph2dItems"
      :groups="graph2dGroups"
      :options="graph2dOptions"
      @click="graph2dEvent('click')"
      @contextmenu="graph2dEvent('contextmenu')"
      @current-time-tick="graph2dEvent('currentTimeTick')"
      @double-click="graph2dEvent('doubleClick')"
      @changed="graph2dEvent('changed')"
      @rangechange="graph2dEvent('rangechange')"
      @rangechanged="graph2dEvent('rangechanged')"
      @timechange="graph2dEvent('timechange')"
      @timechanged="graph2dEvent('timechanged')"
      @items-add="graph2dEvent('items-add')"
      @items-update="graph2dEvent('items-update')"
      @items-remove="graph2dEvent('items-remove')"
      @groups-mounted="graph2dEvent('groups-mounted')"
      @groups-add="graph2dEvent('groups-add')"
      @groups-update="graph2dEvent('groups-update')"
      @groups-remove="graph2dEvent('groups-remove')">
    </graph-2d>
    <div class="events">
      <p>
        Graph2d events: <br/>
        {{ graph2dEvents }}
      </p>
    </div>


    <network
      class="w-100 h-90 network"
      ref="network"
      :nodes="networkNodes"
      :edges="networkEdges"
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

    <button @click="addNode">Add node</button>
    <button @click="addEdge">Add edge</button>
    <button @click="resetNetwork">Reset Network</button>
    <button @click="removeNode">Remove Node</button>
    <button @click="removeEdge">Remove Edge</button>
    <div class="events">
      <p>
        Network events: <br/>
        {{ networkEvents }}
      </p>
    </div>

  </header>

  <main>
    <TheWelcome/>
    <Timeline
      :groups="graphdata.groups"
      :items="graphdata.items"
      :options="graphdata.options"
    />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}
</style>
