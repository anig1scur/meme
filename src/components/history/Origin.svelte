<script>
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Gene from '../../assets/imgs/the_selfish_gene.jpg';
  import Line from './Line.svelte';
  import Book from './Book.svelte';
  import Title from './Title.svelte';
  import MemeToDNA from '../animation/meme_to_DNA.svelte';

  gsap.registerPlugin(ScrollTrigger);

  let container;

  onMount(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: container,
        start: 'top top',
        end: 'bottom top',
        scrub: true,
        pin: true,
        // markers: true,
      },
    });

    gsap
      .timeline({
        scrollTrigger: {
          trigger: '.book',
          start: 'top 80%',
          end: 'top top',
          scrub: true,
          // pin: true,
          // markers: true,
        },
      })
      .to('.dna', {
        scale: 1.4,
        rotate: '25deg',
        translateY: -30,
      })
      .fromTo(
        '.book',
        {delay: 0, scale: 0.7, rotateX: '3deg', rotateY: '-25deg'},
        {scale: 1, rotateX: '0deg', rotateY: '12deg'},
      )
      .to('.desc', {
        opacity: 1,
        ease: 'power1.out',
      });

    // gsap.set( '#home-bg', {
    //   delay:0,
    //   background:"linear-gradient(to top, #FFF8EA 0%,#FFD16E 47%,#FFCA58 100%)",
    //   // background:"linear-gradient(217deg, #FFCA58, #FFCA58 70.71%),  linear-gradient(127deg, #FFCA58, #FFCA58 70.71%), linear-gradient(336deg, #FFCA58, rgba(0,0,255,0) 70.71%)"
    // })
    tl.fromTo('.title', {opacity: 0, y: 30, scale: 0.5}, {opacity: 1, y: -60, scale: 1, duration: 1.5}, '<');
    tl.fromTo('.quote', {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: 1.5});
    tl.fromTo('.author', {opacity: 0}, {opacity: 1, duration: 1}).to(
      '#home-bg',
      {
        // backgroundColor: "#668960",
        // background:"linear-gradient(to top, #F6FFF5 0%,#B1E6A9 47%,#6AAC5F 100%)",
        duration: 2,
      },
      '-=4',
    );
  });
</script>

<div id="the_selfish_gene">
  <MemeToDNA />
  <div
    bind:this={container}
    class="text-yellow-700 w-[80%] mx-auto h-screen flex gap-24 justify-center items-center"
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

    <div class=" text-yellow-900 font-georgia flex flex-col items-end max-w-xl">
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
