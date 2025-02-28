<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Title from '$assets/imgs/chronicle_of_meme.png';

  gsap.registerPlugin(ScrollTrigger);

  const images = Object.values(
    import.meta.glob(['$assets/imgs/characteristic/**.svg'], {
      eager: true,
      as: 'url',
    }),
  );

  let container;
  let title;

  onMount(() => {
    const imgElements = container.querySelectorAll('.img');

    const updatePositions = () => {
      const windowWidth = window.innerWidth;
      const scaleFactor = windowWidth < 768 ? 0.8 : 1;
      const topOffset = windowWidth < 768 ? 10 : 0;

      const verticalSpacing = windowWidth < 768 ? 12 : 8;
      const verticalSpacingRight = windowWidth < 768 ? 18 : 5;

      for (let i = 0; i < 3; i++) {
        const img = imgElements[i];
        gsap.set(img, {
          position: 'absolute',
          left: `${i * 15}%`,
          top: `${40 + (i - 1) * verticalSpacing - topOffset}vh`,
          width: `clamp(150px, ${15 * scaleFactor}vw, 240px)`,
          height: 'auto',
          zIndex: 10,
        });
      }

      for (let i = 3; i < 6; i++) {
        const img = imgElements[i];
        gsap.set(img, {
          position: 'absolute',
          right: `${5 + (i - 3) * 15}%`,
          top: `${30 + (i - 3) * verticalSpacingRight - topOffset}vh`,
          width: `clamp(150px, ${15 * scaleFactor}vw, 240px)`,
          height: 'auto',
          zIndex: 10,
        });
      }
    };

    updatePositions();

    window.addEventListener('resize', updatePositions);

    return () => {
      window.removeEventListener('resize', updatePositions);
    };
  });
</script>

<div
  class="relative"
  bind:this={container}
>
  <div class="h-screen fixed top-0 bg-[#FFCA58] w-full"></div>
  <div class="relative">
    <img
      src={Title}
      class="w-[80%] mt-[15vh] md:mt-[30vh] mx-auto md:w-[75%] h-auto"
    />
  </div>
  <div
    class="c1 absolute -left-[12.5%] top-[50vh] md:top-[40vh] h-[70vh] w-[125vw] rounded-[50%] bg-gradient-to-b from-[#fff4dd] to-[#e4b040] bg-[linear-gradient(90deg, #fff4dd 0.00%, #e4b040 100.00%)]"
  />
  <div
    class="c2 absolute -right-[15%] top-[40vh] md:top-[30vh] h-[60vh] w-[60vw] right-0 rounded-[50%] bg-gradient-to-r from-[#22c55d] to-[#adff81] bg-[linear-gradient(-2deg, #22c55d 0.00%, #adff81 100.00%)]"
  />

  {#each images as src, i}
    <img
      {src}
      alt={`image ${i + 1}`}
      class={`img img-${i}`}
    />
  {/each}
</div>

<style>
</style>
