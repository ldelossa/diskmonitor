import psutil
import json
import sys
from diskmonitor import Monitor
from diskmonitor.emailer import Emailer
from threading import Thread


def extract_disk_names():
    return [disk for disk in psutil.disk_io_counters(perdisk=True)]


def launch_monitor(disk_name, config_file):
    email_client = Emailer(config=config_file)
    monitor = Monitor(disk_name=disk_name, config=config_file, email_client=email_client)
    monitor.start_monitor()
    return


if __name__ == "__main__":

    #load in json configuration file
    with open('config.json') as f:
        config = json.load(f)

    disks = extract_disk_names()

    for disk in disks:
        t = Thread(target=launch_monitor, args=(disk, config), daemon=True)
        t.start()

    while True:
        command = input("Monitor Started, type exit to quit\n")
        if command == "exit":
            sys.exit(1)







