<script lang="js">
  import Header from '../components/Header.svelte';
  import Footer from '../components/Footer.svelte';

  import Origin from '../components/history/Origin.svelte';
  import CircleTransition from '../components/history/CircleTransition.svelte';
  import SlideTransition from '../components/history/SlideTransition.svelte';
  import Intro from '../components/history/Intro.svelte';
  import S90 from '../components/history/90s.svelte';
  import Timeline from '../components/history/Timeline.svelte';
  import Pc from '../components/retro/pc.svelte';
  import Youtube from '../components/retro/youtube.svelte';
  import AlignmentChart from '../components/AlignmentChart.svelte';
  import gsap from 'gsap';
  import {onMount} from 'svelte';

  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  gsap.registerPlugin(ScrollTrigger);

  onMount(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        start: 'top bottom+=60%',
        end: '+=600',
        scrub: true,
        // markers: true,
        trigger: '#alignment_trigger',
        toggleActions: 'play none none reverse',
      },
    })
    tl.to('.header', {
      opacity: 0,
      translateY: -60,
    }).to("#home-bg", {
      backgroundColor: "white"
    })
  })
</script>

<!-- <Ball /> -->

<Header />

<div class="font-routedgothic">
  <div
    id="home-bg"
    class="h-screen fixed top-0 bg-[#FFCA58] w-full"
  ></div>
  <Timeline />
  <Intro />
  <div class="h-[100vh] opacity-0" />
  <div
    id="alignment_trigger"
    class="h-[120vh] opacity-0"
  />

  <SlideTransition
    id="alignment_chart_wrapper"
    triggerElement={'#alignment_trigger'}
    duration={5}
    color="white"
  >
    <AlignmentChart />
  </SlideTransition>

  <div id="history">
    <Origin />
    <CircleTransition
      triggerElement={'#the_selfish_gene'}
      duration={5}
      color="white"
    >
      <Pc />
    </CircleTransition>

    <S90 />
    <SlideTransition
      id="youtube_wrapper"
      triggerElement={'#early_internet_memes'}
      duration={5}
      color="white"
    >
      <Youtube />
    </SlideTransition>
    <section
      id="rise_of_video_and_social_media_memes"
      class="section"
    >
      <div class="flex flex-col items-center">
        <h1 class="text-5xl font-bold mb-16">Millennium</h1>

        <p>I RUN OUT OF MY IMAGINATION</p>

        <p>SO MISERABLE</p>
      </div>
    </section>
    <section
      id="meme_explosion_and_emojis"
      class="section"
    >
      <h2>4</h2>
      <p>4...</p>
    </section>

    <section
      id="short_form_video_meme_culture"
      class="section"
    >
      <h2>5</h2>
      <p>5...</p>
    </section>

    <section
      id="revival_and_cross_platform_memes"
      class="section"
    >
      <h2>6</h2>
      <p>6...</p>
    </section>

    <section
      id="future_of_memes"
      class="section"
    ></section>
  </div>
</div>
<section class="section"></section>
<Footer />

<style>
  .section {
    position: relative;
    min-height: 200vh;
    z-index: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
</style>
