<script>
  import { page } from '$app/state';
  import "../app.css";
  import { buttonVariants } from "$lib/components/ui/button";

  const jobTabText = "Visualize Careers";
  const chatTabText = "Career Chat";

  let { children } = $props();
</script>

<!-- <slot></slot> -->
<header class="border-border/40 bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur shadow-sm">
  <div class="container flex h-14 max-w-screen-2xl items-center">
    <nav class="flex gap-4 items-center">
      <a 
        href="/" 
        class={
          // buttonVariants({ variant: "ghost" }) + 
          " text-base over:text-foreground/80 transition-colors text-foreground/60 "
        }
        class:font-bold={page.url.pathname === "/"}
        class:text-foreground={page.url.pathname === "/"}
      >
        {jobTabText}
      </a>
      <a 
        href="/chat" 
        class={
        // buttonVariants({ variant: "ghost" }) + 
        " text-base hover:text-foreground/80 transition-colors text-foreground/60"}
        class:font-bold={page.url.pathname === "/chat"}
        class:text-foreground={page.url.pathname === "/chat"}
      >
        {chatTabText}
      </a>
    </nav>
  </div>
</header>
<main class="md:px-6">
  {@render children()}
</main>

