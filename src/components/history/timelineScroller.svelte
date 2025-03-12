<script>
  import {onMount} from 'svelte';
  import {gsap} from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';
  gsap.registerPlugin(ScrollTrigger);

  export let timelineData = [];
  export let scrollerRef = null;

  // Add idx property to each timeline item
  timelineData = timelineData.map((item, idx) => ({...item, idx}));

  let activeSegment = timelineData[0]?.id;
  let activeIdx = 0;
  let indicatorPosition = 0;
  let scrollTriggers = [];
  let currentProgress = 0;

  function handleSegmentClick(segment) {
    const targetElement = document.getElementById(segment.id);
    // if (targetElement) {
    //   gsap.to(window, {
    //     duration: 1,
    //     scrollTo: {
    //       y: targetElement,
    //       offsetY: 0,
    //     },
    //     ease: 'power2.inOut',
    //   });
    // }
  }

  onMount(() => {
    timelineData.forEach((segment, index) => {
      const trigger = ScrollTrigger.create({
        trigger: `#${segment.id}`,
        start: 'top center',
        end: 'bottom center',
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
            if (index < timelineData.length - 1) {
              const nextPos = timelineData[index + 1].position;
              const currentPos = segment.position;
              const progress = self.progress;
              indicatorPosition = currentPos + (nextPos - currentPos) * progress;
              currentProgress = progress;
            } else {
              indicatorPosition = segment.position;
              currentProgress = self.progress;
            }
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
  class="z-50 fixed right-5 top-1/2 -translate-y-1/2 h-4/5 w-16 flex flex-col items-center translate-x-full opacity-0"
>
  {#each timelineData as segment, index}
    <div
      class="relative flex flex-col items-center my-1 gap-2"
      style="height: {index === timelineData.length - 1
        ? 'auto'
        : `${timelineData[index + 1].position - segment.position}%`}"
    >
      <div
        class="relative cursor-pointer transition-all duration-300 ease-in-out"
        on:click={() => handleSegmentClick(segment)}
      >
        <div
          class={`w-3 h-3 rounded-full transition-all duration-300 ease-in-out border-[1px] border-black
          ${segment.id !== activeSegment ? 'bg-[#85D6FF]' : 'bg-[#FE7B7B]'}
          `}
          style="transform: scale({segment.id === activeSegment ? 1.5 : 1})"
        ></div>
      </div>
      <div
        class="absolute left-5 -top-1 text-md transition-all duration-300 ease-in-out whitespace-nowrap"
        class:font-bold={segment.id === activeSegment}
      >
        {segment.title}
      </div>
      {#if index < timelineData.length - 1}
        <div class="flex-1 w-full flex items-center justify-center">
          <div
            class={`relative w-2 h-full rounded-full ${segment.idx > activeIdx ? '' : 'bg-[#85D6FF]'} border-[1.5px] border-black overflow-hidden`}
          >
            <div
              class={`absolute left-0 top-0 w-full ${segment.id === activeSegment ? 'bg-[#FE7B7B]' : 'opacity-0'} transition-all duration-300 ease-in-out`}
              style="height: {segment.id === activeSegment
                ? `${currentProgress * 100}%`
                : segment.idx > activeIdx
                  ? '0%'
                  : '100%'}"
            ></div>
          </div>
        </div>
      {/if}
    </div>
  {/each}
</div>
