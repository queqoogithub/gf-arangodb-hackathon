<script>
  import { onMount } from 'svelte';
  import * as Tabs from "$lib/components/ui/tabs";
  import JobGraph from '../components/JobGraph.svelte';
  import SkillGraph from '../components/SkillGraph.svelte';

  let activeTab = 'jobs'; // Default tab

/**
 * Sets the active tab for the navigation.
 * @param {string} tab - The identifier of the tab to be set as active.
 */
  function setActiveTab(tab) {
    activeTab = tab;
  }

  const jobTab = "Visualize Careers";
  const chatTab = "Career Chat";
</script>

<!-- <main class="mx-auto h-full">
  <JobGraph /> -->
<!-- <main class="container mx-auto h-full">  -->
<main class="mx-auto h-full"> 
  <JobGraph />
  <!-- <header class="border-border/40 bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur">
    <div class="container flex h-14 max-w-screen-2xl items-center">
      <nav class="flex items-center gap-6 text-sm">
        <a href="/" class="hover:text-foreground/80 transition-colors text-foreground/60">
          {jobTab}
        </a>
        <a href="/chat" class="hover:text-foreground/80 transition-colors text-foreground/60">
          {chatTab}
        </a>
      </nav>
    </div>
  </header> -->
    <!-- <Tabs.Root value="jobs" class="space-y-4">
      <Tabs.List>
        <Tabs.Trigger value="jobs">{jobTab}</Tabs.Trigger>
        <Tabs.Trigger value="skills">{chatTab}</Tabs.Trigger>
      </Tabs.List>
      <Tabs.Content value="jobs">
        <JobGraph />
      </Tabs.Content>
      <Tabs.Content value="skills">
        <SkillGraph />
      </Tabs.Content>
    </Tabs.Root> -->

  
  <!-- <nav class="tabs mb-4">
    <button 
      class="tab-button {activeTab === 'jobs' ? 'active' : ''}" 
      on:click={() => setActiveTab('jobs')}
    >
      Visualize Careers
    </button>
    <button 
      class="tab-button {activeTab === 'skills' ? 'active' : ''}" 
      on:click={() => setActiveTab('skills')}
    >
      Career Chat
    </button>
  </nav>

  <div class="tab-content"> 
    {#if activeTab === 'jobs'}
      <JobGraph />
    {:else}
      <SkillGraph />
    {/if}
  </div>  -->
</main>

<style>
  .tabs {
    display: flex;
    gap: 1rem;
    border-bottom: 1px solid #ccc;
  }
  
  .tab-button {
    padding: 0.5rem 1rem;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
  }
  
  .tab-button.active {
    border-bottom: 3px solid #4299e1;
    color: #4299e1;
    font-weight: bold;
  }

  .tab-content {
    margin-top: 1rem;
  }
</style>
