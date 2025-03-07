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
      <Dialog.Content class="sm:max-w-[425px]">
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
        <div>
          <p>salary:</p>
          <p>experience:</p>
          <p>level:</p>
          <p>category:</p>
          <p>specialized knowledge:</p>
          <p>soft skills:</p>
          <p>matching interests:</p>
          <p>education:</p>
        </div>
        <!-- <Resizable.PaneGroup direction="horizontal">
          <Resizable.Pane>
            <p>salary:</p>
            <p>experience:</p>
            
          </Resizable.Pane>
          <Resizable.Handle  />
          <Resizable.Pane>
            <p>{modalData?.min_salary ?? "unknown"} - {modalData?.max_salary ?? "unknown"} baht</p>
            <p>{modalData?.min_exp ?? "unknown"} - {modalData?.max_exp ?? "unknown"} year(s)</p>
          </Resizable.Pane>
        </Resizable.PaneGroup> -->
        <!-- <div class="grid gap-4 py-4">
          <div class="grid grid-cols-4 items-center gap-4">
            <Label for="name" class="text-right">Name</Label>
            <Input id="name" value="Pedro Duarte" class="col-span-3" />
          </div>
          <div class="grid grid-cols-4 items-center gap-4">
            <Label for="username" class="text-right">Username</Label>
            <Input id="username" value="@peduarte" class="col-span-3" />
          </div>
        </div> -->
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