export default function Hero() {
  return (
    <section style={{
      padding: '6rem 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '4rem',
      maxWidth: '1200px',
      margin: '0 auto'
    }}>
      
      {/* LEFT TEXT SIDE */}
      <div style={{ flex: 1 }}>
        <h1 style={{
          fontSize: '3.8rem',
          fontWeight: '700',
          color: 'var(--kilimanjaro)',
          lineHeight: '1.1',
          marginBottom: '1.5rem'
        }}>
          Crafting elegant digital experiences with intention and clarity.
        </h1>

        <p style={{
          fontSize: '1.3rem',
          lineHeight: '1.7',
          color: 'var(--warrior)',
          maxWidth: '550px'
        }}>
          I’m Ibtisam, a software engineer passionate about building 
          thoughtful, minimalistic, human-centered digital products.
        </p>
      </div>


      {/* RIGHT IMAGE SIDE */}
      <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
        <img 
          src="images/IMG_8181.PNG"
          alt="Ibtisam portrait"
          style={{
            width: '100%',
            maxWidth: '420px',
            borderRadius: '12px',
            objectFit: 'cover',
            boxShadow: '0 8px 30px rgba(0,0,0,0.08)'
          }}
        />
      </div>

    </section>
  );
}