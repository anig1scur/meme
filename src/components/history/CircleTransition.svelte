<script>
  import {onMount, onDestroy} from 'svelte';
  import {gsap} from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  export let triggerElement;
  export let duration = 10;
  export let color = '#3498db';

  let circle;

  onMount(() => {
    if (!triggerElement) return;

    let tl = gsap.timeline({
      scrollTrigger: {
        trigger: triggerElement,
        start: 'bottom bottom',
        end: `+=${duration * 50}%`,
        scrub: true,
        pin: true,
        toggleActions: 'play none none reverse',
      },
    });
    tl.fromTo(circle, {scale: 0}, {scale: 250, ease: 'power2.inOut'});
  });

  onDestroy(() => {
    ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
  });
</script>

<div
  bind:this={circle}
  class="circle"
  style="background-color: {color};"
></div>

<style>
  .circle {
    position: fixed;
    left: -100px;
    bottom: -100px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    transform: scale(0);
  }
</style>
