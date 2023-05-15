# main worker application
import json
import pika
import os
from ShowRunThread import ShowRunThread
from BlockdeviceThread import BlockdeviceThread
from BlockingThread import BlockingThread
from UnblockdeviceThread import UnblockdeviceThread
from UnblockThread import UnblockThread

BLOCKING = "blocking"
SHOWRUN = "showrun"
DEVICEBLOCKING = "deviceblocking"
UNBLOCKDEVICE = "unblockdevice"
UNBLOCK = "unblock"

if os.getuid() != 0:
    exit(1)


def start_receiving():
    print("Worker: starting rabbitmq, listening for work requests")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    worker_queue = "waf"
    channel.queue_declare(queue=worker_queue, durable=True)
    print(f"\n\n [*] Worker: waiting for messages on queue: {worker_queue}.")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        on_message_callback=receive_work_request, queue=worker_queue
    )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"Worker: shutting down")
        channel.close()
        connection.close()
        exit()


def receive_work_request(capture_channel, method, _, body):
    capture_channel.basic_ack(delivery_tag=method.delivery_tag)
    work_info = json.loads(body)
    if "work_type" not in work_info:
        print(f" !!! Received work request with no work_type: {work_info}")
        return
    if work_info["work_type"] not in [BLOCKING, SHOWRUN, DEVICEBLOCKING, UNBLOCKDEVICE, UNBLOCK]:
        print(
            f" !!! Received work request for unknown work_type: {work_info['work_type']}")
        return
    print(
        f"Received work: {work_info['work_type']} full work info: {work_info}")
    process_work_request(work_info["work_type"], work_info)
    print("\n\n [*] Worker: waiting for messages.")


def process_work_request(work_type, work_info):
    if "waf" not in work_info:
        waf = "localhost:5000"
    else:
        waf = work_info["waf"]
    if work_type == BLOCKING:
        work_thread = BlockingThread(waf, work_info)
    elif work_type == SHOWRUN:
        work_thread = ShowRunThread(waf, work_info)
    elif work_type == DEVICEBLOCKING:
        work_thread = BlockdeviceThread(waf, work_info)
    elif work_type == UNBLOCKDEVICE:
        work_thread = UnblockdeviceThread(waf, work_info)
    elif work_type == UNBLOCK:
        work_thread = UnblockThread(waf, work_info)
    else:
        print(f"Worker: unknown work type: {work_type}")
        return
    work_thread.start()


if __name__ == "__main__":
    start_receiving()
