<script>
  import {LayerCake, Svg} from 'layercake';
  import Radar from '../chart/Radar.svelte';
  import AxisRadial from '../chart/AxisRadial.svelte';
  import rawData from '/public/meme_stats.json';

  const seriesKey = 'name';
  const xKey = ['humour', 'sarcasm', 'offensive', 'motivational', 'sentiment'];

  const data = rawData.slice(0, 9).map((d) => {
    const [humour, sarcasm, offensive, motivational] = d.emotion;
    const sentiment = (humour + motivational - sarcasm - offensive + 10) / 4;

    return {
      ...d,
      humour,
      sarcasm,
      offensive,
      motivational,
      sentiment,
    };
  });
</script>

<div class="font-routedgothic mt-28 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-12">
  {#each data as item}
    <div class="radar-chart">
      <LayerCake
        padding={{top: 20, right: 40, bottom: 20, left: 40}}
        x={xKey}
        xDomain={[0, 5]}
        xRange={({width, height}) => [0, Math.min(width, height) / 2]}
        data={[item]}
      >
        <Svg>
          <AxisRadial />
          <Radar />
        </Svg>
      </LayerCake>
      <div class="meme-name">{item.name}</div>
    </div>
  {/each}
</div>
