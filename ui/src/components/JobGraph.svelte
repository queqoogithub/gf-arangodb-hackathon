<script>
  import { onMount } from 'svelte';
  import ForceGraph from '../lib/ForceGraph.svelte';
  import BaseGraph from '../lib/BaseGraph.svelte';

  let nlQuery = '';
  let isLoading = false;
  let graphData = { nodes: [], edges: [] };
  /**
 * @type {Error|null} error - Holds the error object if an error occurs, otherwise null.
 */
  let error = null;

  async function generateJobGraph() {
    if (!nlQuery.trim()) {
      error = new Error("Please enter a natural language query");
      return;
    }
    
    error = null;
    isLoading = true;
    
    try {
      const response = await fetch('/api/job_graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ queries: [nlQuery] })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate job graph');
      }
      
      graphData = await response.json();
      
    } catch (err) {
      error = (err instanceof Error) ? err : new Error('An unknown error occurred');
      console.error('Error generating job graph:', err);
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="h-full bg-white-100 p-10">
  <!-- <h2 class="text-xl font-bold text-blue-500 mb-4">Jobs Graph</h2> -->
  
  <section class="p-4 rounded-md">
    <!-- <h3 class="text-center text-gray-700 mb-2">NLQ &lt;input&gt;</h3> -->
    <h2 class="text-center font-medium text-stone-700 mb-2">Tell us what you're interested in</h2>
    <div class="flex gap-2">
      <textarea 
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border min-h-fit rounded-md text-stone-800 placeholder-stone-300"
      ></textarea>
      <!-- <input
        type="text"
        bind:value={nlQuery}
        placeholder="I like to paint and I know how to code"
        class="flex-grow p-2 border rounded-md text-stone-800 placeholder-stone-300"
      /> -->
      <button 
        on:click={generateJobGraph}
        disabled={isLoading}
        class="bg-lime-600 text-stone-50 px-4 py-2 rounded-md hover:bg-lime-700 disabled:bg-stone-400"
      >
        {isLoading ? 'Loading...' : 'Generate'}
      </button>
    </div>
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </section>
  
  <section class="graph-section h-full p-4 rounded-md">
    <!-- <h3 class="text-center text-gray-700">JOBS GRAPH &lt;output&gt;</h3> -->
    <h3 class="text-center font-medium text-stone-700 mb-2">Job Matches Based on Your Interests & Skills</h3>
    <div class="graph-container h-full outline-2 outline-red-600 bg-stone-100 rounded-md border">
        <BaseGraph />
      <!-- {#if graphData.nodes.length > 0}
        <ForceGraph {graphData} />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter a query and click Generate to see the job graph
        </div>
      {/if} -->
    </div>
  </section>
</main>