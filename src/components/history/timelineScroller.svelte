<script>
  import {onMount} from 'svelte';
  import {gsap} from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  import Head from '$assets/imgs/cat/head.png';
  import Body from '$assets/imgs/cat/body.png';
  import Tail from '$assets/imgs/cat/tail.png';
  gsap.registerPlugin(ScrollTrigger);

  export let timelineData = [];
  export let scrollerRef = null;

  export let catImages = {
    head: Head,
    body: Body,
    tail: Tail,
  };

  timelineData = timelineData.map((item, idx) => ({...item, idx}));

  let activeSegment = timelineData[0]?.id;
  let activeIdx = 0;
  let indicatorHeight = 0;
  let scrollTriggers = [];
  let currentProgress = 0;

  function handleSegmentClick(segment) {
    const targetElement = document.getElementById(segment.id);
    if (targetElement) {
      gsap.to(window, {
        duration: 1,
        scrollTo: {
          y: targetElement,
          offsetY: 0,
        },
        ease: 'power2.inOut',
      });
    }
  }

  onMount(() => {
    timelineData.forEach((segment, index) => {
      const trigger = ScrollTrigger.create({
        trigger: `#${segment.id}`,
        start: 'top top-=500',
        end: 'bottom top-=500',
        scrub: true,
        onEnter: () => {
          activeSegment = segment.id;
          activeIdx = segment.idx;
        },
        onEnterBack: () => {
          activeSegment = segment.id;
          activeIdx = segment.idx;
        },
        onUpdate: (self) => {
          if (self.isActive) {
            const progress = self.progress;
            indicatorHeight = ((segment.idx + progress) / timelineData.length) * 100;
            currentProgress = progress;
          }
        },
      });
      scrollTriggers.push(trigger);
    });

    return () => {
      scrollTriggers.forEach((trigger) => trigger.kill());
    };
  });
</script>

<div
  bind:this={scrollerRef}
  class="timeline-container"
>
  {#each timelineData as segment, index}
    <div
      class="cat-segment"
      on:click={() => handleSegmentClick(segment)}
    >
      {#if index === 0}
        <img
          src={catImages.head}
          class="cat-image"
          alt="Cat Head"
        />
      {/if}

      {#if index > 0 && index < timelineData.length - 1}
        <img
          src={catImages.body}
          class="cat-image"
          alt="Cat Body"
        />
      {/if}

      {#if index === timelineData.length - 1}
        <img
          src={catImages.tail}
          class="cat-image"
          alt="Cat Tail"
        />
      {/if}

      {#if index === 0}
        <div
          class="progress-indicator"
          style="height: {indicatorHeight}%"
        ></div>
      {/if}
    </div>
  {/each}
</div>

<style>
  .timeline-container {
    position: fixed;
    right: -120px;
    top: 20%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 50;
  }

  .cat-segment {
    width: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .cat-image {
    width: 100%;
    height: auto;
    object-fit: contain;
  }

  .progress-indicator {
    position: absolute;
    right: 0px;
    width: 5px;
    background-color: gainsboro;
    transition: height 0.3s ease-in-out;
  }
</style>
