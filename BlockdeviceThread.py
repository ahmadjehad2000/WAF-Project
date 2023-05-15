import subprocess
from threading import Thread
from datetime import date, datetime
from utilities import send_deviceblocking
from socket import gethostname
from netmiko import *
from datetime import datetime
import uuid
from Logs import update_logs


class BlockdeviceThread(Thread):
    def __init__(self, destination, deviceblocking_info):
        super().__init__()
        print(
            f"BlockingThread: initializing thread object: blocking_info={deviceblocking_info}")
        if "target" not in deviceblocking_info:
            print(
                f"BlockingThread: missing information in blocking_info: {deviceblocking_info}")
            return
        self.destination = destination
        self.target = deviceblocking_info["target"]
        self.token = deviceblocking_info["token"]

    def process_blocking(self, deviceblocking_output):
        status_code = send_deviceblocking(
            gethostname(),
            self.destination,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            deviceblocking_output,
        )
        print(f"\nBlockingThread: blocking sent, result={status_code}\n")

    def run(self):
        print(f"Starting Blocking thread for {self.target}")
        print(f"Executing command access-list")
        device = {
            'device_type': 'cisco_ios',
            'host': '192.168.11.100',
            'username': 'admin',
            'password': 'waf',
            'secret': 'waf'
        }
        ssh = ConnectHandler(**device)
        ssh.enable()
        deviceblocking_output = ssh.send_command_timing(
            command_string="""
     configure terminal
     access-list 100 deny ip host %s any
     end
     show access-lists 100""" % self.target
        )
        nowdate = datetime.now()
        deviceblocking_output = str(deviceblocking_output+"Device Blocked")
        if deviceblocking_output is None:
            print(f"DeviceBlockingThread: blocking failed for {self.target}")
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_deviceblock_failed",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/deviceblock",
                "log_host": self.target,
            }
            update_logs(log)
            return
        else:
            print(
                f"DeviceBlockingThread: blocking succeeded for {self.target}")

            self.process_blocking(
                deviceblocking_output)
            print(deviceblocking_output)
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_deviceblock_succsess",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/deviceblock",
                "log_host": self.target,
            }
        update_logs(log)
        print(f"Completed Device Blocking thread for {self.target}")
