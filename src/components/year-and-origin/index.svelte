<script>
  import {tweened} from 'svelte/motion';
  import * as easings from 'svelte/easing';
  import {scaleLinear, scaleOrdinal, scaleSqrt} from 'd3';
  import Bubble from '../visualization/Bubble.svelte';
  import Grid from '../visualization/Grid.svelte';
  import rawData from './meme_details.json';

  let yearRanges = Array.from({length: 7}, (_, i) => ({
    min: 2000 + i * 5,
    max: 2005 + i * 5,
    label: `${2000 + i * 5}-${2005 + i * 5}`,
  }));

  const validOrigins = [
    'Instagram',
    'Tumblr',
    'Facebook',
    'TikTok',
    '4chan',
    'Twitter',
    'YouTube',
    'Reddit',
    'Unknown',
    'Other',
  ];
  const validOriginsSet = new Set(validOrigins);

  const normalizeOrigin = (origin) => (validOriginsSet.has(origin) ? origin : 'Other');

  const margin = {top: 20, bottom: 80, left: 80, right: 20};
  const width = 900;
  const height = 600;
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  $: xScale = scaleOrdinal()
    .domain(yearRanges.map((r) => r.label))
    .range([...Array(yearRanges.length).keys()].map((i) => (i / (yearRanges.length - 1)) * innerWidth));

  const minYear = 2000;
  const maxYear = 2025;
  const yearStep = 2.5;

  $: xScaleFine = scaleLinear().domain([minYear, maxYear]).range([0, innerWidth]);

  const getYearBucket = (year) => Math.floor(year / yearStep) * yearStep;

  const groupedMemeData = rawData.reduce((acc, {year, origin}) => {
    const yearBucket = !year || year === 'Unknown' || Number(year) < 2000 ? 'before' : getYearBucket(year);
    const originGroup = normalizeOrigin(origin);
    const key = `${yearBucket}-${originGroup}`;

    if (!acc[key]) acc[key] = {year: yearBucket, origin: originGroup, count: 0};
    acc[key].count++;

    return acc;
  }, {});

  const memeData = Object.values(groupedMemeData);
  console.log(memeData);

  const animatedMemeData = tweened(memeData, {
    delay: 300,
    duration: 1500,
    easing: easings.cubicOut,
  });

  animatedMemeData.set(memeData);

  const maxCount = Math.max(...memeData.map((d) => d.count));

  const rScale = scaleSqrt().domain([0, maxCount]).range([5, 50]);

  $: yScale = scaleOrdinal()
    .domain(validOrigins)
    .range([...Array(validOrigins.length).keys()].map((i) => (i / (validOrigins.length - 1)) * innerHeight));

  const xAxisTicks = ['<1995', 2000, 2005, 2010, 2015, 2020, 2025];

  const colorScale = scaleOrdinal()
    .domain([...validOrigins, 'Other'])
    .range(['#FF265C', '#FFE700', '#4ED7E9', '#70ED02', '#9370DB', '#FF8C00', '#808080']);
</script>

<svg
  {width}
  {height}
>
  <g transform={`translate(${margin.left},${margin.top})`}>
    <Grid
      gridType="xGrid"
      {innerHeight}
      {innerWidth}
      scale={xScale}
      ticks={xAxisTicks}
    />
    <Grid
      gridType="yGrid"
      {innerHeight}
      {innerWidth}
      scale={yScale}
      ticks={validOrigins}
    />

    <!-- <text transform={`translate(${-30},${innerHeight / 2}) rotate(-90)`}>Origin</text> -->
    <!-- <text
      x={innerWidth / 2}
      y={innerHeight + 40}>Year Range</text
    > -->

    {#each $animatedMemeData as d}
      <Bubble
        cx={xScaleFine(d.year)}
        cy={yScale(d.origin)}
        r={rScale(d.count)}
        fill={colorScale(d.origin)}
      />
    {/each}
  </g>
</svg>
