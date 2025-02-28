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

  onMount(() => {
    const imgElements = container.querySelectorAll('.img');

    imgElements.forEach((img, index) => {
      const leftPosition = (index / (imgElements.length - 1)) * 80;
      img.style.left = `${leftPosition}%`;

      gsap.to(img, {
        y: Math.random() * 200 - 100,
        scale: 1,
        opacity: 1,
        duration: 1.2,
        ease: 'elastic.out(1, 0.75)',
        scrollTrigger: {
          trigger: `.trigger-${index}`,
          start: 'top 80%',
          end: 'bottom 60%',
          scrub: 0.5,
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
  {#each images as src, i}
    <div class={`trigger-${i} h-48 w-full my-32`}></div>

    <img
      {src}
      alt={`image ${i + 1}`}
      class="img"
    />
  {/each}

  <div class="text-overlay">Chronicle of Meme</div>
</div>

<style>
  .scroll-container {
    position: relative;
    height: 100vh;
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
  }

  .text-overlay {
    position: fixed;
    top: 10%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 2rem;
    font-weight: bold;
    color: black;
    z-index: 10;
  }
</style>
