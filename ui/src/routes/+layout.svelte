<script>
  import { page } from '$app/state';
  import "../app.css";

  const jobTab = "Visualize Careers";
  const chatTab = "Career Chat";

  let { children } = $props();
</script>

<!-- <slot></slot> -->
<header class="border-border/40 bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur">
  <div class="container flex h-14 max-w-screen-2xl items-center">
    <nav class="flex items-center gap-6 text-sm">
      <a 
        href="/" 
        class="hover:text-foreground/80 transition-colors text-foreground/60"
        class:font-bold={page.url.pathname === "/"}
        class:text-foreground={page.url.pathname === "/"}
      >
        {jobTab}
      </a>
      <a 
        href="/chat" 
        class="hover:text-foreground/80 transition-colors text-foreground/60"
        class:font-bold={page.url.pathname === "/chat"}
        class:text-foreground={page.url.pathname === "/chat"}
      >
        {chatTab}
      </a>
    </nav>
  </div>
</header>
<main class="px-6">
  {@render children()}
</main>

