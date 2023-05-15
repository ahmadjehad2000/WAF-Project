from time import sleep
import requests
import json
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor
from sys import path
path.append("/home/admin/Downloads/Tool-WAF-Graduation-development/")


def get_devices():

    response = requests.get("http://127.0.0.1:5000/devices")
    if response.status_code != 200:
        print(
            f" !!!  Failed to retrieve devices from server: {response.reason}")
        return {}

    print(" devices successfully retrieved")
    return response.json()


def defineDevices():
    name = input('enter device name: ')
    type = input('enter device type: ')
    host = input('enter ip: ')
    user = input('enter user: ')
    passwd = input('enter pass: ')
    device = {
        "device_name": name,
        "device_type": type,
        "host": host,
        "username": user,
        "password": passwd,
        "available": False
    }
    updateDevice(device)


def updateDevice(device):
    rsp = requests.put("http://127.0.0.1:5000/devices", json=device)
    if rsp.status_code != 204:
        print("Error updating devices via REST API")
    else:
        print("successfully updated devices via REST API")


def updateStatus(hosts):
    ans, unans = scapy.arping(hosts['host'])
    ans.summary()
    if ans:
        hosts['available'] = True
    elif unans:
        hosts['available'] = False
    updateDevice(hosts)


# def printDevices():
#     jsonobj = requests.get("http://127.0.0.1:5000/devices")
#     if jsonobj.status_code != 200:
#         print("Error getting devices via REST API")
#     else:
#         devices = jsonobj.json()
#         for i in devices:
#             print(i)
#             print(tabulate([devices[i]['device_name']],
#                   [devices[i]['device_name']], [devices[i]['host']], [devices[i]['username']], [devices[i]['password']]))
#             print("\n")
if __name__ == "__main__":
    while True:
        hosts = get_devices()
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.map(updateStatus, hosts.values())
       	sleep(2)
	
