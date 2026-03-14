'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { fadeUp, stagger } from '@/lib/animations'

interface Project {
  id: number
  title: string
  description: string
  detail: string
  tags: string[]
  year: string
  floatDuration: number
  floatDelay: number
}

const projects: Project[] = [
  {
    id: 1,
    title: 'Waternet Dashboard',
    description: 'Predictive maintenance for water pipe infrastructure.',
    detail:
      'Built an end-to-end ML pipeline to predict pipe failures before they happen. Trained an XGBoost model on historical break data, weather patterns, and pipe characteristics. Wrapped in a Streamlit dashboard with real-time filtering and map visualisation, deployed via Docker.',
    tags: ['Python', 'XGBoost', 'Streamlit', 'Docker'],
    year: '2024',
    floatDuration: 5.2,
    floatDelay: 0,
  },
  {
    id: 2,
    title: 'ibtisam.cloud',
    description: 'Scroll-driven portfolio with a portal reveal animation.',
    detail:
      'Designed and built this portfolio from scratch — no templates. The core experience is a scroll-driven laptop zoom that transitions into a fantasy world. Built with Next.js 13 App Router, Framer Motion, TypeScript, and Tailwind CSS.',
    tags: ['Next.js', 'Framer Motion', 'TypeScript', 'Tailwind'],
    year: '2025',
    floatDuration: 6.0,
    floatDelay: 0.9,
  },
  {
    id: 3,
    title: 'Coming soon',
    description: 'Next project in progress.',
    detail: 'Something is being built. Check back soon.',
    tags: [],
    year: '2025',
    floatDuration: 4.8,
    floatDelay: 1.7,
  },
]

export default function ProjectsSection() {
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const selectedProject = projects.find((p) => p.id === selectedId) ?? null

  return (
    <section id="projects" className="relative py-36 px-6 z-[20]">
      <div className="max-w-5xl mx-auto">

        {/* Section header */}
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="mb-20"
        >
          <motion.p
            variants={fadeUp}
            className="text-xs font-medium tracking-[0.22em] text-semolina uppercase mb-4"
          >
            Selected Work
          </motion.p>
          <motion.h2
            variants={fadeUp}
            className="text-4xl md:text-5xl font-light text-cotton-field tracking-tight"
          >
            Projects
          </motion.h2>
        </motion.div>

        {/* Floating cards grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          {projects.map((project, i) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ duration: 0.7, delay: i * 0.14, ease: [0.22, 1, 0.36, 1] }}
              // Float animation via CSS
              animate={{ y: [0, -(8 + i * 2), 0] }}
              // ^ This conflicts with whileInView. Use style instead:
              style={{
                animation: `float-card ${project.floatDuration}s ease-in-out infinite`,
                animationDelay: `${project.floatDelay}s`,
                // Fade out card in grid when it's the selected (expanded) one
                opacity: selectedId !== null && selectedId !== project.id ? 0.35 : 1,
                transition: 'opacity 0.3s ease',
              }}
              onClick={() => setSelectedId(project.id)}
              whileHover={{ scale: 1.05, y: -16, transition: { duration: 0.3 } }}
              className="glass-card rounded-2xl p-7 cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <span className="text-xs font-medium tracking-[0.18em] text-semolina/70 uppercase">
                  {String(i + 1).padStart(2, '0')} · {project.year}
                </span>
                <span className="text-cotton-field/30 text-sm group-hover:rotate-45 transition-transform">↗</span>
              </div>

              <h3 className="text-lg font-medium text-cotton-field mb-3 leading-snug">
                {project.title}
              </h3>
              <p className="text-sm text-cotton-field/55 leading-relaxed mb-6">
                {project.description}
              </p>

              {project.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[11px] px-2.5 py-1 rounded-full text-semolina/70"
                      style={{ background: 'rgba(200, 166, 141, 0.1)' }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {/* ── Fly-toward overlay (click to enter project) ── */}
      <AnimatePresence>
        {selectedProject && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-6 md:p-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            onClick={() => setSelectedId(null)}
          >
            {/* Backdrop blur */}
            <div
              className="absolute inset-0"
              style={{ background: 'rgba(10, 6, 24, 0.82)', backdropFilter: 'blur(18px)' }}
            />

            {/* Project detail card — flies in from bottom */}
            <motion.div
              className="relative max-w-2xl w-full glass-card rounded-3xl p-10 md:p-14"
              initial={{ scale: 0.6, y: 80, opacity: 0 }}
              animate={{ scale: 1, y: 0, opacity: 1 }}
              exit={{ scale: 0.6, y: 80, opacity: 0 }}
              transition={{ type: 'spring', damping: 26, stiffness: 220 }}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close */}
              <button
                onClick={() => setSelectedId(null)}
                className="absolute top-6 right-6 w-8 h-8 rounded-full flex items-center justify-center text-cotton-field/40 hover:text-cotton-field transition-colors"
                style={{ background: 'rgba(255,255,255,0.05)' }}
              >
                ✕
              </button>

              <p className="text-xs font-medium tracking-[0.22em] text-semolina uppercase mb-3">
                {selectedProject.year}
              </p>
              <h2 className="text-3xl md:text-4xl font-light text-cotton-field tracking-tight mb-6">
                {selectedProject.title}
              </h2>
              <p className="text-cotton-field/65 leading-relaxed mb-8">
                {selectedProject.detail}
              </p>

              {selectedProject.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {selectedProject.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-xs px-3 py-1.5 rounded-full text-semolina/80"
                      style={{ background: 'rgba(200, 166, 141, 0.12)' }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  )
}
