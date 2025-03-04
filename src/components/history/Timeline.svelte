<script>
  import TimelineScroller from './timelineScroller.svelte';
  import {onMount} from 'svelte';
  import gsap from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  const timelineData = [
    {id: 'the_selfish_gene', desc: 'The Selfish Gene', title: '1976', position: 0},
    {id: 'early_internet_memes', desc: 'Early Internet Memes', title: '1990', position: 10},
    {
      id: 'rise_of_video_and_social_media_memes',
      desc: 'Rise of Video & Social Media Memes',
      title: '2000',
      position: 20,
    },
    {id: 'meme_explosion_and_emojis', desc: 'Meme Explosion & Emojis', title: '2010', position: 40},
    {id: 'short_form_video_meme_culture', desc: 'Short-Form Video Meme Culture', title: '2015', position: 60},
    {id: 'revival_and_cross_platform_memes', desc: 'Revival & Cross-Platform Memes', title: '2020', position: 80},
    {id: 'future_of_memes', title: 'now', position: 100},
  ];

  export let triggerElementId = 'history';

  let scroller;

  onMount(() => {
    gsap.to(scroller, {
      x: '-100%',
      duration: 1,
      opacity: 1,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: `#${triggerElementId}`,
        start: 'top top',
        end: 'bottom 30%',
        toggleActions: 'play reverse play reverse',
      },
    });
  });
</script>

<TimelineScroller
  {timelineData}
  bind:scrollerRef={scroller}
/>
