import React from 'react'
import { Button, AppBar, Toolbar, Box, Typography } from "@mui/material"


export default function Header({ hasChanges }) {
    return <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    LAVI
                </Typography>
                <Button color="inherit" disabled={!hasChanges}>Run Changes</Button>
            </Toolbar>
        </AppBar>
    </Box>
}