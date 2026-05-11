
export default function TopBar() {
    
  return (
    <div style={{
      display:"flex", alignItems:"center", justifyContent:"space-between",
      padding:"0 16px", height:"54px",
      background:"rgba(6,8,16,0.95)", borderBottom:"1px solid rgba(255,255,255,0.08)",
      flexShrink:0
    }}>
      <div style={{ display:"flex", alignItems:"center", gap:"10px" }}>
        <div style={{
          width:"30px", height:"30px", borderRadius:"8px",
          background:"linear-gradient(135deg,#00ffaa,#4da6ff)",
          display:"flex", alignItems:"center", justifyContent:"center",
          fontWeight:"700", fontSize:"13px", color:"#000"
        }}>A</div>
        <div>
          <div style={{ fontSize:"15px", fontWeight:"700", letterSpacing:".1em", background:"linear-gradient(90deg,#00ffaa,#4da6ff)", WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent" }}>PulseAid</div>
          <div style={{ fontSize:"8px", color:"rgba(240,244,255,0.3)", letterSpacing:".2em" }}>DISASTER RESPONSE</div>
        </div>
      </div>
      <div style={{ display:"flex", alignItems:"center", gap:"6px",
        padding:"4px 10px", borderRadius:"20px",
        border:"1px solid rgba(0,255,170,0.25)",
        background:"rgba(0,255,170,0.06)",
        fontSize:"9px", color:"#00ffaa", letterSpacing:".08em"
      }}>
        <div style={{ width:"5px", height:"5px", borderRadius:"50%", background:"#00ffaa", boxShadow:"0 0 6px #00ffaa", animation:"blink 1.5s infinite" }}></div>
        ONLINE
      </div>
    </div>
  )
}
