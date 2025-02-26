<script>
  export let gridType;
  export let scale;
  export let innerHeight;
  export let innerWidth;
  export let ticks;
</script>

{#if gridType == 'xGrid'}
  {#each ticks as tick}
    <line
      x1={scale(tick)}
      x2={scale(tick)}
      y1={0}
      y2={innerHeight}
      class="gridline"
    ></line>
    <text
      x={scale(tick)}
      y={innerHeight + 60}
      class="ticklabel x">{tick}</text
    >
  {/each}
{/if}

{#if gridType == 'yGrid'}
  {#each ticks as tick}
    <line
      x1={0}
      x2={innerWidth}
      y1={scale(tick)}
      y2={scale(tick)}
      class="gridline"
    ></line>
    <text
      x={-80}
      y={scale(tick) + 5}
      class="ticklabel">{tick}</text
    >
  {/each}
{/if}

<style>
  text.ticklabel {
    font-size: 11px;
    fill: #aaaaaa;
  }
  text.ticklabel.x {
    text-anchor: middle;
  }
</style>
