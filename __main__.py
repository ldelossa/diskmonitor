import json
import sys
import cmd
import signal
from os import path
from diskmonitor.functions import *
from diskmonitor.manager import Manager
from diskmonitor.daemon3x import daemon
from time import sleep
import argparse



class DiskMonitor_CMD(cmd.Cmd):

    def do_exit(self, rest=None):
        sys.exit(1)

    def do_dump_monitors(self, rest=None):
        manager.dump_monitors()

    def do_dump_alerts(self, disk_input=None, rest=None,):
        manager.dump_alerts(disk_input)

    def do_dump_metrics(self, rest=None):
        manager.dump_metrics()

    def do_launch_monitor(self, disk_input=None, rest=None):
        if disk_input is not None:
            if any([disk_input == d for d in extract_disk_names()]):
                manager.launch_monitors(disk_input)
            elif disk_input == 'all':
                manager.launch_monitors()
            else:
                print('Disk not recognized')
            return

    def do_stop_monitor(self, disk_input, rest=None):
        if disk_input is None:
            print('No monitor supplied')
        else:
            manager.stop_monitor(disk_input)
            # else:
            #     print('Disk not recognized')
            # return

    def do_list_disks(self, rest=None):
        print(extract_disk_names())

class Daemon(daemon):
    def run(self):
        manager.launch_monitors()
        while True:
            sleep(0.1)

if __name__ == "__main__":

    # parse arguments to determine if we should detach
    parser = argparse.ArgumentParser()
    parser.add_argument("--detached", "-d", action='store_true',
                        help="Runs as daemon with no cli")
    args = parser.parse_args()

    # load in json configuration file
    directory = path.dirname(__file__)
    filename = path.join(directory, 'config.json')
    with open(filename) as f:
        config = json.load(f)

    # check if email configuration is enabled
    if any([v is None for k, v in config['email_config'].items()]):
        print('Email configuration not set')
        sys.exit(1)

    # find disks on system
    disks = extract_disk_names()

    # start monitor manager
    manager = Manager(disks, config)

    # if detached argument is present, daemonize, otherwise, run interactive CMD loop.
    if args.detached is True:
        daemon = Daemon('/tmp/diskmonitor.pid')
        signal.signal(signal.SIGTERM, daemon.stop)
        daemon.start()
    else:
        DiskMonitor_CMD().cmdloop()