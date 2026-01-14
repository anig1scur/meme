<script>
  import {useLocation, navigate} from 'svelte-routing';
  import {spring} from 'svelte/motion';

  let isOpen = false;
  let clientWidth;
  let isAnimating = false;
  let location = useLocation();
  $: ({pathname} = $location);

  const scaleSpring = spring(1, {
    stiffness: 0.2,
    damping: 0.8,
  });

  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const navItems = [
    {path: `${base}/`, label: 'Meme'},
    {path: `${base}/gallery`, label: 'Gallery'},
    {path: `${base}/random`, label: 'Random'},
    {path: `${base}/visualization`, label: 'Visualization'},
  ];

  async function handleNavigation(newPath) {
    if (isAnimating || newPath === pathname) return;

    isAnimating = true;
    await scaleSpring.set(0.65);
    await scaleSpring.set(1);

    navigate(newPath);
    isAnimating = false;

    if (isOpen) {
      isOpen = false;
    }
  }
</script>

<svelte:window bind:innerWidth={clientWidth} />

{#if clientWidth <= 640}
  <div class="font-routedgothic fixed top-4 z-10 left-4">
    {#if isOpen}
      <button
        class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50"
        onclick={() => (isOpen = false)}
      ></button>
    {/if}
    <button
      class="p-2 bg-green-500 z-50 text-white outline-double outline-2 outline-green-600 transition-transform duration-300"
      style="transform: translateX({isOpen ? '190px' : '0'})"
      onclick={() => (isOpen = !isOpen)}
    >
      ☰
    </button>

    <aside
      class="fixed top-0 flex flex-col left-0 h-full w-48 bg-green-500 p-4 pt-10 border-r-2 border-green-950 z-40 transition-transform duration-300"
      style="transform: translateX({isOpen ? '0' : '-100%'})"
    >
      {#each navItems as item}
        <button
          class={`px-3 py-1 rounded transition-all duration-200 text-white ${pathname === item.path ? ' text-yellow-700 bg-yellow-200 border-2 border-green-950 italic rounded px-3 py-[1px]' : ''}`}
          onclick={() => handleNavigation(item.path)}
          style="transform: scale({pathname === item.path ? $scaleSpring : 1})"
        >
          {item.label}
        </button>
      {/each}
    </aside>
  </div>
{:else}
  <header
    class="font-routedgothic header fixed p-4 py-5 top-0 left-0 w-full h-[3rem] bg-green-500 z-50 border-y-[3px] border-green-950 flex items-center justify-center space-x-4"
  >
    {#each navItems as item}
      <button
        style="transform: scale({pathname === item.path ? $scaleSpring : 1})"
        class={`px-3 py-1 rounded transition-all duration-200 text-white ${pathname === item.path ? ' bg-yellow-200 text-yellow-700 border-solid border-2 border-green-800 italic rounded px-3 py-[1px]' : ''}`}
        onclick={() => handleNavigation(item.path)}
      >
        {item.label}
      </button>
    {/each}
  </header>
{/if}
