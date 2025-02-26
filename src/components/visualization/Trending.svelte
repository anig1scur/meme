<script>
  import stats from '/public/meme_stats.json';
  import LineGraph from '../chart/LineGraph.svelte';

  let _stats = stats.filter((item) => Array.isArray(item.trend));
  let currentPage = 1;
  const itemsPerPage = 9;
  const total = 63;
  const totalPages = Math.ceil(total / itemsPerPage);

  const pagedData = () => {
    return _stats.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
  };

  const goto = (page) => {
    if (page > 0 && page <= totalPages) {
      currentPage = page;
    }
  };
</script>

<div class="font-routedgothic mt-28 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-12">
  {#each pagedData() as data, index}
    <LineGraph
      {data}
      {index}
    />
  {/each}
</div>

<div class="flex justify-center space-x-4 mt-6 mb-12">
  {#each Array(totalPages).fill(0) as _, pageIndex}
    <button on:click={() => goto(pageIndex + 1)}>
      <div
        class="w-4 h-4 rounded-full border-2 border-green-600 {currentPage === pageIndex + 1 ? 'bg-green-600 bg-opacity-50' : ''}"
      ></div>
    </button>
  {/each}
</div>
