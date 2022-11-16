import * as React from 'react';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import Service from '../service';
import { Autocomplete, Button, DialogActions, FormControl, IconButton, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';

const steps = [
  {
    label: "General",
    description: [`LAVI is a tool built to help uncover hidden vulnerabilities that can be nested deeply inside a project's dependency tree. 
                  The UI allows users to get a more indepth look into those vulnerabilities, and make informed decisions on how to deal with them.`]
  },
  {
    label: "Header",
    description: [
      `The header contains some buttons that allow for easy control over the status of your vulnerability investigation.`,
      `On the right side, there are controls for viewing the original dependency tree (which when clicked, changes to allow you to go back to the modified dependency tree), 
                  a button to scan the modified tree, and a button to revert back to the original state of the tree.`,
    ]
  },
  {
    label: "Table",
    description: [
      `The first row of the table shows accumulated low severity, medium severity, and high severity vulnerability counts for the current tree (original or modified).`,
      `The following rows show each individual direct dependency (as provided by the package manager on your system), along with individual counts for low, medium, and high severity vulnerabilities.
      There is also a button on the left which will expand the row to show each indirect dependency, and the vulnerability that applies to it. This button will be disabled if there are no vulnerabilities found.`,
      `On the right side of the row, there is an edit button which is how you can modify dependency versions. Once a version is changed, you can reset it with the reset button that pops up.
      Once you change a version, the vulnerability counts for that row will disappear because you now need to rescan the tree using the "Run Changes" button in the header to find new vulnerabilities.`
    ]
  },
  {
    label: "Installation",
    description: [
      `Due to the nature of program dependencies, where they can be provided as a range of values, your system must install them first, so the package manager can pin them to an exact version. That is done during the installation phase of the scanning process.`,
      `Then, the tree will be fully rescanned, and allow you to look at the new vulnerabilities, and compare them to the original vulnerabilities.`
    ]
  },
]

function HelpModal({ onClose, open }) {

  const handleClose = () => {
    onClose();
  };

  const [activeStep, setActiveStep] = React.useState(0);
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };


  return (
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>
        <div>LAVI Help</div>
        <Typography style={{ fontSize: "14px" }}>
          {steps[activeStep].label}
        </Typography>
      </DialogTitle>
      <DialogContent style={{ width: "500px" }}>
        {steps[activeStep].description.map((t) => <div><Typography>{t}</Typography><br /></div>)}
      </DialogContent>
      <DialogActions>
        <div style={{ flexGrow: 1 }}>
          <IconButton disabled={activeStep === 0} onClick={handleBack}>
            <KeyboardArrowLeftIcon />
          </IconButton>
        </div>
        <div style={{ flexGrow: 1 }}>
          <Button autoFocus onClick={handleClose}>
            Close
          </Button>
        </div>
        <IconButton disabled={activeStep === steps.length - 1} onClick={handleNext}>
          <KeyboardArrowRightIcon />
        </IconButton>
      </DialogActions>
    </Dialog>
  );
}

export default HelpModal