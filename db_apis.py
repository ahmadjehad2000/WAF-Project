from extensions import db
from datetime import datetime
import time
import re


def remove_internals(d):

    return {k: v for (k, v) in d.items() if not k.startswith("_")}


def get_all_hosts():

    hosts = {host["host"]: remove_internals(
        host) for host in db.hosts.find()}
    return hosts


def get_host(host):

    hosts = db.hosts.find_one({"host": host})
    return remove_internals(hosts)


def set_host(host):

    existing_host = db.hosts.find_one({"host": host["host"]})
    if not existing_host:
        db.hosts.insert_one(host)
    else:
        db.hosts.update_one({"host": host["host"]}, {"$set": host})


def getCapture():
    captures = {capture["id"]: remove_internals(
        capture) for capture in db.captures.find()}
    return captures


def setCapture(capture):
    existing_cap = db.hosts.find_one({"id": capture["id"]})
    if not existing_cap:
        db.captures.insert_one(capture)
    else:
        db.captures.insert_one(capture)


def getBlockingIP(target, token):
    max_wait = 100
    start_time = datetime.now()
    while(datetime.now() - start_time).total_seconds() < max_wait:
        blocking = db.blocking.find_one({"target": target, "token": token})
        if not blocking:
            time.sleep(5)
            continue
        return remove_internals(blocking)
    return {}


def get_portscan(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        scan = db.portscans.find_one({"target": target, "token": token})
        if not scan:
            time.sleep(5)
            continue

        # print(f"found it, returning scan: {scan}")
        return remove_internals(scan)

    return {}  # portscan results never found


def get_showrun(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        showrun = db.showruns.find_one({"target": target, "token": token})
        if not showrun:
            time.sleep(5)
            continue

        # print(f"found it, returning scan: {scan}")
        return remove_internals(showrun)

    return {}  # portscan results never found


def get_traceroute(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        traceroute = db.traceroutes.find_one(
            {"target": target, "token": token})
        if not traceroute:
            time.sleep(5)
            continue

        # print(f"found it, returning traceroute: {traceroute}")
        return remove_internals(traceroute)

    return {}  # traceroute results never found


def getDevices():

    devices = {device["host"]: remove_internals(
        device) for device in db.devices.find()}
    return devices


def setDevice(device):

    db.devices.insert_one(device)


def get_device(host):

    host = db.devices.find_one({"host": host})
    return remove_internals(host)


# def check_devices(hostip):
#     device = db.devices.count_documents({"host": hostip})
#     if device >= 1:
#         return True
#     else:
#         return False

def getLogs():
    logs = {log["log_type"]: remove_internals(
        log) for log in db.logs.find()}
    return logs


def setLog(log):
    db.logs.insert_one(log)


def gethosts():
    hosts = {host["host"]: remove_internals(
        host) for host in db.hosts.find()}
    return hosts


def setHosts(host):
    db.hosts.insert_one(host)


def record_blocking_data(blocking_data):
    db.blocking.insert_one(blocking_data)


def record_showrun_data(showrun_data):
    db.blocking.insert_one(showrun_data)


def record_portscan_data(portscan_data):

    db.portscans.insert_one(portscan_data)


def record_traceroute_data(traceroute_data):

    db.traceroutes.insert_one(traceroute_data)


def record_deviceblocking_data(deviceblocking_data):

    db.deviceblocking.insert_one(deviceblocking_data)


def record_unblockdevice_data(unblockdevice_data):

    db.unblockdevice.insert_one(unblockdevice_data)


def record_unblocking_data(unblocking_data):
    db.unblocking.insert_one(unblocking_data)
