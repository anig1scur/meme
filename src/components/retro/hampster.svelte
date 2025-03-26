<script>
  import {onMount} from 'svelte';
  import Hamster from '$assets/videos/HamsterDance.mp4';
  import HamsterPoster from '$assets/imgs/hamster_poster.png';
  let video;
  let isPlaying = false;

  onMount(() => {
    video = document.getElementById('video-player');
  });

  function togglePlay() {
    if (isPlaying) {
      video.pause();
    } else {
      video.play();
    }
    isPlaying = !isPlaying;
  }
</script>

<div class="relative rounded-lg p-2 w-full text-center">
  <video
    poster={HamsterPoster}
    id="video-player"
    class="w-full rounded-lg"
  >
    <source
      src={Hamster}
      type="video/mp4"
    />
  </video>
  <button
    class="mt-3 bg-[#FFD0DE] text-[#8A2A47] px-2 py-1 rounded-lg hover:bg-[#f7b3c8] transition"
    on:click={togglePlay}
  >
    {isPlaying ? 'Pause' : 'Play'}
  </button>
</div>
