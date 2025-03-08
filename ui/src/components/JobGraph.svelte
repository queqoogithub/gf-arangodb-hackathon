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
  import { Textarea } from '$lib/components/ui/textarea';
  import { type Node, type Edge } from '@xyflow/svelte';
  import { writable } from 'svelte/store';
  import type { JobGraphResponse, APINode } from '../types';
  import Button from '../lib/components/ui/button/button.svelte';
  import Input from '../lib/components/ui/input/input.svelte';
  import { Separator } from '$lib/components/ui/separator';

  const xPosInterval = 200;
  const yPosInterval = 200;

  let nlQuery = '';
  let isLoading = false;

  let graphData: JobGraphResponse;
  let nodes = writable<Node[]>([]);
  let edges = writable<Edge[]>([]);
  let jobDetails = writable<{ [key: string]: APINode }>({});
  let error: Error | null = null;

  async function generateJobGraph() {
    if (!nlQuery.trim()) {
      error = new Error('Please enter a natural language query');
      return;
    }

    nodes.set([]);
    edges.set([]);
    jobDetails.set({});
    // jobDetails = {};

    error = null;
    isLoading = true;

    try {
      const response = await fetch(
        'https://go-soft-hack-api-10-343673271091.us-central1.run.app/gen_graph',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query: nlQuery })
        }
      );

      if (!response.ok) {
        throw new Error('Failed to generate job graph');
      }

      graphData = await response.json();

      const { mappedNodes, mappedEdges, mappedJobDetails } =
        mapAPINodesToNodesAndEdges(graphData);

      // Additional start position that is not a job node
      mappedNodes.push({
        id: 'start-node',
        type: 'input',
        data: { label: 'start' },
        position: { x: xPosInterval * 2, y: 0 }
      });

      nodes.set(mappedNodes);
      edges.set(mappedEdges);
      jobDetails.set(mappedJobDetails);
      // jobDetails = mappedJobDetails;
    } catch (err) {
      error =
        err instanceof Error ? err : new Error('An unknown error occurred');
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

  function mapAPINodesToNodesAndEdges(response: JobGraphResponse): {
    mappedNodes: Node[];
    mappedEdges: Edge[];
    mappedJobDetails: { [key: string]: APINode };
  } {
    const mappedNodes: Node[] = [];
    const mappedEdges: Edge[] = [];
    // const mappedJobDetails: APINode[] = [];
    const mappedJobDetails: { [key: string]: APINode } = {};

    response?.nodes?.forEach((node, i) => {
      // First layer of nodes
      mappedNodes.push({
        id: node.job, // current data set has unique job name, so it can be an id for now
        // type: 'input',
        data: { label: node.job },
        position: { x: i * (xPosInterval * 2), y: yPosInterval }
      });

      mappedEdges.push({
        id: `start-node-${node.job}`,
        source: 'start-node',
        target: node.job
      });

      mappedJobDetails[node.job] = node;
      // mappedJobDetails.push(node);

      // Since there will only be maximum 2 layers, no need for recursion here.
      // 2nd layer of nodes
      node?.children?.forEach((child, j) => {
        mappedNodes.push({
          id: child.job,
          type: 'output',
          data: { label: child.job },
          position: {
            x: i * xPosInterval * 2 + j * xPosInterval,
            y: yPosInterval * 2
          }
        });

        mappedEdges.push({
          id: `${node.job}-${child.job}`,
          source: node.job,
          target: child.job
        });

        mappedJobDetails[child.job] = child;
      });
    });

    return { mappedNodes, mappedEdges, mappedJobDetails };
  }
</script>

<main class="min-h-full max-w-5xl bg-background p-8 mx-auto">
  <section class="min-h-full rounded-md mb-8 max-w-4xl mx-auto">
    <form on:submit={generateJobGraph}>
      <!-- <Label for="job-graph-query">What Are You Passionate About?</Label> -->
      <p class="text-center text-8xl mb-2">🧙🏼‍♂️</p>
      <h3 class="text-center text-2xl font-medium text-stone-700">
        Discover Unexpected Career Paths
      </h3>
      <h3 class="text-center text-xl font-medium text-stone-700 mb-8">
        with a Personalized Graph!
      </h3>
      <article class="mb-8 text-sm text-gray-500">
        <p class="mb-6">
          I’ll generate a career roadmap based on your skills, interests, and
          experience—but not just the usual jobs! 🎉
        </p>
        <Separator class="mb-4" />

        <p class="font-semibold text-base mb-4">👉 How it works:</p>
        <article class="pl-6 mb-6">
          <ol class="list-none list-inside space-y-2 mb-2">
            <li><strong>✅ Enter your details</strong></li>
            <ul class="list-disc list-inside ml-4">
              <li>
                <strong>Skills:</strong> (e.g., Python, graphic design, leadership)
              </li>
              <li>
                <strong>Interests:</strong> (e.g., AI, finance, healthcare)
              </li>
              <li>
                <strong>Education level:</strong> (e.g., Bachelor in Art, Highschool,
                PhD in Physics)
              </li>
            </ul>
            <li>
              <strong>✅ I match your skills to multiple career paths</strong>
            </li>
            <ul class="list-disc list-inside ml-4">
              <li>
                some may be traditional, while others could be unique but still
                use your strengths.
              </li>
            </ul>
            <li>
              <strong
                >✅ See how your skills can transfer across different
                industries!</strong
              >
            </li>
          </ol>
        </article>

        <p class="font-semibold mb-2">Example input:</p>
        <blockquote class="p-3 bg-gray-100 border-l-4 border-green-500">
          "I have skills in <strong>market analysis</strong> and
          <strong>problem solving</strong>. I’m interested in
          <strong>business development</strong>
          and
          <strong>sales</strong>. I have a
          <strong>Bachelor's in Retail Management.</strong>"
        </blockquote>
      </article>
      <!-- <h2 class="text-center font-medium text-stone-700 mb-2">with a Personalized Graph! 🚀</h2> -->

      <div class="flex w-full items-center space-x-2">
        <Input
          id="job-graph-query"
          bind:value={nlQuery}
          placeholder="Ask away"
          class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
        />
        <Button
          onclick={generateJobGraph}
          disabled={isLoading}
          class="bg-green-600 text-stone-50 px-4 py-2 rounded-md hover:bg-green-700 disabled:bg-stone-400"
        >
          {isLoading ? 'Loading...' : 'Explore'}
        </Button>
      </div>
    </form>
    {#if error}
      <p class="text-destructive text-sm mt-2">{error}</p>
    {/if}
  </section>

  <section class="h-[70vh] rounded-md max-w-4xl mx-auto">
    <h3 class="text-center font-medium text-xl text-stone-700 mb-2">
      Job Trends Tailored for You
    </h3>
    <BaseGraph {nodes} {edges} {jobDetails} />
  </section>
</main>
