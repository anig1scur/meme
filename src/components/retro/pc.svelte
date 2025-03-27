<script>
  import {onMount} from 'svelte';
  import {draggable} from '@neodrag/svelte';
  import DancingBaby from '../animation/DancingBaby.svelte';
  import Hampster from './hampster.svelte';

  let currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
  let isNotepadOpen = true;
  let isSettingsOpen = false;
  let isPlayerOpen = true;
  let notepadContent =
    'The 90s gave us some of the first viral memes, like Dancing Baby and Hampster Dance, spreading through emails and early websites. Despite slow internet, these simple, quirky animations became digital culture icons, paving the way for modern memes.';
  let isPlaying = false;
  let volume = 50;

  onMount(() => {
    const interval = setInterval(() => {
      currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    }, 1000);

    return () => clearInterval(interval);
  });

  function toggleWindow(windowName) {
    if (windowName === 'notepad') isNotepadOpen = !isNotepadOpen;
    if (windowName === 'settings') isSettingsOpen = !isSettingsOpen;
    if (windowName === 'player') isPlayerOpen = !isPlayerOpen;
  }

  function togglePlay() {
    isPlaying = !isPlaying;
  }
</script>

<div class="min-h-screen bg-zinc-100 flex flex-col w-screen font-vcr">
  <div
    class="w-full h-8 bg-gradient-to-r from-[#D12459] to-[#FFD0DE] flex justify-between items-center px-4 text-white"
  >
    <div class="flex items-center space-x-2">
      <button class="p-3 rounded hover:bg-gray-500">MemeOS</button>
      <button class="p-3 rounded hover:bg-gray-500">File</button>
      <button class="p-3 rounded hover:bg-gray-500">Edit</button>
      <button class="p-3 rounded hover:bg-gray-500">View</button>
    </div>
    <div>{currentTime}</div>
  </div>

  <!-- Desktop -->
  <div class="flex-1 p-4 relative bg-zinc-100 overflow-hidden">
    <!-- Desktop background pattern -->
    <div class="absolute inset-0 grid grid-cols-8 grid-rows-6 opacity-10">
      {#each Array(48) as _, i}
        <div class="border border-pink-300 flex items-center justify-center text-pink-400">
          <span class="text-4xl">♪</span>
        </div>
      {/each}
    </div>

    <!-- Desktop icons -->
    <div class="absolute top-4 left-4 flex flex-col items-center space-y-6">
      <div
        class="flex flex-col items-center cursor-pointer"
        on:click={() => toggleWindow('notepad')}
      >
        <div class="w-12 h-12 bg-white border border-gray-400 flex items-center justify-center">
          <div class="w-8 h-8 bg-gray-100 border-b border-r border-gray-400"></div>
        </div>
        <span class="mt-1 text-sm text-center bg-white px-1">Notepad</span>
      </div>

      <div
        class="flex flex-col items-center cursor-pointer"
        on:click={() => toggleWindow('settings')}
      >
        <div class="w-12 h-12 bg-white border border-gray-400 flex items-center justify-center">
          <div class="w-8 h-8 flex items-center justify-center">
            <span class="text-xl">⚙️</span>
          </div>
        </div>
        <span class="mt-1 text-sm text-center bg-white px-1">Settings</span>
      </div>

      <div
        class="flex flex-col items-center cursor-pointer"
        on:click={() => toggleWindow('player')}
      >
        <div class="w-12 h-12 bg-white border border-gray-400 flex items-center justify-center">
          <div class="w-8 h-8 flex items-center justify-center">
            <span class="text-xl">♬</span>
          </div>
        </div>
        <span class="mt-1 text-sm text-center bg-white px-1">Music</span>
      </div>
    </div>

    {#if isNotepadOpen}
      <div
        use:draggable
        class="absolute cursor-pointer top-12 left-36 w-80 bg-white border border-gray-500 shadow-lg"
      >
        <div
          class="bg-gradient-to-r from-[#D12459] to-[#FFD0DE] text-white px-2 py-1 flex justify-between items-center"
        >
          <span>Notepad</span>
          <button
            class="px-1 hover:bg-pink-600"
            on:click={() => toggleWindow('notepad')}>✕</button
          >
        </div>
        <textarea
          class="w-full h-48 p-2 text-sm focus:outline-none resize-none border-b border-gray-300"
          placeholder="What's on your mind?"
          bind:value={notepadContent}
        ></textarea>
        <div class="p-2 text-xs text-gray-500">
          <div>Lines: {notepadContent.split('\n').length}</div>
          <div>Characters: {notepadContent.length}</div>
        </div>
      </div>
    {/if}

    {#if isSettingsOpen}
      <div
        use:draggable
        class="absolute cursor-pointer top-72 left-96 w-72 bg-white border border-gray-500 shadow-lg"
      >
        <div
          class="bg-gradient-to-r from-[#D12459] to-[#FFD0DE] text-white px-2 py-1 flex justify-between items-center"
        >
          <span>Settings</span>
          <button
            class="px-1 hover:bg-pink-600"
            on:click={() => toggleWindow('settings')}>✕</button
          >
        </div>
        <div class="p-3">
          <h3 class="font-medium text-gray-800 mb-2">Appearance</h3>

          <div class="mb-4">
            <div class="text-sm text-gray-600 mb-1">Theme Color</div>
            <div class="flex space-x-2">
              <div class="w-6 h-6 bg-pink-400 rounded-full border-2 border-gray-400 cursor-pointer"></div>
              <div class="w-6 h-6 bg-purple-400 rounded-full border border-gray-400 cursor-pointer"></div>
              <div class="w-6 h-6 bg-blue-400 rounded-full border border-gray-400 cursor-pointer"></div>
              <div class="w-6 h-6 bg-green-400 rounded-full border border-gray-400 cursor-pointer"></div>
            </div>
          </div>

          <div class="mb-4">
            <div class="text-sm text-gray-600 mb-1">Desktop Pattern</div>
            <select class="text-sm border border-gray-300 rounded p-1 w-full">
              <option>Music Notes</option>
              <option>Raindrops</option>
              <option>Solid Color</option>
              <option>Pixel Art</option>
            </select>
          </div>

          <div>
            <div class="text-sm text-gray-600 mb-1">Sound Effects</div>
            <label class="flex items-center text-sm">
              <input
                type="checkbox"
                class="mr-2"
                checked
              />
              Enable typing sounds
            </label>
            <label class="flex items-center text-sm">
              <input
                type="checkbox"
                class="mr-2"
                checked
              />
              Enable click sounds
            </label>
          </div>
        </div>
      </div>
    {/if}

    <div
      use:draggable
      class="absolute cursor-pointer top-[35%] left-[24%] w-96 bg-white border border-gray-500 shadow-lg"
    >
      <div class="bg-gradient-to-r from-[#D12459] to-[#FFD0DE] text-white px-2 py-1 flex justify-between items-center">
        <span>Hampster Dance</span>
        <button
          class="px-1 hover:bg-pink-600"
          on:click={() => alert('it just did nothing!')}>✕</button
        >
      </div>
      <Hampster />
    </div>

    {#if isPlayerOpen}
      <div
        use:draggable
        class="absolute cursor-pointer top-[50%] left-32 w-64 bg-white border border-gray-500 shadow-lg"
      >
        <div
          class="bg-gradient-to-r from-[#D12459] to-[#FFD0DE] text-white px-2 py-1 flex justify-between items-center"
        >
          <span>Meme Player</span>
          <button
            class="px-1 hover:bg-pink-600"
            on:click={() => toggleWindow('player')}>✕</button
          >
        </div>
        <div class="p-3">
          <div class="mb-3 text-center relative">
            <div
              class="mx-auto w-32 h-32 rounded-full bg-cat bg-contain animate-pulse flex items-center justify-center
                 filter grayscale-[100%]"
            ></div>
            <span class="text-2xl text-pink-500 absolute top-[30%]">♪</span>
            <div class="mt-2 font-medium text-gray-800">Why Cats Are So Cute?</div>
            <div class="text-xs text-gray-500">Meow</div>
          </div>

          <div class="flex items-center justify-center space-x-3 mb-3">
            <button class="text-xl text-gray-600 hover:text-pink-500">⏮</button>
            <button
              class="text-2xl text-gray-800 hover:text-pink-500"
              on:click={togglePlay}
            >
              {isPlaying ? '⏸' : '▶'}
            </button>
            <button class="text-xl text-gray-600 hover:text-pink-500">⏭</button>
          </div>

          <div class="mb-2">
            <div class="relative h-1 w-full bg-gray-200 rounded-full">
              <div
                class="absolute top-0 left-0 h-1 bg-gradient-to-r from-[#D12459] to-[#FFD0DE] rounded-full"
                style="width: 35%"
              ></div>
            </div>
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>1:23</span>
              <span>4:56</span>
            </div>
          </div>

          <div class="flex items-center">
            <span class="text-sm mr-2">🔊</span>
            <input
              type="range"
              min="0"
              max="100"
              bind:value={volume}
              class="w-full"
            />
          </div>
        </div>
      </div>
    {/if}
  </div>

  <div class="w-full h-6 bg-zinc-500 px-4 flex items-center justify-between text-white text-xs">
    <div class="flex items-center space-x-4">
      <span>CPU: 2%</span>
      <span>RAM: 128Mb</span>
    </div>
    <div class="flex items-center space-x-3">
      <button class="px-1 py-0.5 bg-gradient-to-r from-[#D12459] to-[#FFD0DE] rounded text-xs">wifi</button>
      <button class="px-1 py-0.5 bg-gray-700 rounded text-xs">vol</button>
      <button class="px-1 py-0.5 bg-gray-700 rounded text-xs">bat</button>
    </div>
  </div>

  <div
    use:draggable
    class="absolute text-[#8A2A47] cursor-pointer top-32 left-[48%] w-[600px] h-[430px] bg-mail bg-contain bg-no-repeat border shadow-lg"
  >
    <div class="relative flex p-4 items-center gap-2 justify-between top-[48%] bg-white m-2 border-2 border-[#E8D9D9]">
      Kindly check the attached DANCING BABY &nbsp; ->
      <DancingBaby />
    </div>
  </div>
</div>
