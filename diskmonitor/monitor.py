from diskmonitor.disk import Disk
from socket import gethostname
from datetime import datetime
from os import uname

class Monitor(object):
    def __init__(self, *, disk_name, config, email_client, metrics_que):
        self.monitored_disk = disk_name
        self.poll_interval = config['monitor_config']['poll_interval']
        self.disk = Disk(self.monitored_disk)
        self.email_client = email_client
        self.hostname = uname()[1]
        self._disk_up = True
        self._metrics_que = metrics_que
        self._config = config
        self._last_poll_datetime = None


    def _check(self):
        try:
            self.disk.poll()
            self._last_poll_datetime = datetime.now()
        except LookupError:
            self._disk_up = False

        if not self._disk_up:
            self.email_client.msg = "Disk is down! " + str(self.monitored_disk) + " on host " + str(gethostname())
            # self.email_client.send_mail()
            print(self.email_client.msg)

        for key in self._config['io_thresholds']:
            if self.disk.iometrics[self.monitored_disk][key] > self._config['io_thresholds'][key]:

                alert = {'dev': self.monitored_disk, 'metric': key,
                         'current_value': self.disk.iometrics[self.monitored_disk][key],
                         'threshold': self._config['io_thresholds'][key],
                         'hostname': self.hostname,
                         'time': self._last_poll_datetime.strftime('%b, %a %Y %H:%M:%S')}

                self._append_metrics_to_que(alert)
                self.email_client.append_to_message_q(alert)
        return

    def _append_metrics_to_que(self, alert):
        self._metrics_que.append(alert)

    def start_monitor(self):
        while True:
            if (self._last_poll_datetime is None):
                self._check()
            elif ((datetime.now() - self._last_poll_datetime).total_seconds() >= self.poll_interval):
                # print('Interval up!')
                self._check()





