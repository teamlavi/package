import './App.css';
import Service from "./service"
import React, { useEffect, useState } from 'react';
import { getVulnDataStats, parseApiResponse } from './utils';
import { createTheme, ThemeProvider } from "@mui/material"
import Header from './components/header';
import VulnerabilityTable from './components/table'
import { SnackbarProvider } from 'notistack';

function App() {

  const [original, setOriginal] = useState(null)
  const [resp, setResp] = useState(null)
  const [pkgs, setPkgs] = useState({})
  const [stats, setStats] = useState([])

  const [originalPkgs, setOriginalPkgs] = useState({})
  const [originalStats, setOriginalStats] = useState([])

  const [changedVersions, setChangedVersions] = useState({})
  const theme = createTheme({});
  const [viewCurrent, setViewCurrent] = useState(true)

  const update = () => {
    Service.getCds().then(r => {
      Service.getVulns().then(v => {
        const vulns = v.data
        const resp = r.data
        const tempPkgs = parseApiResponse(resp, vulns)
        const tempStats = getVulnDataStats(resp.nodes, tempPkgs)
        setPkgs(tempPkgs)
        setStats(tempStats)
        setResp(resp)
      })
    })
    Service.getOriginalCds().then(r => {
      Service.getOriginalVulns().then(v => {
      const resp = r.data
      const tempPkgs = parseApiResponse(resp, v.data)
      const tempStats = getVulnDataStats(resp.nodes, tempPkgs)
      setOriginalPkgs(tempPkgs)
      setOriginalStats(tempStats)
      setOriginal(resp)
      })
    })
  }

  useEffect(() => {
    // call api
    update()
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <SnackbarProvider maxSnack={3}>
      {resp && <>
        <Header 
          cds={resp}
          originalCds={original}
          cmd={resp.cmdType} 
          update={update} 
          viewCurrent={viewCurrent} 
          setViewCurrent={setViewCurrent} 
          setChangedVersions={setChangedVersions} 
          changedVersions={changedVersions} 
          repo={resp.repository} 
        />
          <div style={{overflow: 'auto', marginTop: "64px", maxHeight: "calc(100vh - 64px)"}}>
            <VulnerabilityTable
              viewCurrent={viewCurrent}
              changedVersions={changedVersions}
              setChangedVersions={setChangedVersions}
              repo={resp.repository} 
              cds={viewCurrent ? resp : original} 
              stats={viewCurrent ? stats : originalStats} 
              nodes={viewCurrent ? resp.nodes : original.nodes} 
              pkgs={viewCurrent ? pkgs : originalPkgs} 
            />
          </div>
        </>
        }
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
