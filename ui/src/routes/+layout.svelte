<script>
  import { page } from '$app/state';
  import '../app.css';
  import { buttonVariants } from '$lib/components/ui/button';

  const jobTabText = 'Visualize Careers';
  const chatTabText = 'Career Chat';
  const appName = 'Hidden Paths';

  let { children } = $props();
</script>

<!-- <slot></slot> -->
<main class="flex flex-col min-h-screen bg-stone-50">
  <nav class="bg-green-600 py-4 sticky top-0 w-full shadow-md">
    <div class="container max-w-5xl mx-auto flex justify-between items-center">
      <a
        href="/"
        class="font-bold text-white rounded-md py-2 px-4 bg-stone-700 hover:bg-stone-600"
      >
        ✨ {appName}
      </a>

      <div class="text-right">
        <nav class="flex gap-4 items-center">
          <a
            href="/"
            class={buttonVariants({ variant: 'ghost' }) +
              ' hover:text-stone-800/70 transition-colors text-stone-50 '}
            class:font-bold={page.url.pathname === '/'}
            class:text-foreground={page.url.pathname === '/'}
            class:text-stone-100={page.url.pathname === '/'}
          >
            <b>{jobTabText}</b>
          </a>
          <a
            href="/chat"
            class={buttonVariants({ variant: 'ghost' }) +
              ' hover:text-stone-800/70 transition-colors text-stone-50'}
            class:font-bold={page.url.pathname === '/chat'}
            class:text-foreground={page.url.pathname === '/chat'}
            class:text-stone-100={page.url.pathname === '/chat'}
          >
            <b>{chatTabText}</b>
          </a>
        </nav>
      </div>
    </div>
  </nav>

  <main class="md:px-6 flex-grow">
    {@render children()}
  </main>

  <footer
    class="bg-stone-700 py-6 text-center text-stone-500 border-border/40 w-full border-b backdrop-blur shadow-md"
  >
    <nav class="mb-2">
      <a
        href="https://github.com/queqoogithub/gf-arangodb-hackathon"
        class="hover:text-green-500 text-stone-50 px-4">GitHub</a
      >
      <a
        href="https://www.youtube.com/watch?v=e6U7orYysY0"
        class="hover:text-green-500 text-stone-50 px-4">Youtube</a
      >
      <a
        href="https://arangodbhackathon.devpost.com/"
        class="hover:text-green-500 text-stone-50 px-4">Hackathon</a
      >
    </nav>
    <p class="text-stone-50">&copy; 2025 {appName}</p>
  </footer>
</main>
