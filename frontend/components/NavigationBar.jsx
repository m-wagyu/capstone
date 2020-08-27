import React, { useState } from 'react'
import { Nav, NavDropdown, Navbar, Container } from 'react-bootstrap'

export default function NavigationBar() {

    // True for online, False for offline
    const [serverStatus, setServerStatus] = useState(true)

    function handleTerminateClick(event) {
        // HTTP Request To Do
        console.log("Server action: Terminate");
    }

    function handleReloadClick(event) {
        // HTTP Request To Do
        console.log("Server action: Reload");
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
                                <NavDropdown.Item onClick={handleReloadClick}><span className="text-success">Reload</span></NavDropdown.Item>
                                <NavDropdown.Item onClick={handleTerminateClick}><span className="text-danger">Terminate</span></NavDropdown.Item>
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