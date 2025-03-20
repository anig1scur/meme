<script>
  import {onMount} from 'svelte';

  export let imageUrl = '';

  // Default wallpaper - retro sunset scene, simulating the effect in the image
  let defaultWallpaper =
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Cdefs%3E%3ClinearGradient id='sunset' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%23FFB6C1'/%3E%3Cstop offset='35%25' stop-color='%23E6C8C8'/%3E%3Cstop offset='70%25' stop-color='%23C8A2C8'/%3E%3Cstop offset='100%25' stop-color='%23A9A9A9'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='800' height='600' fill='url(%23sunset)'/%3E%3Cpath d='M400,360 C400,360 350,220 300,360 C250,500 550,500 500,360 C450,220 400,360 400,360 Z' fill='%23615858'/%3E%3Cpath d='M400,360 C400,360 390,330 380,360 C370,390 430,390 420,360 C410,330 400,360 400,360 Z' fill='url(%23sunset)'/%3E%3C/svg%3E";

  let icons = [
    {name: 'Computer', icon: '[]='},
    {name: 'Documents', icon: '≣'},
    {name: 'Trash', icon: '♲'},
  ];

  let menuItems = ['File', 'Edit', 'View', 'Tools', 'Help'];
  let statusItems = ['Downloads', 'Documents', 'Settings'];
  let showDesktop = true;

  // Current time
  let currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

  // Blinking cursor effect
  let cursorVisible = true;

  onMount(() => {
    // Time update
    const timer = setInterval(() => {
      currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    }, 60000);

    // Cursor blinking effect
    const cursorTimer = setInterval(() => {
      cursorVisible = !cursorVisible;
    }, 500);

    return () => {
      clearInterval(timer);
      clearInterval(cursorTimer);
    };
  });
</script>

<div class="flex justify-center items-center p-4 w-full h-full">
  <!-- Monitor shell -->
  <div class="relative">
    <!-- Monitor frame - gray shell with ripple texture -->
    <div
      class="relative bg-gray-400 rounded-lg p-4 shadow-xl border-8 border-gray-500"
      style="background-image: repeating-radial-gradient(circle at 50% 50%, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 8%); box-shadow: 0 0 20px rgba(0,0,0,0.3);"
    >
      <!-- Ripple border details -->
      <div
        class="absolute inset-0 rounded-lg"
        style="background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 0px, rgba(255,255,255,0.1) 2px, transparent 2px, transparent 4px); 
                  border: 12px solid transparent; 
                  border-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.2) 0px, rgba(255,255,255,0.2) 2px, rgba(200,200,200,0.3) 2px, rgba(200,200,200,0.3) 4px) 12;"
      ></div>

      <!-- Screen area -->
      <div
        class="bg-gray-900 overflow-hidden relative"
        style="width: 500px; height: 380px;"
      >
        <!-- Screen content -->
        <div class="w-full h-full relative">
          {#if showDesktop}
            <!-- Desktop wallpaper -->
            <div
              class="w-full h-full"
              style="background-image: url({imageUrl ||
                defaultWallpaper}); background-size: cover; background-position: center;"
            >
              <!-- Top menu bar - accurately replicate the style in the image -->
              <div
                class="bg-gray-300 bg-opacity-90 flex justify-between items-center px-2 py-1 border-b border-gray-500"
              >
                <!-- OS icon -->
                <div class="flex items-center">
                  <div class="text-sm font-bold pr-2 text-pink-900">Retro OS</div>
                  <div class="h-4 w-px bg-gray-500"></div>
                </div>

                <!-- Menu items -->
                <div class="flex space-x-4">
                  {#each menuItems as item}
                    <div class="text-xs hover:bg-gray-500 px-2 py-1 cursor-pointer font-bold text-gray-800">{item}</div>
                  {/each}
                </div>

                <!-- Time -->
                <div class="text-xs font-mono bg-gray-400 px-2 py-0.5 w-18 rounded-sm">{currentTime}</div>
              </div>

              <!-- Desktop icons - accurately replicate the style in the image -->
              <div class="grid grid-cols-1 gap-4 p-4">
                {#each icons as icon}
                  <div
                    class="flex flex-col items-center cursor-pointer hover:bg-white hover:bg-opacity-20 p-2 rounded w-20"
                  >
                    <div class="text-lg mb-1 bg-gray-200 bg-opacity-50 p-1 rounded-sm font-mono">{icon.icon}</div>
                    <div
                      class="text-xs text-white drop-shadow-md font-bold"
                      style="text-shadow: 1px 1px 2px rgba(0,0,0,0.8);"
                    >
                      {icon.name}
                    </div>
                  </div>
                {/each}
              </div>

              <!-- Bottom status bar - accurately replicate the style in the image -->
              <div
                class="absolute bottom-0 left-0 right-0 h-8 bg-gray-400 flex items-center px-2 border-t border-white"
              >
                <div
                  class="bg-pink-200 rounded-sm px-2 py-0.5 text-xs font-bold text-gray-800 mr-2 shadow-inner border border-gray-500"
                >
                  Start
                </div>
                <div class="flex-1 flex items-center">
                  {#each statusItems as item, i}
                    {#if i > 0}
                      <div class="h-4 w-px bg-gray-500 mx-2"></div>
                    {/if}
                    <div class="text-xs font-bold text-gray-800 hover:text-gray-900 cursor-pointer">{item}</div>
                  {/each}
                </div>
                <!-- <div class="text-xs font-mono bg-gray-300 px-2 py-0.5 rounded-sm border border-gray-500">1:1</div> -->
              </div>
            </div>
          {/if}

          <!-- Screen borders - simulate CRT monitor border -->
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-gray-700 via-gray-500 to-gray-700"></div>
          <div
            class="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-gray-700 via-gray-500 to-gray-700"
          ></div>
          <div class="absolute top-0 left-0 h-full w-1 bg-gradient-to-b from-gray-700 via-gray-500 to-gray-700"></div>
          <div class="absolute top-0 right-0 h-full w-1 bg-gradient-to-b from-gray-700 via-gray-500 to-gray-700"></div>

          <!-- Window margins with different colors - simulate shadow effect -->
          <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
            <div class="absolute top-0 left-0 w-full h-2 bg-white opacity-30"></div>
            <div class="absolute bottom-0 left-0 w-full h-2 bg-black opacity-30"></div>
            <div class="absolute top-0 left-0 h-full w-2 bg-white opacity-30"></div>
            <div class="absolute top-0 right-0 h-full w-2 bg-black opacity-30"></div>
          </div>

          <!-- Screen reflection effect -->
          <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white to-transparent opacity-10"></div>

          <!-- CRT scan line effect -->
          <div
            class="absolute top-0 left-0 w-full h-full pointer-events-none"
            style="background: repeating-linear-gradient(transparent, transparent 1px, rgba(0,0,0,0.1) 1px, rgba(0,0,0,0.1) 2px);"
          ></div>

          <!-- CRT curve effect -->
          <div
            class="absolute top-0 left-0 w-full h-full pointer-events-none rounded-lg"
            style="box-shadow: inset 0 0 30px 10px rgba(0,0,0,0.3);"
          ></div>

          <!-- Slight flicker effect -->
          <div
            class="absolute top-0 left-0 w-full h-full pointer-events-none opacity-5 animate-pulse"
            style="background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0));"
          ></div>
        </div>
      </div>

      <!-- Monitor bottom control buttons - accurately replicate the style in the image -->
      <!-- <div class="flex justify-center mt-3 space-x-2 mb-3">
        <button class="w-8 h-3 bg-gray-500 rounded-sm hover:bg-gray-600 border border-gray-600"></button>
        <button class="w-8 h-3 bg-gray-500 rounded-sm hover:bg-gray-600 border border-gray-600"></button>
        <button class="w-8 h-3 bg-gray-500 rounded-sm hover:bg-gray-600 border border-gray-600"></button>
        <button class="w-8 h-3 bg-pink-300 rounded-sm hover:bg-pink-400 border border-gray-600"></button>
        <button class="w-8 h-3 bg-gray-500 rounded-sm hover:bg-gray-600 border border-gray-600"></button>
        <button class="w-8 h-3 bg-gray-500 rounded-sm hover:bg-gray-600 border border-gray-600"></button>
      </div> -->

      <!-- Power indicator light -->
      <!-- <div class="absolute bottom-2 right-4 w-2 h-2 rounded-full bg-pink-400 animate-pulse"></div> -->

      <!-- Brand logo -->
      <div
        class="absolute -bottom-1 left-0 right-0 mb-1 text-center text-xs font-bold"
        style="color: #5b5b5b; text-shadow: 1px 1px 1px rgba(255,255,255,0.5);"
      >
        Woai Meme
      </div>
    </div>

    <!-- Monitor stand - more accurately replicate the style in the image -->
    <div
      class="mx-auto"
      style="width: 140px;"
    >
      <!-- Support -->
      <div class="h-16 bg-gradient-to-b from-gray-400 to-gray-500 rounded-b-lg relative">
        <!-- Support texture -->
        <div
          class="absolute inset-0 opacity-30"
          style="background-image: repeating-linear-gradient(90deg, transparent, transparent 5px, rgba(255,255,255,0.2) 5px, rgba(255,255,255,0.2) 10px);"
        ></div>

        <!-- Support decoration -->
        <div
          class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-10 h-4 bg-gray-600 rounded-sm"
        ></div>
      </div>

      <!-- Base -->
      <div class="h-3 w-full bg-gray-700 rounded-b-lg shadow-lg"></div>
    </div>
  </div>
</div>
