import './App.css';
import Service from "./service"
import React, { useEffect, useState } from 'react';
import { getVulnDataStats, parseApiResponse } from './utils';
import { createTheme, ThemeProvider } from "@mui/material"
import Header from './components/header';
import VulnerabilityTable from './components/table'

function App() {

  const [original, setOriginal] = useState(null)
  const [resp, setResp] = useState(null)
  const [pkgs, setPkgs] = useState({})
  const [stats, setStats] = useState({})

  const [originalPkgs, setOriginalPkgs] = useState({})
  const [originalStats, setOriginalStats] = useState({})

  const [changedVersions, setChangedVersions] = useState({})
  const theme = createTheme({});
  const [viewCurrent, setViewCurrent] = useState(true)

  const update = () => {
    Service.getCds().then(r => {
      const resp = r.data
      const tempPkgs = parseApiResponse(resp)
      const tempStats = getVulnDataStats(resp.nodes, tempPkgs)
      setResp(resp)
      setPkgs(tempPkgs)
      setStats(tempStats)
    })
    Service.getOriginalCds().then(r => {
      const resp = r.data
      const tempPkgs = parseApiResponse(resp)
      const tempStats = getVulnDataStats(resp.nodes, tempPkgs)
      setOriginal(resp)
      setOriginalPkgs(tempPkgs)
      setOriginalStats(tempStats)
    })
  }

  useEffect(() => {
    // call api
    update()
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <div style={{ width: "100%", height: "100%" }}>
      {resp && <>
        <Header update={update} viewCurrent={viewCurrent} setViewCurrent={setViewCurrent} setChangedVersions={setChangedVersions} changedVersions={changedVersions} repo={resp.repository} />
        <div style={{ display: "flex" }}>
          <div style={{ flexGrow: 1 }}>
            <VulnerabilityTable
              viewCurrent={viewCurrent}
              changedVersions={changedVersions}
              setChangedVersions={setChangedVersions}
              repo={resp.repository} 
              stats={viewCurrent ? stats : originalStats} 
              nodes={viewCurrent ? resp.nodes : original.nodes} 
              pkgs={viewCurrent ? pkgs : originalPkgs} 
            />
          </div>
        </div>
        </>
        }
      </div>
    </ThemeProvider>
  );
}

export default App;
