import './app.css';
import App from './App.svelte';
import {mount} from 'svelte';

window.addEventListener('contextmenu', (e: MouseEvent) => {
  import.meta.env.PROD ? e.preventDefault() : void 0;
});

const app = mount(App, {
  target: document.body,
  props: {
    url: window.location.pathname,
  },
});

export default app;
