import React from "react";
import { Form, Button, Col, Alert } from "react-bootstrap";

export default function AddRulesFormComponent({
  formInput,
  handleOnAddRules,
  error,
}) {
  return (
    <Form>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form.Row>
        <Form.Group as={Col}>
          <Form.Label>
            SID <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" type="text" {...formInput.sid} />
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>
            GID <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" type="text" {...formInput.gid} />
        </Form.Group>
      </Form.Row>

      <Form.Row>
        <Form.Group as={Col}>
          <Form.Label>
            Action <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" as="select" {...formInput.action}>
            <option value="pass">Pass</option>
            <option value="reject">Reject</option>
            <option value="drop">Drop</option>
            <option value="alert">Alert</option>
          </Form.Control>
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>
            Protocol <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" as="select" {...formInput.proto}>
            <option value="tcp">TCP</option>
            <option value="udp">UDP</option>
            <option value="icmp">ICMP</option>
            <option value="ip">IP</option>
          </Form.Control>
        </Form.Group>
      </Form.Row>

      <Form.Row>
        <Form.Group as={Col}>
          <Form.Label>
            Source Address <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" type="text" {...formInput.src_addr} />
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>
            Source Port <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" type="text" {...formInput.src_port} />
        </Form.Group>
      </Form.Row>

      <Form.Row>
        <Form.Group as={Col}>
          <Form.Label>
            Direction <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" as="select" {...formInput.direction}>
            <option value={"->"}>{"->"} Uni-Directional</option>
            <option value={"<>"}>{"<>"} Bi-Directional</option>
          </Form.Control>
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>
            Enabled <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" as="select" {...formInput.enabled}>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </Form.Control>
        </Form.Group>
      </Form.Row>

      <Form.Row>
        <Form.Group as={Col}>
          <Form.Label>
            Destination Address <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" type="text" {...formInput.dst_addr} />
        </Form.Group>
        <Form.Group as={Col}>
          <Form.Label>
            Destination Port <span className="text-danger">*</span>
          </Form.Label>
          <Form.Control size="sm" type="text" {...formInput.dst_port} />
        </Form.Group>
      </Form.Row>

      <Form.Group>
        <Form.Label>
          Message <span className="text-danger">*</span>
        </Form.Label>
        <Form.Control size="sm" type="text" {...formInput.msg} />
      </Form.Group>

      <div className="d-flex justify-content-end">
        <Button className="px-5" size="sm" onClick={handleOnAddRules}>
          Add Rule
        </Button>
      </div>
    </Form>
  );
}
