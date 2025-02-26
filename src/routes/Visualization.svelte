<script lang="js">
  import Header from '../components/Header.svelte';
  import Footer from '../components/Footer.svelte';
  import YearAndOrigin from '../components/visualization/YearAndOrigin.svelte';
  import Trending from '../components/visualization/Trending.svelte';
  import Sentiment from '../components/visualization/Sentiment.svelte';
</script>

<Header />
<div class="mt-24 flex items-center justify-center min-h-screen flex-col">
  <YearAndOrigin />
  <Trending />
  <Sentiment />
</div>
<Footer />
