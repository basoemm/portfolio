export default function LaptopHero() {
  return (
    <section
      style={{
        height: "100vh",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--cotton-field)",
      }}
    >
      <div
        style={{
          position: "relative",
          width: "900px",
          maxWidth: "90vw",
        }}
      >
        {/* Screen (code) */}
        <div
          style={{
            position: "absolute",
            top: "7%",
            left: "7%",
            width: "86%",
            height: "56%",
            overflow: "hidden",
            borderRadius: "4px",
            zIndex: 1,
          }}
        >
          <img
            src="/images/code.png"
            alt="Code"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        </div>

        {/* Laptop frame */}
        <img
          src="/images/laptop.png"
          alt="Laptop frame"
          style={{
            width: "100%",
            height: "auto",
            display: "block",
            position: "relative",
            zIndex: 2,
            pointerEvents: "none",
          }}
        />
      </div>
    </section>
  );
}