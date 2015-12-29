from diskmonitor.functions import *
from diskmonitor.monitor import Monitor
from diskmonitor.emailer import Emailer
from collections import deque
from threading import Thread
from operator import itemgetter
from collections import defaultdict


class Manager(object):
    def __init__(self, disks, config):
        self._disks = disks
        self._monitors = []
        self._config = config
        self._email_client = Emailer(config=self._config)
        self._alerts_q = deque()
        self.metrics_q = deque()

        (Thread(target=self._email_client.start_client, name='email_client', daemon=True)).start()

    def _launch(self, disk=None):
        monitor = Monitor(disk_name=disk,
                          config=self._config,
                          email_client=self._email_client,
                          alerts_que=self._alerts_q,
                          metrics_que=self.metrics_q)
        monitor.start_monitor()
        return

    def launch_monitors(self, disk):
        if disk:
            t = Thread(target=self._launch, args=(disk,), name=disk, daemon=True)
            self._monitors.append({'_thread': t, 'monitored_disk': disk})
            t.start()

        else:
            for disk in self._disks:
                t = Thread(target=self._launch, args=(disk,), name=disk, daemon=True)
                self._monitors.append({'_thread': t, 'monitored_disk': disk})
                t.start()

    def dump_monitors(self):
        print(self._monitors)

    def dump_alerts(self, disk):
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







