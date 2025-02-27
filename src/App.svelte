<script lang="ts">
  import Home from './routes/Home.svelte';
  import Gallery from './routes/Gallery.svelte';
  import Random from './routes/Random.svelte';
  import Meme from './routes/Meme.svelte';
  import Visualization from './routes/Visualization.svelte';
  import NoMatch from './components/NoMatch.svelte';
  import {Router, Route} from 'svelte-routing';

  export let url: string = '';
</script>

<svelte:head>
  {#if import.meta.env.PROD}
    <script
      defer
      data-domain={document.location.host}
      src="https://plausible.joincommunity.xyz/js/script.js"
    ></script>
  {/if}
</svelte:head>

<Router {url}>
  <main class="select-none">
    <Route
      path="/"
      component={Home}
    />
    <Route
      path="/gallery"
      component={Gallery}
    />
    <Route
      path="/random"
      component={Random}
    />
    <Route
      path="/meme"
      component={Meme}
    />
    <Route
      path="/visualization"
      component={Visualization}
    />
    <Route
      path="*"
      component={NoMatch}
    />
  </main>
</Router>
