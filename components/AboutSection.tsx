'use client'

import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { fadeUp, stagger } from '@/lib/animations'

const stats = [
  { label: 'Focus', value: 'Full-Stack' },
  { label: 'Location', value: 'Amsterdam' },
  { label: 'Status', value: 'Available' },
]

export default function AboutSection() {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section id="about" className="py-32 px-6 border-t border-kilimanjaro/8" ref={ref}>
      <div className="max-w-5xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          animate={isInView ? 'visible' : 'hidden'}
          className="grid grid-cols-1 md:grid-cols-2 gap-16 items-start"
        >
          {/* Left — label + headline */}
          <div>
            <motion.p
              variants={fadeUp}
              className="text-xs font-medium tracking-[0.18em] text-semolina uppercase mb-4"
            >
              About
            </motion.p>
            <motion.h2
              variants={fadeUp}
              className="text-4xl md:text-5xl font-light text-kilimanjaro tracking-tight leading-[1.1]"
            >
              Software engineer<br />by craft
            </motion.h2>
          </div>

          {/* Right — bio + stats */}
          <div className="space-y-6">
            <motion.p variants={fadeUp} className="text-warrior/80 leading-relaxed">
              I build software with a focus on experience — the kind that feels
              intuitive, performs well, and doesn&apos;t get in the way of what matters.
            </motion.p>
            <motion.p variants={fadeUp} className="text-warrior/80 leading-relaxed">
              Studying at Amsterdam University of Applied Sciences, working at
              the intersection of software engineering and data science.
            </motion.p>

            <motion.div
              variants={fadeUp}
              className="pt-4 grid grid-cols-3 gap-6 border-t border-kilimanjaro/8"
            >
              {stats.map((item) => (
                <div key={item.label}>
                  <p className="text-xs text-warrior/50 mb-1">{item.label}</p>
                  <p className="text-sm font-medium text-kilimanjaro">{item.value}</p>
                </div>
              ))}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
