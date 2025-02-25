<script>
  export let name;
  export let year;
  export let image;
</script>

<div class="w-[85%] mb-4">
  <img
    class="w-full grayscale object-contain"
    src={'top50/images/' + image}
    alt={name}
  />
  <div class="flex py-2 items-end justify-between font-routedgothic text-[#36312F]">
    <div class="text-2xl">{name}</div>
    <div>{year}</div>
  </div>
</div>
