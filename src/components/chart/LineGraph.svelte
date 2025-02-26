<script>
  import {
    line,
    scaleTime,
    scaleLinear,
    easeLinear,
    timeFormat,
    curveBasis,
    timeParse,
    axisBottom,
    bisector,
    axisLeft,
    select,
  } from 'd3';
  import {onMount} from 'svelte';

  export let data;
  export let index;
  const width = 260;
  const height = 120;
  const padding = 20;

  const parseDate = timeParse('%Y.%m');
  const formatDate = timeFormat('%b, %Y');
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

  const xScale = scaleTime()
    .domain([months[0], months[months.length - 1]]) // Use time scale for x-axis
    .range([padding, width - padding]);

  const yScale = scaleLinear()
    .domain([0, Math.max(...data.trend)])
    .range([height - padding, padding]);

  const pathLine = line()
    .x((_, i) => xScale(months[i]))
    .y((d) => yScale(d))
    .curve(curveBasis);

  const xAxis = axisBottom(xScale)
    .ticks(5)
    .tickFormat(timeFormat('%Y'))
    .tickSize(-height + 2 * padding);

  const yAxis = axisLeft(yScale)
    .ticks(5)
    .tickSize(-width + 2 * padding);

  let tooltipVisible = false;
  let tooltipData = {x: 0, y: 0, value: 0, date: ''};

  function showTooltip(event) {
    const rect = event.target.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;

    const bisectDate = bisector((d) => d).left;
    const date = xScale.invert(mouseX);
    const index = bisectDate(months, date, 1);
    const dataIndex = index - 1;

    if (dataIndex >= 0 && dataIndex < data.trend.length) {
      tooltipData = {
        x: event.pageX,
        y: event.pageY,
        value: data.trend[dataIndex],
        date: formatDate(months[dataIndex]),
      };
      tooltipVisible = true;
    }
  }

  function hideTooltip() {
    tooltipVisible = false;
  }

  onMount(() => {
    const svg = select(`#chart-${index}`);

    svg
      .select('.x-axis')
      .call(xAxis)
      .attr('transform', `translate(0, ${height - padding})`)
      .attr('class', 'text-[10px]')
      .call((g) => {
        g.select('.domain').remove();
        g.selectAll('.tick line').attr('class', 'gridline');
        g.selectAll('.tick text').attr('class', 'fill-gray-400 translate-y-2');
      });

    svg
      .select('.y-axis')
      .call(yAxis)
      .attr('transform', `translate(${padding}, 0)`)
      .attr('class', 'text-[10px]')
      .call((g) => {
        g.select('.domain').remove();
        g.selectAll('.tick line').attr('class', 'gridline');
        g.selectAll('.tick text').attr('class', 'fill-gray-400 -translate-x-1');
      });

    const path = svg.selectChildren('path');
    if (path.node()) {
      const pathLength = path.node().getTotalLength();
      path
        .attr('stroke-dasharray', pathLength)
        .attr('stroke-dashoffset', pathLength)
        .transition()
        .delay(index * 200)
        .duration(1500)
        .ease(easeLinear)
        .attr('stroke-dashoffset', 0);
    }
  });
</script>

<div class="bg-white rounded-lg p-4">
  <a
    target="_blank"
    href={`https://trends.google.com/trends/explore?date=all&q=${data.name}`}
    title={data.name}
    class="block text-sm font-medium text-gray-700 mb-2 text-center truncate max-w-60"
  >
    {data.name}
  </a>
  <svg
    {width}
    {height}
    on:mousemove={showTooltip}
    on:mouseleave={hideTooltip}
    id={`chart-${index}`}
    class="overflow-visible"
  >
    <g class="x-axis" />
    <g class="y-axis" />
    <path
      d={pathLine(data.trend)}
      stroke={`hsl(${(index * 360) / 9}, 100%, 50%)`}
      stroke-width="1.5"
      fill="none"
      stroke-linecap="round"
    />
  </svg>
  {#if tooltipVisible}
    <div
      class="absolute pointer-events-none bg-white p-2 rounded-lg text-xs shadow-lg border border-gray-200"
      style="left: {tooltipData.x + 10}px; top: {tooltipData.y - 40}px"
    >
      <p class="text-gray-600">{tooltipData.date}</p>
      <p class="font-semibold text-blue-400">{tooltipData.value}</p>
    </div>
  {/if}
</div>

<style>
  path {
    transition: stroke-width 0.3s ease-in-out;
  }

  path:hover {
    stroke-width: 2;
  }
</style>
