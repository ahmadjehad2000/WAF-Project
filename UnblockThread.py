import subprocess
from threading import Thread
from datetime import datetime
from utilities import *
from socket import gethostname
import uuid
from Logs import update_logs
from hosts import update_host


class UnblockThread(Thread):
    def __init__(self, destination, unblock_info):
        super().__init__()
        print(
            f"UnblockThread: initializing thread object: blocking_info={unblock_info}")
        if "target" not in unblock_info:
            print(
                f"UnblockThread: missing information in blocking_info: {unblock_info}")
            return
        self.destination = destination
        self.target = unblock_info["target"]
        self.token = unblock_info["token"]

    def process_blocking(self, unblock_output):
        status_code = send_unblock(
            gethostname(),
            self.destination,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            unblock_output,
        )
        print(f"\nUnblokcThread: blocking sent, result={status_code}\n")

    def run(self):
        print(f"Starting Blocking thread for {self.target}")
        print(f"Executing command iptables -D INPUT -s {self.target}-j DROP")
        unblock_output = subprocess.check_output(
            ["iptables", "-D", "INPUT", "-s", self.target, "-j", "DROP"])
        unblock_output = str(unblock_output.decode('utf-8')+"unblock")
        nowdate = datetime.now()
        if unblock_output is None:
            print(f"Unblock failed for {self.target}")
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_unblock_failed",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/unblokc",
                "log_host": self.target,
            }
            update_logs(log)
            return
        else:
            print(f"UNblock succeeded for {self.target}")
        # iptables -I INPUT -s 192.168.1.100 -j DROP
            self.process_blocking(
                unblock_output)
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_unblock_succsess",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/unblock",
                "log_host": self.target,
            }
            host = {
                "host": self.target,
                "status": "normal"

            }
            update_host(host)
        update_logs(log)
        print(f"Completed UNblocks thread for {self.target}")
