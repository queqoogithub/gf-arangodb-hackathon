import { sveltekit } from '@sveltejs/kit/vite';

import { defineConfig } from 'vite';
 
export default defineConfig({

    plugins: [sveltekit()],

    server: {

        // Allow all hosts

        allowedHosts: true

    }

});