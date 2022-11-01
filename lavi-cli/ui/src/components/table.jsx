import React from 'react';
import { getVulnDataStats, parseApiResponse } from '../utils';
import { Collapse, Box, Typography, Table, TableHead, TableRow, TableCell, TableBody, IconButton } from "@mui/material"
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import EditIcon from '@mui/icons-material/Edit';
import ChangeVersionDialog from "./changeVersionDialog"

const CustomTableRow = ({ row, nodes }) => {
    const [open, setOpen] = React.useState(false);
    const [dialogOpen, setDialogOpen] = React.useState(false)
    return <React.Fragment>
        <ChangeVersionDialog open={dialogOpen} onClose={() => setDialogOpen(false)} />
        <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
            <TableCell>
                <IconButton
                    disabled={row.vulnerabilities.length === 0}
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
            <TableCell align="right">{row.version}</TableCell>
            <TableCell align="right">{row.severities.low}</TableCell>
            <TableCell align="right">{row.severities.medium}</TableCell>
            <TableCell align="right">{row.severities.high}</TableCell>
            <TableCell align="right">
                <IconButton onClick={() => setDialogOpen(true)}>
                    <EditIcon />
                </IconButton>
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
                                    <TableCell>Package Name</TableCell>
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


function VulnerabilityTable({ pkgs, stats, nodes }) {

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
                {Object.keys(stats).map(k =>
                    <CustomTableRow nodes={nodes} row={stats[k]} key={k} />
                )}
            </TableBody>
        </Table>

    );
}

export default VulnerabilityTable;
