const clouds = [
  { width: 340, height: 90,  top: '8%',  duration: 45, delay: 0,    blur: 20 },
  { width: 480, height: 120, top: '22%', duration: 62, delay: -22,   blur: 26 },
  { width: 220, height: 70,  top: '5%',  duration: 32, delay: -12,   blur: 14 },
  { width: 400, height: 100, top: '40%', duration: 70, delay: -38,   blur: 22 },
  { width: 260, height: 80,  top: '55%', duration: 50, delay: -8,    blur: 18 },
]

export default function CloudLayer() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-10">
      {clouds.map((cloud, i) => (
        <div
          key={i}
          className="absolute"
          style={{
            top: cloud.top,
            width: cloud.width,
            height: cloud.height,
            animation: `cloud-drift ${cloud.duration}s linear infinite`,
            animationDelay: `${cloud.delay}s`,
          }}
        >
          {/* Main cloud body */}
          <div
            className="absolute inset-0 rounded-full"
            style={{
              background: 'rgba(230, 170, 200, 0.10)',
              filter: `blur(${cloud.blur}px)`,
            }}
          />
          {/* Cloud puff — brighter inner core */}
          <div
            className="absolute"
            style={{
              top: '15%',
              left: '20%',
              width: '55%',
              height: '65%',
              borderRadius: '50%',
              background: 'rgba(245, 190, 215, 0.15)',
              filter: `blur(${Math.round(cloud.blur * 0.55)}px)`,
            }}
          />
        </div>
      ))}
    </div>
  )
}
