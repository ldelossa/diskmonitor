from diskmonitor.disk import Disk
from time import sleep
from socket import gethostname

class Monitor(object):
    def __init__(self, *, disk_name, config, email_client):
        self.monitored_disk = disk_name
        self.read_time_threshold = config['monitor_config']['read_time_threshold']
        self.write_time_threshold = config['monitor_config']['write_time_threshold']
        self.poll_interval = config['monitor_config']['poll_interval']
        self.disk_obj = Disk(self.monitored_disk)
        self.email_client = email_client
        self.disk_up = True

    def _check(self):
        try:
            self.disk_obj.poll()
        except LookupError:
            self.disk_up = False

        if not self.disk_up:
            self.email_client.msg = "Disk is down! " + str(self.monitored_disk) + " on host " + str(gethostname())
            self.email_client.send_mail()
            print(self.email_client.msg)

        if self.disk_obj.read_time > self.read_time_threshold:
            self.email_client.msg = "High disk read times! " + str(self.monitored_disk) + " on host " + str(gethostname())
            self.email_client.send_mail()
            print(self.email_client.msg)

        if self.disk_obj.write_time > self.write_time_threshold:
            self.email_client.msg = "High disk write times! " + str(self.monitored_disk) + " on host  " + str(gethostname())
            self.email_client.send_mail()
            print(self.email_client.msg)

        return

    def start_monitor(self):
        while True:
            self._check()
            sleep(self.poll_interval)





