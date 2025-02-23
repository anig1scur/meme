<script>
  import {Router, Link, useLocation} from 'svelte-routing';

  let isOpen = false;
  let clientWidth;
  const location = useLocation();

  const navItems = [
    {path: '/', label: 'Gallery'},
    {path: '/random', label: 'Random'},
    {path: '/meme', label: 'Meme'},
    {path: '/visualization', label: 'Visualization'},
  ];
</script>

<svelte:window bind:innerWidth={clientWidth} />

{#if clientWidth <= 768}
  <div class="font-routedgothic fixed top-4 z-10 left-4">
    {#if isOpen}
      <button
        class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50"
        on:click={() => (isOpen = false)}
      ></button>
    {/if}
    <button
      class="p-2 bg-green-500 z-50 text-white outline-double outline-2 outline-green-600 transition-transform duration-300"
      style="transform: translateX({isOpen ? '190px' : '0'})"
      on:click={() => (isOpen = !isOpen)}
    >
      ☰
    </button>

    <aside
      class="fixed top-0 flex flex-col left-0 h-full w-48 bg-green-500 p-4 pt-10 border-r-2 border-green-950 z-40 transition-transform duration-300"
      style="transform: translateX({isOpen ? '0' : '-100%'})"
    >
      <Router>
        {#each navItems as item}
          <Link
            to={item.path}
            class={`px-3 py-1 rounded transition-all duration-200 text-white ${$location.pathname === item.path ? ' text-yellow-700 bg-yellow-200 border-2 border-green-950 italic rounded px-3 py-[1px]' : ''}`}
            on:click={() => (isOpen = false)}
          >
            {item.label}
          </Link>
        {/each}
      </Router>
    </aside>
  </div>
{:else}
  <header
    class="font-routedgothic fixed p-4 py-5 top-0 left-0 w-full h-[3rem] bg-green-500 z-50 border-y-[3px] border-green-950 flex items-center justify-center space-x-4"
  >
    <Router>
      {#each navItems as item}
        <Link
          to={item.path}
          class={`px-3 py-1 rounded transition-all duration-200 text-white ${$location.pathname === item.path ? ' bg-yellow-200 text-yellow-700 border-2 border-green-800 italic rounded px-3 py-[1px]' : ''}`}
        >
          {item.label}
        </Link>
      {/each}
    </Router>
  </header>
{/if}
