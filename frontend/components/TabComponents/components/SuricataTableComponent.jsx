import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import TablePagination from '@material-ui/core/TablePagination';
import Button from '@material-ui/core/Button';
import { Row, Col } from 'react-bootstrap'

const useStyles = makeStyles({
    root: {
        width: '100%',
    },
    container: {
        maxHeight: 500,
    },
});

// Usage
// Example of columns variable
// must includes title and column/object name for data variable
// var columns = [
//     {title: "First Name", data_row_name: "first_name", title_props: {align: center, ...}, data_row_props: {...}},
//     {title: "Last Name", data_row_name: "last_name", title_props: {align: right, ...}, data_row_props: {...}}
// ]

export default function SuricataTableComponent({ columns, data, loading }) {

    // Check if column is empty
    if (!columns.length) return (<Typography variant="h5">No Columns for SuricataTableComponent</Typography>)

    const classes = useStyles();
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };
    return (
        <>
            <Paper className={classes.root}>
                <TableContainer className={classes.container}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                {
                                    columns.map((each, i) => {
                                        return (<TableCell key={i} {...each.title_props}>{each.title}</TableCell>)
                                    })
                                }
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data &&
                                data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, key) => {
                                    return (
                                        <TableRow tabIndex={-1} key={key}>
                                            {
                                                columns.map((each, i) => {
                                                    return (<TableCell key={i} {...each.data_row_props}>{row[each.data_row_name]}</TableCell>)
                                                })
                                            }
                                        </TableRow>
                                    );
                                })
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[10, 25, 50]}
                    component="div"
                    count={data.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onChangePage={handleChangePage}
                    onChangeRowsPerPage={handleChangeRowsPerPage}
                />
            </Paper>
        </>
    )
}