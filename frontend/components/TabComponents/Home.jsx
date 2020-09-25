import React, { useState, useEffect } from "react";
import Typography from "@material-ui/core/Typography";
import { Row, Col } from "react-bootstrap";
import axios from "axios";
import SuricataTableComponent from "./components/SuricataTableComponent.jsx";
import ReloadButtonComponent from "./components/ReloadButtonComponent.jsx";
import CONFIG from "../../config";

export default function Home({ setShowLoading, showLoading }) {
  const [messages, setMessages] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [count, setCount] = useState(0);

  useEffect(() => {
    getMessages();
  }, [page, rowsPerPage]);

  function getMessages() {
    setShowLoading(true);
    axios.get(CONFIG.BASE_URL + "/api/run_log").then((response) => {
      setCount(response.data.msg.total || 0);
      setMessages(response.data.msg.reverse() || []);
      setShowLoading(false);
    });
  }

  return (
    <>
      <Row className="w-100 p-0 m-0">
        <Col className="p-0">
          <Typography variant="h5">
            Running Messages:{" "}
            {messages.length === 0 && showLoading === false ? (
              <span className="text-danger">No Data</span>
            ) : (
              ""
            )}
          </Typography>
        </Col>
        <Col className="p-0 d-flex justify-content-end">
          <ReloadButtonComponent reloadDataFunc={getMessages} />
        </Col>
      </Row>
      <br />

      <SuricataTableComponent
        data={messages}
        page={page}
        setPage={setPage}
        rowsPerPage={rowsPerPage}
        setRowsPerPage={setRowsPerPage}
        count={count || messages.length}
        noPagination={true}
        columns={[
          {
            title: "Time",
            data_row_name: "ts",
            title_props: { align: "center" },
            data_row_props: { align: "center", component: "th", scope: "row" },
          },
          {
            title: "Type",
            data_row_name: "type",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "Message",
            data_row_name: "msg",
            title_props: { align: "right" },
            data_row_props: { align: "right" },
          },
        ]}
      />
    </>
  );
}
