import * as React from "react"
import { Grid, Button, Typography } from "@mui/material"

import Layout from "../components/Layout/Layout"
import Seo from "../components/seo"
import HomepageCard from "../components/HomepageCard/HomepageCard"
import { darken, alpha } from "@mui/system"
import { styled } from '@mui/material/styles'
import { Link } from "gatsby"

const Downloads = () => {
	return <Layout disablePadding style={{ backgroundColor: "white" }} showFooter>
		<Seo title="Documentation" />
			<Grid
				container
				direction="column"
				alignItems="center"
				justifyContent="center"
				sx={{ pt: "2em", pb: "2em", backgroundColor: "#2a445c", color: "white" }}
			>
				<Grid item xs={12}>
					<Typography variant="h1"
						component="h1" sx={{
							fontSize: '60px',
							lineHeight: 'normal',
							letterSpacing: '2px',
							textAlign: 'center',
							fontWeight: 600,
						}}>LAVI</Typography>
					<Typography variant="p"
						component="p" sx={{
							textAlign: 'center',
							paddingTop: "15px",
							fontSize: "24px",
							fontWeight: 200,
						}}>Downloads</Typography>
				</Grid>
			</Grid>
            <div style={{padding: "4em 4em"}}>
				<Typography 
					variant="h1" 
					component="h1" 
					sx={{
						fontSize: '45px',
						lineHeight: 'normal',
						letterSpacing: '2px',
						fontWeight: 600,
					}}>
						LAVI Downloads
				</Typography>
				<Typography style={{paddingTop: "2em"}}>
                    MacOS (non M series CPU): <a href="/downloads/lavi/lavi-cli-darwin-arm64.zip">Download</a>
				</Typography>
				<Typography style={{paddingTop: "2em"}}>
                    MacOS (Intel CPU): <a href="/downloads/lavi/lavi-cli-darwin-amd64.zip">Download</a>
				</Typography>
				<Typography style={{paddingTop: "2em"}}>
                    Linux AMD64: <a href="/downloads/lavi/lavi-cli-linux-amd64.zip">Download</a>
				</Typography>
				<Typography style={{paddingTop: "2em"}}>
                    Linux ARM64: <a href="/downloads/lavi/lavi-cli-linux-arm64.zip">Download</a>
				</Typography>
				<Typography style={{paddingTop: "2em"}}>
                    Windows AMD64: <a href="/downloads/lavi/lavi-cli-windows-amd64.zip">Download</a>
				</Typography>
			</div>
	</Layout>
}

/**
 * Head export to define metadata for the page
 *
 * See: https://www.gatsbyjs.com/docs/reference/built-in-components/gatsby-head/
 */
export const Head = () => <Seo title="Downloads" />

export default Downloads
