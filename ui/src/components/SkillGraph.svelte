<script lang="ts">
  import { marked } from 'marked';
  import Button from '../lib/components/ui/button/button.svelte';
  import Input from '../lib/components/ui/input/input.svelte';
  // import Card from '../lib/components/ui/card/card.svelte';
  import * as Card from '$lib/components/ui/card';
  import Separator from '../lib/components/ui/separator/separator.svelte';

  let jobName = '';
  let isLoading = false;
  let responseText = '';
  $: formattedResponse = responseText ? marked(responseText) : '';
  let error: Error | null = null;

  async function generateResponse() {
    if (!jobName.trim()) {
      error = new Error('Please enter your job interests and skills');
      return;
    }

    error = null;
    isLoading = true;
    responseText = '';

    try {
      const chatResponse = await fetch(
        'https://go-soft-hack-api-10-343673271091.us-central1.run.app/chat',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query: jobName })
        }
      );

      if (!chatResponse.ok) {
        throw new Error('Failed to generate response');
      }

      const { response } = await chatResponse.json();
      responseText = response;
    } catch (err) {
      error =
        err instanceof Error ? err : new Error('An unknown error occurred');
      console.error('Error generating skill graph:', err);
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="skill-graph-container max-w-5xl mx-auto p-8 bg-white">
  <!-- <h2 class="text-xl font-bold text-green-500 mb-4">🔮 Tell us more to foresee your inner talent</h2> -->
  <!-- <Card.Root>
    <Card.Content> -->
  <section class="input-section rounded-md mb-12 max-w-3xl mx-auto">
    <!-- <h3 class="text-center font-medium text-gray-700 mb-2">Share your skills, job experience, and passions</h3> -->
    <h3 class="text-center font-medium text-2xl text-gray-700 mb-8">
      Welcome! 👋 I’m your career assistant.
    </h3>
    <article class="mb-6 text-sm text-gray-500">
      <p>
        <strong>Ask me anything</strong> about careers, skills, and job opportunities!
      </p>
      <Separator class="my-4" />
      <p class="pb-2">
        <strong>Here are some examples of what you can ask:</strong>
      </p>
      <ul class="pl-4 pb-2">
        <li class="mb-1">
          ✅ What jobs can I do with these skills: Python, data analysis,
          problem-solving?
        </li>
        <li class="mb-1">✅ What skills do I need to become an AI Engineer?</li>
        <li class="mb-1">
          ✅ I have a Bachelor in Computer Science. What careers are suitable
          for me?
        </li>
        <li class="mb-1">✅ I’m interested in Gaming. What are some career options?</li>
      </ul>
      <p>
        💡 Be specific! The more details you provide, the better recommendations
        I can give. 🚀
      </p>
    </article>

    <form class="flex gap-2" on:submit={generateResponse}>
      <Input
        type="text"
        bind:value={jobName}
        placeholder="Ask away"
        class="flex-grow p-2 border rounded-md bg-background"
      />
      <Button
        on:click={generateResponse}
        disabled={isLoading}
        class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 disabled:bg-gray-400"
      >
        {isLoading ? 'Loading...' : 'Explore'}
      </Button>
    </form>
    {#if error}
      <p class="text-red-500 mt-2">{error}</p>
    {/if}
  </section>

  <section class="response-section rounded-md max-w-3xl mx-auto">
    <h3 class="text-center text-xl font-medium text-gray-700 mb-4">
      Career Opportunity Insights
    </h3>
    <div
      class="response-container min-h-[8rem] p-4 bg-white rounded-md border border-gray-200"
    >
      {#if formattedResponse}
        <div
          class="text-gray-700 text-base prose prose-green prose-sm max-w-none"
        >
          {@html formattedResponse}
        </div>
      {:else}
        <div class="flex items-center justify-center h-full text-gray-400">
          Enter your job interests and skills, then click Explore to see the
          analysis
        </div>
      {/if}
    </div>
  </section>
  <!-- </Card.Content>
  </Card.Root> -->
</main>
