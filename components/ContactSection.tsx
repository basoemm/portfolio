'use client'

import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { fadeUp, stagger } from '@/lib/animations'

export default function ContactSection() {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section id="contact" className="py-40 px-6 bg-kilimanjaro" ref={ref}>
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          variants={stagger}
          initial="hidden"
          animate={isInView ? 'visible' : 'hidden'}
        >
          <motion.p
            variants={fadeUp}
            className="text-xs font-medium tracking-[0.18em] text-semolina uppercase mb-6"
          >
            Get in touch
          </motion.p>

          <motion.h2
            variants={fadeUp}
            className="text-5xl md:text-7xl font-light text-cotton-field tracking-tight leading-[1.05] mb-8"
          >
            Let&apos;s build<br />something
          </motion.h2>

          <motion.p
            variants={fadeUp}
            className="text-warrior/70 mb-12 max-w-sm mx-auto leading-relaxed"
          >
            Open to new opportunities, collaborations, and interesting conversations.
          </motion.p>

          <motion.div
            variants={fadeUp}
            className="flex flex-wrap items-center justify-center gap-4"
          >
            <a
              href="https://www.linkedin.com/in/ibtisam-mahamed-83096628b"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-semolina text-kilimanjaro font-medium rounded-full hover:bg-semolina/85 transition-colors duration-200"
            >
              LinkedIn
            </a>
            <a
              href="mailto:hello@ibtisam.cloud"
              className="px-8 py-4 border border-cotton-field/20 text-cotton-field rounded-full hover:bg-cotton-field/8 transition-colors duration-200"
            >
              Send Email
            </a>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
