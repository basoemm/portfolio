/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Original warm palette (kept for reference)
        'cotton-field': '#f4efe8',
        'silver-bird': '#faf7f2',
        'kilimanjaro': '#3b342e',
        'warrior': '#7a685b',
        'semolina': '#c8a68d',
        // Fantasy / portal palette
        'portal': '#0d0a1a',
        'sky-deep': '#1a0838',
        'sky-mid': '#4a1050',
        'sky-rose': '#8a3060',
        'sky-warm': '#c87060',
      },
      fontFamily: {
        sans: ['var(--font-inter)', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      animation: {
        'cloud-drift': 'cloud-drift var(--duration, 40s) linear infinite',
        'float-card': 'float-card var(--float-duration, 5s) ease-in-out infinite',
        'twinkle': 'twinkle var(--twinkle-duration, 3s) ease-in-out infinite',
        'ray-pulse': 'ray-pulse 8s ease-in-out infinite',
      },
      keyframes: {
        'cloud-drift': {
          '0%': { transform: 'translateX(-20vw)' },
          '100%': { transform: 'translateX(120vw)' },
        },
        'float-card': {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '33%': { transform: 'translateY(-10px) rotate(0.4deg)' },
          '66%': { transform: 'translateY(-5px) rotate(-0.3deg)' },
        },
        'twinkle': {
          '0%, 100%': { opacity: '0.3', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.4)' },
        },
        'ray-pulse': {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '0.65' },
        },
      },
    },
  },
  plugins: [],
}
