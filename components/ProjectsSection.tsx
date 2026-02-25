'use client'

import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { fadeUp, stagger } from '@/lib/animations'

const projects = [
  {
    id: 1,
    title: 'Waternet Dashboard',
    description:
      'Predictive maintenance system for water pipe infrastructure. XGBoost ML model + Streamlit dashboard deployed via Docker.',
    tags: ['Python', 'XGBoost', 'Streamlit', 'Docker'],
    year: '2024',
  },
  {
    id: 2,
    title: 'ibtisam.cloud',
    description:
      'Scroll-driven personal portfolio with a laptop zoom reveal animation. Built on Next.js 13, Framer Motion, and Tailwind.',
    tags: ['Next.js', 'Framer Motion', 'TypeScript', 'Tailwind'],
    year: '2025',
  },
  {
    id: 3,
    title: 'Coming soon',
    description: 'Next project in progress.',
    tags: [],
    year: '2025',
  },
]

export default function ProjectsSection() {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section id="projects" className="py-32 px-6" ref={ref}>
      <div className="max-w-5xl mx-auto">
        <motion.div
          variants={stagger}
          initial="hidden"
          animate={isInView ? 'visible' : 'hidden'}
        >
          <motion.p
            variants={fadeUp}
            className="text-xs font-medium tracking-[0.18em] text-semolina uppercase mb-4"
          >
            Selected Work
          </motion.p>
          <motion.h2
            variants={fadeUp}
            className="text-4xl md:text-5xl font-light text-kilimanjaro tracking-tight mb-16"
          >
            Projects
          </motion.h2>

          <div className="space-y-3">
            {projects.map((project, i) => (
              <motion.div
                key={project.id}
                variants={fadeUp}
                className="group border border-kilimanjaro/10 rounded-2xl p-8 bg-silver-bird hover:border-kilimanjaro/20 hover:bg-white/60 transition-all duration-300 cursor-pointer"
              >
                <div className="flex items-start justify-between gap-6">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-xs text-warrior/60">{project.year}</span>
                      <span className="w-4 h-px bg-kilimanjaro/15" />
                      <span className="text-xs font-medium tracking-widest text-semolina/80">
                        {String(i + 1).padStart(2, '0')}
                      </span>
                    </div>
                    <h3 className="text-lg font-medium text-kilimanjaro mb-2 group-hover:text-warrior transition-colors duration-200">
                      {project.title}
                    </h3>
                    <p className="text-sm text-warrior/80 leading-relaxed max-w-xl">
                      {project.description}
                    </p>
                  </div>

                  <motion.div
                    className="flex-shrink-0 w-9 h-9 rounded-full border border-kilimanjaro/12 flex items-center justify-center text-warrior/50 text-sm group-hover:border-kilimanjaro/30 group-hover:text-kilimanjaro transition-all duration-200"
                    whileHover={{ rotate: 45 }}
                    transition={{ duration: 0.2 }}
                  >
                    ↗
                  </motion.div>
                </div>

                {project.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-6">
                    {project.tags.map((tag) => (
                      <span
                        key={tag}
                        className="text-xs px-3 py-1 rounded-full bg-kilimanjaro/5 text-warrior/70"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
