<script>
  import TimelineScroller from './timelineScroller.svelte';

  const myTimelineData = [
    {id: 'chapter0', title: '1960', position: 0},
    {id: 'chapter1', title: '1980', position: 20},
    {id: 'chapter2', title: '1980', position: 40},
    {id: 'chapter3', title: '2000', position: 60},
    {id: 'chapter4', title: '2010', position: 80},
    {id: 'conclusion', title: '2020', position: 90},
    {id: 'conclusion2', title: 'now', position: 100},
  ];
</script>

<TimelineScroller timelineData={myTimelineData}>
  <section
    id="intro"
    class="story-section"
  >
    <h2>1</h2>
    <p>1...</p>
  </section>

  <section
    id="chapter1"
    class="story-section"
  >
    <h2>2</h2>
    <p>2...</p>
  </section>

  <section
    id="chapter2"
    class="story-section"
  >
    <h2>3</h2>
    <p>...</p>
  </section>

  <section
    id="chapter3"
    class="story-section"
  >
    <h2>4</h2>
    <p>4...</p>
  </section>

  <section
    id="chapter4"
    class="story-section"
  >
    <h2>5</h2>
    <p>5...</p>
  </section>

  <section
    id="conclusion"
    class="story-section"
  >
    <h2>6</h2>
    <p>6...</p>
  </section>

  <section
    id="conclusion2"
    class="story-section"
  >
    <h2>7</h2>
    <p>7...</p>
  </section>
</TimelineScroller>

<style>
  .story-section {
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
</style>
