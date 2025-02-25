<script>
  // This is a very simple component: it receives 4 properties and returns an svg circle with these properties
  export let cx;
  export let cy;
  export let r;
  export let fill;
</script>

<!--Equivalent to cx={cx} cy={cy} r={r} fill={fill)-->
<circle
  {cx}
  {cy}
  {r}
  {fill}
></circle>

<style>
  /*Styles in Svelte are scoped, which means that the css below only adds a black stroke to the circles returned by this component. Any other circles somewhere in your app/html will not be affected*/
  circle {
    stroke: black;
  }
</style>
