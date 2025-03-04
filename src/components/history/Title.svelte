<script>
  export let text = 'The Selfish Gene';
  export let className = 'title';
</script>

<h1 class={`text-4xl font-bold text-[#713f125a] flex space-x-3 items-end ${className}`}>
  {#each text.toUpperCase().split(' ') as word}
    <span class="flex items-end">
      <span class="text-7xl stroke">{word[0]}</span>
      <span class="text-5xl mb-[4px] stroke">{word.slice(1)}</span>
    </span>
  {/each}
</h1>

<style>
  .stroke {
    -webkit-text-stroke: 1.5px #713f12;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
  }
</style>
