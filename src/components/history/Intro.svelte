<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Title from '$assets/imgs/chronicle_of_meme.png';

  gsap.registerPlugin(ScrollTrigger);

  const characters = Object.values(
    import.meta.glob(['$assets/imgs/characteristic/**.svg'], {
      eager: true,
      as: 'url',
    }),
  );

  const figures = Object.values(
    import.meta.glob(['$assets/imgs/intro/**.jpg', '$assets/imgs/intro/**.png'], {
      eager: true,
      as: 'url',
    }),
  );

  let container;

  onMount(() => {
    const charElements = container.querySelectorAll('.char');
    const titleElement = container.querySelector('.title-char');

    const updatePositions = () => {
      const windowWidth = window.innerWidth;
      const scaleFactor = windowWidth < 768 ? 0.8 : 1;
      const topOffset = windowWidth < 768 ? 10 : 0;

      const verticalSpacing = windowWidth < 768 ? 12 : 8;
      const verticalSpacingRight = windowWidth < 768 ? 18 : 5;

      for (let i = 0; i < 3; i++) {
        const char = charElements[i];
        gsap.set(char, {
          left: `${i * 15}%`,
          top: `${70 + (i - 1) * verticalSpacing - topOffset}vh`,
          width: `clamp(150px, ${15 * scaleFactor}vw, 240px)`,
        });
      }

      for (let i = 3; i < 6; i++) {
        const char = charElements[i];
        gsap.set(char, {
          right: `${5 + (i - 3) * 15}%`,
          top: `${65 + (i - 3) * verticalSpacingRight - topOffset}vh`,
          width: `clamp(150px, ${15 * scaleFactor}vw, 240px)`,
        });
      }
    };

    updatePositions();

    gsap.to(titleElement, {
      scrollTrigger: {
        trigger: container,
        start: 'top top',
        end: '+=600',
        scrub: true,
        // markers: true,
      },
      y: '-15vh',
      scale: 0.7,
      ease: 'power1.out',
    });

    // Animate all characters up and fade out
    charElements.forEach((char) => {
      gsap.to(char, {
        scrollTrigger: {
          trigger: container,
          start: 'top top',
          end: '+=400',
          scrub: true,
          // markers: true,
        },
        y: '-40vh',
        scale: 0.7,
        rotate: (Math.random() * 2 - 1) * 20,
        ease: 'power1.out',
      });
    });

    window.addEventListener('resize', updatePositions);

    return () => {
      window.removeEventListener('resize', updatePositions);
    };
  });

  onMount(() => {
    gsap.to(container, {
      scrollTrigger: {
        trigger: container,
        start: '95% center',
        end: 'bottom top',
        scrub: true,
        // markers: true,
      },
      opacity: 0,
      ease: 'power1.out',
    });
  });

  onMount(() => {
    const figureElements = container.querySelectorAll('.figure');
    figureElements.forEach((fig, index) => {
      const leftPosition = (index / (figureElements.length - 1)) * 80;
      fig.style.left = `${leftPosition}%`;

      gsap.to(fig, {
        y: Math.random() * 100 - 100,
        scale: 1,
        opacity: 1,
        left: `${leftPosition}%`,
        ease: 'power2.in',
        scrollTrigger: {
          trigger: `.trigger-${index}`,
          start: 'top top',
          end: 'bottom top',
          scrub: true,
          // markers: true,
        },
      });
    });
  });
</script>

<div
  id="intro"
  class="relative h-[250vh]"
  bind:this={container}
>
  <div class="relative">
    <img
      src={Title}
      class="title-char w-[80%] mt-[15vh] md:mt-[30vh] mx-auto md:w-[75%] h-auto fixed left-0 right-0"
    />
  </div>
  <div
    class="c1 fixed -left-[12.5%] top-[60vh] md:top-[70vh] h-[70vh] w-[110vw] rounded-[50%] bg-gradient-to-b from-[#fff4dd] to-[#e4b040] bg-[linear-gradient(90deg, #fff4dd 0.00%, #e4b040 100.00%)]"
  />
  <div
    class="c2 fixed top-[50vh] md:top-[60vh] left-[50%] h-[60vh] w-[70vw] right-0 rounded-[50%] bg-gradient-to-r from-[#22c55d] to-[#adff81] bg-[linear-gradient(-2deg, #22c55d 0.00%, #adff81 100.00%)]"
  />

  {#each characters as src, i}
    <img
      {src}
      alt={`char ${i}`}
      class={`char char-${i} fixed h-auto z-10`}
    />
  {/each}
  <div class="h-16" />
  {#each figures as src, i}
    <div class={`trigger-${i} h-16 w-full mt-16`}></div>
    <img
      {src}
      alt={`figure ${i}`}
      class={`figure figure-${i}`}
    />
  {/each}
</div>

<style>
  .figure {
    position: fixed;
    bottom: 0;
    scale: 0.75;
    opacity: 0;
    width: auto;
    height: 30vh;
    max-width: 40vw;

    filter: drop-shadow(6px 0 0 white) drop-shadow(-6px 0 0 white) drop-shadow(0 6px 0 white)
      drop-shadow(0 -6px 0 white);
  }
</style>
