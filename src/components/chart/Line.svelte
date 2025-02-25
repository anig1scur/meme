<script>
  import {draw} from 'svelte/transition';

  import {line, curveBasis, scaleLinear, timeParse} from 'd3';

  export let data;

  const data_ = data.filter((item) => Array.isArray(item.trend)).slice(10,100)

  const parseDate = timeParse('%Y.%m');
  const months = Array.from({length: 48}, (_, i) => parseDate(`2004.${(i + 1).toString().padStart(2, '0')}`));

  const xScale = scaleLinear()
    .domain([0, months.length - 1])
    .range([5, 200]);

  const yScale = scaleLinear()
    .domain([0, Math.max(...data_.flatMap((d) => d.trend))])
    .range([5, 85]);

  const pathLine = line()
    .x((_, i) => xScale(i))
    .y((d) => yScale(d))
    .curve(curveBasis);
</script>

<svg
  viewBox="0 0 100 100"
  width="900"
>
  {#each data_ as { trend }, index}
    <path
      transition:draw={{duration: 2000}}
      d={pathLine(trend)}
      stroke={`hsl(${(index * 360) / data_.length}, 100%, 50%)`}
    />
  {/each}
</svg>

<style>
  path {
    stroke-width: 0.6;
    fill: none;
    stroke-linecap: round;
  }
</style>
