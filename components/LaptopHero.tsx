'use client'

import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import Image from 'next/image'
import { SCROLL, OFFSET } from '@/lib/constants'

export default function LaptopHero() {
  const sectionRef = useRef<HTMLDivElement>(null)

  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: OFFSET.SECTION,
  })

  const scale = useTransform(scrollYProgress, [0, 1], SCROLL.LAPTOP_SCALE)
  const textOpacity = useTransform(scrollYProgress, SCROLL.TEXT_FADE_RANGE, [1, 0])
  const textY = useTransform(scrollYProgress, SCROLL.TEXT_FADE_RANGE, SCROLL.TEXT_Y_RANGE)

  return (
    <section ref={sectionRef} className="relative" style={{ height: SCROLL.SECTION_HEIGHT }}>
      <div className="sticky top-0 h-screen overflow-hidden bg-cotton-field">

        {/* Hero text */}
        <motion.div
          style={{ opacity: textOpacity, y: textY }}
          className="absolute top-0 left-0 right-0 flex flex-col items-center pt-36 z-10 pointer-events-none select-none"
        >
          <p className="text-xs font-medium tracking-[0.2em] text-semolina uppercase mb-5">
            Software Engineer
          </p>
          <h1 className="text-5xl md:text-7xl font-light text-kilimanjaro tracking-tight leading-[1.1] text-center">
            Building digital<br />experiences
          </h1>
        </motion.div>

        {/* Laptop — centered in viewport */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.div
            style={{ scale }}
            className="relative w-[820px] max-w-[88vw]"
          >
            {/* Screen content */}
            <div
              className="absolute overflow-hidden z-10"
              style={{
                top: '7%',
                left: '7%',
                width: '86%',
                height: '56%',
                borderRadius: '4px',
              }}
            >
              <Image
                src="/images/code.png"
                alt="Code preview"
                fill
                className="object-cover"
                priority
              />
            </div>

            {/* Laptop frame */}
            <Image
              src="/images/laptop.png"
              alt="Laptop"
              width={820}
              height={530}
              className="relative z-20 pointer-events-none w-full h-auto block"
              priority
            />
          </motion.div>
        </div>

        {/* Scroll hint */}
        <motion.div
          style={{ opacity: textOpacity }}
          className="absolute bottom-8 left-0 right-0 flex flex-col items-center gap-3 pointer-events-none select-none"
        >
          <span className="text-[10px] tracking-[0.2em] text-warrior/60 uppercase">Scroll</span>
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}
            className="w-px h-8 bg-warrior/25"
          />
        </motion.div>
      </div>
    </section>
  )
}
