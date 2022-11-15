import React, { useEffect, useState } from 'react'
import { Button, AppBar, Toolbar, Box, Typography, IconButton } from "@mui/material"
import InstallModal from './installModal'
import Service from '../service'
import InfoIcon from '@mui/icons-material/Info';
import HelpDialog from './helpModal';
import HelpModal from './helpModal';
import InstallConfirmation from './installConfirmation';
import DownloadIcon from '@mui/icons-material/Download';
import UploadIcon from '@mui/icons-material/Upload';
import { useSnackbar } from 'notistack';

export default function Header({ cds, originalCds, viewCurrent, setViewCurrent, repo, cmd, setChangedVersions, changedVersions, update }) {
    const [confirmModalOpen, _setConfirmModalOpen] = useState(false)
    const [modalOpen, setModalOpen] = useState(false)
    const [helpModalOpen, setHelpModalOpen] = useState(false)
    const [id, setId] = useState("")
    const fileInputRef = React.useRef(null);
    const { enqueueSnackbar } = useSnackbar();
    
    const canRevert = JSON.stringify(cds) !== JSON.stringify(originalCds);

    const runChanges = () => {
        Service.runInstall(cds.cmdType, { packages: changedVersions }).then(r => {
            setId(r.data.id)
            setModalOpen(true)
        })
    }
    
    const runRevert = () => {
        Service.revert(cds.cmdType).then(r => {
            setId(r.data.id)
            setModalOpen(true)
        })
    }
    const [func, setFunc] = useState("revert")

    const setConfirmModalOpen = (v, f) => {
        if (f) {
            setFunc(f)
        }
        _setConfirmModalOpen(v)
    }

    const downloadCds = () => {
        const fileName = "tree";
        const json = JSON.stringify(cds, null, 2);
        const blob = new Blob([json], { type: "application/json" });
        const href = URL.createObjectURL(blob);

        // create "a" HTLM element with href to file
        const link = document.createElement("a");
        link.href = href;
        link.download = fileName + ".json";
        document.body.appendChild(link);
        link.click();

        // clean up "a" element & remove ObjectURL
        document.body.removeChild(link);
        URL.revokeObjectURL(href);
    }

    const handleFileSelect = event => {
        const fileObj = event.target.files && event.target.files[0];
        if (!fileObj) {
            return;
        }

        const fileReader = new FileReader();
        fileReader.readAsText(fileObj, "UTF-8");
        fileReader.onload = e => {
            let data = null
            try {
                data = JSON.parse(e.target.result)
            } catch {
                enqueueSnackbar(`Failed to read file`, { variant: "error" })
                return
            }
            Service.uploadCds(data).then(r => {
                const cv = {}
                for (const node of Object.values(r.data.nodes)) {
                    cv[node.package] = node.version
                }
                setChangedVersions(cv)
            }).catch((e) => {
                if (e.response) {
                    enqueueSnackbar(e.response.data.error, { variant: 'error' })
                }
            })
        };
    }

    return <Box sx={{ flexGrow: 1 }}>
        <AppBar position="fixed">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ marginRight: "0.25em" }}>
                    LAVI
                </Typography>
                <Typography variant="h6" component="div" sx={{ fontFamily: "monospace", fontSize: "16px", flexGrow: 1 }}>
                    [{cmd}]
                </Typography>
                <Button style={{ marginRight: "1em" }} color="inherit" onClick={() => setViewCurrent(!viewCurrent)}>View {viewCurrent ? "Original" : "Modified"}</Button>
                <Button style={{ marginRight: "1em" }} color="inherit" disabled={!canRevert} onClick={() => setConfirmModalOpen(true, "revert")}>Revert</Button>
                <Button style={{ marginRight: "0.75em" }} color="inherit" onClick={() => setConfirmModalOpen(true, "install")} disabled={Object.keys(changedVersions).length === 0}>Run Changes</Button>
                <IconButton onClick={() => setHelpModalOpen(true)} style={{ color: "white" }}>
                    <InfoIcon />
                </IconButton>
                <IconButton style={{ marginLeft: "0.25em" }} onClick={downloadCds} style={{ color: "white" }}>
                    <DownloadIcon />
                </IconButton>
                <IconButton style={{ marginLeft: "0.25em" }} onClick={() => fileInputRef.current.click()} style={{ color: "white" }}>
                    <UploadIcon />
                </IconButton>
                <InstallConfirmation open={confirmModalOpen} onClose={(v) => {
                    setConfirmModalOpen(false)
                    if (v) {
                        func === "revert" ? runRevert() : runChanges()
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
        <input
            style={{ display: 'none' }}
            ref={fileInputRef}
            type="file"
            onChange={handleFileSelect}
        />
    </Box>
}