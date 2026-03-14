'use client'

import { motion } from 'framer-motion'
import { fadeUp, stagger } from '@/lib/animations'

export default function ContactSection() {
  return (
    <section id="contact" className="relative py-44 px-6 z-[20] overflow-hidden">
      {/* Portal gate glow at bottom */}
      <div
        className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at 50% 100%, rgba(200, 112, 80, 0.35) 0%, rgba(138, 48, 96, 0.15) 45%, transparent 70%)',
          filter: 'blur(10px)',
        }}
      />

      <div className="max-w-4xl mx-auto text-center relative">
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
        >
          <motion.p
            variants={fadeUp}
            className="text-xs font-medium tracking-[0.22em] text-semolina uppercase mb-6"
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
            className="text-cotton-field/45 mb-14 max-w-sm mx-auto leading-relaxed"
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
              className="px-8 py-4 bg-semolina text-portal font-medium rounded-full hover:bg-semolina/80 transition-colors duration-200"
            >
              LinkedIn
            </a>
            <a
              href="mailto:hello@ibtisam.cloud"
              className="px-8 py-4 text-cotton-field rounded-full hover:bg-cotton-field/6 transition-colors duration-200"
              style={{ border: '1px solid rgba(244, 239, 232, 0.18)' }}
            >
              Send Email
            </a>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
