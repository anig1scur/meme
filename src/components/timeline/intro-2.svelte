<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  gsap.registerPlugin(ScrollTrigger);

  const images = Object.values(
    import.meta.glob(['$assets/imgs/intro/**.jpg', '$assets/imgs/intro/**.png'], {
      eager: true,
      as: 'url',
    }),
  );

  let container;
  let title;

  onMount(() => {
    const imgElements = container.querySelectorAll('.img');

    gsap.to(title, {
      y: 100,
      rotate: -6,
      scale: 2,
      opacity: 1,
      ease: 'elastic.out(1, 0.9)',
      scrollTrigger: {
        trigger: `.trigger`,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true,
        // markers: true,
      },
    });

    imgElements.forEach((img, index) => {
      const leftPosition = (index / (imgElements.length - 1)) * 80;
      if (index >= 1) {
        img.style.left = `${leftPosition}%`;
      }

      gsap.to(img, {
        y: Math.random() * 200 - 100,
        scale: 1,
        opacity: 1,
        left: `${leftPosition}%`,
        ease: 'elastic.out(1, 0.75)',
        scrollTrigger: {
          trigger: `.trigger-${index}`,
          start: 'bottom bottom',
          end: 'bottom top',
          scrub: true,
          // markers: true,
        },
      });
    });
  });
</script>

<div
  class="scroll-container"
  bind:this={container}
>
  <div class="h-screen top-0w-full"></div>
  <div class="trigger h-[200vh] w-full absolute -bottom-0" />
  <div class="h-screen w-full" />
  {#each images as src, i}
    <div class={`trigger-${i} h-16 w-full mb-32 `}></div>

    <img
      {src}
      alt={`image ${i + 1}`}
      class={`img img-${i}`}
    />
  {/each}

  <div
    class="text-overlay text-white"
    bind:this={title}
  >
    Chronicle of Meme
  </div>
</div>

<style>
  .scroll-container {
    position: relative;
  }

  .img {
    position: fixed;
    bottom: 10%;
    scale: 70%;
    opacity: 0;
    transform-origin: bottom center;
    width: auto;
    height: 30vh;
    max-width: 40vw;

    filter: drop-shadow(6px 0 0 white) drop-shadow(-6px 0 0 white) drop-shadow(0 6px 0 white)
      drop-shadow(0 -6px 0 white);
  }

  /* .img-0 {
    bottom: 0%;
    left: 20%;
    scale: 2;
    opacity: 1;
  } */

  .text-overlay {
    position: fixed;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 2rem;
    font-weight: bold;
    z-index: 10;
    opacity: 0;
  }
</style>
