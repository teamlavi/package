import React, { useEffect, useState } from 'react'
import { Button, AppBar, Toolbar, Box, Typography, IconButton } from "@mui/material"
import InstallModal from './installModal'
import Service from '../service'
import InfoIcon from '@mui/icons-material/Info';
import HelpDialog from './helpModal';
import HelpModal from './helpModal';
import InstallConfirmation from './installConfirmation';

export default function Header({ viewCurrent, setViewCurrent, repo, cmd, setChangedVersions, changedVersions, update }) {
    const [confirmModalOpen, setConfirmModalOpen] = useState(false)
    const [modalOpen, setModalOpen] = useState(false)
    const [helpModalOpen, setHelpModalOpen] = useState(false)
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
                <Typography variant="h6" component="div" sx={{ marginRight: "0.25em" }}>
                    LAVI
                </Typography>
                <Typography variant="h6" component="div" sx={{fontFamily: "monospace", fontSize: "16px", flexGrow: 1}}>
                    [{cmd}]
                </Typography>
                <Button style={{marginRight: "1em"}} color="inherit" onClick={() => setViewCurrent(!viewCurrent)}>View {viewCurrent ? "Original" : "Modified"}</Button> 
                <Button style={{marginRight: "0.5em"}} color="inherit" onClick={() => setConfirmModalOpen(true)} disabled={Object.keys(changedVersions).length === 0}>Run Changes</Button> 
                <IconButton onClick={() => setHelpModalOpen(true)} style={{color: "white"}}>
                    <InfoIcon />
                </IconButton>
                <InstallConfirmation open={confirmModalOpen} onClose={(v) => {
                    setConfirmModalOpen(false)
                    if (v) {
                        runChanges()
                    }
                }} />
                <InstallModal update={update} id={id} open={modalOpen} onClose={(result) => {
                    if (result === "success") {
                        setChangedVersions({})
                        update()
                    }
                    setId("")
                    setModalOpen(false)
                }} />
                <HelpModal open={helpModalOpen} onClose={() => setHelpModalOpen(false)} />
            </Toolbar>
        </AppBar>
    </Box>
}