import * as React from "react"
import { Grid, Button, Typography } from "@mui/material"

import Layout from "../components/Layout/Layout"
import Seo from "../components/seo"
import HomepageCard from "../components/HomepageCard/HomepageCard"
import { darken, alpha } from "@mui/system"
import { styled } from '@mui/material/styles'
import { Link } from "gatsby"

const GreenButton = styled(Button)(({theme}) => ({
    '&:hover': {
		backgroundColor: darken("#8db74a", 0.2) + "!important",
		transition: '0.5s!important',
	},
	backgroundColor: '#8db74a!important',
	transition: '0.5s!important',
}))

const TextButton = styled(Button)(({theme}) => ({
    color: '#8db74a!important',
	'&:hover': {
		backgroundColor: alpha(darken("#8db74a", 0.2), 0.1) + "!important",
		transition: '0.5s!important',
	},
	transition: '0.5s!important',
}))


const DocsPage = () => {
	return <Layout disablePadding style={{ backgroundColor: "white" }} showFooter>
		<Seo title="Documentation" />
			<Grid
				container
				direction="column"
				alignItems="center"
				justifyContent="center"
				sx={{ pt: "4em", pb: "4em", backgroundColor: "#2a445c", color: "white" }}
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
						}}>Language Agnostic Vulnerability Identifier</Typography>
				</Grid>
			</Grid>
			<Grid
				container
				sx={{ p: "4em" }}
				spacing={8}
			>
				<Grid item xs={4}>
					<Typography sx={{fontSize: "20px", fontWeight: 200, pb: 2}}>
						Find vulnerable packages in your project
					</Typography>
					<Typography>
					By scanning through the dependencies and libraries used in the project, LAVI is able to identify any known vulnerabilities and alert the user. This allows users to proactively address any potential security risks, ensuring the safety and security of their project. 
					</Typography>
				</Grid>
				<Grid item xs={4}>
					<Typography sx={{fontSize: "20px", fontWeight: 200, pb: 2}}>
						Look for non-vulnerable packages to replaced
					</Typography>
					<Typography>
					LAVI's remediation feature is a valuable tool for addressing vulnerabilities in your project. By providing accurate replacement versions for vulnerable packages, LAVI ensures that your project is always using secure, up-to-date code. This helps to improve the performance and reliability of your project, as well as reduce the likelihood of encountering any vulnerabilities.
					</Typography>
				</Grid>
				<Grid item xs={4}>
					<Typography sx={{fontSize: "20px", fontWeight: 200, pb: 2}}>
						Learn about vulnerability rates in repositories
					</Typography>
					<Typography>
						LAVI's subproduct LAVA, helps perform research on package repositories to learn about vulnerability rates. LAVA provides a number of useful queries to generate insights into a specific language's vulnerability statistics.
					</Typography>
				</Grid>
			</Grid>
			{/* <hr style={{margin: 0, backgroundColor: "gray"}} />
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
						LAVI
				</Typography>
				<Typography style={{paddingTop: "2em"}}>
					LAVI searches through packages included in your project to determine if any known vulnerabilities are included in a package. If it finds vulnerabilities it explains what they are, where to find more information about the vulnerability and optionally will help you find alternate package versions that aren't vulnerable.
				</Typography>
			</div> */}
	</Layout>
}

/**
 * Head export to define metadata for the page
 *
 * See: https://www.gatsbyjs.com/docs/reference/built-in-components/gatsby-head/
 */
export const Head = () => <Seo title="Documentation" />

export default DocsPage
