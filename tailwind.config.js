/** @type {import('tailwindcss').Config} */

module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{svelte,js,ts,jsx,tsx}",
    ],
    theme: {
      fontFamily: {
        'routedgothic': ['"RoutedGothic"', ],
        'icon': ['"Icon"', ],
      }
    }
}
