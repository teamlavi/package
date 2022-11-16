import React from 'react';
import { getPackagePath, getVulnDataStats, parseApiResponse } from '../utils';
import { Collapse, Box, Typography, Tooltip, Table, TableHead, TableRow, TableCell, TableBody, IconButton, Icon, TableSortLabel } from "@mui/material"
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import EditIcon from '@mui/icons-material/Edit';
import ChangeVersionDialog from "./changeVersionDialog"
import RefreshIcon from '@mui/icons-material/Refresh';

const hoverWrapper = (str) => {
    return <Tooltip title="Unknown. Please run the changes to update.">
        <span>{str}</span>
    </Tooltip>
}

const OverflowTip = ({ children }) => {
  const [isOverflowed, setIsOverflow] = React.useState(false);
  const textElementRef = React.useRef();
  React.useEffect(() => {
    setIsOverflow(textElementRef.current.scrollWidth > textElementRef.current.clientWidth);
  }, []);
  return (
    <Tooltip title={children} disableHoverListener={!isOverflowed}>
      <div
        ref={textElementRef}
        style={{
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
        }}
      >
        {children}
      </div>
    </Tooltip>
  );
};

const CustomTableRow = ({ cds, viewCurrent, changedVersions, setChangedVersions, repo, row, nodes }) => {
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
            <TableCell align="right">{changeVers && viewCurrent ? <b>{changeVers}</b> : row.version}</TableCell>
            <TableCell align="right">{changeVers && viewCurrent ? hoverWrapper("-") : row.severities.low}</TableCell>
            <TableCell align="right">{changeVers && viewCurrent ? hoverWrapper("-") : row.severities.medium}</TableCell>
            <TableCell align="right">{changeVers && viewCurrent ? hoverWrapper("-") : row.severities.high}</TableCell>
            <TableCell align="right">{changeVers && viewCurrent ? hoverWrapper("-") : row.severities.critical}</TableCell>
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
            <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={8}>
                <Collapse in={open && !changeVers} timeout="auto" unmountOnExit>
                    <Box sx={{ margin: 1 }}>
                        <Typography variant="h6" gutterBottom component="div">
                            Vulnerabilities
                        </Typography>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Package Name</TableCell>
                                    <TableCell align="right">Package Version</TableCell>
                                    <TableCell align="right">Package Path</TableCell>
                                    <TableCell align="right">CVE ID</TableCell>
                                    <TableCell align="right">CVE Severity</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {row.vulnerabilities.map(v => {
                                    const node = nodes[v.associatedWith]
                                    const path = getPackagePath(cds, node.id)
                                    const pathString = path.join(" > ")
                                    return <>
                                        {v.vulnerabilities.map((vulnRow) => (
                                            <TableRow key={node.package + vulnRow.cveId}>
                                                <TableCell component="th" scope="row">
                                                    {node.package}
                                                </TableCell>
                                                <TableCell align="right">{node.version}</TableCell>
                                                <TableCell align="right"><OverflowTip>{pathString}</OverflowTip></TableCell>
                                                <TableCell align="right">
                                                    <a href={vulnRow.url} target="_blank">{vulnRow.cveId}</a>
                                                </TableCell>
                                                <TableCell align="right">
                                                    {vulnRow.severity === 0 && "LOW"}
                                                    {vulnRow.severity === 1 && "MEDIUM"}
                                                    {vulnRow.severity === 2 && "HIGH"}
                                                    {vulnRow.severity === 3 && "CRITICAL"}
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

const sorts = {
    "name": (a, b) => {
        return a.name < b.name ? -1 : (a.name > b.name ? 1 : 0)
    },
    "critSev": (a, b) => {
        return a.severities.critical > b.severities.critical ? -1 : (a.severities.critical < b.severities.critical ? 1 : 0)
    },
    "highSev": (a, b) => {
        return a.severities.high > b.severities.high ? -1 : (a.severities.high < b.severities.high ? 1 : 0)
    },
    "medSev": (a, b) => {
        return a.severities.medium > b.severities.medium ? -1 : (a.severities.medium < b.severities.medium ? 1 : 0)
    },
    "lowSev": (a, b) => {
        return a.severities.low > b.severities.low ? -1 : (a.severities.low < b.severities.low ? 1 : 0)
    }
}


function VulnerabilityTable({ viewCurrent, changedVersions, setChangedVersions, repo, pkgs, stats, nodes, cds }) {

    const [pkgStats, accumStats] = stats
    const [sortType, setSortType] = React.useState("name")
    const [sortDir, setSortDir] = React.useState("asc")

    const createSortHandler = (p) => (event) => {
        if (sortType === p) {
            console.log(sortDir === "asc" ? "desc" : "asc")
            setSortDir(sortDir === "asc" ? "desc" : "asc")
        }
        setSortType(p)
    };

    const values = Object.values(pkgStats)
    values.sort(sorts[sortType])
    if (sortDir === "desc") {
        values.reverse()
    }
    

    return (
        <Table stickyHeader sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
                <TableRow>
                    <TableCell></TableCell>
                    <TableCell
                        sortDirection={sortType === "name" ? sortDir : false}
                    >
                        <TableSortLabel
                            active={sortType === "name"}
                            direction={sortType === "name" ? sortDir : 'asc'}
                            onClick={createSortHandler("name")}
                        >
                            Name
                        </TableSortLabel>
                    </TableCell>
                    <TableCell align="right">
                        Package Version
                    </TableCell>
                    <TableCell
                        align="right"
                        sortDirection={sortType === "lowSev" ? sortDir : false}
                    >
                        <TableSortLabel
                            active={sortType === "lowSev"}
                            direction={sortType === "lowSev" ? sortDir : 'asc'}
                            onClick={createSortHandler("lowSev")}
                        >
                            Low Severity
                        </TableSortLabel>
                    </TableCell>
                    <TableCell
                        align="right"
                        sortDirection={sortType === "medSev" ? sortDir : false}
                    >
                        <TableSortLabel
                            active={sortType === "medSev"}
                            direction={sortType === "medSev" ? sortDir : 'asc'}
                            onClick={createSortHandler("medSev")}
                        >
                            Medium Severity
                        </TableSortLabel>
                    </TableCell>
                    <TableCell
                        align="right"
                        sortDirection={sortType === "highSev" ? sortDir : false}
                    >
                        <TableSortLabel
                            active={sortType === "highSev"}
                            direction={sortType === "highSev" ? sortDir : 'asc'}
                            onClick={createSortHandler("highSev")}
                        >
                            High Severity
                        </TableSortLabel>
                    </TableCell>
                    <TableCell
                        align="right"
                        sortDirection={sortType === "critSev" ? sortDir : false}
                    >
                        <TableSortLabel
                            active={sortType === "critSev"}
                            direction={sortType === "critSev" ? sortDir : 'asc'}
                            onClick={createSortHandler("critSev")}
                        >
                            Critical Severity
                        </TableSortLabel>
                    </TableCell>
                    <TableCell align="right"></TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                <TableRow>
                    <TableCell><IconButton sx={{ height: "20px" }}><Icon /></IconButton></TableCell>
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
                    <TableCell align="right">
                        {accumStats.critical}
                    </TableCell>
                    <TableCell align="right"><IconButton sx={{ height: "20px" }}><Icon /></IconButton></TableCell>
                </TableRow>
                {values.map(k =>
                    <CustomTableRow cds={cds} viewCurrent={viewCurrent} changedVersions={changedVersions} setChangedVersions={setChangedVersions} repo={repo} nodes={nodes} row={k} key={k.id} />
                )}
            </TableBody>
        </Table>

    );
}

export default VulnerabilityTable;
