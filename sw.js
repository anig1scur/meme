if(!self.define){let s,e={};const i=(i,n)=>(i=new URL(i+".js",n).href,e[i]||new Promise((e=>{if("document"in self){const s=document.createElement("script");s.src=i,s.onload=e,document.head.appendChild(s)}else s=i,importScripts(i),e()})).then((()=>{let s=e[i];if(!s)throw new Error(`Module ${i} didn’t register its module`);return s})));self.define=(n,l)=>{const t=s||("document"in self?document.currentScript.src:"")||location.href;if(e[t])return;let r={};const o=s=>i(s,t),u={module:{uri:t},exports:r,require:o};e[t]=Promise.all(n.map((s=>u[s]||o(s)))).then((s=>(l(...s),r)))}}define(["./workbox-4723e66c"],(function(s){"use strict";self.addEventListener("message",(s=>{s.data&&"SKIP_WAITING"===s.data.type&&self.skipWaiting()})),s.precacheAndRoute([{url:"assets/contagious.svg",revision:null},{url:"assets/index-DdBIxqEj.js",revision:null},{url:"assets/index-DJO3gYvj.css",revision:null},{url:"assets/intertextuality.svg",revision:null},{url:"assets/participatory.svg",revision:null},{url:"assets/relatable.svg",revision:null},{url:"assets/selfreplicating.svg",revision:null},{url:"assets/symbolic.svg",revision:null},{url:"manifest.webmanifest",revision:"a48910bf79831c7dc163aff1ef7e21fa"}],{}),s.cleanupOutdatedCaches(),s.registerRoute(new s.NavigationRoute(s.createHandlerBoundToURL("index.html")))}));
