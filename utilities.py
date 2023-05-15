from datetime import datetime
import requests
from pprint import pformat, pprint


def send_blocking(source, destination, target, token, timestamp, blocking_output):
    blocking_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "blocking_output": pformat(blocking_output),
    }
    rsp = requests.post(
        "http://" + destination + "/workerbroker/blocking", json=blocking_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /blocking/store response: {rsp.status_code}, {rsp.content}"
        )
    else:
        print(f"{str(datetime.now())[:-3]}: Blocking sent")
    return rsp.status_code


def send_showrun(source, destination, target, token, timestamp, showrun_output):
    showrun_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "showrun_output": showrun_output,
    }
    rsp = requests.post(
        "http://" + destination + "/workerbroker/showrun", json=showrun_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /workerbroker/showrun response: {rsp.status_code}, {rsp.content}"
        )
    else:
        print(f"{str(datetime.now())[:-3]}: command sent")
    return rsp.status_code


def send_deviceblocking(source, destination, target, token, timestamp, deviceblocking_output):
    deviceblocking_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "deviceblocking_output": deviceblocking_output,
    }
    rsp = requests.post(
        "http://" + destination + "/workerbroker/deviceblocking", json=deviceblocking_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /workerbroker/deviceblocking response: {rsp.status_code}, {rsp.content}"
        )
    else:
        print(f"{str(datetime.now())[:-3]}: command sent")
    return rsp.status_code


def send_unblockdevice(source, destination, target, token, timestamp, unblockdevice_output):
    unblockdevice_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "unblockdevice_output": unblockdevice_output,
    }
    rsp = requests.post(
        "http://" + destination + "/workerbroker/unblockdevice", json=unblockdevice_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /workerbroker/unblock device response: {rsp.status_code}, {rsp.content}"
        )
    else:
        print(f"{str(datetime.now())[:-3]}: command sent")
    return rsp.status_code


def send_unblock(source, destination, target, token, timestamp, unblock_output):
    unblock_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "unblockdevice_output": unblock_output,
    }
    rsp = requests.post(
        "http://" + destination + "/workerbroker/unblock", json=unblock_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /workerbroker/unblock device response: {rsp.status_code}, {rsp.content}"
        )
    else:
        print(f"{str(datetime.now())[:-3]}: command sent")
    return rsp.status_code
