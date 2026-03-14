'use client'

import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { SCROLL, OFFSET } from '@/lib/constants'
import { useIsMobile } from '@/lib/hooks'
import StarField from './StarField'

export default function LaptopHero() {
  const sectionRef = useRef<HTMLDivElement>(null)
  const isMobile = useIsMobile()

  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: OFFSET.SECTION,
  })

  // Laptop zoom — disabled on mobile
  const scale = useTransform(
    scrollYProgress,
    [0, 1],
    isMobile ? [1, 1] : SCROLL.LAPTOP_SCALE
  )

  // Hero text fades out early
  const textOpacity = useTransform(
    scrollYProgress,
    isMobile ? [0, 1] : SCROLL.TEXT_FADE_RANGE,
    [1, isMobile ? 1 : 0]
  )
  const textY = useTransform(
    scrollYProgress,
    isMobile ? [0, 1] : SCROLL.TEXT_FADE_RANGE,
    isMobile ? ([0, 0] as [number, number]) : SCROLL.TEXT_Y_RANGE
  )

  // Stars fade out as sky takes over
  const starsOpacity = useTransform(scrollYProgress, [0.35, 0.65], [1, 0])

  // Fantasy sky fades in as laptop fills the screen
  const skyOpacity = useTransform(scrollYProgress, [0.55, 0.92], [0, 1])

  // Sticky bg transitions to match the next section top (seamless join)
  const containerBg = useTransform(
    scrollYProgress,
    [0.82, 1],
    ['#0d0a1a', '#1a0838']
  )

  // Glow around laptop builds as you scroll toward the portal
  const glowOpacity = useTransform(scrollYProgress, [0, 0.55], [0.3, 0.8])

  return (
    // Mobile: 100vh (no zoom). Desktop: 300vh (extra space drives the zoom)
    <section ref={sectionRef} className="relative h-screen md:h-[300vh]">
      <motion.div
        style={{ backgroundColor: containerBg }}
        className="sticky top-0 h-screen overflow-hidden bg-[#0d0a1a]"
      >

        {/* ── Stars ── */}
        <motion.div style={{ opacity: starsOpacity }} className="absolute inset-0 z-0">
          <StarField />
        </motion.div>

        {/* ── Fantasy sky (fades in on scroll) ── */}
        <motion.div style={{ opacity: skyOpacity }} className="absolute inset-0 z-[1] pointer-events-none">
          <div
            className="absolute inset-0"
            style={{
              background: 'linear-gradient(to bottom, #1a0838 0%, #4a1050 35%, #8a3060 68%, #c87060 100%)',
            }}
          />
          {/* Sunray from bottom */}
          <div
            className="absolute inset-0 animate-ray-pulse"
            style={{
              background: 'radial-gradient(ellipse at 50% 108%, rgba(200, 112, 80, 0.55) 0%, rgba(160, 70, 100, 0.25) 32%, transparent 60%)',
            }}
          />
        </motion.div>

        {/* ── Desk surface (dark gradient at bottom) ── */}
        <div
          className="absolute bottom-0 left-0 right-0 h-44 z-[10] pointer-events-none"
          style={{
            background: 'linear-gradient(to top, rgba(6, 3, 14, 0.96) 0%, rgba(6, 3, 14, 0.4) 55%, transparent 100%)',
          }}
        />

        {/* ── Hero text ── */}
        <motion.div
          style={{ opacity: textOpacity, y: textY }}
          className="absolute top-0 left-0 right-0 flex flex-col items-center pt-[13vh] z-[20] pointer-events-none select-none"
        >
          <p className="text-xs font-medium tracking-[0.22em] text-semolina uppercase mb-5">
            Software Engineer
          </p>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-light text-cotton-field tracking-tight leading-[1.08] text-center px-6">
            Building digital<br />experiences
          </h1>
          <p className="mt-5 text-xs text-cotton-field/30 tracking-[0.18em] uppercase">
            scroll to enter
          </p>
        </motion.div>

        {/* ── Laptop on desk ── */}
        <div className="absolute inset-0 flex items-end justify-center pb-10 md:pb-16 z-[20]">
          <motion.div style={{ scale }} className="relative flex flex-col items-center">

            {/* Glow halo */}
            <motion.div style={{ opacity: glowOpacity }} className="absolute inset-0 pointer-events-none z-0">
              <div className="absolute" style={{ inset: '-60px', background: 'radial-gradient(ellipse at 50% 55%, rgba(200,166,141,0.28) 0%, transparent 68%)', filter: 'blur(28px)' }} />
            </motion.div>

            {/* Lid / Screen */}
            <div style={{ width: '560px', maxWidth: '80vw', height: '350px', background: '#1a1a2e', borderRadius: '12px 12px 0 0', border: '8px solid #3a3a4a', borderBottom: 'none', position: 'relative', boxShadow: '0 -4px 40px rgba(0,0,0,0.6)' }}>
              {/* Camera dot */}
              <div style={{ position: 'absolute', top: '6px', left: '50%', transform: 'translateX(-50%)', width: '6px', height: '6px', borderRadius: '50%', background: '#2a2a3a' }} />
              {/* Screen content */}
              <div style={{ position: 'absolute', inset: '12px', background: '#0d1117', borderRadius: '4px', overflow: 'hidden', padding: '12px', fontFamily: 'monospace', fontSize: '11px', lineHeight: '1.7' }}>
                <div style={{ display: 'flex', gap: '6px', marginBottom: '10px' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f57' }} />
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#febc2e' }} />
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#28c840' }} />
                </div>
                <p><span style={{ color: '#c792ea' }}>const</span> <span style={{ color: '#82aaff' }}>portal</span> <span style={{ color: '#fff' }}>=</span> <span style={{ color: '#c3e88d' }}>createMagic</span><span style={{ color: '#fff' }}>()</span></p>
                <p><span style={{ color: '#c792ea' }}>const</span> <span style={{ color: '#82aaff' }}>world</span> <span style={{ color: '#fff' }}>= {'{'}</span></p>
                <p style={{ paddingLeft: '16px' }}><span style={{ color: '#f78c6c' }}>name</span><span style={{ color: '#fff' }}>:</span> <span style={{ color: '#c3e88d' }}>&apos;Ibtisam&apos;</span><span style={{ color: '#fff' }}>,</span></p>
                <p style={{ paddingLeft: '16px' }}><span style={{ color: '#f78c6c' }}>role</span><span style={{ color: '#fff' }}>:</span> <span style={{ color: '#c3e88d' }}>&apos;Software Engineer&apos;</span><span style={{ color: '#fff' }}>,</span></p>
                <p style={{ paddingLeft: '16px' }}><span style={{ color: '#f78c6c' }}>passion</span><span style={{ color: '#fff' }}>:</span> <span style={{ color: '#c3e88d' }}>&apos;Building experiences&apos;</span></p>
                <p><span style={{ color: '#fff' }}>{'}'}</span></p>
                <p style={{ marginTop: '8px', color: '#546e7a' }}>{'// scroll to enter the portal'}</p>
                <p><span style={{ color: '#82aaff' }}>portal</span><span style={{ color: '#fff' }}>.</span><span style={{ color: '#ffcb6b' }}>open</span><span style={{ color: '#fff' }}>(world)</span></p>
              </div>
            </div>

            {/* Base / Keyboard */}
            <div style={{ width: '580px', maxWidth: '83vw', height: '22px', background: 'linear-gradient(to bottom, #3a3a4a, #2a2a38)', borderRadius: '0 0 4px 4px', position: 'relative' }}>
              {/* Trackpad hint */}
              <div style={{ position: 'absolute', bottom: '4px', left: '50%', transform: 'translateX(-50%)', width: '80px', height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px' }} />
            </div>

            {/* Bottom foot */}
            <div style={{ width: '600px', maxWidth: '86vw', height: '6px', background: 'linear-gradient(to bottom, #222230, #1a1a28)', borderRadius: '0 0 8px 8px', boxShadow: '0 8px 40px rgba(0,0,0,0.8)' }} />

            {/* Desk reflection */}
            <div style={{ width: '300px', height: '12px', background: 'rgba(200,166,141,0.15)', filter: 'blur(12px)', borderRadius: '50%', marginTop: '4px' }} />
          </motion.div>
        </div>

        {/* ── Scroll hint — desktop only ── */}
        <motion.div
          style={{ opacity: textOpacity }}
          className="absolute bottom-[9vh] left-0 right-0 hidden md:flex flex-col items-center gap-3 pointer-events-none select-none z-30"
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}
            className="w-px h-10 bg-semolina/30"
          />
        </motion.div>
      </motion.div>
    </section>
  )
}
