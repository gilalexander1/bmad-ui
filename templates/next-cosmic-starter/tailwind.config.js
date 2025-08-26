/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  presets: [require('../../packages/cosmic-theme/tailwind.preset.cjs')],
  theme: {
    extend: {},
  },
  plugins: [],
}

