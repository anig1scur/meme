<script>
  import {getContext, onMount} from 'svelte';
  import {line, curveCardinalClosed} from 'd3';
  import {tweened} from 'svelte/motion';
  import {cubicOut} from 'svelte/easing';

  const {data, width, height, xGet, config} = getContext('LayerCake');

  export let fill = '#f0c';
  export let stroke = '#f0c';
  export let strokeWidth = 2;
  export let fillOpacity = 0.5;
  export let r = 4.5;
  export let circleFill = '#f0c';
  export let circleStroke = '#fff';
  export let circleStrokeWidth = 1;

  let animationScale = tweened(0, {
    duration: 1500,
    easing: cubicOut,
  });

  let radarEl;
  let observer;

  function startAnimation() {
    animationScale.set(1);
  }

  onMount(() => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            startAnimation();
            // observer.disconnect();
          }
        });
      },
      {threshold: 0.1},
    );

    if (radarEl) {
      observer.observe(radarEl);
    }

    return () => {
      if (observer) {
        observer.disconnect();
      }
    };
  });

  $: angleSlice = (Math.PI * 2) / $config.x.length;
  $: path = line()
    .curve(curveCardinalClosed)
    .x((d, i) => d * $animationScale * Math.cos(angleSlice * i - Math.PI / 2))
    .y((d, i) => d * $animationScale * Math.sin(angleSlice * i - Math.PI / 2));
</script>

<g
  bind:this={radarEl}
  transform="translate({$width / 2}, {$height / 2})"
>
  {#each $data as row}
    {@const xVals = $xGet(row)}
    <path
      class="path-line"
      d={path(xVals)}
      {stroke}
      stroke-width={strokeWidth}
      {fill}
      fill-opacity={fillOpacity}
    ></path>
    {#each xVals as circleR, i}
      {@const thisAngleSlice = angleSlice * i - Math.PI / 2}
      <circle
        cx={circleR * $animationScale * Math.cos(thisAngleSlice)}
        cy={circleR * $animationScale * Math.sin(thisAngleSlice)}
        {r}
        fill={circleFill}
        stroke={circleStroke}
        stroke-width={circleStrokeWidth}
      ></circle>
    {/each}
  {/each}
</g>

<style>
  .path-line {
    stroke-linejoin: round;
    stroke-linecap: round;
  }
</style>
