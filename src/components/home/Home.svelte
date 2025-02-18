<script lang="ts">
  import CursorFollower from '../CursorFollower.svelte';
  import {onMount} from 'svelte';

  let memeData = [];

  onMount(async () => {
    const response = await fetch('/meme_details.json');
    memeData = await response.json();
  });
</script>

<CursorFollower />

<div class="font-routedgothic mt-12 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 p-6">
  {#each Array(5) as _, index}
    <div class="flex flex-col">
      {#each memeData.filter((_, i) => i % 5 === index) as meme}
        <div class="h-fit">
          <img
            src={'top50/images/' + meme.image}
            alt={meme.name}
            class="w-full h-auto object-cover"
          />
          <div class="p-4">
            <h3 class="text-xl font-semibold text-gray-800">{meme.name}</h3>
            <p class="text-gray-600 mt-2">{meme.desc}</p>
            <p class="mt-4 text-sm text-gray-500">{meme.year} | {meme.origin}</p>
            <p class="mt-2 text-sm font-semibold">{meme.type}</p>
            <a
              href={meme.link}
              target="_blank"
              class="text-blue-500 hover:underline mt-4 block"
            >
              Know your meme
            </a>
          </div>
        </div>
      {/each}
    </div>
  {/each}
</div>
