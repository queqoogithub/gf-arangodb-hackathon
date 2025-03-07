import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()]
  // server: {
  //   port: 8080
  // }
});

// export default defineConfig({
// 	plugins: [sveltekit()],
//   server: {
//     port:  5173,  // Use the PORT environment variable or default to 5173
// 		strictPort: true
//   }
// })
