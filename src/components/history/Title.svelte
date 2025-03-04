<script>
  export let text = "The Selfish Gene";
  export let className = "title";
</script>

<h1 class={`text-4xl font-bold text-brown-800 flex space-x-3 items-end ${className}`}>
  {#each text.toUpperCase().split(" ") as word}
    <span class="flex items-end">
      <span class="text-6xl ">{word[0]}</span>
      <span class="text-4xl mb-[2px]">{word.slice(1)}</span>
    </span>
  {/each}
</h1>
