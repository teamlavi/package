import React, { useEffect, useState } from 'react'
import { Button, AppBar, Toolbar, Box, Typography } from "@mui/material"
import InstallModal from './installModal'
import Service from '../service'


export default function Header({ viewCurrent, setViewCurrent, repo, setChangedVersions, changedVersions, update }) {
    const [modalOpen, setModalOpen] = useState(false)
    const [id, setId] = useState("")
    const runChanges = () => {
        Service.runInstall(repo, {packages: changedVersions}).then(r => {
            setId(r.data.id)
            setModalOpen(true)
        })
    }

    return <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    LAVI
                </Typography>
                <Button style={{marginRight: "1em"}} color="inherit" onClick={() => setViewCurrent(!viewCurrent)}>View {viewCurrent ? "Original" : "Modified"}</Button> 
                <Button color="inherit" onClick={runChanges} disabled={Object.keys(changedVersions).length === 0}>Run Changes</Button> 
                <InstallModal update={update} id={id} open={modalOpen} onClose={(result) => {
                    if (result === "success") {
                        setChangedVersions({})
                        update()
                    }
                    setModalOpen(false)
                }} />
            </Toolbar>
        </AppBar>
    </Box>
}