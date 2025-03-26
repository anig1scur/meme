<script>
  import DancingBaby from '$assets/imgs/timeline/dancing_baby.gif';
  import {fade, scale} from 'svelte/transition';
  export let src = DancingBaby;

  let isOpen = false;
</script>

<div class="relative cursor-pointer">
  <img
    on:click={() => (isOpen = true)}
    {src}
    class="h-40 object-contain"
    alt="Dancing Baby"
  />

  {#if isOpen}
    <div
      transition:fade
      class="fixed inset-0 bg-white/90 z-50 flex items-center justify-center"
      on:click={() => (isOpen = false)}
    >
      <div
        transition:scale
        class="relative max-w-4xl max-h-[90vh] p-4"
      >
        <img
          {src}
          class="max-w-full max-h-full object-contain"
          alt="Dancing Baby Enlarged"
        />

        <button
          on:click|stopPropagation={() => (isOpen = false)}
          class="absolute top-0 right-0 m-4 p-2 bg-white/10 hover:bg-white/20 rounded-full text-white transition-colors duration-200"
        >
          <div class="hover:rotate-90 transition-transform duration-200">✕</div>
        </button>
      </div>
    </div>
  {/if}
</div>
