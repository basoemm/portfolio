export default function Contact() {
  return (
    <section style={{
      padding: '6rem 2rem',
      maxWidth: '900px',
      margin: '0 auto',
      textAlign: 'center'
    }}>
      
      <h1 style={{
        fontSize: '3rem',
        color: 'var(--kilimanjaro)',
        marginBottom: '1rem'
      }}>
        Get in touch
      </h1>

      <p style={{
        color: 'var(--warrior)',
        fontSize: '1.2rem',
        marginBottom: '2rem'
      }}>
        Let’s connect — whether it’s about software engineering,  
        design, FemIT, mentoring, or a new opportunity.
      </p>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '1rem'
      }}>
        
        {/* LinkedIn */}
        <a 
          href="www.linkedin.com/in/ibtisam-mahamed-83096628b"
          target="_blank"
          style={{
            padding: '0.9rem 1.5rem',
            borderRadius: '8px',
            border: '2px solid var(--kilimanjaro)',
            color: 'var(--kilimanjaro)',
            fontWeight: '600'
          }}
        >
          LinkedIn
        </a>

        {/* Download CV */}
        <a 
          href="/Ibtisam-CV.pdf"
          target="_blank"
          style={{
            padding: '0.9rem 1.5rem',
            borderRadius: '8px',
            background: 'var(--semolina)',
            color: 'white',
            fontWeight: '600'
          }}
        >
          Download CV
        </a>

      </div>

    </section>
  );
}