import React, { useState, useEffect } from 'react';
import { Nav, NavDropdown, Navbar, Container } from 'react-bootstrap';
import LinearProgress from '@material-ui/core/LinearProgress';
import axios from 'axios';
import FormData from 'form-data';
import CONFIG from '../config';

export default function NavigationBar() {
    // True for online, False for offline
    const [serverStatus, setServerStatus] = useState(false);
    const [isWaiting, setIsWatiting] = useState(false);

    useEffect(() => {
        getServerStatus();
    }, []);

    function handleServerAction(func_name, event) {
        // USAGE
        // func_name: proc_start | proc_reload | proc_stop | refresh
        event.preventDefault();

        if (func_name !== 'refresh') {
            const form_data = new FormData();
            form_data.append('function', func_name);

            axios
                .post(`${CONFIG.BASE_URL}/api/server_action/`, form_data, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then((response) => {
                    if (response.data.result === 'success') {
                        setIsWatiting(true);
                        // Wait 2 second before refresh server status
                        sleep(2000).then(() => {
                            getServerStatus();
                            setIsWatiting(false);
                        });
                    }
                });
        } else {
            getServerStatus();
        }
    }

    function getServerStatus() {
        // HTTP Request To Do
        axios.get(`${CONFIG.BASE_URL}/api/server_status/`).then((response) => {
            if (response.data.result === 'success') {
                setServerStatus(true);
                return;
            }
            setServerStatus(false);
        });
    }

    function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    return (
        <>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
                <Container>
                    <Navbar.Brand href="/">
                        Suricata NIDS Control Program
                    </Navbar.Brand>
                    <Navbar.Toggle />
                    <Navbar.Collapse className="justify-content-end">
                        <Nav>
                            <Nav.Item>
                                <Navbar.Text>
                                    Server Status:{' '}
                                    {serverStatus ? (
                                        <span className="text-success">
                                            Online
                                        </span>
                                    ) : (
                                        <span className="text-danger">
                                            Offline
                                        </span>
                                    )}
                                </Navbar.Text>
                            </Nav.Item>
                            <Nav.Item>
                                <NavDropdown
                                    title="Action"
                                    className="text-light"
                                    id="collasible-nav-dropdown"
                                >
                                    <NavDropdown.Item
                                        onClick={(e) =>
                                            handleServerAction('proc_start', e)
                                        }
                                    >
                                        <span className="text-success">
                                            Start
                                        </span>
                                    </NavDropdown.Item>
                                    <NavDropdown.Item
                                        onClick={(e) =>
                                            handleServerAction('proc_reload', e)
                                        }
                                    >
                                        <span className="text-warning">
                                            Reload
                                        </span>
                                    </NavDropdown.Item>
                                    <NavDropdown.Item
                                        onClick={(e) =>
                                            handleServerAction('proc_stop', e)
                                        }
                                    >
                                        <span className="text-danger">
                                            Terminate
                                        </span>
                                    </NavDropdown.Item>
                                    <NavDropdown.Divider />
                                    <NavDropdown.Item
                                        onClick={(e) =>
                                            handleServerAction('refresh', e)
                                        }
                                    >
                                        <span className="text-primary">
                                            Refresh Status
                                        </span>
                                    </NavDropdown.Item>
                                </NavDropdown>
                            </Nav.Item>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            <LinearProgress
                color="secondary"
                className={isWaiting ? 'visible' : 'invisible'}
            />
        </>
    );
}
