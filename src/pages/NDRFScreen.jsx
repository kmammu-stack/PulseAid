export default function NDRFScreen() {
  const dispatch = [
    { rank:1, zone:"Zone A — Sector 4, Koramangala", meta:"28 CRITICAL · 3.1KM · ETA 22 MIN", score:"P:94", scoreColor:"#ff4060" },
    { rank:2, zone:"Zone A — Sector 7, 80 Ft Road",  meta:"12 CRITICAL · 4.8KM · ETA 31 MIN", score:"P:81", scoreColor:"#ff4060" },
    { rank:3, zone:"Zone B — BTM 2nd Stage",          meta:"7 CRITICAL · 6.2KM · ETA 38 MIN",  score:"P:67", scoreColor:"#ff8800" },
    { rank:4, zone:"Zone D — HSR Sector 2",           meta:"0 CRITICAL · 44 INJURED · 7.9KM",  score:"P:42", scoreColor:"#ff8800" },
    { rank:5, zone:"Zone C — Indiranagar 100ft",      meta:"0 CRITICAL · 8 INJURED · 9.1KM",   score:"P:18", scoreColor:"#00ffaa" },
  ]

  const rankStyle = (r) => {
    if (r===1) return { background:"#ff4060", color:"#fff", boxShadow:"0 0 12px rgba(255,64,96,.5)" }
    if (r===2) return { background:"#ff8800", color:"#000", boxShadow:"0 0 10px rgba(255,136,0,.4)" }
    if (r===3) return { background:"#ffd060", color:"#000", boxShadow:"0 0 10px rgba(255,208,96,.3)" }
    return { background:"rgba(255,255,255,0.06)", color:"rgba(240,244,255,0.4)", border:"1px solid rgba(255,255,255,0.1)" }
  }

  return (
    <div style={{ padding:"12px", background:"#060810", minHeight:"100%" }}>

      {/* STATS */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:"8px", marginBottom:"14px" }}>
        {[
          { num:"47",   label:"Critical", color:"#ff4060", glow:"rgba(255,64,96,.15)"  },
          { num:"183",  label:"Injured",  color:"#ffd060", glow:"rgba(255,208,96,.12)" },
          { num:"1,204",label:"Safe",     color:"#00ffaa", glow:"rgba(0,255,170,.15)"  },
        ].map(s => (
          <div key={s.label} style={{ padding:"12px 8px", borderRadius:"12px", border:"1px solid rgba(255,255,255,0.08)", background:"rgba(255,255,255,0.04)", textAlign:"center", position:"relative", overflow:"hidden" }}>
            <div style={{ position:"absolute", inset:0, background:`radial-gradient(ellipse at 50% 120%,${s.glow},transparent 70%)`, pointerEvents:"none" }} />
            <div style={{ fontSize:"22px", fontWeight:"700", fontFamily:"monospace", color:s.color, textShadow:`0 0 12px ${s.color}60` }}>{s.num}</div>
            <div style={{ fontSize:"8px", color:"rgba(240,244,255,0.4)", letterSpacing:".1em", textTransform:"uppercase", marginTop:"3px" }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* DISPATCH */}
      <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:"8px" }}>
        <div style={{ fontSize:"10px", fontWeight:"700", letterSpacing:".1em", textTransform:"uppercase", color:"rgba(240,244,255,0.5)" }}>AI Dispatch Priority</div>
        <button style={{ fontSize:"9px", padding:"3px 10px", borderRadius:"6px", border:"1px solid rgba(255,255,255,0.12)", background:"rgba(255,255,255,0.04)", color:"rgba(240,244,255,0.5)", cursor:"pointer", fontFamily:"monospace" }}>↻ Refresh</button>
      </div>

      {dispatch.map(d => (
        <div key={d.rank} style={{ display:"flex", alignItems:"center", gap:"10px", padding:"10px 12px", borderRadius:"12px", border:"1px solid rgba(255,255,255,0.08)", background:"rgba(255,255,255,0.04)", marginBottom:"7px", cursor:"pointer", transition:"all .2s" }}>
          <div style={{ width:"26px", height:"26px", borderRadius:"50%", display:"flex", alignItems:"center", justifyContent:"center", fontSize:"11px", fontWeight:"800", fontFamily:"monospace", flexShrink:0, ...rankStyle(d.rank) }}>{d.rank}</div>
          <div style={{ flex:1 }}>
            <div style={{ fontSize:"11px", fontWeight:"600", marginBottom:"2px" }}>{d.zone}</div>
            <div style={{ fontSize:"9px", color:"rgba(240,244,255,0.4)", fontFamily:"monospace" }}>{d.meta}</div>
          </div>
          <div style={{ fontSize:"10px", fontWeight:"700", fontFamily:"monospace", padding:"2px 7px", borderRadius:"5px", background:`${d.scoreColor}20`, color:d.scoreColor }}>{d.score}</div>
        </div>
      ))}

      {/* REPORT BTN */}
      <button style={{ width:"100%", padding:"12px", borderRadius:"10px", border:"1px solid rgba(255,255,255,0.12)", background:"transparent", color:"rgba(240,244,255,0.5)", fontSize:"11px", fontWeight:"600", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center", gap:"8px", marginTop:"4px", transition:"all .3s" }}
        onMouseOver={e => { e.currentTarget.style.borderColor="rgba(0,255,170,.4)"; e.currentTarget.style.color="#00ffaa" }}
        onMouseOut={e => { e.currentTarget.style.borderColor="rgba(255,255,255,0.12)"; e.currentTarget.style.color="rgba(240,244,255,0.5)" }}>
        📋 Generate NDRF Incident Report
      </button>
    </div>
  )
}