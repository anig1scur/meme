<script lang="js">
  import Header from '../components/Header.svelte';
  import Footer from '../components/Footer.svelte';

  import Intro from '../components/history/Intro.svelte';
  import Origin from '../components/history/Origin.svelte';
  import Timeline from '../components/history/Timeline.svelte';
</script>

<Header />
<div class="font-routedgothic">
  <Intro />
  <Timeline />
  <div id="history">
    <Origin />
    <section
      id="the_selfish_gene"
      class="section"
    >
      <h2>1</h2>
      <p>1...</p>
    </section>

    <section
      id="early_internet_memes"
      class="section"
    >
      <h2>2</h2>
      <p>2...</p>
    </section>

    <section
      id="rise_of_video_and_social_media_memes"
      class="section"
    >
      <h2>3</h2>
      <p>...</p>
    </section>

    <section
      id="meme_explosion_and_emojis"
      class="section"
    >
      <h2>4</h2>
      <p>4...</p>
    </section>

    <section
      id="short_form_video_meme_culture"
      class="section"
    >
      <h2>5</h2>
      <p>5...</p>
    </section>

    <section
      id="revival_and_cross_platform_memes"
      class="section"
    >
      <h2>6</h2>
      <p>6...</p>
    </section>

    <section
      id="future_of_memes"
      class="section"
    ></section>
  </div>
</div>
<section
class="section"
></section>
<Footer />

<style>
  .section {
    min-height: 200vh;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
</style>
