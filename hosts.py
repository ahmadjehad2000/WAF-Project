
import requests
from sys import path
path.append("/home/admin/Downloads/Tool-WAF-Graduation-development/")


def update_host(host):
    rsp = requests.put("http://127.0.0.1:5000/hosts", json=host)
    if rsp.status_code != 204:
        print("Failed updating the hosts")
    else:
        print("hosts updated successufully")
