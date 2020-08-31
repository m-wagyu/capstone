import React, { useState, useEffect } from 'react';
import Typography from '@material-ui/core/Typography';
import { Row, Col } from 'react-bootstrap'
import Button from '@material-ui/core/Button';
import ClearIcon from '@material-ui/icons/Clear';
import SuricataTableComponent from './components/SuricataTableComponent.jsx'
import ReloadButtonComponent from './components/ReloadButtonComponent.jsx'
import axios from 'axios'

import CONFIG from '../../config'


const columns = [
    {
        title: "Time",
        data_row_name: "time",
        title_props: { align: "center" },
        data_row_props: { align: "center", component: "th", scope: "row" }
    },
    {
        title: "Action",
        data_row_name: "action",
        title_props: { align: "center" },
        data_row_props: { align: "center" }
    },
    {
        title: "Source & Destination",
        data_row_name: "src_dst",
        title_props: { align: "center" },
        data_row_props: { align: "center" }
    },
    {
        title: "Protocol",
        data_row_name: "proto",
        title_props: { align: "center" },
        data_row_props: { align: "center" }
    },
    {
        title: "Message",
        data_row_name: "message",
        title_props: { align: "center" },
        data_row_props: { align: "center" }
    }
]

export default function Alert({ setShowLoading, showLoading }) {

    const [alerts, setAlerts] = useState([])

    useEffect(() => {
        getAlerts()
    }, [])

    function getAlerts() {
        setShowLoading(true)
        // http://127.0.0.1:5000/api/alerts
        axios.get(CONFIG.BASE_URL + '/api/alerts').then(response => {
            setAlerts(response.data.msg.alerts.reverse())
            setShowLoading(false)
        })
    }

    function clearAlerts() {
        setShowLoading(true)
        axios.get('https://cors-anywhere.herokuapp.com/http://ids.idostuff.today/api/clear_log').then(() => {
            setShowLoading(false)
        })
    }

    return (
        <>
            <Row className="w-100 p-0 m-0">

                <Col className="p-0">
                    <Typography variant="h5">Alert Messages: {alerts.length === 0 && showLoading === false ? <span className="text-danger">No Data</span> : ""}</Typography>
                </Col>
                <Col className="p-0 d-flex justify-content-end">
                    <Button variant="contained" color="secondary" startIcon={<ClearIcon />} className="mr-3" onClick={clearAlerts}>Clear Alerts</Button>
                    <ReloadButtonComponent reloadDataFunc={getAlerts} />
                </Col>
            </Row>
            <br />

            <SuricataTableComponent columns={columns} data={alerts} />

        </>
    )
}