<script lang="ts">
  import { writable, get } from 'svelte/store';

  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    ConnectionLineType,
  } from '@xyflow/svelte';
  import Modal from '../lib/Modal.svelte';
  import * as Dialog from "$lib/components/ui/dialog";
  import * as Resizable from "$lib/components/ui/resizable";
  import { Button } from "$lib/components/ui/button";
  import { Label } from "$lib/components/ui/label";
  import { Input } from "$lib/components/ui/input";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import * as Accordion from "$lib/components/ui/accordion";
  import type { JobGraphResponse, APINode } from '../types';
 
  // 👇 this is important! You need to import the styles for Svelte Flow to work
  import '@xyflow/svelte/dist/style.css';

  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position.
  let props = $props();
 
  let showModal = $state(false);
  let modalData = $state<APINode | null>(null);

  function handleNodeClick(event: any) {
    const nodeLabel = event.detail.node.data.label;

    const jobDetails = get<{ [key: string]: APINode }>(props.jobDetails);

    const jobDetail = jobDetails[nodeLabel];
    console.dir($state.snapshot(props.jobDetails))
    console.log(jobDetail)
    // $inspect(props.jobDetails)

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
    <!-- <Modal bind:showModal>
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
    </Modal> -->
    <Dialog.Root bind:open={showModal}>
      <!-- <Dialog.Content class="sm:max-w-[425px]"> -->
      <Dialog.Content >
        <Dialog.Header>
          <Dialog.Title>{modalData?.job}</Dialog.Title>
          <Dialog.Description>
            <Accordion.Root>
              <Accordion.Item value="item-1">
                <Accordion.Trigger>Job Description</Accordion.Trigger>
                <Accordion.Content>
                  {modalData?.job_description}
                </Accordion.Content>
              </Accordion.Item>
            </Accordion.Root>
          </Dialog.Description>
        </Dialog.Header>
        <div class="grid grid-cols-2 gap-4 py-4">
            <p class="font-bold text-left">Salary:</p>
            <p>{modalData?.min_salary ?? "Unknown"} - {modalData?.max_salary ?? "Unknown"} Baht</p>
            
            <p class="font-bold text-left">Experience:</p>
            <p>{modalData?.min_exp ?? "Unknown"} - {modalData?.max_exp ?? "Unknown"} year(s)</p>
      
            <p class="font-bold text-left">Level:</p>
            <p>{modalData?.level ?? "Unknown"}</p>
      
            <p class="font-bold text-left">Category:</p>
            <p>{modalData?.category ?? "Unknown"}</p>
      
            <p class="font-bold text-left">Specialized Knowledge:</p>
            <p class="break-words overflow-wrap-anywhere">{modalData?.hard_skill?.join(', ') ?? "Unknown"}</p>
      
            <p class="font-bold text-left">Soft Skills:</p>
            <p class="break-words overflow-wrap-anywhere">{modalData?.soft_skill?.join(', ') ?? "Unknown"}</p>
      
            <p class="font-bold text-left">Matching Interests:</p>
            <p class="break-words overflow-wrap-anywhere">{modalData?.interest?.join(', ') ?? "Unknown"}</p>
      
            <p class="font-bold text-left">Education:</p>
            <p class="break-words overflow-wrap-anywhere">{modalData?.education?.join(', ') ?? "Unknown"}</p>
        </div>
        <Dialog.Footer>
          <Button type="submit" on:click={() => showModal = false}>Close</Button>
        </Dialog.Footer>
      </Dialog.Content>
    </Dialog.Root>

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