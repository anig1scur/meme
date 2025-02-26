<script>
  import {LayerCake, Svg} from 'layercake';
  import Radar from '../chart/Radar.svelte';
  import AxisRadial from '../chart/AxisRadial.svelte';

  const data = [
    {
      name: 'Allison',
      fastball: 10,
      change: 0,
      slider: 4,
      cutter: 8,
      curve: 5,
    },
  ];

  const seriesKey = 'name';
  const xKey = ['fastball', 'change', 'slider', 'cutter', 'curve'];

  const seriesNames = Object.keys(data[0]).filter((d) => d !== seriesKey);

  data.forEach((d) => {
    seriesNames.forEach((name) => {
      d[name] = +d[name];
    });
  });
</script>

<div class="mt-16 flex justify-center items-center">
  <div class="w-96 h-96">
    <LayerCake
      padding={{top: 10, right: 10, bottom: 10, left: 10}}
      x={xKey}
      xDomain={[0, 10]}
      xRange={({width, height}) => [0, Math.min(width, height) / 2]}
      {data}
    >
      <Svg>
        <AxisRadial />
        <Radar />
      </Svg>
    </LayerCake>
  </div>
</div>
