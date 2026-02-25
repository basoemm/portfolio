'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 60)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? 'bg-cotton-field/95 backdrop-blur-md border-b border-kilimanjaro/5'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
        <Link
          href="/"
          className="text-kilimanjaro font-medium tracking-tight hover:text-warrior transition-colors duration-200"
        >
          Ibtisam
        </Link>

        <div className="flex items-center gap-8">
          <Link
            href="#projects"
            className="text-sm text-warrior hover:text-kilimanjaro transition-colors duration-200"
          >
            Projects
          </Link>
          <Link
            href="#about"
            className="text-sm text-warrior hover:text-kilimanjaro transition-colors duration-200"
          >
            About
          </Link>
          <Link
            href="#contact"
            className="text-sm px-5 py-2 bg-kilimanjaro text-cotton-field rounded-full hover:bg-warrior transition-colors duration-200"
          >
            Contact
          </Link>
        </div>
      </div>
    </nav>
  )
}
