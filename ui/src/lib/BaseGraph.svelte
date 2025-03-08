<script lang="ts">
  import { writable, get } from 'svelte/store';

  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    ConnectionLineType,
  } from '@xyflow/svelte';
  import * as Dialog from "$lib/components/ui/dialog";
  import * as Resizable from "$lib/components/ui/resizable";
  import { Button } from "$lib/components/ui/button";
  import { Label } from "$lib/components/ui/label";
  import { Input } from "$lib/components/ui/input";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import * as Sheet from "$lib/components/ui/sheet";
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

    if (jobDetail != null) {
      modalData = jobDetail;
      showModal = true;
    }
  }

</script>
 
<!--
👇 By default, the Svelte Flow container has a height of 100%.
This means that the parent container needs a height to render the flow.
-->
<!-- <div style:height="50vh"> -->
  <fragment>
    <Sheet.Root bind:open={showModal} >
      <Sheet.Content class="overflow-auto">
        <Sheet.Header>
          <Sheet.Title>{modalData?.job}</Sheet.Title>
          <Sheet.Description>
            <Accordion.Root>
              <Accordion.Item value="item-1">
                <Accordion.Trigger>Job Description</Accordion.Trigger>
                <Accordion.Content>
                  {modalData?.job_description}
                </Accordion.Content>
              </Accordion.Item>
            </Accordion.Root>
          </Sheet.Description>
        </Sheet.Header>
        <!-- <div class="max-h-[60vh] overflow-y-auto"> -->
          <div class="grid grid-cols-2 gap-4 py-4">
              <Label class="font-bold text-left">Salary:</Label>
              <p>{modalData?.min_salary ?? "Unknown"} - {modalData?.max_salary ?? "Unknown"} Baht</p>
              
              <Label class="font-bold text-left">Experience:</Label>
              <p>{modalData?.min_exp ?? "Unknown"} - {modalData?.max_exp ?? "Unknown"} year(s)</p>
        
              <Label class="font-bold text-left">Level:</Label>
              <p>{modalData?.level ?? "Unknown"}</p>
        
              <Label class="font-bold text-left">Category:</Label>
              <p>{modalData?.category ?? "Unknown"}</p>
        
              <Label class="font-bold text-left">Specialized Knowledge:</Label>
              <p class="break-words overflow-wrap-anywhere">{modalData?.hard_skill?.join(', ') ?? "Unknown"}</p>
        
              <Label class="font-bold text-left">Soft Skills:</Label>
              <p class="break-words overflow-wrap-anywhere">{modalData?.soft_skill?.join(', ') ?? "Unknown"}</p>
        
              <Label class="font-bold text-left">Matching Interests:</Label>
              <p class="break-words overflow-wrap-anywhere">{modalData?.interest?.join(', ') ?? "Unknown"}</p>
        
              <Label class="font-bold text-left">Education:</Label>
              <p class="break-words overflow-wrap-anywhere">{modalData?.education?.join(', ') ?? "Unknown"}</p>
          </div>
        <!-- </div> -->
        <!-- <Sheet.Footer>
          <Button type="submit" on:click={() => showModal = false}>Close</Button>
        </Sheet.Footer> -->
      </Sheet.Content>
    </Sheet.Root>

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