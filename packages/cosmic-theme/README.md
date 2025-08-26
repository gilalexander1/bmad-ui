# BMAD Cosmic Theme

Reusable Tailwind preset and CSS utilities to apply the BMAD “cosmic/matrix” UI across projects.

NPM package (public): `cosmic-tailwind-theme`

## Install (monorepo/local path)

- Copy this folder to your repo under `packages/cosmic-theme` (already done here), or publish as a private package later.

## Use in a Next.js + Tailwind app

1) Tailwind preset

- In your app’s `tailwind.config.js` (monorepo path example):

```js
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  presets: [require('../packages/cosmic-theme/tailwind.preset.cjs')],
  theme: { extend: {} },
};
```

2) CSS utilities (monorepo path example)

- Import CSS once (e.g., in `src/app/globals.css` or main CSS):

```css
@import '../packages/cosmic-theme/css/cosmic.css';
/* Optionally add Google fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
```

3) Using the published npm package

Install:
```bash
npm install cosmic-tailwind-theme
```

Config (npm):
```js
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  presets: [require('cosmic-tailwind-theme')],
}
```

CSS import (npm):
```css
@import 'cosmic-tailwind-theme/css/cosmic.css';
```

4) Example usage

- Apply background and stars to a container:

```tsx
<div className="relative cosmic-bg cosmic-stars min-h-screen p-8">
  <header className="glass p-6 border border-matrix-green/30">
    <h1 className="text-3xl font-bold text-gradient">Cosmic UI</h1>
  </header>
  <button className="glass-button text-matrix-green font-mono px-4 py-2 mt-4">
    Launch
  </button>
  
</div>
```

## What’s included

- Tailwind tokens: `cosmic` palette, `matrix.green`, glass colors, animations, keyframes, fonts.
- CSS utilities: `.glass`, `.glass-heavy`, `.glass-button`, `.matrix-text`, `.terminal`, `.text-gradient`, `.cosmic-pulse`, `.form-input`, `.progress-bar`, etc.
- Optional backgrounds: `.cosmic-bg` and `.cosmic-stars` (scoped; not global).

## Notes

- Keep tokens in the preset; UI behaviors in CSS.
- Consumers can add `@tailwindcss/typography` as needed.
- Fonts are loaded via Google Fonts import (customize if offline or self-hosted).

## Roadmap

- Provide a Tailwind plugin variant that emits utilities (no CSS import).
- Starter templates for Vite/React and Next.js.
