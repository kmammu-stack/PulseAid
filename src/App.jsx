import { useState } from "react"
import MapScreen from "./pages/MapScreen"
import TriageScreen from "./pages/TriageScreen"
import AlertsScreen from "./pages/AlertsScreen"
import NDRFScreen from "./pages/NDRFScreen"
import TopBar from "./components/TopBar"
import BottomNav from "./components/BottomNav"

export default function App() {
  const [screen, setScreen] = useState("map")
  const screens = {
    map: <MapScreen />,
    triage: <TriageScreen />,
    alerts: <AlertsScreen />,
    ndrf: <NDRFScreen />
  }
  return (
    <div style={{ height:"100vh", display:"flex", flexDirection:"column", background:"#060810", color:"#f0f4ff", overflow:"hidden" }}>
      <TopBar />
      <div style={{ flex:1, overflowY:"auto" }}>
        {screens[screen]}
      </div>
      <BottomNav active={screen} onChange={setScreen} />
    </div>
  )
}