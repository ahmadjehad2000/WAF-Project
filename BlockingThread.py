import subprocess
from threading import Thread
from datetime import date, datetime
import uuid
from utilities import send_blocking
from socket import gethostname
from hosts import update_host
from sys import path
path.append("/home/admin/Downloads/Tool-WAF-Graduation-development/")


class BlockingThread(Thread):
    def __init__(self, destination, blocking_info):
        super().__init__()
        print(
            f"BlockingThread: initializing thread object: blocking_info={blocking_info}")
        if "target" not in blocking_info:
            print(
                f"BlockingThread: missing information in blocking_info: {blocking_info}")
            return
        self.destination = destination
        self.target = blocking_info["target"]
        self.token = blocking_info["token"]

    def process_blocking(self, blocking_output):
        status_code = send_blocking(
            gethostname(),
            self.destination,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            blocking_output,
        )
        print(f"\nBlockingThread: blocking sent, result={status_code}\n")

    def run(self):
        from Logs import update_logs

        print(f"Starting Blocking thread for {self.target}")
        print(f"Executing command iptables -I INPUT -s {self.target}-j DROP")
        blocking_output = subprocess.check_output(
            ["iptables", "-I", "INPUT", "-s", self.target, "-j", "DROP"])
        blocking_output = str(blocking_output.decode('utf-8')+"Blocking")
        if blocking_output is None:
            print(f"BlockingThread: blocking failed for {self.target}")
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_blocker_failed",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/blocking",
                "log_host": self.target,
            }
            update_logs(log)
            return
        else:
            print(f"BlockingThread: blocking succeeded for {self.target}")
        # iptables -I INPUT -s 192.168.1.100 -j DROP
            self.process_blocking(
                blocking_output)
            nowdate = datetime.now()
            log = {
                "id": str(uuid.uuid4().fields[-1])[:5],
                "log_type": "worker_blocker_succsess",
                "log_timestamp": nowdate.strftime("%d/%m/%Y:%H:%M:%S"),
                "log_url": "127.0.0.1:5000/blocking",
                "log_host": self.target,
            }
            host = {
                "host": self.target,
                "status": "blocked"

            }
            update_host(host)
        update_logs(log)
        print(f"Completed Blocking thread for {self.target}")
