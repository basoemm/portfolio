import Link from 'next/link'

export default function Navbar() {
  return (
    <nav
      style={{
        width: '100%',
        padding: '1.5rem 2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'var(--cotton-field)',
        borderBottom: '1px solid rgba(0,0,0,0.05)',
        position: 'relative',
      }}
    >
      <div
        style={{
          fontWeight: 600,
          fontSize: '1.1rem',
          color: 'var(--kilimanjaro)'
        }}
      >
        Ibtisam
      </div>

      <div style={{ display: 'flex', gap: '2rem' }}>
        <Link href="/">Home</Link>
        <Link href="/projects">Projects</Link>
        <Link href="/about">About</Link>
        <Link
          href="/contact"
          style={{
            color: 'white',
            background: 'var(--semolina)',
            padding: '0.5rem 1rem',
            borderRadius: '6px'
          }}
        >
          Contact
        </Link>
      </div>
    </nav>
  )
}
