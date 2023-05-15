from asyncio.proactor_events import _ProactorDuplexPipeTransport
from flask import Flask, redirect, request
from sys import stdout
from time import sleep
import json
from typing import Any
import colorama
import requests
from tabulate import tabulate
from colorama import Fore, Back
import re
from sqlipattern import *
from httprequestcap import updatecap
colorama.init(autoreset=True)


class findAnomaly:
    def __init__(self) -> None:
        pass

    def refreshCap(self):
        self.rsp = requests.get("http://127.0.0.1:5000/capture")
        self.jsonObj = self.rsp.json()
        return self.jsonObj

    def findSqli(self, url):
        # jsonObj = self.refreshCap()
        # for i in jsonObj:
        #     url = str(jsonObj[i]['url'])

        if pattern_apost(url) or pattern_comment(url) or pattern_keyword(url.upper()):
            print(Back.RED+"SQLi FOUND IN "+url)
            # capture = {
            #     "id": jsonObj[i]['id'],
            #     "srcip": jsonObj[i]['srcip'],
            #     "dstip": jsonObj[i]['dstip'],
            #     "method": jsonObj[i]['method'],
            #     "httpver": jsonObj[i]['httpver'],
            #     "url": jsonObj[i]['url'],
            #     "timestamp": jsonObj[i]['timestamp'],
            #     "Date": jsonObj[i]['Date'],
            #     "full-packet-info": jsonObj[i]['full-packet-info'],
            #     "status": "anomaly",
            # }

            # updatecap(capture)
            return True

        else:
            print(Back.BLUE+"NORMAL"+url)
            return False

        # print(value['url'])
        # print(value['timestamp'],
        # value['Date'])


# def main():

#         # while True:
#         #     anomal.findSqli()
#         #     anomal.refreshCap()
#         #     sleep(5)
#         #     print("new captures")

    # def handle_redirect(self):
    #     rsp = requests.get(
    #         "http://192.168.73.152/checkdb.php", params={"waf": "waf"})
    #     return rsp.content


if __name__ == "__main__":
    while True:
        anomal = findAnomaly()
        anomal.findSqli()
