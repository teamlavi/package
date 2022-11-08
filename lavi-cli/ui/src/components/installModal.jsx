import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Service from '../service';
import { Button, DialogActions, FormControl, CircularProgress, MenuItem, Select, Typography } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';

function 
InstallModal({ open, onClose, id }) {
    const [text, setText] = React.useState("")
    const [status, setCompleted] = React.useState("installing")
    const [error, setError] = React.useState("")
    const [interval, setIntervalV] = React.useState(null)

    React.useEffect(() => {
        if (open && (status !== "error" && status !== "success")) {
            const int = setInterval(() => {
                Service.getStdout(id).then(r => {
                    setText(r.data.stdout)
                })
                Service.getStatus(id).then(r => {
                    setCompleted(r.data.status)
                    setError(r.data.error)
                })
            }, 1000)
            setIntervalV(int)
            return () => {
                clearInterval(int)
            }
        } else {
            if (interval) {
                clearInterval(interval)
            }
        }
    }, [open])

    const closeWrapper = (st) => {
        setText("")
        setCompleted("installing")
        onClose(st)
    }

    return (
        <Dialog open={open} maxWidth="md" disableEscapeKeyDown onClose={(_, reason) => { }}>
            <DialogTitle>
                <div style={{display: "flex", alignItems: 'center', gap: "0.5em"}}>
                    <div>Installation Status</div>
                    {status === "success" && <CheckIcon size="1em" color="success" />}
                    {(status === "installing" || status === "vulns") && <CircularProgress size="1em" /> }
                    {status === "error" && <CloseIcon size="1em" color="error"/> }
                </div>
                <Typography style={{fontSize: "14px"}}>
                    {status === "installing" && "Installing selected package versions"}
                    {status === "vulns" && "Scanning for package vulnerabilities" }
                    {status === "error" && `Error: ${error}` }
                </Typography>
            </DialogTitle>
            <DialogContent style={{ padding: "20px 24px" }}>
                <div style={{ width: "800px", height: "350px", maxWidth: "800px", maxHeight: "350px", background: "black", color: "white", fontFamily: "ui-monospace", borderRadius: "5px", padding: "10px", overflow: "auto" }}>
                    <pre>{text}</pre>
                </div>
            </DialogContent>
            <DialogActions>
                <Button onClick={() => closeWrapper(status)} disabled={status !== "error" && status !== "success"}>Close</Button>
            </DialogActions>
        </Dialog>
    );
}

export default InstallModal