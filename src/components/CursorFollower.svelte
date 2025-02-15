<script>
  import {onMount} from 'svelte';
  import {gsap} from 'gsap';

  let text = 'WOAIMEME';
  let characters = text.split('');
  let spans = [];
  let positions = Array.from({length: characters.length}, () => ({
    x: window.innerWidth / 2,
    y: window.innerHeight / 2,
  }));

  const spacing = 20;
  let mouse = {x: window.innerWidth / 2, y: window.innerHeight / 2};

  onMount(() => {
    const handleMouseMove = (event) => {
      mouse.x = event.clientX;
      mouse.y = event.clientY;
    };

    window.addEventListener('mousemove', handleMouseMove);
    gsap.ticker.add(updatePositions);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      gsap.ticker.remove(updatePositions);
    };
  });

  function updatePositions() {
    positions[0].x += (mouse.x - positions[0].x) * 0.2;
    positions[0].y += (mouse.y - positions[0].y) * 0.2;

    for (let i = 1; i < positions.length; i++) {
      let prev = positions[i - 1];
      let curr = positions[i];

      let angle = Math.atan2(prev.y - curr.y, prev.x - curr.x);

      curr.x = prev.x - Math.cos(angle) * spacing;
      curr.y = prev.y - Math.sin(angle) * spacing;
    }

    spans.forEach((span, i) => {
      let curr = positions[i];
      span.style.transform = `translate(${curr.x}px, ${curr.y}px)`;
    });
  }
</script>

<div class="fixed font-routedgothic text-xl pointer-events-none">
  {#each characters as char, i}
    <span
      bind:this={spans[i]}
      style="position: absolute;">{char}</span
    >
  {/each}
</div>
