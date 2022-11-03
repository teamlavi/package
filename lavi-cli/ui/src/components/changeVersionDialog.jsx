import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';


function ChangeVersionDialog({ onClose, open }) {

  const handleClose = () => {
    onClose();
  };

  const handleListItemClick = (value) => {
    onClose(value);
  };

  return (
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>Change Version</DialogTitle>
      <DialogContent>
        This will only allow us to get the results for the single package changed, not its indirect deps. So I was thinking we should allow the user to "test install" the changed dependencies, and add a "revert" button to go back to the prev dependencies. That way we can get full information instead of changing a package and saying "this package isn't vulnerable, but its indirect might be idk figure it out"
      </DialogContent>
    </Dialog>
  );
}

export default ChangeVersionDialog