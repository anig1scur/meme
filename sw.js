if(!self.define){let s,e={};const i=(i,l)=>(i=new URL(i+".js",l).href,e[i]||new Promise((e=>{if("document"in self){const s=document.createElement("script");s.src=i,s.onload=e,document.head.appendChild(s)}else s=i,importScripts(i),e()})).then((()=>{let s=e[i];if(!s)throw new Error(`Module ${i} didn’t register its module`);return s})));self.define=(l,n)=>{const t=s||("document"in self?document.currentScript.src:"")||location.href;if(e[t])return;let r={};const o=s=>i(s,t),u={module:{uri:t},exports:r,require:o};e[t]=Promise.all(l.map((s=>u[s]||o(s)))).then((s=>(n(...s),r)))}}define(["./workbox-4723e66c"],(function(s){"use strict";self.addEventListener("message",(s=>{s.data&&"SKIP_WAITING"===s.data.type&&self.skipWaiting()})),s.precacheAndRoute([{url:"assets/contagious.svg",revision:null},{url:"assets/index-Bui5HT_l.css",revision:null},{url:"assets/index-C5xAlY7X.js",revision:null},{url:"assets/intertextuality.svg",revision:null},{url:"assets/participatory.svg",revision:null},{url:"assets/relatable.svg",revision:null},{url:"assets/selfreplicating.svg",revision:null},{url:"assets/symbolic.svg",revision:null},{url:"manifest.webmanifest",revision:"a48910bf79831c7dc163aff1ef7e21fa"}],{}),s.cleanupOutdatedCaches(),s.registerRoute(new s.NavigationRoute(s.createHandlerBoundToURL("index.html")))}));
