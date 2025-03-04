<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Gene from '../../assets/imgs/the_selfish_gene.jpg';
  import Line from './Line.svelte';
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

    tl.fromTo(
      '.book',
      {scale: 0.8, x: '-30%', rotateX: '10deg', rotateY: '0deg'},
      {scale: 1.2, x: '-15%', rotateX: '-0.2deg', rotateY: '12deg', rotateZ: -5, zIndex: 10},
    ).to('.desc', {
      opacity: 1,
      ease: 'power1.out',
    });
    tl.fromTo('.title', {opacity: 0, y: 30, scale: 0.5}, {opacity: 1, y: -60, scale: 1, duration: 1.5}, '<');
    tl.fromTo('.quote', {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: 1.5});
    tl.fromTo('.author', {opacity: 0}, {opacity: 1, duration: 1})
      .to('.book', {
        scale: 5,
        rotate: '75deg',
        duration: 10,
      })
      .to(
        '#home-bg',
        {
          backgroundColor: '#6AAC5F',
          duration: 6,
        },
        '-=4',
      );
  });
</script>

<div
  bind:this={container}
  id="the_selfish_gene"
>
  <div class="text-yellow-700 mx-auto w-[60%] h-screen flex gap-12 justify-between items-center">
    <div class="relative z-10">
      <Book image={Gene} />
      <div class=" -z-10 desc absolute opacity-0 left-[80%] translate-x-12 w-[40vw] flex items-center gap-3">
        <div class="w-16 h-16 rotate-[160deg]">
          <Line />
        </div>
        <div class="translate-y-6">
          The meme first appeared in Richard Dawkins’ first book, “The Selfish Gene” (1976), and was an attempt to
          understand why some behaviours, from an evolutionary perspective, seemed to make no sense but, somehow or
          other, were found to be very common in human societies.
        </div>
      </div>
    </div>
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
