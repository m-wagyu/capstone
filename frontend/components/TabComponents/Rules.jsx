import React, { useState, useEffect } from "react";
import { Typography, Button } from "@material-ui/core";
import CloseIcon from "@material-ui/icons/Close";
import AddIcon from "@material-ui/icons/Add";
import axios from "axios";

import { Row, Col, Alert } from "react-bootstrap";

import SuricataTableComponent from "./components/SuricataTableComponent.jsx";
import ReloadButtonComponent from "./components/ReloadButtonComponent.jsx";
import AddRulesFormComponent from "./components/AddRulesFormComponent.jsx";

import CONFIG from "../../config";

export default function Rules() {
  const [rules, setRules] = useState([]);
  const [showAddRuleForm, setShowAddRuleForm] = useState(false);

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [count, setCount] = useState(0);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const formDataInit = {
    sid: formInput(""),
    gid: formInput(""),
    action: formInput("pass"),
    proto: formInput("tcp"),
    src_addr: formInput(""),
    src_port: formInput(""),
    direction: formInput("uni"),
    enabled: formInput("true"),
    dst_addr: formInput(""),
    dst_port: formInput(""),
    msg: formInput(""),
  };

  let formDataInput = { ...formDataInit };

  useEffect(() => {
    getRules();
  }, [page, rowsPerPage]);

  function getRules() {
    axios
      .get(`${CONFIG.BASE_URL}/api/rules/?page=${page}&count=${rowsPerPage}`)
      .then((response) => {
        if (response.data.msg.rules) {
          const filteredResponse = [];

          setCount(response.data.msg.total || 0);

          response.data.msg.rules.forEach((each, i) => {
            let rule = {};

            rule.enable = each.enable ? "Yes" : "No";
            rule.sid = each.option.sid;
            rule.gid = each.option.gid;
            rule.message = each.option.msg;

            rule.action = each.action;
            rule.protocol = each.header.proto;
            rule.source = `${each.header.src_addr}:${each.header.src_port}`;
            rule.direction = each.header.direction;
            rule.destination = `${each.header.dst_addr}:${each.header.dst_port}`;

            filteredResponse.push(rule);
          });
          setRules(filteredResponse || []);
          return;
        }
      });
  }

  function addNewRules() {
    if (!showAddRuleForm) {
      setShowAddRuleForm(true);
    } else {
      setShowAddRuleForm(false);
      formDataInput = formDataInit;
      setError("");
      setSuccess("");
    }
  }

  function formInput(initialValue) {
    const [value, setValue] = useState(initialValue);

    function handleChange(e) {
      setValue(e.target.value);
    }

    return { value, onChange: handleChange };
  }

  function handleOnAddRules(event) {
    event.preventDefault();

    // Reset Errors
    let hasError = false;
    setError("");
    setSuccess("");

    // form input data
    let convertFormDataInput = {};

    // Check if there are empty fields in form
    for (let each in formDataInput) {
      if (formDataInput[each].value) {
        if (each === "enabled") {
          convertFormDataInput[each] =
            formDataInput[each].value === "true" ? "True" : "";
          continue;
        }
        convertFormDataInput[each] = formDataInput[each].value;
        continue;
      }
      hasError = true;
      setError("Fill in the form!");
      break;
    }

    if (!hasError) {
      axios
        .post(
          `${CONFIG.BASE_URL}/api/add_rule/`,
          getFormData(convertFormDataInput),
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((response) => {
          if (response.data.result === "success") {
            // Reset Form
            formDataInput = formDataInit;
            // Set success
            setSuccess("Your have successfully added in a new rule!");
            // Close Form
            setShowAddRuleForm(false);
            // Get new Rules
            getRules();
          } else {
            setError("Something went wrong and It did not add rule!");
          }
        })
        .catch((e) => {
          setError("Something went wrong and It did not add rule!");
        });
    }
  }

  function getFormData(object) {
    const formData = new FormData();
    Object.keys(object).forEach((key) => formData.append(key, object[key]));
    return formData;
  }

  return (
    <>
      <Row className="w-100 p-0 m-0">
        <Col className="p-0">
          <Typography variant="h5">Network Rules</Typography>
        </Col>
        <Col className="p-0 d-flex justify-content-end">
          <Button
            variant="contained"
            color="secondary"
            disableElevation
            className="mr-3"
            onClick={addNewRules}
          >
            <span
              className={`MuiButton-startIcon MuiButton-iconSizeLarge addRulesIcon ${
                showAddRuleForm ? "addRulesIconToClose" : ""
              }`}
            >
              <AddIcon />
            </span>
            {showAddRuleForm ? "CLOSE FORM" : "ADD RULES"}
          </Button>
          <ReloadButtonComponent reloadDataFunc={getRules} />
        </Col>
      </Row>

      <br />

      {success && (
        <Alert variant={success ? "success" : ""}>
          <Row>
            <Col sm={10}>{success}</Col>
            <Col className="text-right">
              <CloseIcon fontSize="small" onClick={() => setSuccess(false)} />
            </Col>
          </Row>
        </Alert>
      )}

      {showAddRuleForm && (
        <AddRulesFormComponent
          formInput={formDataInput}
          handleOnAddRules={handleOnAddRules}
          error={error}
        />
      )}

      <br />

      <SuricataTableComponent
        data={rules}
        page={page}
        setPage={setPage}
        rowsPerPage={rowsPerPage}
        setRowsPerPage={setRowsPerPage}
        count={count || rules.length}
        columns={[
          {
            title: "Enable",
            data_row_name: "enable",
            title_props: { align: "center" },
            data_row_props: { component: "th", scope: "row", align: "center" },
          },
          {
            title: "SID",
            data_row_name: "sid",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "GID",
            data_row_name: "gid",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "Protocol",
            data_row_name: "protocol",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "Source",
            data_row_name: "source",
            title_props: {
              align: "center",
              style: {
                maxWidth: 210,
                overflow: "auto",
              },
            },
            data_row_props: {
              align: "center",
              style: {
                maxWidth: 210,
                overflow: "auto",
              },
            },
          },
          {
            title: "Direction",
            data_row_name: "direction",
            title_props: { align: "center" },
            data_row_props: { align: "center" },
          },
          {
            title: "Destination",
            data_row_name: "destination",
            title_props: {
              align: "center",
              style: {
                maxWidth: 210,
                overflow: "auto",
              },
            },
            data_row_props: {
              align: "center",
              style: {
                maxWidth: 210,
                overflow: "auto",
              },
            },
          },
          {
            title: "Action",
            data_row_name: "action",
            title_props: { align: "center" },
            data_row_props: { align: "center", className: "text-capitalize" },
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
