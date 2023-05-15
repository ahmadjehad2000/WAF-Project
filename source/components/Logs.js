import React, { Component } from 'react';
import Button from '@material-ui/core/Button'
import Grid from "@material-ui/core/Grid";
import MaterialTable from "material-table";

class Logs extends Component {

    constructor(props) {
        super(props);
        this.state = {
            logs: [],
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };
    }

    countdown() {
        this.setState({ countdownValue: this.state.countdownValue - 1 })
        if (this.state.countdownValue === 0) {
            this.fetchLogs()
        }
    }

    fetchLogs() {

        let requestUrl = "http://127.0.0.1:5000/logs"
        fetch(requestUrl)
            .then(res => res.json())
            .then((data) => {
                console.log(data)
                this.setState({ logs: data })
                this.setState({ countdownValue: process.env.REACT_APP_REFRESH_RATE })
            })
            .catch((e) => {
                console.log(e)
                this.setState({ countdownValue: process.env.REACT_APP_REFRESH_RATE })
            });
    }



    componentDidMount() {
        this.fetchLogs(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }



    render() {

        const { logs } = this.state;

        return (
            <div className="container" style={{ maxWidth: "100%" }}>
                <link
                    rel="stylesheet"
                    href="https://fonts.googleapis.com/icon?family=Material+Icons"
                />
                <Grid container direction="row" justify="space-between" alignItems="center">
                    <h2>Logs Table</h2>
                    <h6>Time until refresh: {this.state.countdownValue} seconds</h6>
                    <Button variant="contained" onClick={() => {
                        this.fetchLogs()
                    }}>Refresh Logs</Button>
                </Grid>
                <MaterialTable
                    title="Logging is important"
                    columns={[
                        { title: 'Log type', field: 'log_type' },
                        { title: 'log Timestamp', field: 'log_timestamp', defaultSort: 'desc' },
                        { title: 'log URL', field: 'log_url' },
                        { title: 'log host', field: 'log_host' },
                    ]}
                    data={Object.values(logs)}
                    options={{
                        sorting: true,
                        padding: "dense",
                        pageSize: 10

                    }}

                />

            </div>
        );
    }
}

export default Logs;
