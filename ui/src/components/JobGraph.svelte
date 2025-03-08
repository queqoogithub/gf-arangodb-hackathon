<!-- <script lang="ts" context="module">
  import { z } from "zod";

  export const formSchema = z.object({
    nlq: z.string().nonempty()
  });
  export type FormSchema = typeof formSchema;
</script> -->

<script lang="ts">
  import { onMount } from 'svelte';
  import ForceGraph from '../lib/ForceGraph.svelte';
  import BaseGraph from '../lib/BaseGraph.svelte';
  import { Textarea } from "$lib/components/ui/textarea";
  import { type Node, type Edge } from '@xyflow/svelte';
  import { writable } from 'svelte/store';
  import type { JobGraphResponse, APINode } from '../types';
  import Label from '../lib/components/ui/label/label.svelte';
  import Button from '../lib/components/ui/button/button.svelte';
  import Input from '../lib/components/ui/input/input.svelte';
  // import { superForm, type Infer, type SuperValidated } from 'sveltekit-superforms';
  // import LoaderCircle from "lucide-svelte/icons/loader-circle";
  // import { LoaderCircle } from '@lucide/svelte';


  const xPosInterval = 200;
  const yPosInterval = 200;

  let nlQuery = '';
  let isLoading = false;

  let graphData: JobGraphResponse;
  let nodes= writable<Node[]>([]);
  let edges = writable<Edge[]>([]);
  // let jobDetails: {[key: string]: APINode} = {};
  // let jobDetails: {[key: string]: APINode} = $state({});
  let jobDetails = writable<{[key: string]: APINode}>({});
  let error: Error | null = null;

  async function generateJobGraph() {
    if (!nlQuery.trim()) {
      error = new Error("Please enter a natural language query");
      return;
    }
    
    nodes.set([]);
    edges.set([]);
    jobDetails.set({});
    // jobDetails = {};

    error = null;
    isLoading = true;
    
    try {
      const response = await fetch('https://go-soft-hack-api-10-343673271091.us-central1.run.app/gen_graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: nlQuery })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate job graph');
      }
      
      graphData = await response.json();

      const { mappedNodes, mappedEdges, mappedJobDetails } = mapAPINodesToNodesAndEdges(graphData)

      // Additional start position that is not a job node
      mappedNodes.push({
        id:   "start-node",
        type: 'input',
        data: {label: 'start'},
        position: {x: xPosInterval*2, y: 0},
      });

      nodes.set(mappedNodes);
      edges.set(mappedEdges);
      jobDetails.set(mappedJobDetails);
      // jobDetails = mappedJobDetails;

    } catch (err) {
      error = (err instanceof Error) ? err : new Error('An unknown error occurred');
      console.error('Error generating job graph:', err);
    } finally {
      isLoading = false;
    }
  }

  // Node
  // {
  //     id: '1',
  //     type: 'input',
  //     data: { label: 'Start' },
  //     position: { x: 200, y: 0 }
  //   },

  // Edge
  // {
  //     id: '1-2',
  //     source: '1',
  //     target: '2',
  //   },

  function mapAPINodesToNodesAndEdges(response: JobGraphResponse): {mappedNodes: Node[], mappedEdges: Edge[], mappedJobDetails: {[key: string]: APINode}} {
    const mappedNodes: Node[] = [];
    const mappedEdges: Edge[] = [];
    // const mappedJobDetails: APINode[] = [];
    const mappedJobDetails: {[key: string]: APINode} = {};

    response?.nodes?.forEach((node, i) => {
      // First layer of nodes
      mappedNodes.push({
        id:   node.job, // current data set has unique job name, so it can be an id for now
        // type: 'input',
        data: {label: node.job},
        position: {x: i * (xPosInterval * 2), y: yPosInterval},
      });

      mappedEdges.push({
        id: `start-node-${node.job}`,
        source: 'start-node',
        target: node.job,
      });

      mappedJobDetails[node.job] = node;
      // mappedJobDetails.push(node);

      // Since there will only be maximum 2 layers, no need for recursion here.
      // 2nd layer of nodes
      node?.children?.forEach((child, j) => {
        mappedNodes.push({
          id:   child.job,
          type: 'output',
          data: {label: child.job},
          position: {x: (i * xPosInterval * 2 + (j * xPosInterval)), y: yPosInterval * 2},
        });

        mappedEdges.push({
          id: `${node.job}-${child.job}`,
          source: node.job,
          target: child.job,
        });

        // mappedJobDetails.push(node);
        mappedJobDetails[child.job] = child;
      });
    });

    // for (let i = 0; i < response?.nodes.length; i++) {
    //   const node = response?.nodes[i];

    //   // First layer of nodes
    //   nodes.push({
    //     id:   node.job, // current data set has unique job name, so it can be an id for now
    //     type: 'input',
    //     data: {label: node.job},
    //     position: {x: 0, y: 0},
    //   });

    //   // Since there will only be maximum 2 layers, no need for recursion here.
    //   // 2nd layer of nodes
    //   for (const child of node.children) {
    //     nodes.push({
    //       id:   child.job,
    //       type: 'input',
    //       data: {label: child.job},
    //       position: {x: 0, y: 0},
    //     });
    //   }
    // }

    return {mappedNodes, mappedEdges, mappedJobDetails};
  }

  // import { zodClient } from "sveltekit-superforms/adapters";

  // let data: SuperValidated<Infer<FormSchema>>;
  // export { data as form};
  // const form = superForm(data, {
  //   validators: zodClient(formSchema),
  //   onUpdate: ({form: f}) => {
  //     if (f.valid) {

  //     } else {

  //     }
  //   }
  // })

  // const { form: formData, enhance}  = form;
</script>

<!-- <main class="min-h-full bg-stone-100 p-8"> -->
<main class="min-h-full bg-background p-8">
  <!-- <h2 class="text-xl font-bold text-blue-500 mb-4">Jobs Graph</h2> -->
  
  <section class="min-h-full rounded-md mb-8">
    <!-- <form on:submit={generateJobGraph}>
      <Label for="job-graph-query">What Are You Passionate About?</Label>
      <div class="flex w-full items-center space-x-2">
        <Input 
        id="job-graph-query"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
        />
        <Button
          onclick={generateJobGraph}
          disabled={isLoading}
          class="bg-lime-600 text-stone-50 px-4 py-2 rounded-md hover:bg-lime-700 disabled:bg-stone-400"
        >
          {isLoading ? 'Loading...' : 'Explore'}
        </Button>
      </div>
    </form> -->

    <form on:submit={generateJobGraph}>
      <!-- <Label for="job-graph-query">What Are You Passionate About?</Label> -->
      <h2 class="text-center font-medium text-stone-700 mb-2">What Are You Passionate About?</h2>
      <div class="flex w-full items-center space-x-2">
        <Input 
        id="job-graph-query"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
        />
        <Button
          onclick={generateJobGraph}
          disabled={isLoading}
          class="bg-lime-600 text-stone-50 px-4 py-2 rounded-md hover:bg-lime-700 disabled:bg-stone-400"
        >
          {isLoading ? 'Loading...' : 'Explore'}
        </Button>
      </div>
    </form>


    <!-- <form action="" method="POST" use:enhance> -->
      <!-- <Form.Control let:attrs>
        <Form.Label for="job-graph-query">What Are You Passionate About?</Form.Label>
        <Input 
          {...attrs}
          bind:value={$formData.nlq}
        />
        <Form.FieldErrors /> -->
        <!-- <Label for="job-graph-query">What Are You Passionate About?</Label>
        <Input 
          id="job-graph-query"
          bind:value={nlQuery}
          placeholder="I like to paint and I know how to code"
          class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
        /> -->
      <!-- </Form.Control>
      <Form.Button
        onclick={generateJobGraph}
        disabled={isLoading}
      >
        Explore
      </Form.Button> -->

      <!-- <Textarea
        id="job-graph-textarea"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
      /> -->
      <!-- <Button         
        onclick={generateJobGraph}
        disabled={isLoading}
      >
        Explore
      </Button>
      {#if error}
        <p class="text-muted-foreground text-sm">
          {error}
        </p>
      {/if} -->
    <!-- </form> -->


    <!-- <h2 class="text-center font-medium text-stone-700 mb-2">What Are You Passionate About?</h2> -->
    <!-- <div class="flex gap-2"> -->

      <!-- <Label>What Are You Passionate About?</Label> -->
      <!-- <Textarea
        id="job-graph-textarea"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
      /> -->
      <!-- <textarea
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
      ></textarea> -->
      <!-- <input
        type="text"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border rounded-md text-stone-800 placeholder-stone-300"
      /> -->
      <!-- <button 
        onclick={generateJobGraph}
        disabled={isLoading}
        class="bg-lime-600 text-stone-50 px-4 py-2 rounded-md hover:bg-lime-700 disabled:bg-stone-400"
      >
        {isLoading ? 'Loading...' : 'Explore'}
      </button> -->
    <!-- </div> -->
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </section>
  
  <section class="h-[70vh] rounded-md">
    <!-- <h3 class="text-center text-gray-700">JOBS GRAPH &lt;output&gt;</h3> -->
    <h3 class="text-center font-medium text-stone-700 mb-2">Job Trends Tailored for You</h3>
    <!-- <div class="graph-container min-h-[75vh] outline-2 outline-red-600 bg-stone-100 rounded-md border"> -->
    <BaseGraph {nodes} {edges} {jobDetails} />


      <!-- {#if graphData.nodes.length > 0}
        <ForceGraph {graphData} />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter a query and click Generate to see the job graph
        </div>
      {/if} -->
    <!-- </div> -->
  </section>
</main>
