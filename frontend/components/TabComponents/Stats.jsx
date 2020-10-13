import React, { useState, useEffect } from 'react';
import { Typography, Button } from '@material-ui/core';
import UpdateIcon from '@material-ui/icons/Update';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import { Row, Col } from 'react-bootstrap';

import ReloadButtonComponent from './components/ReloadButtonComponent.jsx';

import axios from 'axios';
import CONFIG from '../../config';

export default function Stats() {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        getStats();
    }, []);

    function getStats() {
        axios.get(CONFIG.BASE_URL + '/api/stats').then((response) => {
            setStats(response.data.msg);
        });
    }

    const interfaceTable = () => {
        return (
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Interface Name</TableCell>
                            <TableCell align="center">
                                Invalid Checksums
                            </TableCell>
                            <TableCell align="center">Drop</TableCell>
                            <TableCell align="center">Packets</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {stats &&
                            stats['iface-list'] &&
                            stats['iface-list'].map((row, i) => {
                                return (
                                    <TableRow key={i}>
                                        <TableCell component="th" scope="row">
                                            {row.name}
                                        </TableCell>
                                        <TableCell align="center">
                                            {row['invalid-checksums']}
                                        </TableCell>
                                        <TableCell align="center">
                                            {row.drop}
                                        </TableCell>
                                        <TableCell align="center">
                                            {row.pkts}
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                    </TableBody>
                </Table>
            </TableContainer>
        );
    };

    const counterTable = () => {
        return (
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>SID</TableCell>
                            <TableCell align="center">IP</TableCell>
                            <TableCell align="center">Alert Count</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {stats &&
                            stats.counter &&
                            Object.keys(stats.counter).map((each, i) => {
                                return (
                                    <TableRow key={i}>
                                        <TableCell>{each}</TableCell>
                                        <TableCell align="center">
                                            {
                                                Object.keys(
                                                    stats.counter[each]
                                                )[0]
                                            }
                                        </TableCell>
                                        <TableCell align="center">
                                            {
                                                stats.counter[each][
                                                    Object.keys(
                                                        stats.counter[each]
                                                    )[0]
                                                ]
                                            }
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                    </TableBody>
                </Table>
            </TableContainer>
        );
    };

    return (
        <>
            <Row className="w-100 p-0 m-0">
                <Col className="p-0">
                    <Typography variant="h5">
                        Network Stats: {stats ? `v${stats.version}` : ''}
                    </Typography>
                </Col>
                <Col className="p-0 d-flex justify-content-end">
                    <Button
                        variant="contained"
                        color="secondary"
                        startIcon={<UpdateIcon />}
                        className="mr-3"
                        disabled
                    >
                        Uptime:{' '}
                        {stats
                            ? (parseInt(stats.uptime) / 60 / 60).toFixed(1) +
                              ' Hour(s)'
                            : 'Down'}
                    </Button>
                    <ReloadButtonComponent reloadDataFunc={getStats} />
                </Col>
            </Row>
            <br />
            {interfaceTable()}
            <br />
            {counterTable()}
        </>
    );
}
