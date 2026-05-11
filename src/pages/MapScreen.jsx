export default function MapScreen() {
  const zones = [
    { name:"Zone A — Koramangala", meta:"2,340 residents · 847 unaccounted", risk:"HIGH RISK", color:"#ff4060" },
    { name:"Zone B — BTM Layout",  meta:"1,890 residents · 210 unaccounted", risk:"WARNING",   color:"#ff8800" },
    { name:"Zone C — Indiranagar", meta:"3,120 residents · 12 unaccounted",  risk:"SAFE",      color:"#00ffaa" },
    { name:"Zone D — HSR Layout",  meta:"2,670 residents · 440 unaccounted", risk:"WATCH",     color:"#ffd060" },
  ]

  return (
    <div style={{ padding:"12px", background:"#060810", minHeight:"100%" }}>

      {/* MAP */}
      <div style={{ position:"relative", borderRadius:"14px", overflow:"hidden", height:"240px", border:"1px solid rgba(255,255,255,0.08)", marginBottom:"12px" }}>
        <div style={{ width:"100%", height:"100%", background:"radial-gradient(ellipse 80% 60% at 50% 50%,#0a1628 0%,#060810 100%)", position:"relative", overflow:"hidden" }}>

          {/* grid */}
          <div style={{ position:"absolute", inset:0, backgroundImage:"linear-gradient(rgba(77,166,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(77,166,255,.06) 1px,transparent 1px)", backgroundSize:"28px 28px" }} />

          {/* scan line */}
          <div style={{ position:"absolute", inset:0, background:"linear-gradient(180deg,transparent 40%,rgba(0,255,170,.04) 50%,transparent 60%)", animation:"scan 4s linear infinite" }} />

          {/* heat blobs */}
          <div style={{ position:"absolute", width:"130px", height:"90px", background:"rgba(255,64,96,.3)", borderRadius:"50%", filter:"blur(22px)", top:"28%", left:"30%", animation:"heatPulse 3s ease-in-out infinite" }} />
          <div style={{ position:"absolute", width:"90px",  height:"70px", background:"rgba(255,136,0,.25)", borderRadius:"50%", filter:"blur(22px)", top:"50%", left:"58%", animation:"heatPulse 3s ease-in-out infinite 1s" }} />
          <div style={{ position:"absolute", width:"70px",  height:"55px", background:"rgba(0,255,170,.15)", borderRadius:"50%", filter:"blur(22px)", top:"15%", left:"62%" }} />

          {/* pins */}
          {[
            { label:"ZONE A", color:"#ff4060", top:"25%", left:"37%" },
            { label:"ZONE B", color:"#ff8800", top:"48%", left:"60%" },
            { label:"SHELTER",color:"#00ffaa", top:"14%", left:"65%" },
            { label:"NDRF",   color:"#4da6ff", top:"68%", left:"22%" },
          ].map(p => (
            <div key={p.label} style={{ position:"absolute", top:p.top, left:p.left, display:"flex", flexDirection:"column", alignItems:"center", gap:"3px" }}>
              <div style={{ width:"10px", height:"10px", borderRadius:"50%", background:p.color, border:"2px solid #060810", boxShadow:`0 0 8px ${p.color}` }} />
              <div style={{ fontSize:"8px", fontWeight:"700", padding:"2px 5px", borderRadius:"3px", background:"rgba(6,8,16,.85)", border:`1px solid ${p.color}`, color:p.color, whiteSpace:"nowrap" }}>{p.label}</div>
            </div>
          ))}

          {/* legend */}
          <div style={{ position:"absolute", bottom:"8px", left:"8px", background:"rgba(6,8,16,.85)", border:"1px solid rgba(255,255,255,0.08)", borderRadius:"8px", padding:"6px 10px" }}>
            {[["#ff4060","HIGH RISK"],["#ff8800","WARNING"],["#00ffaa","SAFE ZONE"]].map(([c,l]) => (
              <div key={l} style={{ display:"flex", alignItems:"center", gap:"5px", fontSize:"8px", color:"rgba(240,244,255,0.5)", lineHeight:"2", fontFamily:"monospace" }}>
                <div style={{ width:"7px", height:"7px", borderRadius:"50%", background:c, boxShadow:`0 0 4px ${c}` }} />
                {l}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ZONE CARDS */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"8px", marginBottom:"10px" }}>
        {zones.map(z => (
          <div key={z.name} style={{ padding:"10px 12px", borderRadius:"12px", border:"1px solid rgba(255,255,255,0.08)", background:"rgba(255,255,255,0.04)", borderLeft:`3px solid ${z.color}`, cursor:"pointer" }}>
            <div style={{ fontSize:"11px", fontWeight:"600", marginBottom:"2px" }}>{z.name}</div>
            <div style={{ fontSize:"9px", color:"rgba(240,244,255,0.5)", fontFamily:"monospace" }}>{z.meta}</div>
            <div style={{ display:"inline-block", marginTop:"5px", fontSize:"8px", fontWeight:"700", padding:"2px 6px", borderRadius:"4px", background:`${z.color}20`, color:z.color, fontFamily:"monospace" }}>{z.risk}</div>
          </div>
        ))}
      </div>

      {/* EVAC ROUTES */}
      {[
        { icon:"🚶", title:"Evacuation Route — Zone A", sub:"4.2 KM · 18 MIN · AVOID 80FT RD" },
        { icon:"🏕️", title:"Nearest Shelter — NIMHANS Ground", sub:"CAPACITY 68% · FOOD + MEDICAL" },
      ].map(e => (
        <div key={e.title} style={{ display:"flex", alignItems:"center", gap:"10px", padding:"11px 13px", borderRadius:"12px", border:"1px solid rgba(255,255,255,0.08)", background:"rgba(255,255,255,0.04)", cursor:"pointer", marginBottom:"8px", transition:"all .2s" }}>
          <span style={{ fontSize:"20px" }}>{e.icon}</span>
          <div>
            <div style={{ fontSize:"11px", fontWeight:"600", marginBottom:"2px" }}>{e.title}</div>
            <div style={{ fontSize:"9px", color:"rgba(240,244,255,0.5)", fontFamily:"monospace" }}>{e.sub}</div>
          </div>
          <span style={{ marginLeft:"auto", color:"rgba(240,244,255,0.25)" }}>›</span>
        </div>
      ))}

      <style>{`
        @keyframes scan { 0%{transform:translateY(-100%)} 100%{transform:translateY(200%)} }
        @keyframes heatPulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.15)} }
      `}</style>
    </div>
  )
}