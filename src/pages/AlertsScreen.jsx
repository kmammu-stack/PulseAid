import { useState } from "react"

export default function AlertsScreen() {
  const [filter, setFilter] = useState("ALL")

  const alerts = [
    { type:"crit", title:"⚠️ Flash flood detected — Zone A", time:"14:47", body:"Water levels rising at 12cm/hr on 80 Feet Road. Immediate evacuation required for all residents below ground floor.", tags:["CRITICAL","EVAC","ZONE A"], color:"#ff4060" },
    { type:"warn", title:"🌧️ Heavy rainfall forecast — next 6hrs", time:"13:20", body:"IMD predicts 94mm rainfall in the next 6 hours. Zones B and D at elevated risk. Pre-position rescue assets now.", tags:["WARNING","WEATHER","ZONE B/D"], color:"#ff8800" },
    { type:"info", title:"🏕️ Shelter capacity update", time:"12:55", body:"NIMHANS Ground at 68% capacity. SJCE campus shelter now open — accepts up to 500 persons, medical unit on-site.", tags:["INFO","SHELTER"], color:"#4da6ff" },
    { type:"warn", title:"📡 Network degraded — Zone A", time:"12:10", body:"Mobile tower overload in Zone A. SMS fallback active. Bluetooth mesh relay enabled for peer-to-peer communication.", tags:["WARNING","NETWORK"], color:"#ff8800" },
    { type:"info", title:"🚁 NDRF Team 3 deployed", time:"11:48", body:"NDRF rescue team dispatched to Zone A sector 4. ETA 45 minutes. 2 boats, 1 medical unit, 12 personnel.", tags:["INFO","NDRF"], color:"#4da6ff" },
  ]

  const filters = ["ALL","CRITICAL","WARNING","INFO","EVAC","NDRF"]

  return (
    <div style={{ padding:"12px", background:"#060810", minHeight:"100%" }}>

      {/* WS STATUS */}
      <div style={{ display:"flex", alignItems:"center", gap:"6px", padding:"7px 11px", borderRadius:"8px", border:"1px solid rgba(0,255,170,.2)", background:"rgba(0,255,170,.04)", marginBottom:"10px", fontSize:"9px", fontFamily:"monospace", color:"#00ffaa" }}>
        <div style={{ width:"5px", height:"5px", borderRadius:"50%", background:"#00ffaa", boxShadow:"0 0 6px #00ffaa", animation:"blink 1.5s infinite" }} />
        LIVE FEED · WEBSOCKET CONNECTED
        <span style={{ marginLeft:"auto", opacity:.5 }}>↻ AUTO</span>
      </div>

      {/* FILTERS */}
      <div style={{ display:"flex", gap:"6px", marginBottom:"10px", overflowX:"auto", paddingBottom:"2px" }}>
        {filters.map(f => (
          <div key={f} onClick={() => setFilter(f)} style={{
            flexShrink:0, padding:"4px 11px", borderRadius:"20px",
            fontSize:"9px", fontWeight:"600", letterSpacing:".06em",
            fontFamily:"monospace", cursor:"pointer",
            border: filter===f ? "1px solid #00ffaa" : "1px solid rgba(255,255,255,0.12)",
            color: filter===f ? "#00ffaa" : "rgba(240,244,255,0.4)",
            background: filter===f ? "rgba(0,255,170,.08)" : "transparent",
            transition:"all .2s"
          }}>{f}</div>
        ))}
      </div>

      {/* ALERTS */}
      {alerts.map((a, i) => (
        <div key={i} style={{
          borderRadius:"12px", border:"1px solid rgba(255,255,255,0.08)",
          background:"rgba(255,255,255,0.04)", padding:"12px 14px",
          marginBottom:"8px", cursor:"pointer",
          borderLeft:`3px solid ${a.color}`,
          transition:"all .2s"
        }}>
          <div style={{ display:"flex", alignItems:"flex-start", justifyContent:"space-between", gap:"8px", marginBottom:"4px" }}>
            <div style={{ fontSize:"11px", fontWeight:"600", lineHeight:"1.35" }}>{a.title}</div>
            <div style={{ fontSize:"9px", color:"rgba(240,244,255,0.3)", fontFamily:"monospace", flexShrink:0 }}>{a.time}</div>
          </div>
          <div style={{ fontSize:"10px", color:"rgba(240,244,255,0.5)", lineHeight:"1.5", marginBottom:"7px" }}>{a.body}</div>
          <div style={{ display:"flex", gap:"4px", flexWrap:"wrap" }}>
            {a.tags.map(t => (
              <span key={t} style={{ fontSize:"8px", fontWeight:"700", padding:"2px 6px", borderRadius:"4px", fontFamily:"monospace", background:`${a.color}18`, color:a.color }}>{t}</span>
            ))}
          </div>
        </div>
      ))}

      <style>{`@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}`}</style>
    </div>
  )
}