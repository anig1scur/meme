<script>
  import {onMount} from 'svelte';
  import {ThumbsUp, ThumbsDown, Share2, Flag, Star} from 'lucide-svelte';
  import RickRolled from '$assets/videos/RickRolled.mp4';
  import RickPoster from '$assets/imgs/rick_roll_poster.png';

  let isPlaying = false;
  let videoElement;

  onMount(() => {
    if (videoElement) {
      videoElement.pause();
    }
  });

  function togglePlay() {
    if (videoElement) {
      if (isPlaying) {
        videoElement.pause();
      } else {
        videoElement.play();
      }
      isPlaying = !isPlaying;
    }
  }

  const relatedVideos = [
    {
      title: 'Evolution of Dance - By Judson Laipply',
      views: '123,456',
      author: 'JudsonLaipply',
      duration: '6:01',
    },
    {
      title: 'Charlie bit my finger - again!',
      views: '98,765',
      author: 'HDCYT',
      duration: '0:56',
    },
    {
      title: 'Leave Britney Alone!',
      views: '87,654',
      author: 'Chris Crocker',
      duration: '2:13',
    },
    {
      title: 'Numa Numa',
      views: '76,543',
      author: 'Gary Brolsma',
      duration: '1:26',
    },
    {
      title: 'Rick Astley - Never Gonna Give You Up',
      views: '65,432',
      author: 'RickAstleyVEVO',
      duration: '3:33',
    },
  ];
</script>

<div class="max-w-4xl mx-auto bg-white py-8 px-4 font-sans">
  <div class="flex gap-10">
    <div class="flex-1">
      <div class="relative bg-black aspect-video mb-2 w-full overflow-hidden">
        <video
          bind:this={videoElement}
          src={RickRolled}
          poster={RickPoster}
          class="absolute inset-0 w-full h-full object-cover"
          on:click={togglePlay}
        ></video>
        <div
          class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center pointer-events-none {isPlaying
            ? 'hidden'
            : ''}"
        >
          <button
            on:click={togglePlay}
            class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 pointer-events-auto"
          >
            Play
          </button>
        </div>
      </div>

      <div class="border-b pb-4 mb-2">
        <h1 class="text-xl font-bold mb-2">Rick Astley - Never Gonna Give You Up</h1>
        <div class="flex items-center text-gray-600 text-sm">
          <span>Added: April 25, 2009</span>
          <span class="mx-2">|</span>
          <span>From: Rick Astley</span>
          <span class="mx-2">|</span>
          <span>Views: 1,234,567,890</span>
        </div>
      </div>

      <div class="flex items-center gap-4 mb-4 pb-2 border-b">
        <div class="flex items-center gap-2">
          <ThumbsUp class="w-4 h-4" />
          <span class="text-sm">12,345</span>
        </div>
        <div class="flex items-center gap-2">
          <ThumbsDown class="w-4 h-4" />
          <span class="text-sm">123</span>
        </div>
        <button class="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded text-sm">
          <Share2 class="w-4 h-4" />
          Share
        </button>
        <button class="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded text-sm">
          <Star class="w-4 h-4" />
          Favorite
        </button>
        <button class="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded text-sm">
          <Flag class="w-4 h-4" />
          Flag
        </button>
      </div>

      <div class="bg-gray-50 px-4 py-2 rounded mb-2">
        <h2 class="font-bold mb-2">Description:</h2>
        <p class="text-xs text-gray-700">
          “Never Gonna Give You Up” was a global hit in 1987, topping charts in 25 countries including the UK and US. Produced by Stock Aitken Waterman, it was the lead single from Rick Astley's debut album *Whenever You Need Somebody*, which sold over 15 million copies worldwide.
        </p>
        <div class="mt-4 text-xs text-gray-600">
          Tags: viral video, internet meme, 2009
        </div>
      </div>

      <!-- Comments Section -->
      <div>
        <h2 class="font-bold mb-4">Comments</h2>
        <div class="flex gap-4 mb-4">
          <div class="w-10 h-10 bg-gray-200 rounded-full flex-shrink-0"></div>
          <div class="flex-grow">
            <div class="bg-gray-50 p-3 rounded">
              <p class="font-bold text-sm mb-1">User</p>
              <p class="text-sm">This is epic internet history right here!</p>
            </div>
            <div class="text-xs text-gray-500 mt-1">2 hours ago</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Related Videos Sidebar -->
    <div class="w-80 flex-shrink-0">
      <h2 class="font-bold mb-4">Related Videos</h2>
      <div class="space-y-4">
        {#each relatedVideos as video}
          <div class="flex gap-2">
            <div class="w-32 h-24 bg-gray-200 flex-shrink-0 relative">
              <span class="absolute bottom-1 right-1 bg-black text-white text-xs px-1 rounded">
                {video.duration}
              </span>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-blue-800 hover:text-blue-600 cursor-pointer mb-1">
                {video.title}
              </h3>
              <p class="text-xs text-gray-600">From: {video.author}</p>
              <p class="text-xs text-gray-600">{video.views} views</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>
