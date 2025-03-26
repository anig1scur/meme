<script>
  import {onMount} from 'svelte';
  export let bookWidth = 250;
  export let bookHeight = 400;
  export let coverColor = '#5e995c';
  export let image = '';
  export let altText = 'Book cover';
  export let link = '';

  let bookElement;
  let isHovering = false;
  let initialTransform = '';

  function handleMouseMove(event) {
    if (!bookElement || !isHovering) return;

    const rect = bookElement.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const xPercent = (x / rect.width) * 100;
    const yPercent = (y / rect.height) * 100;

    const rotateY = ((xPercent - 50) / 50) * 35;
    const rotateX = -((yPercent - 50) / 50) * 10;

    bookElement.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
  }

  function handleMouseEnter() {
    if (!initialTransform && bookElement) {
      initialTransform = window.getComputedStyle(bookElement).transform;
      if (initialTransform === 'none') {
        initialTransform = '';
      }
    }
    isHovering = true;
  }

  function handleMouseLeave() {
    isHovering = false;
    if (bookElement) {
      bookElement.style.transform = initialTransform;
    }
  }

  onMount(() => {
    if (bookElement) {
      initialTransform = window.getComputedStyle(bookElement).transform;
      if (initialTransform === 'none') {
        initialTransform = '';
      }
    }
  });
</script>

<a
  href={link}
  target="_blank"
  rel="noreferrer noopener"
  class="inline-flex items-center justify-center perspective-600 book-container"
  on:mousemove={handleMouseMove}
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
>
  <div
    bind:this={bookElement}
    class="relative preserve-3d transition-transform duration-300 book z-10"
    style="width: {bookWidth}px; height: {bookHeight}px;"
  >
    <!-- Front cover -->
    <div
      class="absolute top-0 left-0 w-full h-full rounded-r shadow-lg overflow-hidden"
      style="transform: translateZ(15px); background-color: {coverColor};"
    >
      {#if image}
        <img
          src={image}
          alt={altText}
          class="w-full h-full object-cover"
        />
      {/if}
    </div>

    <!-- Spine -->
    <div
      class="absolute top-0.5"
      style="
        left: 0;
        width: 28px;
        height: {bookHeight - 2}px;
        transform: translateX({bookWidth - 16}px) rotateY(90deg);
        background: linear-gradient(90deg, 
          #fff 0%, #f9f9f9 5%, #fff 10%, #f9f9f9 15%, #fff 20%, 
          #f9f9f9 25%, #fff 30%, #f9f9f9 35%, #fff 40%, #f9f9f9 45%, 
          #fff 50%, #f9f9f9 55%, #fff 60%, #f9f9f9 65%, #fff 70%, 
          #f9f9f9 75%, #fff 80%, #f9f9f9 85%, #fff 90%, #f9f9f9 95%, 
          #fff 100%
        );
      "
    ></div>

    <!-- Back cover -->
    <div
      class="absolute top-0 left-0 w-full h-full rounded-r shadow-xl"
      style="
        transform: translateZ(-15px);
        background-color: {coverColor};
        box-shadow: -10px 0 50px 10px #0000006a;
      "
    ></div>
  </div>
</a>

<style>
  .perspective-600 {
    perspective: 600px;
  }

  .preserve-3d {
    transform-style: preserve-3d;
  }
</style>
