<script>
  import { writable } from 'svelte/store';
  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    ConnectionLineType,
    MiniMap
  } from '@xyflow/svelte';
 
  // 👇 this is important! You need to import the styles for Svelte Flow to work
  import '@xyflow/svelte/dist/style.css';
 
  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position.
  const nodes = writable([
    {
      id: '1',
      type: 'input',
      data: { label: 'Start' },
      position: { x: 200, y: 0 }
    },
    {
      id: '2',
      type: 'default',
      data: { label: 'Supercalifragiliticespiladocious' },
      position: { x: 0, y: 150 }
    },
    {
      id: '3',
      type: 'default',
      data: { label: 'Node 3' },
      position: { x: 200, y: 150 }
    },
    {
      id: '4',
      type: 'default',
      data: { label: 'Node 4' },
      position: { x: 400, y: 150 }
    },
    {
      id: '5',
      type: 'default',
      data: { label: 'Node 5' },
      position: { x: 400, y: 300 }
    }
  ]);
 
  // same for edges
  const edges = writable([
    {
      id: '1-2',
      // type: 'default',
      source: '1',
      target: '2',
      // label: 'Edge Text'
    },
    {
      id: '1-3',
      // type: 'default',
      source: '1',
      target: '3',
      // label: 'Edge Text'
    },
  ]);
 
  let props = $props();
  // const snapGrid = /** @type {[number, number]} */ ([25, 25]);
</script>
 
<!--
👇 By default, the Svelte Flow container has a height of 100%.
This means that the parent container needs a height to render the flow.
-->
<!-- <div style:height="50vh"> -->
  <SvelteFlow
    {nodes}
    {edges}
    fitView
    connectionLineType={ConnectionLineType.SmoothStep}
    defaultEdgeOptions={{ type: 'smoothstep', animated: true }}
    on:nodeclick={(event) => console.log('on node click', event.detail.node)}
    {...props}
  >
    <Background variant={BackgroundVariant.Dots} />
    <Controls />
    <!-- <MiniMap /> -->
  </SvelteFlow>
<!-- </div> -->