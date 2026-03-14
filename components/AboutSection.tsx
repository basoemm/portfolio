'use client'

import { motion } from 'framer-motion'
import { fadeUp, stagger } from '@/lib/animations'

const stats = [
  { label: 'Focus', value: 'Full-Stack' },
  { label: 'Location', value: 'Amsterdam' },
  { label: 'Status', value: 'Available' },
]

export default function AboutSection() {
  return (
    <section id="about" className="relative py-36 px-6 z-[20]">
      {/* Subtle divider glow */}
      <div
        className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-px pointer-events-none"
        style={{ background: 'linear-gradient(to right, transparent, rgba(200,166,141,0.3), transparent)' }}
      />

      <div className="max-w-5xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid grid-cols-1 md:grid-cols-2 gap-16 items-start"
        >
          {/* Left */}
          <div>
            <motion.p
              variants={fadeUp}
              className="text-xs font-medium tracking-[0.22em] text-semolina uppercase mb-4"
            >
              About
            </motion.p>
            <motion.h2
              variants={fadeUp}
              className="text-4xl md:text-5xl font-light text-cotton-field tracking-tight leading-[1.1]"
            >
              Software engineer<br />by craft
            </motion.h2>
          </div>

          {/* Right */}
          <div className="space-y-6">
            <motion.p variants={fadeUp} className="text-cotton-field/60 leading-relaxed">
              I build software with a focus on experience — the kind that feels
              intuitive, performs well, and doesn&apos;t get in the way of what matters.
            </motion.p>
            <motion.p variants={fadeUp} className="text-cotton-field/60 leading-relaxed">
              Studying at Amsterdam University of Applied Sciences, working at
              the intersection of software engineering and data science.
            </motion.p>

            <motion.div
              variants={fadeUp}
              className="pt-5 grid grid-cols-3 gap-6"
              style={{ borderTop: '1px solid rgba(200, 166, 141, 0.12)' }}
            >
              {stats.map((item) => (
                <div key={item.label}>
                  <p className="text-xs text-cotton-field/30 mb-1.5">{item.label}</p>
                  <p className="text-sm font-medium text-cotton-field/85">{item.value}</p>
                </div>
              ))}
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
