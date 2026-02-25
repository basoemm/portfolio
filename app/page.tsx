import LaptopHero from '@/components/LaptopHero'
import ProjectsSection from '@/components/ProjectsSection'
import AboutSection from '@/components/AboutSection'
import ContactSection from '@/components/ContactSection'

export default function Home() {
  return (
    <main>
      <LaptopHero />
      <ProjectsSection />
      <AboutSection />
      <ContactSection />
    </main>
  )
}
