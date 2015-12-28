from diskmonitor.collectd_iostat_python import IOStat

class Disk(object):
    """
    Disk object - polls IOstat for metrics. This object is instantiated by each Monitor object.
    """
    def __init__(self, disk_name):
        self.disk_name = disk_name
        self.read_time = None
        self.write_time = None
        self.current_ios = None
        self.metrics = None
        self.iometrics = None
        self._iostats = IOStat(disks=[disk_name])

    def poll(self):
        self.iometrics = self._iostats.get_diskstats()





