import React, { Component } from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import MaterialTable from "material-table";
import CLoudDownloadIcon from "@material-ui/icons/CloudDownload";
import BlockIcon from "@material-ui/icons/Block";
import RemoveCircleOutlineIcon from "@material-ui/icons/RemoveCircleOutline";
import Dialog from '@material-ui/core/Dialog'
import DialogTitle from '@material-ui/core/DialogTitle'
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";

class Devices extends Component {

    constructor(props) {
        super(props);
        this.state = {
            devices: [],
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openShowRunDialog: false,
            openBlockingDialog: false,
            openUnblockingDialog: false,
            renderHost: '',
            showRunResults: '',
            BlockingResults: '',
            UnblockingResults: '',
            token: '',
        };
    }

    countdown() {
        this.setState({ countdownValue: this.state.countdownValue - 1 })
        if (this.state.countdownValue === 0) {
            this.fetchDevices()
        }
    }

    fetchDevices() {

        let requestUrl = "http://127.0.0.1:5000/devices"
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({ devices: data })
                this.setState({ countdownValue: process.env.REACT_APP_REFRESH_RATE })
            })
            .catch((e) => {
                console.log(e)
                this.setState({ countdownValue: process.env.REACT_APP_REFRESH_RATE })
            });
    }

    initiateShowRun(host) {

        this.setState({ showRunResults: { result: "Executing show run ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/showrun?target=' + host
        const requestOptions = { method: 'POST' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ token: data.token })
                this.fetchShowRun(host)
                console.log(this.state.showRunResults)
            })
            .catch(console.log)
    }


    initiateBlocking(host) {

        this.setState({ BlockingResults: { result: "Executing blocking for device ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/deviceblocking?target=' + host
        const requestOptions = { method: 'POST' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ token: data.token })
                this.fetchBlocking(host)
                console.log(this.state.BlockingResults)
            })
            .catch(console.log)
    }



    initiateUnblocking(host) {

        this.setState({ UnblockingResults: { result: "Executing Unblocking..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/unblockdevice?target=' + host
        const requestOptions = { method: 'POST' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ token: data.token })
                this.fetchUnblocking(host)
                console.log(this.state.UnblockingResults)
            })
            .catch(console.log)
    }

    fetchShowRun(host) {
        this.setState({ showRunResults: { result: "retrieving showw run results ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/showrun?target=' + host + '&token=' + this.state.token
        const requestOptions = { method: 'GET' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ showRunResults: data })
                console.log(this.state.showRunResults)
            })
            .catch(console.log)

    }

    fetchBlocking(host) {
        this.setState({ BlockingResults: { result: "retrieving BLocking results ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/deviceblocking?target=' + host + '&token=' + this.state.token
        const requestOptions = { method: 'GET' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ BlockingResults: data })
                console.log(this.state.BlockingResults)
            })
            .catch(console.log)

    }



    fetchUnblocking(host) {
        this.setState({ UnblockingResults: { result: "retrieving unblock results ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/unblockdevice?target=' + host + '&token=' + this.state.token
        const requestOptions = { method: 'GET' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ UnblockingResults: data })
                console.log(this.state.UnblockingResults)
            })
            .catch(console.log)

    }

    componentDidMount() {
        this.fetchDevices(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    renderShowRunDialog(host) {
        this.initiateShowRun(host)
        this.setState({ openShowRunDialog: true, renderHost: host })
    }

    renderBlockingDialog(host) {
        this.initiateBlocking(host)
        this.setState({ openBlockingDialog: true, renderHost: host })
    }

    renderUnblockingDialog(host) {
        this.initiateUnblocking(host)
        this.setState({ openUnblockingDialog: true, renderHost: host })
    }

    handleCloseShowRunDialog(parent) {
        parent.setState({ openShowRunDialog: false })
    }

    handleBlockingDialog(parent) {
        parent.setState({
            openBlockingDialog
                : false
        })
    }
    handleUnblockingDialog(parent) {
        parent.setState({ openUnblockingDialog: false })
    }
    render() {

        const { devices } = this.state;

        return (
            <div className="container" style={{ maxWidth: "100%" }}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Devices Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchDevices()
                    }}>Refresh Devices</Button>
                </Grid>
                <MaterialTable
                    title="Devices Table"
                    columns={[

                        { title: 'Device Name', field: 'device_name', defaultSort: 'asc' },

                        { title: 'IP Address', field: 'host' },

                    ]}
                    data={Object.values(devices)}
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                        rowStyle: (rowData) => {
                            if (!rowData.available) {
                                return { color: 'red' };
                            }
                            else {
                                return { color: 'chartreuse' }
                            }
                        },
                        cellStyle: { fontSize: 14, }
                    }}
                    actions={[
                        {
                            icon: CLoudDownloadIcon,
                            tooltip: 'Show running configuration on device',
                            onClick: (event, rowData) => {
                                this.renderShowRunDialog(rowData.host)
                            }
                        },
                        {
                            icon: BlockIcon,
                            tooltip: 'Block the device',
                            onClick: (event, rowData) => {
                                this.renderBlockingDialog(rowData.host)
                            }
                        },
                        {
                            icon: RemoveCircleOutlineIcon,
                            tooltip: 'Unblock the device',
                            onClick: (event, rowData) => {
                                this.renderUnblockingDialog(rowData.host)
                            }
                        }
                    ]}
                />
                <Dialog
                    open={this.state.openShowRunDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Show running configurarion on this device: {this.state.renderHost}</DialogTitle>
                    <DialogContent>
                        <b>Output for show run:</b><br />
                        Result: {this.state.showRunResults.result}<br />
                        show run results:
                        <br /><br />
                        saved the configurarion file to /home/admin/Documents/{this.state.renderHost}.conf
                        <br /><br />
                        <b>NOTE:</b><br />
                        Please Wait it may take some time
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleCloseShowRunDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
                <Dialog
                    open={this.state.openBlockingDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Blocking device: {this.state.renderHost}</DialogTitle>
                    <DialogContent>
                        <b></b><br />
                        Result: {this.state.BlockingResults.result}<br />
                        <br /><br />
                        Blocked the device {this.state.renderHost}
                        <br /><br />
                        <b>NOTE:</b><br />
                        Please Wait it may take some time
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleBlockingDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
                <Dialog
                    open={this.state.openUnblockingDialog}
                    maxWidth="lg"
                >
                    <DialogTitle>Unlocking device: {this.state.renderHost}</DialogTitle>
                    <DialogContent>
                        <b></b><br />
                        Result: {this.state.UnblockingResults.result}<br />
                        <br /><br />
                        Unblocked the device  {this.state.renderHost}
                        <br /><br />
                        <b>NOTE:</b><br />
                        Please Wait it may take some time
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.handleUnblockingDialog(this)}>
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div >
        );
    }
}

export default Devices;
