import React from 'react';
import Button from '@material-ui/core/Button';
import RefreshIcon from '@material-ui/icons/Refresh';

export default function ReloadButtonComponent({ reloadDataFunc }) {

    function handleOnClick(event) {
        event.preventDefault()
        reloadDataFunc()
    }

    return (
        <Button variant="contained" color="primary" startIcon={<RefreshIcon />} onClick={handleOnClick}>Reload Data</Button>
    )
}