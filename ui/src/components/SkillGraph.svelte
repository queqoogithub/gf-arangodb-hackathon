<script>
  import { onMount } from 'svelte';
  import ForceGraph from '../lib/ForceGraph.svelte';

  let jobName = '';
  let isLoading = false;
  let graphData = { nodes: [], edges: [] };
/**
 * @type {Error|null} error - Holds the error object if an error occurs, otherwise null.
 */
  let error = null;

  async function generateSkillGraph() {
    if (!jobName.trim()) {
      error = new Error("Please enter a job name");
      return;
    }
    
    error = null;
    isLoading = true;
    
    try {
      const response = await fetch('/api/skill_graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify([jobName])
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate skill graph');
      }
      
      graphData = await response.json();
      
    } catch (err) {
      error = err instanceof Error ? err : new Error('An unknown error occurred');
      console.error('Error generating skill graph:', err);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="skill-graph-container">
  <h2 class="text-xl font-bold text-orange-500 mb-4">Skill Graph</h2>
  
  <div class="input-section bg-gray-100 p-4 rounded-md mb-4">
    <h3 class="text-center text-gray-700 mb-2">JOB &lt;input&gt;</h3>
    <div class="flex gap-2">
      <input
        type="text"
        bind:value={jobName}
        placeholder="Enter job title (e.g., 'Data Scientist')"
        class="flex-grow p-2 border rounded-md"
      />
      <button 
        on:click={generateSkillGraph}
        disabled={isLoading}
        class="bg-orange-500 text-white px-4 py-2 rounded-md hover:bg-orange-600 disabled:bg-gray-400"
      >
        {isLoading ? 'Loading...' : 'Generate'}
      </button>
    </div>
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </div>
  
  <div class="graph-section bg-gray-100 p-4 rounded-md">
    <h3 class="text-center text-gray-700 mb-2">SKILL GRAPH &lt;output&gt;</h3>
    <div class="graph-container h-64 bg-white rounded-md border border-gray-200">
      {#if graphData.nodes.length > 0}
        <ForceGraph {graphData} nodeColors={{skill1: "#f8d4ba", skill2: "#bdd8f1"}} />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter a job title and click Generate to see the skill graph
        </div>
      {/if}
    </div>
  </div>
</div>