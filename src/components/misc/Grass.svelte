<script>
  export let color = 'currentColor';
  export let strokeWidth = '2';
</script>

<div class="grass-container">
  <svg
    viewBox="-10 -10 106 114"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    preserveAspectRatio="xMidYMid meet"
  >
    <style>
      .grass-blade-1 {
        animation: sway1 4s ease-in-out infinite;
        transform-origin: 52px 90px;
      }
      .grass-blade-2 {
        animation: sway2 5s ease-in-out infinite;
        transform-origin: 50px 90px;
      }
      .grass-blade-3 {
        animation: sway3 4.5s ease-in-out infinite;
        transform-origin: 58px 90px;
      }

      @keyframes sway1 {
        0%,
        100% {
          transform: rotate(0deg);
        }
        50% {
          transform: rotate(5deg);
        }
      }

      @keyframes sway2 {
        0%,
        100% {
          transform: rotate(0deg);
        }
        50% {
          transform: rotate(-7deg);
        }
      }

      @keyframes sway3 {
        0%,
        100% {
          transform: rotate(0deg);
        }
        50% {
          transform: rotate(6deg);
        }
      }
    </style>

    <g>
      <path
        class="grass-blade-1"
        d="M51.7508 89.3764C46.8424 66.4714 31.0527 25.5123 50.1503 3.05555C58.8533 -7.17824 59.7484 23.877 59.8719 28.7465C60.2342 43.0332 57.3782 58.0896 54.0403 71.9591C53.6191 73.7096 50.1638 89.4389 53.5671 83.552"
        stroke={color}
        stroke-width={strokeWidth}
        stroke-linecap="round"
      />

      <path
        class="grass-blade-2"
        d="M55.6963 89.94C47.8634 70.753 38.2095 40.9109 18.668 29.7903C15.5317 28.0055 11.0087 25.8114 7.30069 27.0869C2.2204 28.8344 -1.14614 36.2692 2.59994 40.6874C9.04442 48.288 19.2441 53.6699 26.8447 60.0878C33.9422 66.0808 40.8448 72.4465 46.3645 79.9614C47.3541 81.3088 50.8938 89.7118 50.3728 88.0611"
        stroke={color}
        stroke-width={strokeWidth}
        stroke-linecap="round"
      />

      <path
        class="grass-blade-3"
        d="M58.4523 86.934C53.3153 65.1437 55.576 46.5024 64.0368 25.5631C65.1418 22.8283 79.5286 -0.850531 81.8933 6.40266C92.3836 38.5793 61.9166 65.1203 51.8135 92.2572"
        stroke={color}
        stroke-width={strokeWidth}
        stroke-linecap="round"
      />
    </g>
  </svg>
</div>
