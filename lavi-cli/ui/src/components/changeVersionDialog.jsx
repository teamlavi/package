import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Service from '../service';
import { Autocomplete, Button, DialogActions, FormControl, InputLabel, MenuItem, Select, TextField } from '@mui/material';


function ChangeVersionDialog({ onClose, repo, ver, packageName, open }) {

  React.useEffect(() => {
    if (open) {
      Service.getVersions(repo, packageName).then(r => {
        setVersions(r.data)
      })
    }
  }, [open])

  const [version, setVersion] = React.useState(ver)
  const [versions, setVersions] = React.useState([])

  const handleClose = () => {
    onClose();
  };

  const handleChange = (e, v) => {
    setVersion(v);
  };

  return (
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>Change Version of {packageName}</DialogTitle>
      <DialogContent style={{ padding: "20px 24px" }}>
      <Autocomplete
  id="combo-box-demo"
  options={versions}
  sx={{ width: 300 }}
  onChange={handleChange}
  renderInput={(params) => <TextField {...params} label="Version" />}
/>
        {/* <FormControl fullWidth>
          <InputLabel id="demo-simple-select-label">Version</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={version}
            label="Version"
            onChange={handleChange}
          >
            {versions.map(v => <MenuItem value={v}>{v}</MenuItem>)}
          </Select>
        </FormControl> */}
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={onClose}>
          Cancel
        </Button>
        <Button onClick={() => onClose(version)}>Ok</Button>
      </DialogActions>
    </Dialog>
  );
}

export default ChangeVersionDialog