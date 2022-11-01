import './App.css';
import React, { useEffect, useState } from 'react';
import testResp from "./test.json"
import { getVulnDataStats, parseApiResponse } from './utils';
import { createTheme, ThemeProvider } from "@mui/material"
import Header from './components/header';
import VulnerabilityTable from './components/table'

function App() {

  const [pkgs, setPkgs] = useState({})
  const [stats, setStats] = useState({})
  const [changedVersions, setChangedVersion] = useState({})
  const theme = createTheme({});

  useEffect(() => {
    // call api
    const tempPkgs = parseApiResponse(testResp)
    const tempStats = getVulnDataStats(testResp.nodes, tempPkgs)
    setPkgs(tempPkgs)
    setStats(tempStats)
  }, [])


  return (
    <ThemeProvider theme={theme}>
      <div style={{ width: "100%", height: "100%" }}>
        <Header hasChanges={false} />
        <div style={{ display: "flex" }}>
          <div style={{ flexGrow: 1 }}>
            <VulnerabilityTable stats={stats} nodes={testResp.nodes} pkgs={pkgs} />
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
