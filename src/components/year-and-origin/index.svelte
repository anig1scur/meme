<script>
  // A Svelte component contains javascript (in a <script> tag), html and css (in a <style> tag). This main App component does not have styling, but the Bubble and Grid components do

  import {tweened} from 'svelte/motion';
  import * as easings from 'svelte/easing';
  import data from './data.js';
  // D3 is is installed here, so we can import the needed functions from it
  import {extent, scaleLinear, scaleLog, scaleOrdinal, scaleSqrt, max} from 'd3';
  // Here we import the custom components, you can check them by clicking the tabs at the top of this code editor
  import Bubble from '../visualization/Bubble.svelte';
  import Grid from '../visualization/Grid.svelte';

  let year = 2018;

  // Here we split the data in 2, which we need in order to animate between them
  const data60 = data.map((d) => {
    let obj = {};
    obj.country = d.country;
    obj.continent = d.continent;
    obj.population = d.population60;
    obj.lifeexp = d.lifeexp60;
    obj.income = d.income60;
    return obj;
  });
  const data18 = data.map((d) => {
    let obj = {};
    obj.country = d.country;
    obj.continent = d.continent;
    obj.population = d.population;
    obj.lifeexp = d.lifeexp;
    obj.income = d.income;
    return obj;
  });

  // With Svelte's tweened, you can interpolate between data values, see https://svelte.dev/docs#tweened. The initial values are set here to be the data from 2018
  const tweenedPoints = tweened(data18, {
    delay: 0,
    duration: 1500,
    easing: easings.cubicOut,
  });

  // With "$:" you can specify reactive statements in Svelte. Svelte checks all variables in the statement, and when one of them changes, the statement is run and everything is updated. In this case, tweenedPoints is updated depending on the selected year radio button. See https://svelte.dev/docs#3_$_marks_a_statement_as_reactive
  $: if (year == 1960) {
    tweenedPoints.set(data60);
  } else {
    tweenedPoints.set(data18);
  }

  const margin = {top: 15, bottom: 50, left: 50, right: 20};
  const width = 800;
  const height = 500;
  const innerHeight = height - margin.top - margin.bottom;
  const innerWidth = width - margin.left - margin.right;

  const maxpop = max(data18, (d) => d.population);

  // Here, the x and y scales (both of them are D3 scales) are declared as reactive. This means that they update whenever tweenedPoints changes, and because tweenedPoints interpolates between values, the scales are transitioned too. If you want fixed scales (which make sense here), you can set the domain of xScale to [400, 70000] and the domain of yScale to [30, 90]. In that case the reactive scales only depend on innerWidth and innerHeight, which might be handy to make responsive charts
  $: xScale = scaleLog()
    //.domain([400, 70000])
    .domain(extent($tweenedPoints, (d) => d.income))
    .range([0, innerWidth]);
  $: xTicks = xScale.ticks();
  $: yScale = scaleLinear()
    //.domain([30, 90])
    .domain(extent($tweenedPoints, (d) => d.lifeexp))
    .range([innerHeight, 0]);
  $: yTicks = yScale.ticks();

  // The scales for the radius and the colors don't depend on variables that might change, so we don't need the reactive "$:" statement
  const rScale = scaleSqrt().domain([0, maxpop]).range([0, 50]);
  const colors = ['#FF265C', '#FFE700', '#4ED7E9', '#70ED02', 'purple'];
  const colorScale = scaleOrdinal().domain(['Asia', 'Europe', 'Africa', 'Americas', 'Oceania']).range(colors);
</script>

<!--Here the returned html starts-->
<!--The radio buttons below are bound to the year variable, declared at the beginning of the javascript.-->
<label>
  <input
    type="radio"
    bind:group={year}
    name="year"
    value={2018}
  />
  2018
</label>
<label>
  <input
    type="radio"
    bind:group={year}
    name="year"
    value={1960}
  />
  1960
</label>

<!--In Svelte "{width}"" is just short for "width={width}", which sets the value of the width property of the html element to the javascript variable width-->
<svg
  {width}
  {height}
>
  <g transform={`translate(${margin.left},${margin.top})`}>
    <!--Here we are using the custom Grid component. We are passing 5 properties to it, notice how these are the same ones as the variables that the component exports (check the Grid.svelte tab). This is how you pass properties from parent to child components-->
    <Grid
      gridType="xGrid"
      {innerHeight}
      {innerWidth}
      scale={xScale}
      ticks={xTicks}
    />
    <Grid
      gridType="yGrid"
      {innerHeight}
      {innerWidth}
      scale={yScale}
      ticks={yTicks}
    />

    <text transform={`translate(${-30},${innerHeight / 2}) rotate(-90)`}>Life expectancy</text>
    <text
      x={innerWidth / 2}
      y={innerHeight + 35}>GDP/capita</text
    >

    <!--In Svelte you can iterate over arrays of data with each blocks, see https://svelte.dev/docs#each. The following block adds a Bubble to the chart for each data element in tweenedPoints-->
    {#each $tweenedPoints as d}
      <Bubble
        cx={xScale(d.income)}
        cy={yScale(d.lifeexp)}
        r={rScale(d.population)}
        fill={colorScale(d.continent)}
      ></Bubble>
    {/each}
  </g>
</svg>
