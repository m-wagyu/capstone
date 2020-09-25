import React, { useState, useEffect } from "react";
import { Typography, Button } from "@material-ui/core";

import { Row, Col } from "react-bootstrap";

import ClearIcon from "@material-ui/icons/Clear";

import SuricataTableComponent from "./components/SuricataTableComponent.jsx";
import ReloadButtonComponent from "./components/ReloadButtonComponent.jsx";

import axios from "axios";

import CONFIG from "../../config";

export default function Alert({ setShowLoading, showLoading }) {
  const [alerts, setAlerts] = useState([]);

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [count, setCount] = useState(0);

  useEffect(() => {
    getAlerts();
  }, [page, rowsPerPage]);

  function getAlerts() {
    setShowLoading(true);
    // http://127.0.0.1:5000/api/alerts
    axios
      .get(`${CONFIG.BASE_URL}/api/alerts/?page=${page}&count=${rowsPerPage}`)
      .then((response) => {
        setCount(response.data.msg.total);
        setAlerts(response.data.msg.alerts.reverse() || []);
        setShowLoading(false);
      });
  }

  function clearAlerts() {
    setShowLoading(true);
    axios.get(`${CONFIG.BASE_URL}/api/clear_log/`).then(() => {
      setShowLoading(false);
    });
  }

  return (
    <>
      <Row className="w-100 p-0 m-0">
        <Col className="p-0">
          <Typography variant="h5">
            Alert Messages:{" "}
            {alerts.length === 0 && showLoading === false ? (
              <span className="text-danger">No Data</span>
            ) : (
              ""
            )}
          </Typography>
        </Col>
        <Col className="p-0 d-flex justify-content-end">
          <Button
            variant="contained"
            color="secondary"
            startIcon={<ClearIcon />}
            className="mr-3"
            onClick={clearAlerts}
          >
            Clear Alerts
          </Button>
          <ReloadButtonComponent reloadDataFunc={getAlerts} />
        </Col>
      </Row>

      <br />

      <SuricataTableComponent
        data={alerts}
        page={page}
        setPage={setPage}
        rowsPerPage={rowsPerPage}
        setRowsPerPage={setRowsPerPage}
        count={count || alerts.length}
        columns={[
          {
            title: "Time",
            data_row_name: "time",
            title_props: { align: "center" },
            data_row_props: { align: "center", component: "th", scope: "row" },
          },
          {
            title: "Action",
            data_row_name: "action",
            title_props: { align: "center" },
            data_row_props: { align: "center", className: "text-capitalize" },
          },
          {
            title: "Source & Destination",
            data_row_name: "src_dst",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "Protocol",
            data_row_name: "proto",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "Message",
            data_row_name: "message",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
        ]}
      />
    </>
  );
}
