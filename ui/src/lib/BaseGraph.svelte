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
  import Modal from '../lib/Modal.svelte';
 
  // 👇 this is important! You need to import the styles for Svelte Flow to work
  import '@xyflow/svelte/dist/style.css';
 
  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position.
 
  let showModal = $state(false);
  let props = $props();
  // const snapGrid = /** @type {[number, number]} */ ([25, 25]);
</script>
 
<!--
👇 By default, the Svelte Flow container has a height of 100%.
This means that the parent container needs a height to render the flow.
-->
<!-- <div style:height="50vh"> -->
  <fragment>
    <Modal bind:showModal>
      <!-- 
        // job
        // job description
        // min - max salary baht
        // min -  max exp [optional]
        // level
        // category
        // required specialized knowledge
        // required soft skills
        // matching interests
        // required education 
      -->
      {#snippet header()}
        <h2>hello</h2>
      {/snippet}
    
      <ol class="definition-list">
        <li>of or relating to modality in logic</li>
        <li>
          containing provisions as to the mode of procedure or the manner of taking effect —used of a
          contract or legacy
        </li>
        <li>of or relating to a musical mode</li>
        <li>of or relating to structure as opposed to substance</li>
        <li>
          of, relating to, or constituting a grammatical form or category characteristically indicating
          predication
        </li>
        <li>of or relating to a statistical mode</li>
      </ol>
    
      <a href="https://www.merriam-webster.com/dictionary/modal">merriam-webster.com</a>
    </Modal>
    <SvelteFlow
      fitView
      connectionLineType={ConnectionLineType.SmoothStep}
      defaultEdgeOptions={{ type: 'smoothstep', animated: true }}
      on:nodeclick={(event) => {
        // props.openModal();
        showModal = true;
        console.log('on node click', event.detail.node)}
      }
      {...props}
    >
      <Background variant={BackgroundVariant.Dots} />
      <Controls />
      <!-- <MiniMap /> -->
    </SvelteFlow>
  </fragment>
<!-- </div> -->