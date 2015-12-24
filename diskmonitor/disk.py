import psutil

class Disk(object):
    def __init__(self, disk_name):
        self.disk_name = disk_name
        self.read_time = None
        self.write_time = None

    def poll(self):
        metrics = psutil.disk_io_counters(perdisk=True)[self.disk_name]
        self.read_time = metrics.read_time
        self.write_time = metrics.write_time



