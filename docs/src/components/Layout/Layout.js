import { Container } from "@mui/material"
import * as React from "react"
import { media } from "../../theme"
import Header from "../Header/Header"

const Layout = ({ children, disablePadding, style = {}, showFooter }) => {

    return (
        <>
            <div
                /* 124 is height of header */
                style={{
                    maxWidth: disablePadding ? "" : `var(--size-content)`,
                    padding: disablePadding ? "" : `var(--size-gutter)`,
                    display: "flex", 
                    minHeight: "calc(100vh)", 
                    flexDirection: "column", 
                    justifyContent: "space-between",
                    ...style
                }}
            >
            <div>
            <Header />
                <Container sx={{overflowX: "clip", paddingTop: "64px"}} disableGutters={disablePadding} maxWidth={disablePadding ? false : undefined}>
                    {children}
                </Container>
            </div>
            </div>
        </>
    )
}

export default Layout
