import React from 'react'
import { AppBar, Grid, IconButton, Toolbar, Typography } from '@mui/material'
import NavigationBarItem from './NavigationBarItem'
import { styled } from '@mui/material/styles'

const Header = () => {

    return (
        <div>
            <AppBar position="fixed">
                <Grid container justifyContent="center">
                    <Grid item xs={11} md={10}>
                        <Toolbar sx={{ padding: 0 }}>
                            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                                LAVI
                            </Typography>
                            <NavigationBarItem title="Home" route="/" />
                            <NavigationBarItem title="Docs" route="/docs/getting-started/getting-started.html" />
                            <NavigationBarItem title="Interactive API Documentation" route="/api/docs" />
                        </Toolbar>
                    </Grid>
                </Grid>
            </AppBar>
        </div>
    );
}

export default Header
