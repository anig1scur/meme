<script>
  import {Router, Link, useLocation} from 'svelte-routing';

  const location = useLocation();

  const navItems = [
    {path: '/gallery', label: 'Gallery'},
    {path: '/random', label: 'Random'},
    {path: '/meme', label: 'Meme'},
    {path: '/visualization', label: 'Visualization'},
  ];
</script>

<header
  class="font-routedgothic fixed p-4 py-5 top-0 left-0 w-full h-[3rem] bg-green-500 z-50 border-y-[3px] border-green-950 flex items-center justify-center space-x-4"
>
  <Router>
    {#each navItems as item}
      <Link
        to={item.path}
        class={`px-3 py-1 rounded transition-all duration-200 text-white ${$location.pathname === item.path ? ' text-green-800 bg-yellow-200 border-2 border-green-800 italic rounded px-3 py-[1px]' : ''}`}
      >
        {item.label}
      </Link>
    {/each}
  </Router>
</header>
