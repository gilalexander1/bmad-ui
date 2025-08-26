# Next.js Cosmic Starter (Template)

A minimal Next.js starter wired to the BMAD Cosmic Theme (Tailwind preset + CSS utilities).

## Use

1) Copy this folder to a new project directory.
2) Install deps:

```bash
npm install
```

3) Ensure the theme is available via relative path (monorepo):
- `presets: [require('../../packages/cosmic-theme/tailwind.preset.cjs')]`
- CSS imports `../../packages/cosmic-theme/css/cosmic.css`

If using outside the monorepo, publish `@bmad/cosmic-theme` or replace paths with your installed package path.

4) Run dev:

```bash
npm run dev
```

Open http://localhost:3000.

## Notes
- Globals import the theme CSS and optional Google Fonts.
- Layout applies `cosmic-bg` and `cosmic-stars` to the body.
- Page demonstrates core utilities: glass, matrix-text, text-gradient, glow, pulse, form-input, progress-bar.
