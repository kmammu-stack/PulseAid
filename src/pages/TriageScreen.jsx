import { useState } from "react"

export default function TriageScreen() {
  const [selected, setSelected] = useState(null)
  const [queued, setQueued] = useState(0)

  function submit() {
    if (!selected) return
    setQueued(q => q + 1)
    setSelected(null)
  }

  const options = [
    { id:"green",  emoji:"🟢", label:"SAFE",     desc:"Uninjured, no help needed", color:"#00ffaa" },
    { id:"yellow", emoji:"🟡", label:"INJURED",  desc:"Hurt, stable, need help",   color:"#ffd060" },
    { id:"red",    emoji:"🔴", label:"CRITICAL", desc:"Urgent rescue needed",      color:"#ff4060" },
  ]

  return (
    <div style={{ padding:"12px", background:"#060810", minHeight:"100%" }}>

      {/* HEADER */}
      <div style={{ textAlign:"center", padding:"16px", marginBottom:"12px", borderRadius:"14px", border:"1px solid rgba(255,255,255,0.08)", background:"rgba(255,255,255,0.04)", position:"relative", overflow:"hidden" }}>
        <div style={{ position:"absolute", inset:0, background:"radial-gradient(ellipse at 50% 100%,rgba(0,255,170,.06),transparent 60%)", pointerEvents:"none" }} />
        <div style={{ fontSize:"16px", fontWeight:"700", letterSpacing:".04em", marginBottom:"4px" }}>Mark Your Status</div>
        <div style={{ fontSize:"9px", color:"rgba(240,244,255,0.4)", letterSpacing:".12em", fontFamily:"monospace" }}>YOUR IDENTITY TOKEN · BLR-4482-K</div>
        {/* QR */}
        <div style={{ width:"72px", height:"72px", margin:"12px auto 6px", background:"white", borderRadius:"8px", padding:"6px", display:"grid", gridTemplateColumns:"repeat(7,1fr)", gap:"1.5px" }}>
          {Array.from({length:49}).map((_,i) => (
            <div key={i} style={{ background: (i%3===0||i%7===0||i%11===0) ? "#000":"#fff", borderRadius:"1px" }} />
          ))}
        </div>
        <div style={{ fontSize:"9px", color:"rgba(240,244,255,0.3)", fontFamily:"monospace" }}>UID · BLR-4482-K</div>
      </div>

      {/* OFFLINE BANNER */}
      <div style={{ display:"flex", alignItems:"center", gap:"8px", padding:"8px 12px", borderRadius:"10px", border:"1px solid rgba(255,136,0,.25)", background:"rgba(255,136,0,.06)", marginBottom:"12px", fontSize:"10px", color:"#ff8800", fontFamily:"monospace" }}>
        <span>📵</span>
        <span>Offline — updates sync on reconnect</span>
        <span style={{ marginLeft:"auto", background:"rgba(255,136,0,.15)", padding:"1px 7px", borderRadius:"4px", fontSize:"9px", fontWeight:"700" }}>{queued} QUEUED</span>
      </div>

      {/* TRIAGE BUTTONS */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:"8px", marginBottom:"12px" }}>
        {options.map(o => (
          <button key={o.id} onClick={() => setSelected(o.id)} style={{
            border:`1.5px solid ${selected===o.id ? o.color : o.color+"50"}`,
            borderRadius:"12px", padding:"16px 6px", cursor:"pointer",
            display:"flex", flexDirection:"column", alignItems:"center", gap:"5px",
            background: selected===o.id ? `${o.color}18` : "transparent",
            boxShadow: selected===o.id ? `0 0 20px ${o.color}30` : "none",
            transition:"all .2s", position:"relative"
          }}>
            {selected===o.id && <span style={{ position:"absolute", top:"6px", right:"8px", fontSize:"10px", color:o.color }}>✓</span>}
            <span style={{ fontSize:"26px" }}>{o.emoji}</span>
            <span style={{ fontSize:"10px", fontWeight:"700", letterSpacing:".06em", color:o.color }}>{o.label}</span>
            <span style={{ fontSize:"8px", color:"rgba(240,244,255,0.5)", textAlign:"center", lineHeight:"1.3" }}>{o.desc}</span>
          </button>
        ))}
      </div>

      {/* SUBMIT */}
      <button onClick={submit} disabled={!selected} style={{
        width:"100%", padding:"13px", border:"none", borderRadius:"10px",
        background: selected ? "linear-gradient(90deg,#00ffaa,#4da6ff)" : "rgba(255,255,255,0.06)",
        color: selected ? "#000" : "rgba(240,244,255,0.25)",
        fontWeight:"700", fontSize:"12px", letterSpacing:".06em",
        cursor: selected ? "pointer" : "default", transition:"all .2s",
        boxShadow: selected ? "0 0 20px rgba(0,255,170,.3)" : "none"
      }}>SUBMIT STATUS</button>

      {/* INFO GRID */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"8px", marginTop:"12px" }}>
        {[
          { label:"Last synced", val:"14:32 IST" },
          { label:"Your zone",   val:"Zone A" },
          { label:"Nearest shelter", val:"4.2 km" },
          { label:"Rescue ETA", val:"~2h 15m", color:"#ff8800" },
        ].map(item => (
          <div key={item.label} style={{ padding:"10px 12px", borderRadius:"10px", border:"1px solid rgba(255,255,255,0.08)", background:"rgba(255,255,255,0.04)" }}>
            <div style={{ fontSize:"8px", color:"rgba(240,244,255,0.3)", fontFamily:"monospace", letterSpacing:".1em", textTransform:"uppercase", marginBottom:"3px" }}>{item.label}</div>
            <div style={{ fontSize:"13px", fontWeight:"700", color: item.color || "#f0f4ff" }}>{item.val}</div>
          </div>
        ))}
      </div>
    </div>
  )
}