import Link from 'next/link';

export default function Navbar() {
  return (
    <nav style={{
      width: '100%',
      display: 'flex',
      justifyContent: 'center',     
      background: 'var(--cotton-field)',
      borderBottom: '1px solid rgba(0,0,0,0.05)',
      position: 'sticky',
      top: 0,
      zIndex: 50,
    }}>
      
      <div style={{
        width: '100%',
        maxWidth: '1200px',          
        padding: '1.5rem 2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>

        {/* LOGO */}
        <div style={{
          fontWeight: 600,
          fontSize: '1.1rem',
          color: 'var(--kilimanjaro)',
          whiteSpace: 'nowrap'
        }}>
          Ibtisam
        </div>

        {/* LINKS */}
        <div style={{
          display: 'flex',
          gap: '1.5rem',
          alignItems: 'center',
          flexWrap: 'wrap',
        }}>

          <Link href="/" style={{ whiteSpace: 'nowrap', color: 'var(--kilimanjaro)' }}>
            Home
          </Link>

          <Link href="/projects" style={{ whiteSpace: 'nowrap', color: 'var(--kilimanjaro)' }}>
            Projects
          </Link>

          <Link href="/about" style={{ whiteSpace: 'nowrap', color: 'var(--kilimanjaro)' }}>
            About
          </Link>

          <Link
            href="/contact"
            style={{
              whiteSpace: 'nowrap',
              color: 'white',
              background: 'var(--semolina)',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              minWidth: '90px',         
              textAlign: 'center'
            }}
          >
            Contact
          </Link>
        </div>

      </div>
    </nav>
  );
}