const tabs = [
  { id:"map",    icon:"🗺️", label:"Map"    },
  { id:"triage", icon:"🆘", label:"Triage" },
  { id:"alerts", icon:"📡", label:"Alerts" },
  { id:"ndrf",   icon:"🚁", label:"NDRF"   },
]

export default function BottomNav({ active, onChange }) {
  return (
    <div style={{
      display:"flex", height:"58px",
      background:"rgba(6,8,16,0.95)", borderTop:"1px solid rgba(255,255,255,0.08)",
      flexShrink:0
    }}>
      {tabs.map(t => (
        <button key={t.id} onClick={() => onChange(t.id)} style={{
          flex:1, display:"flex", flexDirection:"column",
          alignItems:"center", justifyContent:"center", gap:"3px",
          border:"none", background:"transparent",
          color: active === t.id ? "#00ffaa" : "rgba(240,244,255,0.25)",
          cursor:"pointer", transition:"color .2s",
          borderTop: active === t.id ? "2px solid #00ffaa" : "2px solid transparent"
        }}>
          <span style={{ fontSize:"17px" }}>{t.icon}</span>
          <span style={{ fontSize:"9px", letterSpacing:".08em", textTransform:"uppercase" }}>{t.label}</span>
        </button>
      ))}
    </div>
  )
}