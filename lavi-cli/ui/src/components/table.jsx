import React from 'react';
import { getVulnDataStats, parseApiResponse } from '../utils';
import { Collapse, Box, Typography, Table, TableHead, TableRow, TableCell, TableBody, IconButton, Icon } from "@mui/material"
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import EditIcon from '@mui/icons-material/Edit';
import ChangeVersionDialog from "./changeVersionDialog"
import RefreshIcon from '@mui/icons-material/Refresh';

const CustomTableRow = ({ viewCurrent, changedVersions, setChangedVersions, repo, row, nodes }) => {
    const [open, setOpen] = React.useState(false);
    const [dialogOpen, setDialogOpen] = React.useState(false)


    const changeVers = changedVersions[row.name]

    return <React.Fragment>
        <ChangeVersionDialog repo={repo} ver={row.version} packageName={row.name} open={dialogOpen} onClose={(v) => {
            if (v) {
                const cv = { ...changedVersions }
                cv[row.name] = v
                setChangedVersions(cv)
            }
            setDialogOpen(false)
        }} />
        <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
            <TableCell>
                <IconButton
                    disabled={row.vulnerabilities.length === 0 || changeVers}
                    aria-label="expand row"
                    size="small"
                    onClick={() => setOpen(!open)}
                >
                    {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                </IconButton>
            </TableCell>
            <TableCell component="th" scope="row">
                {row.name}
            </TableCell>
            <TableCell align="right">{changeVers ? <b>{changeVers}</b> : row.version}</TableCell>
            <TableCell align="right">{changeVers ? "-" : row.severities.low}</TableCell>
            <TableCell align="right">{changeVers ? "-" : row.severities.medium}</TableCell>
            <TableCell align="right">{changeVers ? "-" : row.severities.high}</TableCell>
            <TableCell align="right">
                {viewCurrent ? <>
                    <IconButton onClick={() => setDialogOpen(true)}>
                        <EditIcon />
                    </IconButton>
                    {changeVers && <IconButton onClick={() => {
                        const cv = { ...changedVersions }
                        delete cv[row.name]
                        setChangedVersions(cv)
                    }}>
                        <RefreshIcon />
                    </IconButton>}
                </>
                    :
                    <>
                        <IconButton disabled>
                            <Icon />
                        </IconButton>
                        {changeVers && <IconButton disabled>
                            <Icon />
                        </IconButton>}
                    </>
                }
            </TableCell>
        </TableRow>
        <TableRow>
            <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={7}>
                <Collapse in={open} timeout="auto" unmountOnExit>
                    <Box sx={{ margin: 1 }}>
                        <Typography variant="h6" gutterBottom component="div">
                            Vulnerable Dependencies
                        </Typography>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Indirect Dependency Name</TableCell>
                                    <TableCell align="right">Package Version</TableCell>
                                    <TableCell align="right">CVE ID</TableCell>
                                    <TableCell align="right">CVE Severity</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {row.vulnerabilities.map(v => {
                                    const node = nodes[v.associatedWith]
                                    return <>
                                        {v.vulnerabilities.map((vulnRow) => (
                                            <TableRow key={node.package + vulnRow.cveId}>
                                                <TableCell component="th" scope="row">
                                                    {node.package}
                                                </TableCell>
                                                <TableCell align="right">{node.version}</TableCell>
                                                <TableCell align="right">{vulnRow.cveId}</TableCell>
                                                <TableCell align="right">
                                                    {vulnRow.severity === 1 && "Low"}
                                                    {vulnRow.severity === 2 && "Medium"}
                                                    {vulnRow.severity === 3 && "High"}
                                                </TableCell>
                                            </TableRow>
                                        ))}

                                    </>
                                })}
                            </TableBody>
                        </Table>
                    </Box>
                </Collapse>
            </TableCell>
        </TableRow>
    </React.Fragment>
}


function VulnerabilityTable({ viewCurrent, changedVersions, setChangedVersions, repo, pkgs, stats, nodes }) {

    const [pkgStats, accumStats] = stats

    return (
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell></TableCell>
                    <TableCell>Package Name</TableCell>
                    <TableCell align="right">
                        Package Version
                    </TableCell>
                    <TableCell align="right">Low Severity Vulnerabilities</TableCell>
                    <TableCell align="right">Medium Severity Vulnerabilities</TableCell>
                    <TableCell align="right">High Severity Vulnerabilities</TableCell>
                    <TableCell align="right"></TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                <TableRow>
                    <TableCell><IconButton sx={{height: "20px"}}><Icon /></IconButton></TableCell>
                    <TableCell component="th" scope="row">
                        Totals
                    </TableCell>
                    <TableCell align="right" />
                    <TableCell align="right">
                        {accumStats.low}
                    </TableCell>
                    <TableCell align="right">
                        {accumStats.medium}
                    </TableCell>
                    <TableCell align="right">
                        {accumStats.high}
                    </TableCell>
                    <TableCell align="right"><IconButton sx={{height: "20px"}}><Icon /></IconButton></TableCell>
                </TableRow>
                {Object.keys(pkgStats).map(k =>
                    <CustomTableRow viewCurrent={viewCurrent} changedVersions={changedVersions} setChangedVersions={setChangedVersions} repo={repo} nodes={nodes} row={pkgStats[k]} key={k} />
                )}
            </TableBody>
        </Table>

    );
}

export default VulnerabilityTable;
