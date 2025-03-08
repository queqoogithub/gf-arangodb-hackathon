<script lang="ts">
  import { marked } from 'marked';
  let jobName = '';
  let isLoading = false;
  let responseText = '';
  $: formattedResponse = responseText ? marked(responseText) : '';
  let error: Error | null = null;

  async function generateResponse() {
    if (!jobName.trim()) {
      error = new Error("Please enter your job interests and skills");
      return;
    }
    
    error = null;
    isLoading = true;
    responseText = '';
    
    try {
      const chatResponse = await fetch('https://go-soft-hack-api-10-343673271091.us-central1.run.app/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: jobName })
      });
      
      if (!chatResponse.ok) {
        throw new Error('Failed to generate response');
      }
      
      const { response } = await chatResponse.json();
      responseText = response;
      
    } catch (err) {
      error = err instanceof Error ? err : new Error('An unknown error occurred');
      console.error('Error generating skill graph:', err);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="skill-graph-container">
  <h2 class="text-xl font-bold text-orange-500 mb-4">🔮 Tell us more to foresee your inner talent</h2>
  
  <div class="input-section bg-gray-100 p-4 rounded-md mb-4">
    <h3 class="text-center text-gray-700 mb-2">Share your skills, job experience, and passions</h3>
    <div class="flex gap-2">
      <input
        type="text"
        bind:value={jobName}
        placeholder="Describe your job interests and skills (e.g., I'm interested in data science and know Python)"
        class="flex-grow p-2 border rounded-md"
      />
      <button 
        on:click={generateResponse}
        disabled={isLoading}
        class="bg-orange-500 text-white px-4 py-2 rounded-md hover:bg-orange-600 disabled:bg-gray-400"
      >
        {isLoading ? 'Loading...' : 'Explore'}
      </button>
    </div>
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </div>
  
  <div class="response-section bg-gray-100 p-4 rounded-md">
    <h3 class="text-center text-gray-700 mb-2">Career Opportunity Insights</h3>
    <div class="response-container min-h-[8rem] p-4 bg-white rounded-md border border-gray-200">
      {#if formattedResponse}
        <div class="text-gray-700 prose prose-orange prose-sm max-w-none">{@html formattedResponse}</div>
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter your job interests and skills, then click Explore to see the analysis
        </div>
      {/if}
    </div>
  </div>
</div>
