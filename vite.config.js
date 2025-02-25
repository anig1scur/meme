import { defineConfig } from 'vite'

import { svelte } from '@sveltejs/vite-plugin-svelte'
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  base: "/",
  plugins: [
    svelte(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: 'inline',
      workbox: {
        globPatterns: ['**/*.{js,css,svg,webp}'],
        cleanupOutdatedCaches: true
      },
      manifest: {
        "name": "woai.meme",
        "description": "meme lover",
        "start_url": "./",
        "theme_color": "#000000",
        "background_color": "#000000",
        "display": "standalone"
      }
    })
  ],
  esbuild: {
    drop: ['console', 'debugger'],
  },
  build: {
    minify: "esbuild",
    chunkSizeWarningLimit: 800,
  }
})
