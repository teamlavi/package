import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Service from '../service';
import { Button, DialogActions, FormControl, CircularProgress, MenuItem, Select, Typography, FormGroup, FormControlLabel, Checkbox } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';

function InstallConfirmation({ open, onClose }) {
    const [confirm, setConfirm] = React.useState(false)
    return (
        <Dialog open={open} maxWidth="md" onClose={() => onClose(false)}>
            <DialogTitle>
                Confirm
            </DialogTitle>
            <DialogContent style={{ padding: "20px 24px" }}>
                <Typography>
                    This operation <b>will</b> install the new dependencies onto your system. However, LAVI will keep track of previous dependencies which will allow for you to revert back to your original installation. There is also a button that allows for downloading your original dependency tree, just as another backup.
                </Typography>
                <FormGroup>
                    <FormControlLabel control={<Checkbox value={confirm} onChange={(e) => setConfirm(e.target.checked)} />} label="I confirm I have read and understand the above statement" />
                </FormGroup>
            </DialogContent>
            <DialogActions>
                <Button onClick={() => onClose(false)}>Cancel</Button>
                <Button onClick={() => onClose(true)} disabled={!confirm}>Ok</Button>
            </DialogActions>
        </Dialog>
    );
}

export default InstallConfirmation