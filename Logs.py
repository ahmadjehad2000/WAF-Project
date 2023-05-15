
import requests
from sys import path
path.append("/home/admin/Downloads/Tool-WAF-Graduation-development")


def update_logs(log):
    rsp = requests.post("http://127.0.0.1:5000/logs", json=log)
    if rsp.status_code != 204:
        print("Failed updating the log")
    else:
        print("log updated successufully")
