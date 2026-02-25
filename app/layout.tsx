import type { Metadata } from 'next'
import localFont from 'next/font/local'
import './globals.css'
import Navbar from '@/components/Navbar'

const inter = localFont({
  src: [
    {
      path: '../public/fonts/Inter-roman.latin.var.woff2',
      weight: '100 900',
      style: 'normal',
    },
    {
      path: '../public/fonts/Inter-italic.latin.var.woff2',
      weight: '100 900',
      style: 'italic',
    },
  ],
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  metadataBase: new URL('https://ibtisam.cloud'),
  title: 'Ibtisam — Software Engineer',
  description: 'Software engineer building digital experiences that matter.',
  openGraph: {
    title: 'Ibtisam — Software Engineer',
    description: 'Software engineer building digital experiences that matter.',
    url: 'https://ibtisam.cloud',
    siteName: 'ibtisam.cloud',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Ibtisam — Software Engineer',
  },
  robots: { index: true, follow: true },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="bg-cotton-field text-kilimanjaro font-sans antialiased overflow-x-hidden">
        <Navbar />
        {children}
      </body>
    </html>
  )
}
