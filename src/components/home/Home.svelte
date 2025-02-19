<script lang="ts">
  import CursorFollower from '../CursorFollower.svelte';
  import {onMount} from 'svelte';

  let memeData = [];

  const colors = [
    'text-pink-500',
    'text-blue-500',
    'text-yellow-500',
    'text-green-500',
    'text-red-500',
    'text-purple-500',
    'text-cyan-500',
    'text-orange-500',
  ];

  function randomItalic() {
    return Math.random() < 0.4 ? 'italic' : '';
  }

  function randomBold() {
    return Math.random() < 0.4 ? 'font-semibold' : '';
  }

  function randomColor() {
    return Math.random() < 0.5 ? colors[Math.floor(Math.random() * colors.length)] : '';
  }

  function randomFontSize(baseSize = 16) {
    return `text-[${baseSize + Math.floor(Math.random() * 4)}px]`;
  }

  function highlightRandomWords(text: string) {
    const words = text.split(' ');
    return words
      .map((word) => (Math.random() < 0.2 ? `<span class="${randomColor()} ${randomItalic()}">${word}</span>` : word))
      .join(' ');
  }

  function randomChar() {
    const arrows = ['⬅⚫', '☟', 'ツ', '︶︶︶︶', '𓆩⟡𓆪', '✮', '☃', '✹', '‰', '❑', '◪', '🦋⃤♡⃤'];
    return Math.random() < 0.6 ? arrows[Math.floor(Math.random() * arrows.length)] : '';
  }

  function randomRotation() {
    return `rotate(${Math.floor(Math.random() * 20)}deg)`;
  }

  function randomGraffiti() {
    const graffitiTypes = [
      `<svg width="40" height="40" style="transform:${randomRotation()}" class="absolute left-[50%] -z-10"><circle cx="20" cy="20" r="10" stroke="#222" stroke-width="2" fill="none"/></svg>`,
      `<svg width="50" height="50" style="transform:${randomRotation()}" class="absolute left-[50%] -z-10"><polygon points="25,5 35,40 5,15 45,15 15,40" stroke="#333" stroke-width="2" fill="none"/></svg>`,
      `<svg width="100" height="40" style="transform:${randomRotation()}" class="absolute left-[50%] -z-10"><path d="M10,30 Q50,-10 90,30" stroke="#444" stroke-width="2" fill="none"/></svg>`,
      `<svg width="40" height="40" style="transform:${randomRotation()}" class="absolute left-[50%] -z-10"><rect x="10" y="10" width="20" height="20" stroke="#555" stroke-width="2" fill="none"/></svg>`,
      `<svg width="40" height="40" style="transform:${randomRotation()}" class="absolute left-[50%] -z-10"><ellipse cx="20" cy="20" rx="15" ry="10" stroke="#666" stroke-width="2" fill="none"/></svg>`,
    ];
    return Math.random() < 0.5 ? graffitiTypes[Math.floor(Math.random() * graffitiTypes.length)] : '';
  }

  onMount(async () => {
    const response = await fetch('/meme_details.json');
    memeData = await response.json();
    console.log(memeData);
  });
</script>

{#if !navigator.userAgent.includes('Mobile')}
  <CursorFollower />
{/if}

<div
  class="font-routedgothic mt-12 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-2 md:gap-4 p-2 md:p-6 overflow-x-hidden"
>
  {#each Array(5) as _, index}
    <div class="flex flex-col">
      {#each memeData.filter((_, i) => i % 5 === index) as meme}
        <div class="h-fit relative">
          <img
            src={'top50/images/' + meme.image}
            alt={meme.name}
            class="w-full h-auto object-cover mb-2"
          />
          <div class="pb-8 relative">
            <h3 class={'text-xl font-semibold text-gray-800 flex items-center' + randomFontSize(18)}>
              <span class={randomColor() + ' ' + randomItalic() + ' ' + randomBold()}>{meme.name}</span>
              <span class="ml-2">{randomChar()}</span>
            </h3>
            {#if meme.about}
              <p class="text-gray-600 mt-2 relative text-base">
                {@html highlightRandomWords(meme.about)}
                {@html randomGraffiti()}
              </p>
            {/if}
            <p class="mt-4 text-sm text-gray-500">{meme.year} &nbsp; | &nbsp; {meme.origin}</p>
            <p class="mt-2 text-sm font-semibold">{meme.type}</p>
            <a
              href={meme.imgflip}
              target="_blank"
              class="text-pink-500 hover:underline mt-2 block"
            >
              Imgflip
            </a>
            <a
              href={meme.link}
              target="_blank"
              class="text-pink-500 hover:underline mt-2 block"
            >
              Know your meme
            </a>
          </div>
        </div>
      {/each}
    </div>
  {/each}
</div>
