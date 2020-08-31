import React, { useState } from 'react'
import { Nav, NavDropdown, Navbar, Container } from 'react-bootstrap'
import axios from 'axios'
import FormData from 'form-data'
import CONFIG from '../config'
export default function NavigationBar() {

    // True for online, False for offline
    const [serverStatus, setServerStatus] = useState(false)

    function handleServerAction(func_name, event) {
        // USAGE
        // func_name: proc_start | proc_reload | proc_stop

        event.preventDefault()
        // const form_data = new FormData()
        // form_data.append('function', func_name)

        // axios.post(CONFIG.BASE_URL + '/home', form_data, {
        //     headers: {
        //         'Content-Type': 'multipart/form-data'
        //     }
        // }).then(response => {
        //     console.log(response);
        // })
    }

    function getServerStatus() {
        // HTTP Request To Do
        setServerStatus(false)
    }

    return (
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <Container>
                <Navbar.Brand href="/">Suricata NIDS Control Program</Navbar.Brand>
                <Navbar.Toggle />
                <Navbar.Collapse className="justify-content-end">
                    <Nav>
                        <Nav.Item>
                            <Navbar.Text>
                                Server Status: {serverStatus ? <span className="text-success">Online</span> : <span className="text-danger">Offline</span>}
                            </Navbar.Text>
                        </Nav.Item>
                        <Nav.Item>
                            <NavDropdown title="Action" className="text-light" id="collasible-nav-dropdown">
                                <NavDropdown.Item onClick={(e) => handleServerAction('proc_start', e)}><span className="text-success">Start</span></NavDropdown.Item>
                                <NavDropdown.Item onClick={(e) => handleServerAction('proc_reload', e)}><span className="text-warning">Reload</span></NavDropdown.Item>
                                <NavDropdown.Item onClick={(e) => handleServerAction('proc_stop', e)}><span className="text-danger">Terminate</span></NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item>About Us</NavDropdown.Item>
                            </NavDropdown>
                        </Nav.Item>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}