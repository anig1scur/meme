<script>
  import {onMount} from 'svelte';
  import {gsap} from 'gsap';
  import {ScrollTrigger} from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  export let timelineData = [];

  let activeSegment = timelineData[0]?.id;
  let indicatorPosition = 0;
  let scrollTriggers = [];

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
        start: 'top center',
        end: 'bottom center',
        onEnter: () => {
          activeSegment = segment.id;
        },
        onEnterBack: () => {
          activeSegment = segment.id;
        },
        onUpdate: (self) => {
          if (self.isActive) {
            if (index < timelineData.length - 1) {
              const nextPos = timelineData[index + 1].position;
              const currentPos = segment.position;
              const progress = self.progress;
              indicatorPosition = currentPos + (nextPos - currentPos) * progress;
            } else {
              indicatorPosition = segment.position;
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

<div class="flex relative w-full h-full">
  <div class="flex-1 overflow-y-auto pr-20">
    <slot></slot>
  </div>

  <div class="fixed right-5 top-1/2 -translate-y-1/2 h-4/5 w-16 flex flex-col items-center">
    <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-white -translate-x-1/2"></div>
    <div
      class="absolute left-1/2 w-3 h-3 rounded-full bg-orange-500 -translate-x-1/2 -translate-y-1/2 z-10 transition-all duration-300 ease-in-out"
      style="top: {indicatorPosition}%"
    ></div>

    {#each timelineData as segment}
      <div
        class="absolute left-0 w-full -translate-y-1/2 flex items-center cursor-pointer transition-all duration-300 ease-in-out"
        style="top: {segment.position}%"
        on:click={() => handleSegmentClick(segment)}
      >
        <div
          class={`w-2 h-2 rounded-full mx-2.5 transition-all duration-300 ease-in-out ${segment.id === activeSegment ? 'w-3 h-3 bg-purple-600' : 'bg-gray-500'}`}
        ></div>
        <div
          class={`text-sm transition-all duration-300 ease-in-out ${segment.id === activeSegment ? 'font-bold text-gray-800' : 'text-gray-500'} hover:text-gray-800`}
        >
          {segment.title}
        </div>
      </div>
    {/each}
  </div>
</div>
