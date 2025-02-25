<script>
  import {tweened} from 'svelte/motion';
  import * as easings from 'svelte/easing';
  import {scaleLinear, scaleOrdinal, scaleSqrt} from 'd3';
  import Bubble from '../chart/Bubble.svelte';
  import Grid from '../chart/Grid.svelte';
  import raw from '/public/meme_stats.json';

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

  const minYear = 1995;
  const maxYear = 2025;
  const yearStep = 2.5;

  $: xScale = scaleLinear().domain([minYear, maxYear]).range([-140, innerWidth]);
  const xAxisTicks = ['<2000', 2005, 2010, 2015, 2020, 2025];

  const getYearBucket = (year) => Math.floor(year / yearStep) * yearStep;

  const groupedMemeData = raw.reduce((acc, {year, origin, ...rest}) => {
    const yearBucket = !year || year === 'Unknown' || Number(year) < 2000 ? 'before' : getYearBucket(year);
    const originGroup = normalizeOrigin(origin);
    const key = `${yearBucket}-${originGroup}`;

    if (!acc[key]) acc[key] = {year: yearBucket, origin: originGroup, count: 0, memes: []};

    acc[key].count++;
    acc[key].memes.push({year, origin, ...rest});

    return acc;
  }, {});
  const memeData = Object.values(groupedMemeData);

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

    {#each $animatedMemeData as d}
      <Bubble
        cx={xScale(d.year)}
        cy={yScale(d.origin)}
        r={rScale(d.count)}
        fill={colorScale(d.origin)}
        data={d.memes}
        origin={d.origin}
        year={d.year}
      />
    {/each}
  </g>
</svg>
