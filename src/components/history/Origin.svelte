<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Gene from '../../assets/imgs/the_selfish_gene.jpg';
  import Line from '../misc/Line.svelte';
  import Book from '../misc/Book.svelte';
  import Title from '../misc/Title.svelte';
  import MemeToDNA from '../animation/MemeToDNA.svelte';

  gsap.registerPlugin(ScrollTrigger);

  let container;

  onMount(() => {
    ScrollTrigger.create({
      trigger: container,
      start: 'top top',
      end: '+=300%',
      pin: true,
      // markers: true,
    });

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: container,
        start: 'top top',
        end: 'bottom top',
        scrub: true,
        // markers: true,
      },
    });

    gsap
      .timeline({
        scrollTrigger: {
          trigger: '.book',
          start: 'top bottom',
          end: 'top top',
          scrub: true,
          // markers: true,
          // pin: true,
        },
      })
      .to('.dna', {
        scale: 1.6,
        rotate: '30deg',
        translateY: 300,
      })
      // .to('#home-bg', {
      //   backgroundColor: '#FFCA58',
      //   duration: 3,
      // })

      .fromTo('.book', {scale: 0.7, rotateX: '3deg', rotateY: '-25deg'}, {scale: 1, rotateX: '0deg', rotateY: '12deg'})
      .to('.desc', {
        opacity: 1,
        ease: 'power1.out',
      });

    tl.fromTo(
      '.title',
      {translateX: 25, opacity: 0, y: 30, scale: 0.5},
      {translateX: -25, opacity: 1, y: -60, scale: 1, duration: 1.5},
      '<',
    )
      .fromTo('.quote', {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: 1.5}, '=')
      .fromTo('.author', {opacity: 0}, {opacity: 1, duration: 1});
  });
</script>

<div
  id="the_selfish_gene"
  class="relative"
>
  <MemeToDNA />
  <div class="h-36" />
  <div
    bind:this={container}
    class="text-[#768C3A] w-[80%] mx-auto h-screen flex gap-24 justify-center items-center pb-12"
  >
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

    <div class=" text-[#768C3A] font-georgia flex flex-col items-end max-w-xl">
      <Title
        className="title text-[#768C3A5a]"
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
