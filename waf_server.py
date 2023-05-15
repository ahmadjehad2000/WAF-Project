from waf_server_utils import fix_target
from flask_cors import CORS
from db_apis import *
from flask import Flask, request
from rabbitMQ_worker_api import *

waf_app = Flask(__name__)
CORS(waf_app)


@waf_app.route("/hosts", methods=["GET", "PUT"])
def hosts():
    if request.method == "GET":
        return gethosts()
    elif request.method == "PUT":
        host = request.get_json()
        setHosts(host)
        return {}, 204


@waf_app.route("/devices", methods=["GET", "PUT"])
def devices():
    if request.method == "GET":
        return getDevices()
    elif request.method == "PUT":
        devices = request.get_json()
        setDevice(devices)
        return {}, 204


@waf_app.route("/capture", methods=["GET", "PUT"])
def capture():
    if request.method == "GET":
        return getCapture()
    elif request.method == "PUT":
        capture = request.get_json()
        setCapture(capture)
        return {}, 204


@waf_app.route("/logs", methods=["GET", "POST"])
def logging():
    if request.method == "GET":
        return getLogs()
    elif request.method == "POST":
        log = request.get_json()
        setLog(log)
        return {}, 204


@waf_app.route("/blocking", methods=["GET", "POST"])
def blockbasedIP():
    target = request.args.get("target")
    if not target:
        return "Must provide target", 400
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "Must provide token to get the blocking service", 400
        return getBlockingIP(target, token)
    elif request.method == "POST":
        token = start_blocking(target)
        return {"token": token}


@waf_app.route("/workerbroker/blocking", methods=["POST"])
def workerBlocking():
    blocking_data = request.get_json()
    record_blocking_data(blocking_data)
    return {}, 204


@waf_app.route("/showrun", methods=["GET", "POST"])
def showRun():
    target = request.args.get("target")
    if not target:
        return "must provide target to get portscan", 400
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "must provide token to get portscan", 400
        return get_portscan(target, token)
    elif request.method == "POST":
        token = start_showrun(target)
        return {"token": token}


@waf_app.route("/workerbroker/showrun", methods=["POST"])
def workershowRun():
    showrun_data = request.get_json()
    record_showrun_data(showrun_data)
    return {}, 204


@waf_app.route("/deviceblocking", methods=["GET", "POST"])
def deviceBlock():
    target = request.args.get("target")
    if not target:
        return "must provide target to get portscan", 400
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "must provide token to get device block", 400
        return get_portscan(target, token)
    elif request.method == "POST":
        token = start_deviceblocking(target)
        return {"token": token}


@waf_app.route("/workerbroker/deviceblocking", methods=["POST"])
def workerdeviceBlocking():
    deviceblocking_data = request.get_json()
    record_deviceblocking_data(deviceblocking_data)
    return {}, 204


@waf_app.route("/unblockdevice", methods=["GET", "POST"])
def unblockDevice():
    target = request.args.get("target")
    if not target:
        return "must provide target to get portscan", 400
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "must provide token to get portscan", 400
        return get_portscan(target, token)
    elif request.method == "POST":
        token = start_unblockdevice(target)
        return {"token": token}


@waf_app.route("/workerbroker/unblockdevice", methods=["POST"])
def workerunblockDevice():
    unblockdevice_data = request.get_json()
    record_unblockdevice_data(unblockdevice_data)
    return {}, 204


@waf_app.route("/unblock", methods=["GET", "POST"])
def unblock():
    target = request.args.get("target")
    if not target:
        return "Must provide target", 400
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "Must provide token to get the blocking service", 400
    elif request.method == "POST":
        token = start_unblock(target)
        return {"token": token}


@waf_app.route("/workerbroker/unblock", methods=["POST"])
def workerunblock():
    unblock_data = request.get_json()
    record_unblocking_data(unblock_data)
    return {}, 204


if __name__ == "__main__":
    waf_app.run()
