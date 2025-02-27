<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Gene from '../../assets/imgs/the_selfish_gene.jpg';
  gsap.registerPlugin(ScrollTrigger);

  let container;

  onMount(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: container,
        start: 'top top',
        end: 'bottom center',
        scrub: 1,
        pin: true,
        markers: false,
      },
    });

    tl.fromTo('.book', {rotate: 0, scale: 0.8, x: '-30%'}, {rotate: -5, scale: 1.2, x: '-15%', duration: 2});

    tl.fromTo('.title', {opacity: 0, y: 30, scale: 0.8}, {opacity: 1, y: -60, scale: 1.2, duration: 1.5}, '<');

    tl.fromTo('.quote', {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: 1.5});

    tl.fromTo('.author', {opacity: 0}, {opacity: 1, duration: 1});
  });
</script>

<div
  class="h-screen relative font-routedgothic"
  bind:this={container}
>
  <div class="text-gray-700 mx-auto w-[60%] h-screen flex justify-between items-center">
    <img
      alt="the_selfish_gene"
      src={Gene}
      class="book w-64 h-96 rounded relative shadow-lg"
    />

    <div class="w-3/5">
      <h2 class="title text-5xl font-bold mb-6">«The Selfish Gene»</h2>
      <p class="quote text-lg leading-relaxed mb-4">
        The survival value of the God meme in the meme pool results from its great psychological appeal.
      </p>
      <p class="author text-base text-right italic">- Richard Dawkins</p>
    </div>
  </div>
</div>
