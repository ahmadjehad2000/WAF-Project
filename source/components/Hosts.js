import React, { Component } from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import BlockIcon from "@material-ui/icons/Block";
import MaterialTable from "material-table";
import RemoveCircleOutlineIcon from "@material-ui/icons/RemoveCircleOutline";
import Dialog from '@material-ui/core/Dialog'
import DialogTitle from '@material-ui/core/DialogTitle'
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";


class Hosts extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hosts: [],
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
            openExtendedPortScanDialog: false,
            portScanHost: '',
            portScanResults: '',
            extendedPortScanResults: '',
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
            this.fetchHosts()
        }
    }

    fetchHosts() {

        let requestUrl = process.env.REACT_APP_WAF_HOST + '/hosts'
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({ hosts: data })
                this.setState({ countdownValue: process.env.REACT_APP_REFRESH_RATE })
            })
            .catch((e) => {
                console.log(e)
                this.setState({ countdownValue: process.env.REACT_APP_REFRESH_RATE })
            });
    }



    componentDidMount() {
        this.fetchHosts()
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    initiateBlocking(host) {

        this.setState({ BlockingResults: { result: "Executing blocking for device ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/blocking?target=' + host
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
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/unblock?target=' + host
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

    fetchBlocking(host) {
        this.setState({ BlockingResults: { result: "retrieving BLocking results ..." } })
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/blocking?target=' + host + '&token=' + this.state.token
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
        let requestUrl = process.env.REACT_APP_WAF_HOST + '/unblock?target=' + host + '&token=' + this.state.token
        const requestOptions = { method: 'GET' }
        fetch(requestUrl, requestOptions)
            .then(res => res.json())
            .then((data) => {
                this.setState({ UnblockingResults: data })
                console.log(this.state.UnblockingResults)
            })
            .catch(console.log)

    }
    renderBlockingDialog(host) {
        this.initiateBlocking(host)
        this.setState({ openBlockingDialog: true, renderHost: host })
    }

    renderUnblockingDialog(host) {
        this.initiateUnblocking(host)
        this.setState({ openUnblockingDialog: true, renderHost: host })
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

        const { hosts } = this.state;

        return (

            <div className="container" style={{ maxWidth: "100%" }}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Hosts Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchHosts()
                    }}>Refresh Hosts</Button>
                </Grid>
                <MaterialTable
                    title="ANy device connected with Webserver is a host"
                    columns={[

                        { title: 'IP Address', field: 'host', defaultSort: 'asc' },
                        { title: 'Status', field: 'status' },



                    ]}
                    data={Object.values(hosts)}
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10,
                        rowStyle: (rowData) => {
                            if (rowData.status === "blocked") {
                                return { color: 'red' };
                            }
                            else {
                                return { color: 'blue' }
                            }
                        },

                        cellStyle: { fontSize: 20, }
                    }}

                    actions={
                        [

                            {
                                icon: BlockIcon,
                                tooltip: 'Block the host',
                                onClick: (event, rowData) => {
                                    this.renderBlockingDialog(rowData.host)
                                },
                            },
                            {
                                icon: RemoveCircleOutlineIcon,
                                tooltip: 'Unblock the host',
                                onClick: (event, rowData) => {
                                    this.renderUnblockingDialog(rowData.host)
                                },
                            }
                        ]}


                />
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
            </div>
        );
    }
}

export default Hosts;
