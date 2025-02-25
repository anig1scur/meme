<script>
  import {line, curveMonotoneX, scaleLinear, timeParse, axisBottom, axisLeft, select} from 'd3';
  import {onMount} from 'svelte';

  export let data;
  const data_ = data.filter((item) => Array.isArray(item.trend)).slice(0, 9);

  const parseDate = timeParse('%Y.%m');

  const startYear = 2004;
  const end = new Date();
  const months = [];

  for (let year = startYear; year <= end.getFullYear(); year++) {
    for (let month = 1; month <= 12; month++) {
      if (year === end.getFullYear() && month > end.getMonth() + 1) {
        break;
      }
      months.push(parseDate(`${year}.${month.toString().padStart(2, '0')}`));
    }
  }

  const width = 260;
  const height = 120;
  const padding = 20;

  const xScale = scaleLinear()
    .domain([0, months.length - 1])
    .range([padding, width - padding]);

  const yScale = scaleLinear()
    .domain([0, Math.max(...data_.flatMap((d) => d.trend))])
    .range([height - padding, padding]);

  const pathLine = line()
    .x((_, i) => xScale(i))
    .y((d) => yScale(d))
    .curve(curveMonotoneX);

  const xAxis = axisBottom(xScale)
    .ticks(5)
    .tickSize(-height + 2 * padding);

  const yAxis = axisLeft(yScale)
    .ticks(5)
    .tickSize(-width + 2 * padding);

  let tooltipVisible = false;
  let tooltipData = {x: 0, y: 0, value: 0, date: ''};

  onMount(() => {
    data_.forEach((_, index) => {
      const svg = select(`#chart-${index}`);

      svg
        .select('.x-axis')
        .call(xAxis)
        .attr('transform', `translate(0, ${height - padding})`)
        .attr('class', 'text-[10px]')
        .call((g) => {
          g.select('.domain').attr('class', 'stroke-gray-100');
          g.selectAll('.tick line').attr('class', 'stroke-gray-200');
          g.selectAll('.tick text').attr('class', 'fill-gray-400');
        });

      svg
        .select('.y-axis')
        .call(yAxis)
        .attr('transform', `translate(${padding}, 0)`)
        .attr('class', 'text-[10px]')
        .call((g) => {
          g.select('.domain').attr('class', 'stroke-gray-200');
          g.selectAll('.tick line').attr('class', 'stroke-gray-200');
          g.selectAll('.tick text').attr('class', 'fill-gray-400');
        });
    });
  });

  function showTooltip(event, trend) {
    const rect = event.target.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;

    const exactIndex = xScale.invert(mouseX);
    const dataIndex = Math.round(exactIndex);
    if (dataIndex >= 0 && dataIndex < trend.length) {
      tooltipData = {
        x: event.pageX,
        y: event.pageY,
        value: trend[dataIndex],
        date: months[dataIndex]
          ? months[dataIndex].toLocaleDateString('default', {year: 'numeric', month: 'short'})
          : months[dataIndex],
      };
      tooltipVisible = true;
    }
  }

  function hideTooltip() {
    tooltipVisible = false;
  }
</script>

<div class="font-routedgothic grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-12">
  {#each data_ as { trend, name }, index}
    <div class="bg-white rounded-lg p-4">
      <h3 class="text-sm font-medium text-gray-700 mb-2 text-center">{name}</h3>
      <svg
        id="chart-{index}"
        {width}
        {height}
        viewBox="0 0 {width} {height}"
        on:mousemove={(e) => showTooltip(e, trend, index)}
        on:mouseleave={hideTooltip}
      >
        <g class="x-axis" />
        <g class="y-axis" />
        <path
          d={pathLine(trend)}
          stroke={`hsl(${(index * 360) / data_.length}, 100%, 50%)`}
          stroke-width="1.5"
          fill="none"
          stroke-linecap="round"
          class="transition-all duration-300 hover:stroke-width-2"
        />
      </svg>
    </div>
  {/each}
</div>

{#if tooltipVisible}
  <div
    class="absolute pointer-events-none bg-white p-2 rounded-lg text-xs shadow-lg border border-gray-200"
    style="left: {tooltipData.x + 10}px; top: {tooltipData.y - 40}px"
  >
    <p class="text-gray-600">{tooltipData.date}</p>
    <p class="font-semibold text-blue-400">{tooltipData.value}</p>
  </div>
{/if}

<style>
  path {
    transition: stroke-width 0.3s ease-in-out;
  }

  path:hover {
    stroke-width: 2;
  }
</style>
