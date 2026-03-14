'use client'

import { useEffect, useState } from 'react'

interface Star {
  x: number
  y: number
  size: number
  opacity: number
  duration: number
  delay: number
}

export default function StarField() {
  const [stars, setStars] = useState<Star[]>([])

  useEffect(() => {
    // Deterministic-looking but varied distribution using index math
    const generated: Star[] = Array.from({ length: 90 }, (_, i) => ({
      x: ((i * 1973 + 31) % 1000) / 10,
      y: ((i * 1301 + 47) % 1000) / 10,
      size: ((i * 7 + 3) % 15) / 10 + 0.4,
      opacity: ((i * 11 + 5) % 6) / 10 + 0.25,
      duration: ((i * 13 + 7) % 20) / 10 + 2.5,
      delay: ((i * 17 + 11) % 30) / 10,
    }))
    setStars(generated)
  }, [])

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {stars.map((star, i) => (
        <div
          key={i}
          className="absolute rounded-full bg-white"
          style={{
            left: `${star.x}%`,
            top: `${star.y}%`,
            width: `${star.size}px`,
            height: `${star.size}px`,
            opacity: star.opacity,
            animation: `twinkle ${star.duration}s ease-in-out infinite`,
            animationDelay: `${star.delay}s`,
          }}
        />
      ))}
    </div>
  )
}
