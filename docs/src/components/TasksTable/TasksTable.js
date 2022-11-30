// import React from 'react'
// import { Table, TableHead, TableRow, TableCell, TableBody } from "@mui/material"

// export default function TasksTable() {

//     return  <Table sx={{ minWidth: 650 }} aria-label="simple table">
//     <TableHead>
//       <TableRow>
//         <TableCell>Priority Task</TableCell>
//         <TableCell align="right">Individual Task</TableCell>
//         <TableCell align="right">Timeline</TableCell>
//         <TableCell align="right">Deliverable</TableCell>
//         <TableCell align="right">Status</TableCell>
//       </TableRow>
//     </TableHead>
//     <TableBody>
//       {tasks.map((row) => (
//         <TableRow
//           key={row["Priority Task"] + row["Individual Task"]}
//           sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
//         >
//           <TableCell component="th" scope="row">
//             {row["Priority Task"]}
//           </TableCell>
//           <TableCell align="right">{row["Individual Task"]}</TableCell>
//           <TableCell align="right">{row["Timeline"]}</TableCell>
//           <TableCell align="right">{row["Deliverable"]}</TableCell>
//           <TableCell align="right">{row["Status"]}</TableCell>
//         </TableRow>
//       ))}
//     </TableBody>
//   </Table>

// }

import { CircularProgress, Menu, Tooltip } from "@mui/material"
import { Box } from "@mui/system"
import * as React from "react"
import { TableContainer, Table, IconButton, TableCell, TableHead, TableRow, TableBody, TablePagination } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import axios from "axios";

const getTimeline = (timeline) => {
    if (timeline === -1) {
        return "???"
    } else if (timeline === 0) {
        return "Ongoing"
    } else {
        return new Date(timeline * 1000).toLocaleDateString(undefined, { 
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
          })
    }
}

const TasksTableRow = ({ row, openRow }) => {
    return (
        <>
            <TableRow
                key={row.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
                <TableCell component="th" scope="row">
                    {`${row.team} #${row.priorityTask}`}
                </TableCell>
                <TableCell align="right">{row.individualTask}</TableCell>
                <TableCell align="right">{getTimeline(row.timeline)}</TableCell>
                <TableCell align="right">{row.deliverable}</TableCell>
                <TableCell align="right">{row.status}</TableCell>
            </TableRow>
        </>
    )
}

const TasksTable = () => {
    const [tasks, setTasks] = React.useState([])
    const [params, setParmas] = React.useState({ offset: 0, limit: 20 })
    const [page, setPage] = React.useState(0)
    const [open, setOpen] = React.useState(false)
    const [values, setValues] = React.useState(null)
    const [edit, setEdit] = React.useState(false)

    const openRow = (row) => {
        console.log(row)
        setValues(row)
        setEdit(true)
        setOpen(true)
    }

    const handleChangePage = async (event, newPage) => {
        setParmas({
            ...params,
            offset: newPage * params.limit,
        })
        setPage(newPage)
    };

    const handleRowsChange = async (event, rows) => {
        setParmas({
            ...params,
            offset: page * rows
        })
    };

    
    // React.useEffect(() => {
    //     axios.get(`${process.env.GATSBY_DOCS_PATH}/tasks`, { params: {limit: params.limit, offset: params.offset }}).then(r => {
    //         setTasks(r.data)
    //     })
    // }, [params, open])

    if (!tasks) {
        return <Box sx={{ display: 'flex', justifyContent: "center", alignItems: "center", height: "inherit" }}>
            <CircularProgress color="primary" />
        </Box>
    }

    return <>
            <TableContainer>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Priority Task</TableCell>
                            <TableCell align="right">Individual Task</TableCell>
                            <TableCell align="right">Timeline</TableCell>
                            <TableCell align="right">Deliverable</TableCell>
                            <TableCell align="right">Status</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {tasks.map((row) => (
                            <TasksTableRow openRow={openRow} key={"r" + row.id} row={row} />
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPageOptions={[10, 15, 20, 25]}
                onRowsPerPageChange={handleRowsChange}
                component="div"
                count={-1}
                rowsPerPage={params.limit}
                onPageChange={handleChangePage}
                page={page}
            />
    </>

}

export default TasksTable