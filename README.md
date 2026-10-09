# Flapstacks

Landing page for Flapstacks. Static HTML and CSS, served by a small Bun file server on Prisma Compute.

Live: <https://t8ii4t9j7jsc14acybtt8yr1.fra.prisma.build/>

## Run locally

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. To run the production server instead:

```sh
pnpm install
pnpm build
pnpm start
```

## Deploy

The app is declared in `module.ts` (one `web` service, see `app/service.ts`). `scripts/build.sh` bundles `app/server.ts` and copies the site into `dist/public/`. Deploy from a machine signed in to the `tylerhogarth` workspace:

```sh
pnpm build
pnpm deploy
```

`pnpm deploy` runs `prisma deploy module.ts --name Flapstacks`, targeting the existing Flapstacks project. The directory is linked to it through the gitignored `.prisma/local.json`; run `prisma project link Flapstacks` on a fresh clone.

## Assets

| File | Purpose |
| --- | --- |
| `src/hero.png` | Original hero artwork (not served) |
| `assets/hero.webp`, `assets/hero-800.webp`, `assets/hero.jpg` | Web-optimised hero variants |
| `assets/og-image.jpg` | Open Graph and Twitter share image (1200 x 630) |
| `assets/og-image-square.jpg` | Square share image (1200 x 1200) |
| `favicon.ico`, `assets/favicon-16.png`, `assets/favicon-32.png` | Favicons |
| `assets/apple-touch-icon.png` | iOS home screen icon (180 x 180) |
| `assets/icon-192.png`, `assets/icon-512.png`, `assets/icon-maskable-512.png` | PWA icons referenced by `site.webmanifest` |

Share and icon images are generated from `src/hero.png` with `scripts/generate-assets.py`.
