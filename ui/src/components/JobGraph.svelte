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

<div class="job-graph-container">
  <h2 class="text-xl font-bold text-blue-500 mb-4">Jobs Graph</h2>
  
  <div class="input-section bg-gray-100 p-4 rounded-md mb-4">
    <h3 class="text-center text-gray-700 mb-2">NLQ &lt;input&gt;</h3>
    <div class="flex gap-2">
      <input
        type="text"
        bind:value={nlQuery}
        placeholder="Enter natural language query (e.g., 'Jobs similar to data scientist')"
        class="flex-grow p-2 border rounded-md"
      />
      <button 
        on:click={generateJobGraph}
        disabled={isLoading}
        class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:bg-gray-400"
      >
        {isLoading ? 'Loading...' : 'Generate'}
      </button>
    </div>
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </div>
  
  <div class="graph-section bg-gray-100 p-4 rounded-md">
    <h3 class="text-center text-gray-700 mb-2">JOBS GRAPH &lt;output&gt;</h3>
    <div class="graph-container h-64 bg-white rounded-md border border-gray-200">
        <BaseGraph />
      {#if graphData.nodes.length > 0}
        <ForceGraph {graphData} />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter a query and click Generate to see the job graph
        </div>
      {/if}
    </div>
  </div>
</div>