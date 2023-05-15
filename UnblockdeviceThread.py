import subprocess
from threading import Thread
from datetime import date, datetime
from utilities import *
from socket import gethostname
from netmiko import *
from datetime import datetime
import uuid
from Logs import update_logs


class UnblockdeviceThread(Thread):
    def __init__(self, destination, unblockdevice_info):
        super().__init__()
        print(
            f"BlockingThread: initializing thread object: blocking_info={unblockdevice_info}")
        if "target" not in unblockdevice_info:
            print(
                f"BlockingThread: missing information in blocking_info: {unblockdevice_info}")
            return
        self.destination = destination
        self.target = unblockdevice_info["target"]
        self.token = unblockdevice_info["token"]

    def process_blocking(self, unblockdevice_output):
        status_code = send_unblockdevice(
            gethostname(),
            self.destination,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            unblockdevice_output,
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
        unblockdevice_output = ssh.send_command_timing(
            command_string="""
     configure terminal
     no access-list 100 deny ip host %s any
     end
     show access-lists 100""" % self.target
        )
        nowdate = datetime.now()
        unblockdevice_output = str(unblockdevice_output+"Device Blocked")
        if unblockdevice_output is None:
            print(f"unblock thread: failed for {self.target}")
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_unblockdevice_failed",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/deviceunblock",
                "log_host": self.target,
            }
            update_logs(log)
            return
        else:
            print(
                f"device unblock: succeeded for {self.target}")

            self.process_blocking(
                unblockdevice_output)
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_unblockdevice_succsess",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/unblockdevice",
                "log_host": self.target,
            }
        update_logs(log)
        print(f"Completed unblocking deviiiiiiice thread for {self.target}")
