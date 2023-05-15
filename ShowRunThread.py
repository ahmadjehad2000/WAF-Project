from threading import Thread
from datetime import datetime
from utilities import send_showrun
from socket import gethostname
from netmiko import *
import uuid


class ShowRunThread(Thread):
    def __init__(self, destination, showrun_info):
        super().__init__()
        print(
            f"showrun: initializing thread object: showrun_info={showrun_info}")
        if "target" not in showrun_info:
            print(
                f"showrun: missing information in showrun_info: {showrun_info}")
            return
        self.destination = destination
        self.target = showrun_info["target"]
        self.token = showrun_info["token"]

    def process_showrun(self, showrun_output):
        status_code = send_showrun(
            gethostname(),
            self.destination,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            showrun_output,
        )
        print(f"\nshowrunThread: command sent, result={status_code}\n")

    def run(self):
        print(f"Starting Show run thread for {self.target}")
        print(f"Executing command show running-config on {self.target}")
        device = {
            'device_type': 'cisco_ios',
            'host': self.target,
            'username': 'admin',
            'password': 'waf',
            'secret': 'waf'

        }
        from Logs import update_logs
        ssh = ConnectHandler(**device)
        ssh.enable()
        showrun_output = ssh.send_command("show run")
        if showrun_output is None:
            print(f"showrun failed for {self.target}")
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_show_run_failed",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/showrun",
                "log_host": self.target,
            }
            update_logs(log)
            return
        else:
            print(f"show run succeeded for {self.target}")
            print(str(showrun_output))
            nowdate = datetime.now()
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_showrun_succsess",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/showrun",
                "log_host": self.target,
            }
        self.process_showrun(
            showrun_output)
        with open(f"/home/admin/Documents/{self.target}.conf", 'w') as file:
            file.writelines(showrun_output)

        update_logs(log)
        print(f"Completedshowrun thread for {self.target}")
