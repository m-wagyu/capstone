import React from 'react'
import { Container } from 'react-bootstrap'

import Paper from '@material-ui/core/Paper';
import Tab from '@material-ui/core/Tab';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import TabPanel from '@material-ui/lab/TabPanel';

// Import components
import NavigationBar from './components/NavigationBar.jsx'
import TabComponents from './components/TabComponents.jsx'

export default function App() {

    const [value, setValue] = React.useState('1');

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <>
            <NavigationBar />

            <Container className="p-0 mt-4">
                <TabContext value={value}>
                    <Paper>
                        <TabList onChange={handleChange} indicatorColor="primary" textColor="primary">
                            <Tab label="Home" value="1" />
                            <Tab label="Alert" value="2" />
                            <Tab label="Stats" value="3" />
                            <Tab label="Rules" value="4" />
                        </TabList>
                    </Paper>
                    <TabPanel value="1" className="p-3"><TabComponents.Home /></TabPanel>
                    <TabPanel value="2" className="p-3"><TabComponents.Alert /></TabPanel>
                    <TabPanel value="3" className="p-3"><TabComponents.Stats /></TabPanel>
                    <TabPanel value="4" className="p-3"><TabComponents.Rules /></TabPanel>
                </TabContext>
            </Container>

        </>
    )
}