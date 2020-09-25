import React, { useState } from 'react'
import { Container } from 'react-bootstrap'

import Paper from '@material-ui/core/Paper';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';
import LinearProgress from '@material-ui/core/LinearProgress';

// Import components
import NavigationBar from './components/NavigationBar.jsx'
import TabComponents from './components/TabComponents.jsx'

export default function App() {

    const [value, setValue] = useState('rules');
    const [showLoading, setShowLoading] = useState(false)

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <>
            <NavigationBar />

            <Container className="mt-4">
                <TabContext value={value}>
                    <Paper>
                        <TabList onChange={handleChange} indicatorColor="primary" textColor="primary">
                            <Tab label="Home" value="home" />
                            <Tab label="Alert" value="alert" />
                            <Tab label="Stats" value="stats" />
                            <Tab label="Rules" value="rules" />
                        </TabList>
                    </Paper>
                    <LinearProgress color="secondary" className={showLoading ? "d-block" : "d-none"} />
                    <TabPanel value="home" className="px-0"><TabComponents.Home setShowLoading={setShowLoading} showLoading={showLoading} /></TabPanel>
                    <TabPanel value="alert" className="px-0"><TabComponents.Alert setShowLoading={setShowLoading} showLoading={showLoading} /></TabPanel>
                    <TabPanel value="stats" className="px-0"><TabComponents.Stats setShowLoading={setShowLoading} showLoading={showLoading} /></TabPanel>
                    <TabPanel value="rules" className="px-0"><TabComponents.Rules setShowLoading={setShowLoading} showLoading={showLoading} /></TabPanel>
                </TabContext>
            </Container>

        </>
    )
}