<script>
  import {onMount, onDestroy} from 'svelte';
  import {gsap} from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  gsap.registerPlugin(ScrollTrigger);
  export let triggerElement;
  export let duration = 10;
  export let color = '#3498db';
  let clipContainer;
  let container;

  let circleSize = 0;
  onMount(() => {
    if (!triggerElement) return;

    let tl = gsap
      .timeline({
        scrollTrigger: {
          trigger: triggerElement,
          start: '60% bottom',
          end: `+=${duration * 50}%`,
          scrub: true,
          // pin: triggerElement,
          // markers: true,
          toggleActions: 'play none none reverse',
          onUpdate: (self) => {
            // Update the circle size based on scroll progress
            circleSize = self.progress * 300;
            if (clipContainer) {
              clipContainer.style.clipPath = `circle(${circleSize}% at 0% 100%)`;
            }
          },
        },
      })
      .to(container, {
        position: 'fixed',
      });
  });
  onDestroy(() => {
    ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
  });
</script>

<div
  class="wrapper"
  bind:this={container}
>
  <div
    bind:this={clipContainer}
    class="clip-container"
    style="background-color: {color}; clip-path: circle(0% at 0% 100%);"
  >
    <div class="relative">
      <slot></slot>
    </div>
  </div>
</div>

<style>
  .wrapper {
    left: 0;
    top: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 0;
  }

  .clip-container {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
