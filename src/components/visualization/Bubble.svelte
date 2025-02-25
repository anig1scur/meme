<script>
  import {spring} from 'svelte/motion';

  export let cx = 0;
  export let cy = 0;
  export let r;
  export let fill;
  export let data;

  let isRect = false;

  let offsetX = spring(0, {stiffness: 0.1, damping: 0.7});
  let offsetY = spring(0, {stiffness: 0.1, damping: 0.7});

  let radius = spring(r, {stiffness: 0.1, damping: 0.7});
  let width = spring(2 * r, {stiffness: 0.1, damping: 0.7});
  let height = spring(2 * r, {stiffness: 0.1, damping: 0.7});
  let cornerRadius = spring(r, {stiffness: 0.1, damping: 0.7});

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
        width.set(400);
        height.set(540);

        const newX = parentWidth / 2 - cx;
        const newY = parentHeight / 2 - cy;

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
    />
    {#if isRect}
      <foreignObject
        x={cx - $width / 2}
        y={cy - $height / 2}
        width={$width}
        height={$height}
      >
        <div
          class="cursor-zoom-out w-full h-full flex flex-col items-center justify-center text-white opacity-0 animate-fade-in"
        >
          {#each data as meme}
            <div class="text-center">
              <strong>{meme.name}</strong><br />
              Year: {meme.year}<br />
            </div>
          {/each}
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
