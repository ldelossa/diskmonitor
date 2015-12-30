from diskmonitor.functions import *
from diskmonitor.monitor import Monitor
from diskmonitor.emailer import Emailer
from collections import deque
from threading import Thread
from operator import itemgetter
from collections import defaultdict


class Manager(object):
    def __init__(self, disks, config):
        """
        Manager object - handles the communication between CLI and monitors
        :param disks: list - list of disks returned by function extract_disk_names()
        :param config: config.json file
        :return:
        """
        self._disks = disks
        self._monitors = {}
        self._config = config
        self._email_client = Emailer(config=self._config)
        self._alerts_q = deque()
        self._metrics_q = deque()
        self._control_q = deque()
        # initialize email client in it's own thread
        (Thread(target=self._email_client.start_client, name='email_client', daemon=True)).start()

    def _launch(self, disk=None):
        """
        Internal function, supplies instructions on launching a monitor thread
        :param disk: string - disk to monitor
        :return:
        """
        monitor = Monitor(disk_name=disk,
                          config=self._config,
                          email_client=self._email_client,
                          alerts_que=self._alerts_q,
                          metrics_que=self._metrics_q,
                          control_que=self._control_q)
        monitor.start_monitor()
        return

    def launch_monitors(self, disk=None):
        """
        Launches a monitor thread.
        :param disk: string - string - disk to monitor
        :return:
        """
        if disk:
            for key in self._monitors:
                if disk == key:
                    print('Monitor for {} is already running \n'.format(disk))
                    return
            t = Thread(target=self._launch, args=(disk,), name=disk, daemon=True)
            self._monitors[disk] = t
            t.start()

        else:
            if len(self._monitors) == len(self._disks):
                print("Monitors already running for all disks")
                return
            for disk in self._disks:
                t = Thread(target=self._launch, args=(disk,), name=disk, daemon=True)
                self._monitors[disk] = t
                t.start()

    def stop_monitor(self, disk):
        """
        Stops a monitor thread, send message on control queue. Monitor listens for message and exits if message
        value is exit and key is the monitor's disk name.
        :param disk: string - disk
        :return:
        """
        if any([disk == d for d in self._monitors]):
            self._control_q.append({disk: 'exit'})

            while self._monitors[disk].isAlive():
                pass
            del self._monitors[disk]


        # self._control_q.append({disk: 'exit'})
        # for monitor in self._monitors:
        #     for d, thread in monitor.items():
        #         if d == disk:
        #             while thread.isAlive():
        #                 pass
        #             self._monitors.remove(monitor)
        #         else:
        #             return

    def dump_monitors(self):
        """
        Dumps monitors registered with manager
        :return:
        """
        print("Number of monitors running {}:\n".format(len(self._monitors)))
        if len(self._monitors) > 0:
            print(self._monitors)
            print("\n")

    def dump_alerts(self, disk):
        """
        Dumps all alerts gathered from time of monitor launch
        :param disk: string - disk
        :return:
        """
        alerts = [alert for alert in self._alerts_q]
        alerts.sort(key=itemgetter('time'))

        dev_dict = defaultdict(list)
        for alert in alerts:
            dev_dict[alert['dev']].append(alert)

        if any([disk == d for d in extract_disk_names()]):
            print(disk)
        for i in dev_dict[disk]:
            print('     ', i)

        else:
            for key in dev_dict:
                print(key)
            for i in dev_dict[key]:
                print('     ', i)
        return

    def dump_metrics(self):
        """
        Dumps out all collected metrics (not sorted)
        :return:
        """
        metrics = [metric for metric in self._metrics_q]
        for metric in metrics:
            print(metric)






