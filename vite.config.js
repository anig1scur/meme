import { defineConfig } from 'vite'

import { svelte } from '@sveltejs/vite-plugin-svelte'
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
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
  build: {
    minify: 'terser',
    chunkSizeWarningLimit: 800,
    terserOptions: {
      ecma: 5,
      compress: {
        unsafe: true,
        drop_console: true,
        booleans_as_integers: true
      },
      format: {
        ascii_only: true
      }
    }
  }
})
