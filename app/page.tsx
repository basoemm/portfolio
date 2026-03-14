import LaptopHero from '@/components/LaptopHero'
import ProjectsSection from '@/components/ProjectsSection'
import AboutSection from '@/components/AboutSection'
import ContactSection from '@/components/ContactSection'
import CloudLayer from '@/components/CloudLayer'

export default function Home() {
  return (
    <main>
      <LaptopHero />

      {/* Fantasy world — everything after the portal */}
      <div
        className="relative overflow-hidden"
        style={{
          background:
            'linear-gradient(to bottom, #1a0838 0%, #4a1050 22%, #8a3060 52%, #c87060 75%, #1a0838 100%)',
        }}
      >
        {/* Animated cloud layer */}
        <CloudLayer />

        {/* Sunray from bottom-center */}
        <div
          className="absolute inset-0 pointer-events-none animate-ray-pulse"
          style={{
            background:
              'radial-gradient(ellipse at 50% 85%, rgba(200, 112, 80, 0.4) 0%, rgba(138, 48, 96, 0.18) 35%, transparent 62%)',
          }}
        />

        <ProjectsSection />
        <AboutSection />
        <ContactSection />
      </div>
    </main>
  )
}
