from diskmonitor.disk import Disk
from datetime import datetime
from os import uname

class Monitor(object):
    """
    Monitor object - performs the polling of disk objects, checking of thresholds, and alerting
    """
    def __init__(self, *, disk_name, config, email_client, alerts_que, metrics_que):
        self.hostname = uname()[1]
        self.monitored_disk = disk_name
        self.disk = Disk(self.monitored_disk)
        self.email_client = email_client
        self._disk_up = True
        self._alerts_que = alerts_que
        self._metrics_que = metrics_que
        self._poll_interval = config['monitor_config']['poll_interval']
        self._config = config
        self._last_poll_datetime = None

    def _check(self):
        """
        Polls disk object for metrics, appends last poll datetime to self._last_poll_datetime,
        appends metrics to metrics queue

        Performs checks against io_thresholds in config.json
        :return: None
        """

        self.disk.poll()
        self._last_poll_datetime = datetime.now()
        # append time and dev to
        self.disk.iometrics[self.monitored_disk]['time'] = self._last_poll_datetime
        self._append_to_que(self.disk.iometrics, 'metric')

        if self._disk_up_check():
            self._io_check()

        return

    def _disk_up_check(self):
        """
        Determines if disk is still up. If last self.disk.poll() did not populate iometrics, disk is not available
        Places alert on the alerts queue
        :return:
        """
        if len(self.disk.iometrics.items()) == 0:

            self._disk_up=False

            alert = {'dev': self.monitored_disk,
                     'metric': 'Disk-Up',
                     'current_value': self._disk_up,
                     'threshold': 'N/A',
                     'hostname': self.hostname,
                     'time': self._last_poll_datetime.strftime('%b, %a %Y %H:%M:%S')}

            self._append_to_que(alert, 'alert')
            self._append_to_que(alert, 'email')
            return False
        else:
            return True

    def _io_check(self):
        """
        For configured io_threshold in config.json, check against value on self.disk.iometrics, if disk metrics
        exceeds configured threshold, create alert and place on alerts queue and email queue (for smtp dispatch)
        :return: None
        """
        for key in self._config['io_thresholds']:
            try:
                if self.disk.iometrics[self.monitored_disk][key] > self._config['io_thresholds'][key]:

                    alert = {'dev': self.monitored_disk,
                             'metric': key,
                             'current_value': self.disk.iometrics[self.monitored_disk][key],
                             'threshold': self._config['io_thresholds'][key],
                             'hostname': self.hostname,
                             'time': self._last_poll_datetime.strftime('%b, %a %Y %H:%M:%S')}

                    self._append_to_que(alert, 'alert')
                    self._append_to_que(alert, 'email')
            except LookupError:
                print('value not specified')
        return

    def _append_to_que(self, item, type):
        """
        Append messages to queue, an abstraction in case queue implementation change
        :param item: the item to place on queue
        :param type: string containing item type. Acceptable values: email, alert, metric
        :return:
        """
        if type == 'alert':
            self._alerts_que.append(item)

        if type == 'email':
            self.email_client.append_to_message_q(item)

        if type == 'metric':
            self._metrics_que.append(item)

        return

    def start_monitor(self):
        """
        Starts monitor, checks current datetime with self._last_poll_datetime, if interval is up performs check
        :return: None
        """
        while True:
            if (self._last_poll_datetime is None):
                self._check()
            elif ((datetime.now() - self._last_poll_datetime).total_seconds() >= self._poll_interval):
                self._check()
        return






