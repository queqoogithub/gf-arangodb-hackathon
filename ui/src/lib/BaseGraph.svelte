<script lang="ts">
  import { writable } from 'svelte/store';

  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    ConnectionLineType,
  } from '@xyflow/svelte';
  import Modal from '../lib/Modal.svelte';
  import type { JobGraphResponse, APINode } from '../types';
 
  // 👇 this is important! You need to import the styles for Svelte Flow to work
  import '@xyflow/svelte/dist/style.css';
 
  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position.
  let props = $props();
 
  let showModal = $state(false);
  let modalData = $state<APINode | null>(null);

  function handleNodeClick(event: any) {
    const nodeLabel = event.detail.node.data.label;
    console.dir(event.detail.node.data.label);
    const jobDetail = props.jobDetails[nodeLabel];
    console.dir(props.jobDetails);
    console.dir(jobDetail);

    if (jobDetail != null) {
      modalData = jobDetail;
    }

    showModal = true;
  }

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
        <h2>{modalData?.job}</h2>
      {/snippet}
    
      <ol class="definition-list">
        <li>description: {modalData?.job_description}</li>
        <li>salary: {modalData?.min_salary ?? "unknown"} - {modalData?.max_salary ?? "unknown"} baht</li>
        <li>experience: {modalData?.min_exp ?? "unknown"} - {modalData?.max_exp ?? "unknown"} year(s)</li>

        <li>level: {modalData?.level}</li>
        <li>category: {modalData?.category}</li>
        <li>required specialized knowledge: {modalData?.hard_skill}</li>
        <li>required soft skills: {modalData?.soft_skill}</li>
        <li>matching interests: {modalData?.interest}</li>
        <li>required education: {modalData?.education}</li>
      </ol>
    </Modal>
    <SvelteFlow
      fitView
      connectionLineType={ConnectionLineType.SmoothStep}
      defaultEdgeOptions={{ type: 'smoothstep', animated: true }}
      on:nodeclick={handleNodeClick}
      {...props}
    >
      <Background variant={BackgroundVariant.Dots} />
      <Controls />
      <!-- <MiniMap /> -->
    </SvelteFlow>
  </fragment>
<!-- </div> -->