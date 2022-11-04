import './App.css';
import axios from "axios"
import React, { useEffect, useState } from 'react';
import testResp from "./test.json"
import { getVulnDataStats, parseApiResponse } from './utils';
import { createTheme, ThemeProvider } from "@mui/material"
import Header from './components/header';
import VulnerabilityTable from './components/table'

function App() {

  const [resp, setResp] = useState(null)
  const [pkgs, setPkgs] = useState({})
  const [stats, setStats] = useState({})
  const [changedVersions, setChangedVersion] = useState({})
  const theme = createTheme({});

  useEffect(() => {
    // call api
    axios.get("http://localhost:8080/api/v1/cds").then(r => {
      const resp = r.data
      const tempPkgs = parseApiResponse(resp)
      const tempStats = getVulnDataStats(resp.nodes, tempPkgs)
      setResp(resp)
      setPkgs(tempPkgs)
      setStats(tempStats)
    })
  }, [])


  return (
    <ThemeProvider theme={theme}>
      <div style={{ width: "100%", height: "100%" }}>
        <Header hasChanges={false} />
        <div style={{ display: "flex" }}>
          <div style={{ flexGrow: 1 }}>
            {resp && <VulnerabilityTable stats={stats} nodes={resp.nodes} pkgs={pkgs} />}
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
