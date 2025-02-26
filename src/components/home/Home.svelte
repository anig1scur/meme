<script lang="ts">
  import CursorFollower from '../CursorFollower.svelte';
  import {onMount} from 'svelte';

  let memeData = [];
  let commonWords = [
    'to',
    'get',
    'it',
    'a',
    'is',
    'the',
    'and',
    'of',
    'in',
    'for',
    'that',
    'this',
    'on',
    'with',
    'by',
    'at',
    'from',
    'be',
    'as',
    'an',
    'are',
    'was',
    'were',
    'been',
    'have',
    'has',
    'had',
    'do',
    'does',
    'did',
    'can',
    'could',
    'will',
    'would',
    'should',
    'may',
    'might',
    'must',
    'shall',
    'their',
    'they',
    'he',
    'she',
    'his',
    'her',
    'them',
    'its',
    'our',
    'your',
    'but',
    'or',
    'one',
    'if',
    'not',
    'am',
  ];

  const commonWordsSet = new Set(commonWords);

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
      .map((word) => {
        const cleanWord = word.toLowerCase().replace(/[^\w]/g, '');
        if (commonWordsSet.has(cleanWord) || Math.random() >= 0.4) {
          return word;
        }
        return `<span class="${randomColor()} ${randomItalic()}">${word}</span>`;
      })
      .join(' ');
  }

  function randomChar() {
    const arrows = ['☟', 'ツ', '︶︶︶︶', '©', '𓆩⟡𓆪', '✮', '☃', '✹', '‰', '❑', '◪', '🦋⃤♡⃤'];
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

  let customizedMeme = {};

  function getCustomizedMeme(meme) {
    const id = meme.image || meme.name;
    if (!customizedMeme[id]) {
      customizedMeme[id] = {
        highlightedAbout: meme.about ? highlightRandomWords(meme.about) : '',
        randomGraffiti: randomGraffiti(),
        randomChar: randomChar(),
        fontSize: randomFontSize(18),
        nameColor: randomColor(),
        nameItalic: randomItalic(),
        nameBold: randomBold(),
      };
    }
    return customizedMeme[id];
  }

  let observer;

  function setupIntersectionObserver() {
    observer = new IntersectionObserver((entries) => {}, {
      root: null,
      rootMargin: '200px',
      threshold: 0.01,
    });
  }

  let loadedMemes = [];
  let pageSize = 20;
  let currentPage = 0;

  function loadMoreMemes() {
    const startIndex = currentPage * pageSize;
    const endIndex = startIndex + pageSize;
    const newMemes = memeData.slice(startIndex, endIndex);

    if (newMemes.length > 0) {
      loadedMemes = [...loadedMemes, ...newMemes];
      currentPage++;
    }
  }

  onMount(async () => {
    setupIntersectionObserver();

    const response = await fetch('/meme_details.json');
    memeData = await response.json();

    loadMoreMemes();

    const scrollHandler = () => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
        loadMoreMemes();
      }
    };

    window.addEventListener('scroll', scrollHandler);

    return () => {
      window.removeEventListener('scroll', scrollHandler);
      observer.disconnect();
    };
  });

  function handleElementVisible(node, meme) {
    const id = meme.image || meme.name;
    node.dataset.memeId = id;
    observer.observe(node);

    return {
      destroy() {
        observer.unobserve(node);
      },
    };
  }
</script>

{#if !navigator.userAgent.includes('Mobile')}
  <CursorFollower />
{/if}

<div
  class="font-routedgothic mt-12 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-2 md:gap-4 p-2 md:p-6 overflow-x-hidden"
>
  {#each Array(5) as _, index}
    <div class="flex flex-col">
      {#each loadedMemes.filter((_, i) => i % 5 === index) as meme}
        {@const customize = getCustomizedMeme(meme)}
        <div
          class="h-fit relative"
          use:handleElementVisible={meme}
        >
          <img
            loading="lazy"
            src={'top/images/' + meme.image}
            alt={meme.name}
            class="w-full h-auto object-cover mb-2 aspect-auto"
          />
          <div class="pb-8 relative">
            <h3 class={'text-xl font-semibold text-gray-800 flex items-center ' + customize.fontSize}>
              <span class={customize.nameColor + ' ' + customize.nameItalic + ' ' + customize.nameBold}
                >{meme.name}</span
              >
              <span class="ml-2">{customize.randomChar}</span>
            </h3>
            {#if meme.about}
              <p class="text-gray-600 mt-2 relative text-base">
                {@html customize.highlightedAbout}
                {@html customize.randomGraffiti}
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
