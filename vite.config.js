import path from "path"
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
  resolve: {
    alias: {
      $assets: path.resolve(__dirname, 'src/assets'),
    }
  },
  esbuild: {
    drop: ['console', 'debugger'],
  },
  build: {
    minify: "esbuild",
    chunkSizeWarningLimit: 800,
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (/\.(png|jpe?g|gif|svg|webp|avif)$/.test(assetInfo.name)) {
            return 'assets/[name][extname]';
          }
          return 'assets/[name]-[hash][extname]';
        }
      }
    }
  }

})
