import json
import uuid
from time import sleep
from scapy.all import *
from scapy.layers.http import HTTPRequest
from tabulate import tabulate
from datetime import time
import requests
from sys import path
path.append("/home/admin/Downloads/Tool-WAF-Graduation-development")


def sniff_scapy(iface=None):
    if iface:

        sniff(filter="port 80", prn=process_packet, iface=iface, store=False)
    else:
        # sniff with default interface
        sniff(filter="port 80", prn=process_packet, store=False)


def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPRequest].Host.decode(
        ) + packet[HTTPRequest].Path.decode()
        httpver = packet[HTTPRequest].Http_Version.decode()
        ip = packet[IP].src
        destip = packet[IP].dst
        method = packet[HTTPRequest].Method.decode()
        nowdate = datetime.now()
        currentdate = nowdate.strftime("%d/%m/%Y:%H:%M:%S")
        currenttime = nowdate.strftime("%H:%M:%S")
        id = str(uuid.uuid4().fields[-1])[:5]
        packetinfo = [packet]
        print(tabulate({"ID": [id], "SRC": [ip], "DST": [destip],
                        "Method": [method, httpver], "URL": [url], "Timestamp": [currenttime, currentdate], "packet": [packetinfo]}, headers="keys"))
        from findAnomaly import findAnomaly
        from hosts import update_host
        from Logs import update_logs
        newurl = str(url)
        anomal = findAnomaly()
        if anomal.findSqli(url=newurl):
            from rabbitMQ_worker_api import start_blocking
            start_blocking(str(ip))
            print("SQLI found ")
            capture = {
                "id": id,
                "srcip": ip,
                "dstip": destip,
                "method": method,
                "httpver": httpver,
                "url": url,
                "timestamp": currenttime,
                "Date": currentdate,
                "full-packet-info": [currentdate, str(packetinfo)],
                "status": "anomaly",
            }
            log = {
                "log_id": id,
                "log_type": "owasp_capture",
                "log_timestamp": currentdate,
                "log_url": url,
                "log_host": ip,
            }
            host = {
                "host": str(ip),
                "status": "blocked"

            }
            update_logs(log)
            update_host(host)
        else:
            print("NO SQLI")
            capture = {
                "id": id,
                "srcip": ip,
                "dstip": destip,
                "method": method,
                "httpver": httpver,
                "url": url,
                "timestamp": currenttime,
                "Date": currentdate,
                "full-packet-info": [currentdate, str(packetinfo)],
                "status": "normal",
            }
            host = {
                "host": str(ip),
                "status": "normal"

            }
            log = {
                "log_id": id,
                "log_type": "normal_capture",
                "log_timestamp": currentdate,
                "log_url": url,
                "log_host": ip,
            }
        update_logs(log)
        updatecap(capture)
        update_host(host)


def updatecap(capture):
    rsp = requests.put("http://127.0.0.1:5000/capture", json=capture)
    if rsp.status_code != 204:
        print(
            f"Error updating capture via REST API capture info:\n SourceIP:{capture['srcip']}\n URL:{capture['url']}\n Timestamp:{capture['timestamp']}")
    else:
        print(
            f"successfully post the capture via REST API info SourceIP:{capture['srcip']} DestIP:{capture['dstip']} URL:{capture['url']}")


def getcap():
    print("Retriving old captures")
    rsp = requests.get("http://127.0.0.1:5000/capture")
    if rsp.status_code != 200:
        print(f"Error getting captures via REST API {rsp.reason}")
        return {}
    else:
        print("Captures retrieved succsefully")
        return rsp.json()


def printcap():
    rsp = requests.get("http://127.0.0.1:5000/capture")
    if rsp.status_code != 200:
        print(f"Error getting captures via REST API {rsp.reason}")
        return {}
    else:
        print("Captures retrieved succsefully")
        with open("packetcapture.json", mode='w') as file:
            packetinfo = str(rsp.json())
            file.write(packetinfo)


if __name__ == "__main__":
    # try:
    sniff_scapy("ens4")
    # except KeyboardInterrupt:
    #     print("shutting down")
    #     exit()
    # finally:
    #     printcap()
    #     sleep(3)
    #     print("shutting down")
