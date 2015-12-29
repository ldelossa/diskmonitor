import json
import sys
import cmd
from os import path
from diskmonitor.emailer import Emailer
from diskmonitor.functions import *
from diskmonitor.manager import Manager
from threading import Thread
from collections import deque


class DiskMonitor_CMD(cmd.Cmd):

    def do_exit(self, rest=None):
        sys.exit(1)

    def do_dump_alerts(self, disk_input=None, rest=None,):
        manager.dump_alerts(disk_input)

    def do_dump_metrics(self, rest=None):
        manager.dump_monitors()


if __name__ == "__main__":

    # load in json configuration file
    dir = path.dirname(__file__)
    filename = path.join(dir, 'config.json')
    with open(filename) as f:
        config = json.load(f)

    if any([v is None for k, v in config['email_config'].items()]):
        print('Email configuration not set')
        sys.exit(1)

    # # create queues
    # alerts_q = deque(maxlen=15)
    # metrics_q = deque(maxlen=150)

    # obtain disks on system
    disks = extract_disk_names()


    # # initiate email client
    # email = Emailer(config=config, msg=None)
    # t = Thread(target=email.start_client, daemon=True)
    # t.start()

    # # initiate monitors
    # for disk in disks:
    #     t = Thread(target=launch_monitor, args=(disk, config, email, alerts_q, metrics_q), daemon=True, )
    #     t.start()

    # initiate manager
    manager = Manager(disks, config)
    manager.launch_monitors()


    # command line loop
    DiskMonitor_CMD().cmdloop()