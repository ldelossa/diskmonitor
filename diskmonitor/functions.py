from diskmonitor.collectd_iostat_python import IOStat


def extract_disk_names():
    """
    Obtains list of disks on system that IOstat recognizes
    :return: List of disk objects
    """
    iostats = IOStat().get_diskstats()
    return [disk_name for disk_name in iostats]