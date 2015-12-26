import psutil
import json
import sys
from diskmonitor import Monitor
from diskmonitor.emailer import Emailer
from threading import Thread
from collections import deque
from diskmonitor.collectd_iostat_python import IOStat

def extract_disk_names():
    iostats = IOStat().get_diskstats()
    return [disk_name for disk_name in iostats]


def launch_monitor(disk_name, config_file, q):
    email_client = Emailer(config=config_file)
    monitor = Monitor(disk_name=disk_name, config=config_file, email_client=email_client, metrics_que=q)
    monitor.start_monitor()
    return

def dump_metrics(q):
    for alert in q:
        print(alert)


if __name__ == "__main__":

    #load in json configuration file
    with open('config.json') as f:
        config = json.load(f)

    metrics_q = deque(maxlen=15)

    disks = extract_disk_names()

    for disk in disks:
        t = Thread(target=launch_monitor, args=(disk, config, metrics_q), daemon=True,)
        t.start()

    while True:
        command = input("Monitor Started, type exit to quit\n")
        if command == "exit":
            sys.exit(1)

        if command == "dump-metrics":
            dump_metrics(metrics_q)







