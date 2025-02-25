<script>
  import data from '/public/meme_stats.json';
  import LineGraph from '../chart/Line.svelte';
</script>

<div class="mt-20">
  <LineGraph {data} />
</div>
