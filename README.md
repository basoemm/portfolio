# Portfolio

Personal portfolio built with Next.js 13 using the App Router.

## Stack

- Next.js 13 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion

## Project structure

- `app/`
- `layout.tsx`: Root layout
- `page.tsx`: Homepage route
- `globals.css`: Global styles (Tailwind + custom styles)
- `components/`
- Reusable UI sections (Navbar, About, Projects, Contact, etc.)
- Animated/visual components (CloudLayer, StarField, LaptopHero)
- `lib/`
- Shared constants, hooks, and animation helpers
- `public/`
- Static assets (fonts, images, favicon)

## Development

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Production

```bash
npm run build
npm run start
```

## Notes

- Styling is handled with Tailwind CSS and global styles in `app/globals.css`.
- Motion and transitions are implemented with Framer Motion.
