// Scroll animation configuration
export const SCROLL = {
  SECTION_HEIGHT: '220vh',
  LAPTOP_SCALE: [1, 2.8] as [number, number],
  TEXT_FADE_RANGE: [0, 0.3] as [number, number],
  TEXT_Y_RANGE: [0, -40] as [number, number],
} as const

// Scroll offset presets for useScroll
export const OFFSET = {
  SECTION: ['start start', 'end start'] as ['start start', 'end start'],
} as const
