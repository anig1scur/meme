<script>
  import {LayerCake, Svg} from 'layercake';
  import Radar from '../chart/Radar.svelte';
  import AxisRadial from '../chart/AxisRadial.svelte';
  import raw from '/public/meme_stats.json';

  const xKey = ['humour', 'sarcasm', 'offensive', 'motivational', 'sentiment'];
  const itemsPerPage = 6;
  const totalPages = 7;
  let currentPage = 0;

  const data = raw.slice(0, itemsPerPage * totalPages).map((d) => {
    const [humour, sarcasm, offensive, motivational] = d.emotion;
    const sentiment = (humour + motivational - sarcasm - offensive + 10) / 4;

    return {...d, humour, sarcasm, offensive, motivational, sentiment};
  });

  const goto = (page) => {
    if (page >= 0 && page <= totalPages) {
      currentPage = page;
    }
  };
</script>

<section class="visualization">
  <div class="font-routedgothic mt-24 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12 mb-12">
    {#each data.slice(currentPage * itemsPerPage, (currentPage + 1) * itemsPerPage) as item}
      <div class="h-64 w-64 flex items-center justify-center flex-col">
        <LayerCake
          width={300}
          height={225}
          x={xKey}
          xDomain={[0, 5]}
          xRange={() => [0, 80]}
          data={[item]}
        >
          <Svg>
            <AxisRadial />
            <Radar />
          </Svg>
        </LayerCake>
        <a
          target="_blank"
          href={item.link}
          title={item.name}
          class="block text-gray-700 text-sm text-center truncate max-w-64"
        >
          {item.name}
        </a>
      </div>
    {/each}
  </div>

  <div class="flex justify-center space-x-4 my-6">
    {#each Array(totalPages).fill(0) as _, pageIndex}
      <button on:click={() => goto(pageIndex)}>
        <div
          class="w-4 h-4 rounded-full border-2 border-[#f0c] {currentPage === pageIndex
            ? 'bg-[#f0c] bg-opacity-50'
            : ''}"
        ></div>
      </button>
    {/each}
  </div>
  <div class="title">Sentiment Radar of Memes</div>
</section>
