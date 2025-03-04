/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{svelte,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'scale-bounce': 'scaleBounce 4s infinite',
      },
      keyframes: {
        scaleBounce: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(0.95)' },
          '100%': { transform: 'scale(1)' },
        },
      },
    },
    fontFamily: {
      routedgothic: ['RoutedGothic',],
      icon: ['Icon', 'serif'],
      georgia: ['Georgia', 'serif'],
    }
  }
}
