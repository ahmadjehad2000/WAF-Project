from tracemalloc import start
import pika
import json
from datetime import datetime


def start_blocking(target):
    print(f"Start blocking process for {target}")
    token = str(datetime.now())
    blocking_info = {
        "waf": "localhost:5000",
        "work_type": "blocking",
        "target": target,
        "token": token,
    }
    blocking_info_json = json.dumps(blocking_info)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="waf", durable=True)
    channel.basic_publish(
        exchange="", routing_key="waf", body=blocking_info_json
    )
    return token


def start_showrun(target):
    print(f"start running showrun for device {target}")
    token = str(datetime.now())
    showrun_info = {
        "waf": "localhost:5000",
        "work_type": "showrun",
        "target": target,
        "token": token,
    }
    showrun_info_json = json.dumps(showrun_info)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="waf", durable=True)
    channel.basic_publish(
        exchange="", routing_key="waf", body=showrun_info_json
    )
    return token


def start_deviceblocking(target):
    print(f"start running blocking device {target}")
    token = str(datetime.now())
    showrun_info = {
        "waf": "localhost:5000",
        "work_type": "deviceblocking",
        "target": target,
        "token": token,
    }
    showrun_info_json = json.dumps(showrun_info)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="waf", durable=True)
    channel.basic_publish(
        exchange="", routing_key="waf", body=showrun_info_json
    )
    return token


def start_unblockdevice(target):
    print(f"start running unblocking device {target}")
    token = str(datetime.now())
    showrun_info = {
        "waf": "localhost:5000",
        "work_type": "unblockdevice",
        "target": target,
        "token": token,
    }
    showrun_info_json = json.dumps(showrun_info)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="waf", durable=True)
    channel.basic_publish(
        exchange="", routing_key="waf", body=showrun_info_json
    )
    return token


def start_unblock(target):
    print(f"start running unblocking {target}")
    token = str(datetime.now())
    unblock_info = {
        "waf": "localhost:5000",
        "work_type": "unblock",
        "target": target,
        "token": token,
    }
    unblock_info_json = json.dumps(unblock_info)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="waf", durable=True)
    channel.basic_publish(
        exchange="", routing_key="waf", body=unblock_info_json
    )
    return token


if __name__ == "__main__":
    start_unblock("192.168.73.1")
