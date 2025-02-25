<script>
  import {spring} from 'svelte/motion';
  import Card from '../Card.svelte';

  export let cx = 0;
  export let cy = 0;
  export let r;
  export let fill;
  export let year;
  export let origin;
  export let data;

  let isRect = false;

  let springConfig = {stiffness: 0.1, damping: 0.7};
  let offsetX = spring(0, springConfig);
  let offsetY = spring(0, springConfig);

  let radius = spring(r, springConfig);
  let width = spring(2 * r, springConfig);
  let height = spring(2 * r, springConfig);
  let cornerRadius = spring(r, springConfig);

  let fillColor = fill;

  let parentWidth = 0;
  let parentHeight = 0;

  function updateParentSize() {
    const svg = document.querySelector('svg');
    if (svg) {
      parentWidth = svg.clientWidth || svg.viewBox.baseVal.width;
      parentHeight = svg.clientHeight || svg.viewBox.baseVal.height;
    }
  }

  function toggleShape(event) {
    isRect = !isRect;

    updateParentSize();

    const targetGroup = event.currentTarget;
    targetGroup.parentNode.appendChild(targetGroup);

    if (isRect) {
      radius.set(0);
      cornerRadius.set(10);

      setTimeout(() => {
        width.set(540);
        height.set(540);
        fillColor = '#E4E2DC';

        const newX = parentWidth / 2.5 - cx;
        const newY = parentHeight / 2 - cy - 30;

        offsetX.set(newX);
        offsetY.set(newY);
      }, 100);
    } else {
      width.set(2 * r);
      height.set(2 * r);
      cornerRadius.set(r);

      offsetX.set(0);
      offsetY.set(0);

      setTimeout(() => {
        radius.set(r);
        fillColor = fill;
      }, 100);
    }
  }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions (because of reasons) -->
<g
  on:click={toggleShape}
  class="cursor-zoom-in stroke-black stroke-[1.5px]"
  transform="translate({$offsetX}, {$offsetY})"
>
  <g>
    <rect
      x={cx - $width / 2}
      y={cy - $height / 2}
      width={$width}
      height={$height}
      {fill}
      rx={$cornerRadius}
      style="transition: fill 0.3s ease; fill: {fillColor}"
    />
    {#if isRect}
      <foreignObject
        class="flex"
        x={cx - $width / 2}
        y={cy - $height / 2}
        width={$width}
        height={$height}
      >
        <div
          class="cursor-zoom-out w-full h-[95%] flex flex-col overflow-auto items-center pt-4 text-white opacity-0 animate-fade-in"
        >
          {#each data as meme}
            <Card {...meme} />
          {/each}
        </div>
        <div class="w-full flex justify-center mt-1 text-sm font-icon">
          {Number(year) ? year.toPrecision(4) : year} | {origin}
        </div>
      </foreignObject>
    {/if}
  </g>
</g>

<style>
  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .animate-fade-in {
    animation: fade-in 0.3s ease-in forwards;
    animation-delay: 0.1s;
  }
</style>
