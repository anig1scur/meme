<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Gene from '../../assets/imgs/the_selfish_gene.jpg';
  import Book from './Book.svelte';
  import Title from './Title.svelte';

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
    tl.fromTo('.title', {opacity: 0, y: 30, scale: 0.5}, {opacity: 1, y: -60, scale: 1, duration: 1.5}, '<');
    tl.fromTo('.quote', {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: 1.5});
    tl.fromTo('.author', {opacity: 0}, {opacity: 1, duration: 1});
  });
</script>

<div
  bind:this={container}
  id="origin"
>
  <!-- <div class="font-icon font-semibold absolute right-[10%] h-full z-10">
    <div class="h-full absolute w-0.5 bg-yellow-700"></div>
    <div class="absolute mt-24 ml-2 font-serif text-3xl">1976</div>
  </div> -->
  <div class="text-yellow-700 mx-auto w-[60%] h-screen flex gap-12 justify-between items-center">
    <img
      alt="the_selfish_gene"
      src={Gene}
      class="book w-64 h-96 rounded relative shadow-lg"
    />

    <!-- <Book image={Gene} /> -->

    <div class=" text-yellow-900 font-georgia flex flex-col w-1/2 items-end">
      <Title
        className="title"
        text="The Selfish Gene"
      />
      <p class="quote text-lg break-all leading-relaxed mb-4">
        “The survival value of the God meme in the meme pool results from its great psychological appeal.”
      </p>
      <p class="author text-base text-right italic">- Richard Dawkins</p>
    </div>
  </div>
</div>

<style>
  .stroke {
    filter: drop-shadow(2px 0 0 white) drop-shadow(-2px 0 0 white) drop-shadow(0 2px 0 white)
      drop-shadow(0 -2px 0 white) drop-shadow(3px -2px 0 white);
  }
</style>
