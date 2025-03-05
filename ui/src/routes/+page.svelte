<script>
  import { onMount } from 'svelte';
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
</script>

<main class="mx-auto h-full">
  <JobGraph />
<!-- <main class="container"> -->
  <!-- <nav class="tabs mb-4">
    <button 
      class="tab-button {activeTab === 'jobs' ? 'active' : ''}" 
      on:click={() => setActiveTab('jobs')}
    >
      Jobs Graph
    </button>
    <button 
      class="tab-button {activeTab === 'skills' ? 'active' : ''}" 
      on:click={() => setActiveTab('skills')}
    >
      Skill Graph
    </button>
  </nav> -->

  <!-- <div class="tab-content"> -->
    <!-- {#if activeTab === 'jobs'}
      <JobGraph />
    {:else}
      <SkillGraph />
    {/if} -->
  <!-- </div> -->
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